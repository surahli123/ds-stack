#!/usr/bin/env python3
"""Check a finished ds-mode readout against its query log, check log, data and metric overlay.

    python3 tools/ds_verify.py readout.md [--queries .ds-queries.log] [--checks .ds-checks.log]
        [--db warehouse.db] [--overlay DIR] [--request request.md] [--json report.json]
    python3 tools/ds_verify.py --run-dir eval/results/<dir>/<run> ...   # result.md, queries.log, checks.log

Seven checks, each with a status of pass, fail, warn, could_not_verify or skipped:

  trace         every number traces to a logged query or check (ds-mode's verify_readout.py)
  replay        every logged query, replayed in order on a temporary copy of the database,
                returns the rows that were logged. Needs --db (or $DS_WAREHOUSE); never
                touches the original. A pasted result can't be replayed: could_not_verify.
  sources       the point estimate on each Headline, Observed, Adjusted and Causal effect line
                appears in the output it cites. A miss is a warn: the number may be derived by
                hand, so the report lists it under "Check by hand" for the reviewer.
  estimand      the Headline is in the unit the request asks for (percent or percentage points,
                when --request names one); a Causal effect number names an identifying design;
                and the Headline number is one of the estimate lines' numbers.
  alternatives  at least one alternative says "ruled in" or "ruled out" (a line without either is
                a warn). "ruled in" means the evidence shows it: a hedged "ruled in" ("unresolved",
                "possible") fails unless it cites a check that flagged, and one that cites no query
                or check is a warn.
  flags         every check that flagged or failed is reported in the readout.
  overlay       when the overlay's metrics.json names the metric, the readout takes its
                definition from metrics.json, and gives no number for a metric marked
                available: false. Needs --overlay (or $DS_OVERLAY_DIR).

The report never weakens a check to pass: what it can't check is could_not_verify, with the
reason. Exit code: 0 no fail, 1 at least one fail, 3 usage error.

Replay uses this reference SQLite adapter (connect()); a warehouse port replaces connect() and
replays into its scratch area, the same way tools/query.py is ported.
"""

import argparse
import json
import os
import re
import shutil
import sqlite3
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
DS_MODE_TOOLS = os.path.join(os.path.dirname(os.path.dirname(HERE)), "ds-mode", "tools")
sys.path.insert(0, DS_MODE_TOOLS)

import guarded_query as gq  # noqa: E402
import verify_readout as vr  # noqa: E402

STATUSES = ("fail", "warn", "could_not_verify", "pass", "skipped")
ESTIMATE = re.compile(r"^\s*[-*]?\s*(headline|observed|adjusted|causal effect)\s*:\s*(.*)$", re.I)
DESIGN = re.compile(r"random|experiment|a/b|\bab test|holdout|control group|diff(?:erence)?-in-diff|"
                    r"regression discontinuity|instrument|synthetic control|stagger|随机|实验|对照组|双重差分|断点", re.I)
RULED = re.compile(r"\bruled\s+(in|out)\b|\bruled\s+it\s+(out|in)\b", re.I)
HEDGE = re.compile(r"unresolved|possib|can'?t\s+(?:be\s+)?rule|cannot\s+(?:be\s+)?rule|not\s+(?:yet\s+)?excluded|"
                   r"open question|未排除|无法排除|不能排除|可能", re.I)
GENERIC_WORDS = {"search", "rate", "share", "count", "per", "the", "of"}


def finding(check, status, message, **extra):
    return {"check": check, "status": status, "message": message, **extra}


def estimate_lines(text):
    """{name: line} for Headline, Observed, Adjusted and Causal effect in the Answer section."""
    found = {}
    for name, body in vr.sections(text):
        if not name.lower().startswith("answer"):
            continue
        for line in body.splitlines():
            match = ESTIMATE.match(line)
            if match and match.group(1).lower() not in found:
                found[match.group(1).lower()] = line.strip()
    return found


def first_number(line):
    numbers = vr.numbers_in(line)
    return numbers[0] if numbers else None


def as_float(token):
    try:
        return float(token.replace("−", "-").replace(",", ""))
    except (AttributeError, ValueError):
        return None


