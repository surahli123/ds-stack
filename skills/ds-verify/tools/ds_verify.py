#!/usr/bin/env python3
"""Check a finished ds-mode readout against its query log, check log, data and metric overlay.

    python3 tools/ds_verify.py readout.md [--queries .ds-queries.log] [--checks .ds-checks.log]
        [--db warehouse.db] [--overlay DIR] [--request request.md] [--json report.json]
    python3 tools/ds_verify.py --run-dir eval/results/<dir>/<run> ...   # result.md, queries.log, checks.log

Seven checks, each with a status of pass, fail, warn, could_not_verify or skipped:

  trace         every number traces to a logged query or check (ds-mode's verify_readout.py)
  replay        every logged query, replayed in order on a private copy of the database,
                returns the rows that were logged. A pasted result can't be replayed.
  sources       the point estimate on each Headline, Observed, Adjusted and Causal effect line
                appears in the output it cites. A miss may be a number derived by hand, so it
                goes on the "check by hand" list; for the Headline it is could_not_verify.
  estimand      the Headline is in the unit the request asks for; a Causal effect number comes
                from a named, un-negated design; the Headline matches an estimate line. A
                "can't tell" Headline fails when Adjusted has a number, the Causal effect is
                "not identified" and no completeness, srm or fanout check flagged: an
                unidentified cause is not a reason to abstain.
  alternatives  each alternative says "ruled in", "ruled out" or "not ruled out". "ruled in"
                means the evidence shows it: a hedged "ruled in" fails unless a flagged check
                backs it. An open alternative is "not ruled out".
  flags         every check that flagged or failed is reported by its tag, unless the same check
                was rerun later on the same input (then it is a warn, for the reviewer).
  overlay       when metrics.json names the metric, the Metric line uses its numerator,
                denominator and filters, and so does the SQL of the queries the Headline cites;
                no estimate line gives a number (rather than "not computed") for a metric marked
                available: false. A query that computes both definitions passes the SQL part.

The first line is "ds-verify: fail" when any check fails, "ds-verify: unverified" when nothing
fails but something that matters couldn't be checked (a missing input, a pasted or unreplayable
source, a Headline number not found in its source), and "ds-verify: pass" otherwise. The report
never weakens a check to pass. Exit code: 0 pass, 1 fail, 2 unverified, 3 usage error.

Port point: scratch_copy() opens a private copy of a SQLite file. A warehouse port replaces that
one function with a copy or scratch schema it may write to; everything else stays.
"""

import argparse
import json
import os
import re
import sqlite3
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
DS_MODE_TOOLS = os.path.join(os.path.dirname(os.path.dirname(HERE)), "ds-mode", "tools")
sys.path.insert(0, DS_MODE_TOOLS)

import guarded_query as gq  # noqa: E402
import query as ds_query  # noqa: E402
import verify_readout as vr  # noqa: E402

STATUSES = ("fail", "could_not_verify", "warn", "pass", "skipped")
ESTIMATE = re.compile(r"^\s*[-*]?\s*(headline|observed|adjusted|causal effect)\s*:\s*(.*)$", re.I)
FROM_CLAUSE = re.compile(r"(?:\bfrom\b|来自|基于|根据|通过)([^;；。]*)", re.I)
DESIGN = re.compile(r"random|experiment|a/b|\bab test|split test|holdout|holdback|control group|treatment|"
                    r"diff(?:erence)?-in-diff|regression discontinuity|instrument|synthetic control|stagger|"
                    r"随机|实验|对照|分流|双重差分|断点", re.I)
NEGATION = re.compile(r"\bno\b|\bnot\b|\bwithout\b|\bnon-?|n't\b|没有|无|非|未", re.I)
RULED = re.compile(r"\bruled\s+(?:it\s+)?(in|out)\b", re.I)
NEGATED_VERDICT = re.compile(r"(?:\bnot|n't|\bcannot|\bnever)\s+(?:be\s+|been\s+|yet\s+)*$", re.I)
HEDGE = re.compile(r"unresolved|possib|can'?t\s+(?:be\s+)?rule|cannot\s+(?:be\s+)?rule|not\s+(?:yet\s+)?excluded|"
                   r"open question|\bmaybe\b|\bperhaps\b|\bmight\b|未排除|无法排除|不能排除|可能|待定", re.I)