def values_in(obj, out):
    """Every number in a logged result or check, strings included."""
    if isinstance(obj, bool) or obj is None:
        return out
    if isinstance(obj, (int, float)):
        out.append(float(obj))
    elif isinstance(obj, str):
        out += [float(m) for m in re.findall(r"[-+]?\d+(?:\.\d+)?", obj.replace("−", "-"))]
    elif isinstance(obj, dict):
        for value in obj.values():
            values_in(value, out)
    elif isinstance(obj, (list, tuple)):
        for value in obj:
            values_in(value, out)
    return out


def shown_in(token, values):
    """True when a value, or a fraction of it times 100, rounds to the number as displayed."""
    number = as_float(token)
    if number is None:
        return True
    clean = token.replace("−", "-").replace(",", "")
    decimals = len(clean.split(".")[1]) if "." in clean else 0
    tolerance = 0.5 * 10 ** -decimals + 1e-9
    return any(abs(abs(x) - abs(number)) <= tolerance for v in values for x in (v, v * 100))


# --- the checks ----------------------------------------------------------------------------------------------

def check_trace(text, queries, checks):
    problems, stats, given = vr.verify(text, queries, checks)
    if problems:
        return [finding("trace", "fail", problem) for problem in problems], given
    return [finding("trace", "pass", f"{stats['numbers']} numbers on {stats['lines']} lines trace to "
                                      f"{len(stats['queries'])} queries and {len(stats['checks'])} checks")], given


def connect(db):
    """Reference adapter: a SQLite file."""
    return sqlite3.connect(db)


def same_rows(logged, replayed):
    if len(logged) != len(replayed):
        return False, f"logged {len(logged)} rows, replay gave {len(replayed)}"
    for i, (a, b) in enumerate(zip(logged, replayed), 1):
        if len(a) != len(b):
            return False, f"row {i} has {len(a)} columns in the log, {len(b)} in the replay"
        for x, y in zip(a, b):
            if isinstance(x, (int, float)) and isinstance(y, (int, float)) and not isinstance(x, bool):
                if abs(x - y) > 1e-9 * max(1.0, abs(x), abs(y)):
                    return False, f"row {i}: logged {x}, replay {y}"
            elif x != y:
                return False, f"row {i}: logged {x!r}, replay {y!r}"
    return True, ""


def check_replay(queries, db):
    ran = [q for q in queries if q.get("status") == "ok" and q.get("id")]
    if not ran:
        return [finding("replay", "skipped", "no logged query ran")]
    if not db:
        return [finding("replay", "could_not_verify", "no database to replay against; pass --db or set DS_WAREHOUSE")]
    if not os.path.exists(db):
        return [finding("replay", "could_not_verify", f"no database at {db}")]
    results = []
    with tempfile.TemporaryDirectory(prefix="ds-verify-") as scratch:
        copy = os.path.join(scratch, os.path.basename(db))
        shutil.copy(db, copy)
        conn = connect(copy)
        try:
            for query in ran:
                qid = query["id"]
                if query.get("source") == "pasted":
                    results.append(finding("replay", "could_not_verify", f"[{qid}] is a pasted result, so it can't be replayed", ref=qid))
                    continue
                try:
                    # The statements passed the runner's guard when they ran; this is a private copy.
                    rows = gq.run(conn, query["sql"], query.get("params") or (), scratch_prefix="",
                                  max_rows=10_000, max_cell_chars=10_000, max_result_chars=10_000_000, max_seconds=120)
                except Exception as err:  # noqa: BLE001 - any failure is reported, not raised
                    results.append(finding("replay", "fail", f"[{qid}] no longer runs: {err}", ref=qid))
                    continue
                ok, why = same_rows(query.get("rows") or [], [list(r) for r in rows])
                results.append(finding("replay", "pass" if ok else "fail",
                                       f"[{qid}] gives the logged rows" if ok else f"[{qid}] gives different rows: {why}", ref=qid))
        finally:
            conn.close()
    return results