CLAUSE_END = re.compile(r"[;；。:：,，]|\.\s")
ALT_LABEL = re.compile(r"^\s*[-*]?\s*(?:alternatives considered|考虑过的其他解释|其他解释|替代解释|备选解释)", re.I)
CHECKS_LABEL = re.compile(r"^\s*[-*]?\s*(?:checks run|已运行的检查|运行的检查|检查项)", re.I)
METRIC_LINE = re.compile(r"^\s*[-*]?\s*(?:metric|指标)\s*[:：]", re.I)
GENERIC_WORDS = {"search", "rate", "share", "count", "per", "the", "of"}
DIRECTION = {"down": re.compile(r"下降|降低|减少|\bfell\b|\bdrop|\bdecline|\bdown\b", re.I),
             "up": re.compile(r"上升|提高|增加|\brose\b|\bincrease|\bup\b", re.I)}


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


def body_of(line):
    match = ESTIMATE.match(line or "")
    return match.group(2) if match else (line or "")


def first_number(line):
    numbers = vr.numbers_in(line)
    return numbers[0] if numbers else None


def as_float(token):
    try:
        return float(token.replace("−", "-").replace(",", ""))
    except (AttributeError, ValueError):
        return None


def decimals(token):
    clean = token.replace("−", "-").replace(",", "")
    return len(clean.split(".")[1]) if "." in clean else 0


def close(shown, value):
    """True when `value` rounds to `shown` at the precision `shown` is written with (sign ignored)."""
    number = as_float(shown)
    return number is not None and abs(abs(value) - abs(number)) <= 0.5 * 10 ** -decimals(shown) + 1e-9


def signed(token):
    return token.strip()[:1] in "+-−"


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


# --- trace ---------------------------------------------------------------------------------------------------

def check_trace(text, queries, checks):
    problems, stats, given = vr.verify(text, queries or [], checks or [])
    if problems:
        return [finding("trace", "fail", problem) for problem in problems], given
    return [finding("trace", "pass", f"{stats['numbers']} numbers on {stats['lines']} lines trace to "
                                      f"{len(stats['queries'])} queries and {len(stats['checks'])} checks")], given


# --- replay --------------------------------------------------------------------------------------------------

def scratch_prefix():
    """The runner's scratch prefix without the per-run suffix, as tools/query.py configures it."""
    prefix = ds_query.DEFAULTS["scratch_prefix"]
    overlay = os.environ.get("DS_OVERLAY_DIR")
    if overlay and os.path.exists(os.path.join(overlay, "runner.json")):
        with open(os.path.join(overlay, "runner.json")) as handle:
            prefix = json.load(handle).get("scratch_prefix", prefix)
    return prefix


def scratch_copy(db, workdir, prefix):
    """Port point. Return a connection to a private copy of the database with no scratch objects in it.

    The copy goes through SQLite's backup API on a read-only connection, so it includes what is still in
    a WAL file and never writes to the source. It lands in `workdir` ($TMPDIR by default)."""
    if not db:
        raise FileNotFoundError("no database to replay against; pass --db or set DS_WAREHOUSE")
    if not os.path.exists(db):
        raise FileNotFoundError(f"no database at {db}")
    source = sqlite3.connect(f"file:{os.path.abspath(db)}?mode=ro", uri=True)
    copy = sqlite3.connect(os.path.join(workdir, "replay.db"))
    try:
        source.backup(copy)
    finally:
        source.close()
    objects = copy.execute("select type, name from sqlite_master where name like ? escape '\\' and type in "
                           "('view', 'table') order by type = 'table'",
                           (prefix.replace("_", "\\_") + "%",)).fetchall()
    for kind, name in objects:
        copy.execute(f'drop {kind} if exists "{name}"')
    copy.commit()
    return copy


def same_rows(logged, replayed):
    if len(logged) != len(replayed):
        return False, f"logged {len(logged)} rows, replay gave {len(replayed)}"
    for i, (a, b) in enumerate(zip(logged, replayed), 1):
        if len(a) != len(b):
            return False, f"row {i} has {len(a)} columns in the log, {len(b)} in the replay"
        for x, y in zip(a, b):
            numbers = all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in (x, y))
            if numbers and abs(x - y) > 1e-9 * max(1.0, abs(x), abs(y)):
                return False, f"row {i}: logged {x}, replay {y}"
            # The log stores non-JSON cells (bytes, dates) as str(), so compare them that way.
            if not numbers and str(x) != str(y):
                return False, f"row {i}: logged {x!r}, replay {y!r}"
    return True, ""


def check_replay(queries, db):
    ran = [q for q in queries or [] if q.get("status") == "ok" and q.get("id")]
    if not ran:
        return [finding("replay", "skipped", "no logged query ran")]
    prefix = scratch_prefix()
    results = []
    with tempfile.TemporaryDirectory(prefix="ds-verify-") as workdir:
        try:
            conn = scratch_copy(db, workdir, prefix)
        except (FileNotFoundError, sqlite3.Error) as err:
            return [finding("replay", "could_not_verify", str(err))]
        try:
            for query in ran:
                qid = query["id"]
                if query.get("source") == "pasted":
                    results.append(finding("replay", "could_not_verify", f"[{qid}] is a pasted result, so it can't be replayed", ref=qid))
                    continue
                try:
                    rows = gq.run(conn, query["sql"], query.get("params") or (), scratch_prefix=prefix,
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


# --- sources -------------------------------------------------------------------------------------------------

def check_sources(text, queries, checks):
    by_query = {q["id"].lower(): q for q in queries or [] if q.get("id")}
    by_check = {c["id"].lower(): c for c in checks or [] if c.get("id")}
    results = []
    for name, line in estimate_lines(text).items():
        number = first_number(line)
        tags = [t for t in vr.tags_in(line) if t != "given"]
        if number is None or not tags:
            continue
        values, replayable = [], False
        for tag in tags:
            if tag.startswith("q") and tag in by_query:
                values_in(by_query[tag].get("rows"), values)
                replayable |= by_query[tag].get("source") != "pasted"
            elif tag.startswith("check:") and tag.split(":", 1)[1] in by_check:
                entry = by_check[tag.split(":", 1)[1]]
                values_in({"summary": entry.get("summary"), "details": entry.get("details")}, values)
                replayable = True
        miss = "could_not_verify" if name == "headline" else "warn"
        if not replayable:
            results.append(finding("sources", miss, f"{name}: {number} cites only pasted results, which can't be replayed",
                                   number=number, tags=tags, line=line))
        elif not values:
            results.append(finding("sources", miss, f"{name}: {number} cites output with no numbers in it",
                                   number=number, tags=tags, line=line))
        elif any(close(number, v) or close(number, v * 100) for v in values):
            results.append(finding("sources", "pass", f"{name}: {number} is in {', '.join(tags)}"))
        else:
            results.append(finding("sources", miss, f"{name}: {number} isn't in {', '.join(tags)}; check it by hand",
                                   number=number, tags=tags, line=line))
    return results


# --- estimand ------------------------------------------------------------------------------------------------

def sentences(text):
    return [s for s in re.split(r"(?<=[.?!。？！])\s*|\n", text or "") if s.strip()]


def units_named(text):
    lowered = text.lower()
    found = set()
    if re.search(r"percentage points?|\bin pp\b|百分点", lowered):
        found.add("pp")
    if re.search(r"\bin percent\b|as a percent|in %|百分比|\bpercent\b(?! ?points?)", lowered):
        found.add("percent")
    return found


def asked_unit(request):
    """The unit the request asks for: from its question sentence first, else the whole request when that
    names only one unit. None when it names none, or both without saying which."""
    questions = [s for s in sentences(request) if re.search(r"[?？]|多少|\bhow\b|\bwhat\b", s, re.I)]
    for scope in (" ".join(questions), request or ""):
        units = units_named(scope)
        if len(units) == 1:
            return units.pop()
        if len(units) > 1:
            return None
    return None


def unit_pairs(line):
    """[(number, unit or None)] in a line, in order, skipping dates, CI levels and digits inside names."""
    pairs = []
    cleaned = vr.CI_LEVEL.sub(" ", vr.DATE.sub(" ", line))
    for match in re.finditer(r"(?<![A-Za-z_#\d.])([-+−]?\d+(?:[.,]\d+)*)\s*(pp|个?百分点|%|％|percent)?", cleaned):
        unit = match.group(2)
        unit = None if not unit else ("pp" if unit.lower() in ("pp", "百分点", "个百分点") else "percent")
        pairs.append((match.group(1), unit))
    return pairs


VALIDITY_CHECKS = ("completeness", "srm", "fanout")


def validity_raised(checks):
    """Names of the data-validity checks that flagged, failed or couldn't run on the data."""
    names = set()
    for c in checks or []:
        name = str(c.get("check") or c.get("id", "")).split("#")[0].lower()
        if name in VALIDITY_CHECKS and str(c.get("status", "")).replace(" ", "_") in ("flag", "fail", "could_not_run"):
            names.add(name)
    return sorted(names)


def check_estimand(text, request=None, checks=None):
    """checks is the check log, or None when it is missing (then the abstain rule is skipped)."""
    lines = estimate_lines(text)
    if "headline" not in lines:
        return [finding("estimand", "fail", "the Answer has no Headline line")]
    results = []
    headline = body_of(lines["headline"])
    abstains = bool(re.match(r"\s*can'?t tell", headline, re.I))
    estimates = {name: first_number(line) for name, line in lines.items() if name != "headline"}
    pairs = unit_pairs(vr.TAGS.sub(" ", headline))
    matched = next(((n, u, e) for n, u in pairs for e, v in estimates.items()
                    if v is not None and as_float(v) is not None and close(n, as_float(v))), None)

    # The unit, read off the Headline number that is an estimate (else the first number with a unit).
    if request is None:
        results.append(finding("estimand", "could_not_verify", "no request was given, so the Headline's unit wasn't checked"))
    elif pairs and not abstains:
        wanted = asked_unit(request)
        unit = matched[1] if matched and matched[1] else next((u for _, u in pairs if u), None)
        if wanted and unit and wanted != unit:
            results.append(finding("estimand", "fail", f"the request asks for {'percentage points' if wanted == 'pp' else 'percent'}, "
                                                       f"and the Headline is in {'pp' if unit == 'pp' else 'percent'}: {lines['headline']}"))
        elif wanted and unit:
            results.append(finding("estimand", "pass", "the Headline is in the unit the request asks for"))

    causal = lines.get("causal effect", "")
    causal_body = body_of(causal)
    if causal and first_number(causal) is not None and not re.search(r"not identified", causal_body, re.I):
        designs = []
        for clause in FROM_CLAUSE.findall(causal_body):
            for hit in DESIGN.finditer(clause):
                if not NEGATION.search(clause[max(0, hit.start() - 30):hit.start()]):
                    designs.append(hit.group(0))
        if designs:
            results.append(finding("estimand", "pass", f"the Causal effect number comes from a named design ({designs[0]})"))
        else:
            results.append(finding("estimand", "fail", "the Causal effect gives a number without 'from <design>' naming an "
                                                       f"identifying design (randomized test, holdout, ...): {causal}"))

    adjusted = lines.get("adjusted", "")
    adjusted_number = first_number(adjusted) is not None and not re.search(r"not computed", adjusted, re.I)
    only_cause_missing = adjusted_number and re.search(r"not identified", causal_body, re.I)
    if abstains and only_cause_missing and checks is not None and not validity_raised(checks):
        results.append(finding("estimand", "fail", "the Headline says can't tell, but Adjusted has a number, the Causal "
                                                   "effect is not identified and no completeness, srm or fanout check "
                                                   "flagged. An unidentified cause is not a reason to abstain: make the "
                                                   "Headline the Adjusted estimate and state its assumption below it"))
    elif not pairs or abstains:
        results.append(finding("estimand", "pass", "the Headline abstains, so it needs no estimate line"))
    elif matched:
        number, _, name = matched
        estimate = estimates[name]
        contradicting = "up" if as_float(estimate) < 0 else "down"
        if signed(number) and signed(estimate) and (as_float(number) < 0) != (as_float(estimate) < 0):
            results.append(finding("estimand", "fail", f"the Headline {number} and the {name} estimate {estimate} differ in sign"))
        elif not signed(number) and as_float(estimate) and DIRECTION[contradicting].search(headline) \
                and not DIRECTION["up" if contradicting == "down" else "down"].search(headline):
            results.append(finding("estimand", "fail", f"the Headline's direction word contradicts the {name} estimate {estimate}"))
        else:
            results.append(finding("estimand", "pass", f"the Headline {number} is the {name} estimate"))
    elif any(number is not None for number in estimates.values()):
        results.append(finding("estimand", "fail", f"no Headline number is one of the estimate lines' numbers "
                                                   f"({', '.join(f'{k} {v}' for k, v in estimates.items() if v)})"))
    else:
        results.append(finding("estimand", "fail", "the Headline gives a number, but no estimate line does"))
    return results


# --- alternatives --------------------------------------------------------------------------------------------

def alternative_lines(text):
    """The list items under 'Alternatives considered', indented or not, or under a heading of that name."""
    for name, body in vr.sections(text):
        if ALT_LABEL.match(name):
            yield from (line.strip() for line in body.splitlines() if re.match(r"^\s*[-*]\s+\S", line))
            continue
        if not name.lower().startswith("why we believe"):
            continue
        inside = False
        for line in body.splitlines():
            if ALT_LABEL.match(line):
                inside = True
                continue
            if CHECKS_LABEL.match(line):
                inside = False
            if inside and re.match(r"^\s*[-*]\s+\S", line):
                yield line.strip()


def verdict_of(line):
    """('in', 'out' or 'open', end index) for the line's first verdict, else (None, None).

    "not ruled out" (or "can't be ruled out") is 'open'; a negated "ruled in" is no verdict."""
    for match in RULED.finditer(line):
        if not NEGATED_VERDICT.search(line[:match.start()]):
            return match.group(1).lower(), match.end()
        if match.group(1).lower() == "out":
            return "open", match.end()
    return None, None


def check_alternatives(text, checks=()):
    raised = {c["id"].lower() for c in checks or [] if c.get("id") and c.get("status") in ("flag", "fail")}
    results = []
    lines = list(alternative_lines(text))
    if not lines:
        return [finding("alternatives", "fail", "no alternatives are listed under 'Alternatives considered'")]
    verdicts = [verdict_of(line) for line in lines]
    if not any(v for v, _ in verdicts):
        results.append(finding("alternatives", "fail", f"none of the {len(lines)} alternatives says 'ruled in', "
                                                       "'ruled out' or 'not ruled out'"))
    for line, (verdict, end) in zip(lines, verdicts):
        if not verdict:
            results.append(finding("alternatives", "warn", f"says none of 'ruled in', 'ruled out' or 'not ruled out': {line}"))
            continue
        if verdict in ("out", "open"):
            results.append(finding("alternatives", "pass", f"{'ruled out' if verdict == 'out' else 'not ruled out'}: {line[:80]}"))
            continue
        after = line[end:]
        clause = CLAUSE_END.split(after, 1)[0]
        hedged = HEDGE.search(clause) or re.match(r"\s*[,，]\s*(?:可能|未排除|无法排除|possibly|maybe|perhaps)", after, re.I)
        tags = vr.tags_in(line)
        anomaly = any(t.startswith("check:") and t.split(":", 1)[1] in raised for t in tags)
        if hedged and not anomaly:
            results.append(finding("alternatives", "fail", "'ruled in' is hedged and no flagged check backs it: an "
                                                           "alternative that wasn't ruled out is not ruled in. Write "
                                                           f"'not ruled out' and what would decide it: {line}"))
        elif hedged:
            results.append(finding("alternatives", "warn", "'ruled in' is hedged; a flagged check shows the anomaly, "
                                                           f"but say which cause is still open: {line}"))
        elif not any(t.startswith(("q", "check:")) for t in tags):
            results.append(finding("alternatives", "warn", f"'ruled in' cites no query or check: {line}"))
        else:
            results.append(finding("alternatives", "pass", f"ruled in with evidence: {line[:80]}"))
    return results


# --- flags ---------------------------------------------------------------------------------------------------

def check_flags(text, checks):
    if checks is None:
        return [finding("flags", "could_not_verify", "no check log, so flagged or failed checks can't be listed")]
    if not checks:
        return [finding("flags", "warn", "the check log is empty: no check ran")]
    lowered = vr._clean(text).lower()
    results = []
    for i, entry in enumerate(checks):
        if entry.get("status") not in ("flag", "fail") or not entry.get("id"):
            continue
        same = [c for c in checks if c.get("check") == entry.get("check") and c.get("status") in ("flag", "fail")]
        cited = f"check:{entry['id'].lower()}" in lowered
        named = len(same) == 1 and re.search(rf"^\s*[-*]?\s*{re.escape(str(entry.get('check')).lower())}\s*:\s*(flag|fail)",
                                             lowered, re.M)
        rerun = next((later["id"] for later in checks[i + 1:] if later.get("id")
                      and later.get("check") == entry.get("check") and later.get("from") == entry.get("from")
                      and (later.get("details") or {}).get("target") == (entry.get("details") or {}).get("target")), None)
        if cited or named:
            results.append(finding("flags", "pass", f"{entry['id']} ({entry['status']}) is reported"))
        elif rerun:
            results.append(finding("flags", "warn", f"{entry['id']} {entry['status']}ed and was rerun on the same input as "
                                                    f"{rerun}; the readout should say why if it matters"))
        else:
            results.append(finding("flags", "fail", f"{entry['id']} {entry['status']}ed and the readout doesn't report it by "
                                                    f"its tag: {str(entry.get('summary', ''))[:120]}"))
    return results or [finding("flags", "pass", "no check flagged or failed")]


# --- overlay -------------------------------------------------------------------------------------------------

def normal(text):
    return re.sub(r"\s+", " ", str(text).lower().replace("_", " ")).strip()


def metric_named(key, entry, text):
    names = [key] + [a for a in entry.get("aliases", []) if isinstance(a, str)]
    for name in names:
        words = [w for w in re.split(r"[_\W]+", name.lower()) if w and w not in GENERIC_WORDS] or [name.lower()]
        if all(re.search(rf"(?<![a-z]){re.escape(w)}(?![a-z])", text) for w in words):
            return True
    return False


def filter_words(expression):
    """The column names and values in a filter such as "traffic_type = 'external'"."""
    return [w for w in re.findall(r"[A-Za-z_][A-Za-z0-9_]*|\d+", str(expression))
            if w.lower() not in {"and", "or", "not", "in", "is", "null", "like"}]


SQL_WORDS = {"sum", "count", "distinct", "avg", "min", "max", "case", "when", "then", "else", "end", "coalesce",
             "nullif", "cast", "as", "and", "or", "not", "in", "is", "null", "like", "real", "float", "integer"}


def identifiers(expression):
    """The column-like names in a metric expression, without SQL keywords and functions."""
    return [w for w in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", str(expression or "")) if w.lower() not in SQL_WORDS]


def sql_behind_estimates(text, queries, checks):
    """SQL of the runner queries the Headline, Observed and Adjusted lines cite, directly, through a check's
    "from", or through the query ids a pasted entry names (such as "interval computed from q5")."""
    lines = estimate_lines(text)
    by_query = {q.get("id"): q for q in queries or []}
    by_check = {str(c.get("id", "")).lower(): c for c in checks or []}
    todo = []
    for name in ("headline", "observed", "adjusted"):
        for tag in vr.tags_in(lines.get(name, "")):
            if tag.startswith("check:"):
                source = (by_check.get(tag.split(":", 1)[1].lower()) or {}).get("from") or []
                todo += [source] if isinstance(source, str) else list(source)
            else:
                todo.append(tag)
    seen, sqls = set(), []
    while todo:
        qid = todo.pop()
        if qid in seen or qid not in by_query:
            continue
        seen.add(qid)
        sql = str(by_query[qid].get("sql") or "")
        if by_query[qid].get("source") == "pasted":
            todo += re.findall(r"\bq\d+\b", sql)  # its text is a description, not SQL the data ran
        else:
            sqls.append(sql)
    return sqls


def base_columns(db):
    """Port point, with scratch_copy(). The lower-cased column names of every table and view, read only;
    an empty set when there is no database."""
    if not db or not os.path.exists(db):
        return set()
    try:
        con = sqlite3.connect(f"file:{os.path.abspath(db)}?mode=ro", uri=True)
        try:
            names = [r[0] for r in con.execute("select name from sqlite_master where type in ('table', 'view')")]
            return {r[1].lower() for n in names for r in con.execute(f'pragma table_info("{n}")')}
        finally:
            con.close()
    except sqlite3.Error:
        return set()


def select_items(sql):
    """{output column name: expression} for the top-level SELECT list of a query, best effort."""
    depth, select_at, from_at = 0, None, None
    for match in re.finditer(r"[()]|\bselect\b|\bfrom\b|'(?:[^']|'')*'", sql, re.I):
        token = match.group(0).lower()
        if token == "(":
            depth += 1
        elif token == ")":
            depth -= 1
        elif depth == 0 and token == "select" and select_at is None:
            select_at = match.end()
        elif depth == 0 and token == "from" and select_at is not None:
            from_at = match.start()
            break
    if select_at is None:
        return {}
    body, items, depth, start = sql[select_at:from_at], {}, 0, 0
    for i, char in enumerate(body + ","):
        depth += char == "("
        depth -= char == ")"
        if char == "," and depth == 0:
            item = body[start:i].strip()
            start = i + 1
            named = re.match(r"(?is)^(.*?\S)\s+(?:as\s+)?\"?([A-Za-z_][A-Za-z0-9_]*)\"?$", item)
            if named and named.group(2).lower() not in SQL_WORDS and named.group(1).lower() not in ("distinct", "all"):
                items[named.group(2).lower()] = named.group(1)
            items.setdefault(item.lower(), item)
    return items


def headline_column(text, queries):
    """(query id, column, expression) for the one result column, in a runner query the Headline cites,
    that holds the Headline number; None when that can't be told."""
    line = estimate_lines(text).get("headline", "")
    number = first_number(line)
    if number is None:
        return None
    by_query = {q.get("id"): q for q in queries or []}
    found = []
    for tag in vr.tags_in(line):
        query = by_query.get(tag)
        if not query or query.get("source") == "pasted" or not query.get("columns"):
            continue
        columns = [str(c).lower() for c in query["columns"]]
        hits = {columns[i] for row in query.get("rows") or [] for i, v in enumerate(row[:len(columns)])
                if isinstance(v, (int, float)) and not isinstance(v, bool) and (close(number, v) or close(number, v * 100))}
        expressions = select_items(str(query.get("sql") or ""))
        found += [(tag, c, expressions[c]) for c in hits if c in expressions]
    return found[0] if len(found) == 1 else None


def check_overlay(text, overlay, request, queries=None, checks=None, db=None):
    path = os.path.join(overlay, "metrics.json") if overlay else None
    if not path or not os.path.exists(path):
        return [finding("overlay", "skipped", "no metrics.json in the overlay")]
    with open(path) as handle:
        catalog = json.load(handle)
    clean = vr._clean(text)
    lines = estimate_lines(text)
    metric_line = next((l for l in clean.splitlines() if METRIC_LINE.match(l)), "")
    where = f"{request or ''}\n{lines.get('headline', '')}\n{metric_line}".lower()
    results = []
    for key, entry in catalog.items():
        if not isinstance(entry, dict):
            continue
        parts = [entry.get("numerator"), entry.get("denominator")]
        by_columns = all(parts) and all(normal(p) in normal(metric_line) for p in parts)
        if not (metric_named(key, entry, where) or by_columns):
            continue
        if entry.get("available") is False:
            numbered = [name for name, line in lines.items() if first_number(line) is not None
                        and not re.match(r"\s*(?:not computed|not identified|can'?t tell)", body_of(line), re.I)]
            if numbered:
                results.append(finding("overlay", "fail", f"the overlay marks {key} unavailable "
                                                          f"({entry.get('note', 'no reason given')}), but the readout gives "
                                                          f"a number on its {', '.join(numbered)} line"))
            else:
                results.append(finding("overlay", "pass", f"{key} is unavailable in the overlay, and no estimate gives a number"))
            continue
        missing = [p for p in parts if p and normal(p) not in normal(metric_line)]
        missing += [w for f in entry.get("filters", []) for w in filter_words(f) if normal(w) not in normal(metric_line)]
        sqls = sql_behind_estimates(text, queries, checks)
        if sqls:
            # The words on the Metric line are easy to fix; the query behind the number has to use them too.
            blob = " ".join(sqls).lower()
            needed = identifiers(parts[0]) + identifiers(parts[1])
            for expression in entry.get("filters", []):
                needed += identifiers(expression)[:1]  # its column; grouping by it and reading one group is fine
            absent = [w for w in dict.fromkeys(needed)
                      if not re.search(rf"(?<![a-z0-9_]){re.escape(w.lower())}(?![a-z0-9_])", blob)]
            if absent:
                results.append(finding("overlay", "fail", f"no query behind the Headline uses {', '.join(absent)} from "
                                                          f"the overlay's definition of {key}: rerun the analysis on that "
                                                          "definition; rewording the Metric line doesn't change the number"))
            else:
                # A query can compute both definitions; the Headline's own column has to be the overlay's.
                hit = headline_column(text, queries)
                if hit:
                    qid, column, expression = hit
                    used = {w.lower() for w in identifiers(expression)}
                    lacking = [w for w in identifiers(parts[0]) + identifiers(parts[1]) if w.lower() not in used]
                    if lacking and used & base_columns(db):
                        results.append(finding("overlay", "fail", f"the Headline is column {column} of {qid}, computed as "
                                                                  f"{' '.join(expression.split())[:90]}, which doesn't use "
                                                                  f"{', '.join(lacking)} from the overlay's definition of {key}"))
        if not missing:
            results.append(finding("overlay", "pass", f"the Metric line uses the overlay's definition of {key}"))
        else:
            claimed = " although it says metrics.json" if "metrics.json" in metric_line.lower() else ""
            results.append(finding("overlay", "fail", f"the overlay defines {key} as {entry.get('numerator')} / "
                                                      f"{entry.get('denominator')} with filters {entry.get('filters', [])}; "
                                                      f"the Metric line lacks {', '.join(missing)}{claimed}: "
                                                      f"{metric_line.strip() or 'no Metric line'}"))
    return results or [finding("overlay", "skipped", "the overlay doesn't define the metric this readout reports "
                                                     "(add aliases to metrics.json if it should)")]


# --- what needs a person -------------------------------------------------------------------------------------

def needs_human(text, checks, findings, given):
    """What a reviewer has to judge, in review order."""
    items = [f"{f['check']}: {f['message']}" for f in findings if f["status"] in ("fail", "could_not_verify")]
    items += [f"check by hand: {f['number']} [{', '.join(f['tags'])}]: {f['line'][:90]}"
              for f in findings if f["check"] == "sources" and f["status"] == "warn"]
    clean = vr._clean(text)
    head = estimate_lines(text).get("headline", "")
    if re.search(r"can'?t tell", head, re.I):
        items.append(f"the Headline abstains: {head}")
    items += [f"[guess]: {line.strip()[:120]}" for line in clean.splitlines() if re.search(r"\[guess\]", line, re.I)]
    items += [f"{c['id']} could not run: {str(c.get('summary', ''))[:100]}"
              for c in checks or [] if c.get("status") == "could_not_run"]
    items += [f"not reconciled: {line.strip()}" for line in clean.splitlines()
              if re.match(r"^\s*[-*]?\s*reconciled\s*:\s*not done", line, re.I)]
    items += [f"[given], confirm against the request: {line}" for line in given]
    return items


# --- running and reporting ---------------------------------------------------------------------------------

def run_all(text, queries, checks, db=None, overlay=None, request=None):
    """queries or checks is None when its log is missing; request is None when none was given."""
    trace, given = check_trace(text, queries, checks)
    findings = (trace + check_replay(queries, db) + check_sources(text, queries, checks)
                + check_estimand(text, request, checks) + check_alternatives(text, checks) + check_flags(text, checks)
                + check_overlay(text, overlay, request, queries, checks, db))
    counts = {status: sum(f["status"] == status for f in findings) for status in STATUSES}
    verdict = "fail" if counts["fail"] else "unverified" if counts["could_not_verify"] else "pass"
    return {"verdict": verdict, "counts": counts, "findings": findings, "given": given,
            "needs_human": needs_human(text, checks, findings, given)}


def render(report):
    counts = report["counts"]
    lines = [f"ds-verify: {report['verdict']} ({counts['fail']} fail, {counts['could_not_verify']} could not verify, "
             f"{counts['warn']} warn, {counts['pass']} pass)"]
    for status in ("fail", "could_not_verify", "warn"):
        for item in report["findings"]:
            if item["status"] == status:
                lines.append(f"  {status.upper():16} {item['check']:12} {item['message']}")
    if report["needs_human"]:
        lines.append("Needs a human, in this order:")
        lines += [f"  {i}. {item}" for i, item in enumerate(report["needs_human"], 1)]
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("readout", nargs="?", help="the readout file")
    parser.add_argument("--run-dir", help="a run directory holding result.md, queries.log and checks.log")
    parser.add_argument("--queries", help="query log (default $DS_QUERIES_LOG, else .ds-queries.log)")
    parser.add_argument("--checks", help="check log (default $DS_CHECKS_LOG, else .ds-checks.log)")
    parser.add_argument("--db", help="SQLite file the queries ran on (default $DS_WAREHOUSE, else ./warehouse.db)")
    parser.add_argument("--overlay", default=os.environ.get("DS_OVERLAY_DIR"), help="overlay folder with metrics.json")
    parser.add_argument("--request", help="a file holding the original request")
    parser.add_argument("--json", help="also write the report as JSON to this file")
    args = parser.parse_args(argv)

    if args.run_dir:
        readout = args.readout or os.path.join(args.run_dir, "result.md")
        queries = args.queries or os.path.join(args.run_dir, "queries.log")
        checks = args.checks or os.path.join(args.run_dir, "checks.log")
        db = args.db
    elif args.readout:
        readout = args.readout
        queries = args.queries or os.environ.get("DS_QUERIES_LOG") or ".ds-queries.log"
        checks = args.checks or os.environ.get("DS_CHECKS_LOG") or ".ds-checks.log"
        db = args.db or os.environ.get("DS_WAREHOUSE") or ("warehouse.db" if os.path.exists("warehouse.db") else None)
    else:
        parser.print_usage(sys.stderr)
        return 3
    try:
        with open(readout, encoding="utf-8") as handle:
            text = handle.read()
        request = open(args.request, encoding="utf-8").read() if args.request else None
    except OSError as err:
        print(f"ds-verify: {err}", file=sys.stderr)
        return 3
    logs = [vr.read_jsonl(path) if os.path.exists(path) else None for path in (queries, checks)]
    report = run_all(text, logs[0], logs[1], db, args.overlay, request)
    print(render(report))
    if args.json:
        with open(args.json, "w") as handle:
            json.dump(report, handle, indent=2, default=str)
    return {"pass": 0, "fail": 1, "unverified": 2}[report["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