def check_sources(text, queries, checks):
    by_query = {q["id"].lower(): q for q in queries if q.get("id")}
    by_check = {c["id"].lower(): c for c in checks if c.get("id")}
    results = []
    for name, line in estimate_lines(text).items():
        number = first_number(line)
        tags = vr.tags_in(line)
        if number is None or not tags:
            continue
        values = []
        for tag in tags:
            if tag.startswith("q") and tag in by_query:
                values_in(by_query[tag].get("rows"), values)
            elif tag.startswith("check:") and tag.split(":", 1)[1] in by_check:
                entry = by_check[tag.split(":", 1)[1]]
                values_in({"summary": entry.get("summary"), "details": entry.get("details")}, values)
        if not values or "given" in tags:
            continue
        if shown_in(number, values):
            results.append(finding("sources", "pass", f"{name}: {number} is in {', '.join(tags)}"))
        else:
            results.append(finding("sources", "warn", f"{name}: {number} isn't in {', '.join(tags)}; check it by hand",
                                   number=number, tags=tags, line=line))
    return results


def asked_unit(request):
    """The unit the request asks for, when it names one: 'pp' or 'percent'."""
    lowered = (request or "").lower()
    if re.search(r"percentage points?|\bin pp\b|百分点", lowered):
        return "pp"
    if re.search(r"\bin percent\b|as a percent|in %|百分比", lowered):
        return "percent"
    return None


def headline_unit(line):
    """The unit right after the Headline's first number: 'pp', 'percent' or None."""
    match = re.search(r"[-+−]?\d+(?:[.,]\d+)*\s*(pp|个?百分点|%|％|percent)", line, re.I)
    if not match:
        return None
    return "pp" if match.group(1).lower() in ("pp", "百分点", "个百分点") else "percent"


def check_estimand(text, request=""):
    lines = estimate_lines(text)
    if "headline" not in lines:
        return [finding("estimand", "fail", "the Answer has no Headline line")]
    results = []
    wanted, given_unit = asked_unit(request), headline_unit(lines["headline"])
    if wanted and given_unit and wanted != given_unit:
        results.append(finding("estimand", "fail", f"the request asks for {'percentage points' if wanted == 'pp' else 'percent'}, "
                                                   f"and the Headline is in {'pp' if given_unit == 'pp' else 'percent'}: "
                                                   f"{lines['headline']}"))
    elif wanted and given_unit:
        results.append(finding("estimand", "pass", f"the Headline is in the unit the request asks for"))
    causal = lines.get("causal effect", "")
    causal_body = ESTIMATE.match(causal).group(2) if causal else ""
    if causal and first_number(causal) is not None and not re.search(r"not identified", causal_body, re.I):
        if DESIGN.search(causal_body):
            results.append(finding("estimand", "pass", "the Causal effect number names its design"))
        else:
            results.append(finding("estimand", "fail", "the Causal effect gives a number but names no identifying "
                                                       f"design (randomized test, holdout, ...): {causal}"))
    headline = ESTIMATE.match(lines["headline"]).group(2)
    head_number = first_number(lines["headline"])
    if head_number is None or re.match(r"\s*can'?t tell", headline, re.I):
        results.append(finding("estimand", "pass", "the Headline abstains, so it needs no estimate line"))
        return results
    estimates = {name: first_number(line) for name, line in lines.items() if name != "headline"}
    matching = [name for name, number in estimates.items()
                if number is not None and as_float(number) == as_float(head_number)]
    if matching:
        results.append(finding("estimand", "pass", f"the Headline {head_number} is the {matching[0]} estimate"))
    elif any(number is not None for number in estimates.values()):
        results.append(finding("estimand", "fail", f"the Headline {head_number} is none of the estimate lines' numbers "
                                                   f"({', '.join(f'{k} {v}' for k, v in estimates.items() if v)})"))
    else:
        results.append(finding("estimand", "fail", "the Headline gives a number, but no estimate line does"))
    return results


def alternative_lines(text):
    for name, body in vr.sections(text):
        if not name.lower().startswith("why we believe"):
            continue
        inside = False
        for line in body.splitlines():
            stripped = line.strip().lower()
            if stripped.startswith(("- alternatives considered", "alternatives considered")):
                inside = True
                continue
            if stripped.startswith(("- checks run", "checks run")):
                inside = False
            if inside and re.match(r"^\s+[-*]\s+\S", line):
                yield line.strip()


def check_alternatives(text, checks=()):
    raised = {c["id"].lower() for c in checks if c.get("id") and c.get("status") in ("flag", "fail")}
    results = []
    lines = list(alternative_lines(text))
    if not lines:
        return [finding("alternatives", "fail", "no alternatives are listed under 'Alternatives considered'")]
    if not any(RULED.search(line) for line in lines):
        results.append(finding("alternatives", "fail", f"none of the {len(lines)} alternatives says 'ruled in' or 'ruled out'"))
    for line in lines:
        verdict = RULED.search(line)
        if not verdict:
            results.append(finding("alternatives", "warn", f"says neither 'ruled in' nor 'ruled out': {line}"))
            continue
        if (verdict.group(1) or verdict.group(2)).lower() == "in":
            after = line[verdict.end():]
            tags = vr.tags_in(line)
            anomaly = any(t.startswith("check:") and t.split(":", 1)[1] in raised for t in tags)
            if HEDGE.search(after) and not anomaly:
                results.append(finding("alternatives", "fail", "'ruled in' is hedged and no flagged check backs it: an "
                                                               "alternative that wasn't ruled out is not ruled in. Say "
                                                               f"what would decide it: {line}"))
            elif HEDGE.search(after):
                results.append(finding("alternatives", "warn", "'ruled in' is hedged; a flagged check shows the anomaly, "
                                                               f"but say which cause is still open: {line}"))
            elif not any(t.startswith(("q", "check:")) for t in tags):
                results.append(finding("alternatives", "warn", f"'ruled in' cites no query or check: {line}"))
            else:
                results.append(finding("alternatives", "pass", f"ruled in with evidence: {line[:80]}"))
        else:
            results.append(finding("alternatives", "pass", f"ruled out: {line[:80]}"))
    return results


def check_flags(text, checks):
    raised = [c for c in checks if c.get("status") in ("flag", "fail") and c.get("id")]
    if not raised:
        return [finding("flags", "pass", "no check flagged or failed")]
    lowered = vr._clean(text).lower()
    results = []
    for entry in raised:
        cited = f"check:{entry['id'].lower()}" in lowered
        named = re.search(rf"^\s*[-*]?\s*{re.escape(entry['check'].lower())}\s*:\s*(flag|fail)", lowered, re.M)
        if cited or named:
            results.append(finding("flags", "pass", f"{entry['id']} ({entry['status']}) is reported"))
        else:
            results.append(finding("flags", "fail", f"{entry['id']} {entry['status']}ed and the readout doesn't report "
                                                    f"it: {entry.get('summary', '')[:120]}"))
    return results


def metric_named(key, entry, text):
    words = [w for w in re.split(r"[_\W]+", key.lower()) if w and w not in GENERIC_WORDS]
    words = words or [key.lower()]
    return all(re.search(rf"\b{re.escape(w)}", text) for w in words)


def check_overlay(text, overlay, request):
    path = os.path.join(overlay, "metrics.json") if overlay else None
    if not path or not os.path.exists(path):
        return [finding("overlay", "skipped", "no metrics.json in the overlay")]
    with open(path) as handle:
        catalog = json.load(handle)
    clean = vr._clean(text)
    lines = estimate_lines(text)
    metric_line = next((l for l in clean.splitlines() if re.match(r"^\s*[-*]?\s*metric\s*:", l, re.I)), "")
    where = f"{request}\n{lines.get('headline', '')}\n{metric_line}".lower()
    results = []
    for key, entry in catalog.items():
        if not isinstance(entry, dict) or not metric_named(key, entry, where):
            continue
        head_number = first_number(lines.get("headline", ""))
        if entry.get("available") is False:
            if head_number is None:
                results.append(finding("overlay", "pass", f"{key} is unavailable in the overlay, and the Headline gives no number"))
            else:
                results.append(finding("overlay", "fail", f"the overlay marks {key} unavailable "
                                                          f"({entry.get('note', 'no reason given')}), but the Headline gives {head_number}"))
            continue
        parts = [entry.get("numerator"), entry.get("denominator")]
        if "metrics.json" in metric_line.lower() or all(p and p.lower() in metric_line.lower() for p in parts):
            results.append(finding("overlay", "pass", f"{key} is taken from metrics.json"))
        else:
            results.append(finding("overlay", "fail", f"the overlay defines {key} as {entry.get('numerator')} / "
                                                      f"{entry.get('denominator')}, and the readout's Metric line doesn't "
                                                      f"use it: {metric_line.strip() or 'no Metric line'}"))
    return results or [finding("overlay", "skipped", "the overlay doesn't define the metric this readout reports")]


# --- running and reporting ---------------------------------------------------------------------------------

def run_all(text, queries, checks, db=None, overlay=None, request=""):
    trace, given = check_trace(text, queries, checks)
    findings = (trace + check_replay(queries, db) + check_sources(text, queries, checks) + check_estimand(text, request)
                + check_alternatives(text, checks) + check_flags(text, checks) + check_overlay(text, overlay, request))
    counts = {status: sum(f["status"] == status for f in findings) for status in STATUSES}
    return {"verdict": "fail" if counts["fail"] else "pass", "counts": counts, "findings": findings, "given": given}


def render(report):
    counts = report["counts"]
    head = (f"ds-verify: {report['verdict']} ({counts['fail']} fail, {counts['warn']} warn, "
            f"{counts['could_not_verify']} could not verify, {counts['pass']} pass)")
    lines = [head]
    for status in ("fail", "could_not_verify", "warn"):
        for item in report["findings"]:
            if item["status"] == status:
                lines.append(f"  {status.upper():16} {item['check']:12} {item['message']}")
    by_hand = [f for f in report["findings"] if f["check"] == "sources" and f["status"] == "warn"]
    if by_hand:
        lines.append("Check by hand (numbers not found in the output they cite):")
        lines += [f"  {f['number']} [{', '.join(f['tags'])}]  {f['line'][:100]}" for f in by_hand]
    for line in report["given"]:
        lines.append(f"Given (confirm against the request): {line}")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("readout", nargs="?", help="the readout file")
    parser.add_argument("--run-dir", help="a run directory holding result.md, queries.log and checks.log")
    parser.add_argument("--queries", help="query log (default $DS_QUERIES_LOG, else .ds-queries.log)")
    parser.add_argument("--checks", help="check log (default $DS_CHECKS_LOG, else .ds-checks.log)")
    parser.add_argument("--db", default=os.environ.get("DS_WAREHOUSE"), help="SQLite file to replay the queries on")
    parser.add_argument("--overlay", default=os.environ.get("DS_OVERLAY_DIR"), help="overlay folder with metrics.json")
    parser.add_argument("--request", help="a file holding the original request, to match metric names")
    parser.add_argument("--json", help="also write the report as JSON to this file")
    args = parser.parse_args(argv)

    if args.run_dir:
        readout = args.readout or os.path.join(args.run_dir, "result.md")
        queries = args.queries or os.path.join(args.run_dir, "queries.log")
        checks = args.checks or os.path.join(args.run_dir, "checks.log")
    elif args.readout:
        readout = args.readout
        queries = args.queries or os.environ.get("DS_QUERIES_LOG") or ".ds-queries.log"
        checks = args.checks or os.environ.get("DS_CHECKS_LOG") or ".ds-checks.log"
    else:
        parser.print_usage(sys.stderr)
        return 3
    try:
        with open(readout, encoding="utf-8") as handle:
            text = handle.read()
        request = open(args.request, encoding="utf-8").read() if args.request else ""
    except OSError as err:
        print(f"ds-verify: {err}", file=sys.stderr)
        return 3
    report = run_all(text, vr.read_jsonl(queries), vr.read_jsonl(checks), args.db, args.overlay, request)
    print(render(report))
    if args.json:
        with open(args.json, "w") as handle:
            json.dump(report, handle, indent=2, default=str)
    return 1 if report["verdict"] == "fail" else 0


if __name__ == "__main__":
    sys.exit(main())
