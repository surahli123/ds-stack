#!/usr/bin/env python3
"""Have a model from another family try to break a ds-mode readout; keep only the findings a rerun proves.

    python3 tools/interrogate.py readout.md --request request.md --analyst-family claude
        [--queries .ds-queries.log] [--checks .ds-checks.log] [--db warehouse.db]
        [--reviewers 1] [--timeout 1200] [--out ds-interrogate] [--json report.json]

The reviewers come from $DS_OVERLAY_DIR/reviewers.json (see overlay.example/reviewers.json), else from the
defaults below: Codex for the GPT family, Claude Code for the Claude family. A reviewer is a command-line
agent run as its own process, so a readout written in Claude Code can be reviewed by Codex and the other way
round, whatever subagents the harness has. Only reviewers whose command is installed are used. They must
come from a family other than --analyst-family (or $DS_ANALYST_FAMILY). When none does, a reviewer of the
same family runs and the report says the review is not independent. When the analyst's or the reviewer's
family is unknown, the report says the family check didn't run.

Each reviewer works in a fresh directory under $TMPDIR, outside the project, with the readout, the request,
the analyst's logs and a private copy of the database, and a small environment (no unrelated keys). It runs
SQL only through ds-mode's query runner, which logs it, and writes findings.json (references/brief.md).
Afterwards its log, queries and findings are copied to --out, without the database copy. A finding is kept
only when all four hold:
  1. its readout_quote is a claim in the readout: at least 15 characters, with words, found in the readout;
  2. its query_id is a query that ran in the reviewer's log, and that query reads a data table of the
     database (a table name outside quotes), so a constant like `select 12.3` proves nothing;
  3. that query, replayed on a fresh copy of the data, gives the logged rows;
  4. its "shows" text quotes that query's output: at least one specific number (a decimal, or an integer of
     3 or more digits that isn't a year) is in the rows, and of its other numbers that aren't already in
     the readout or the analyst's logs, no more are missing from the rows than found in them. A number is
     compared after removing dates from text cells, and times 100 only when it is written with % or pp.
Whether a kept finding breaks the answer is for a person to judge; the report says so.

Exit code: 0 no verified finding, 1 at least one, 2 no reviewer could run, 3 usage error, 4 internal error.
"""

import argparse
import concurrent.futures as futures
import json
import os
import re
import shlex
import shutil
import signal
import sqlite3
import subprocess
import sys
import tempfile
import time
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
SKILLS = os.path.dirname(SKILL)
sys.path.insert(0, os.path.join(SKILLS, "ds-verify", "tools"))

import ds_verify as dv  # noqa: E402

QUERY_PY = os.path.join(SKILLS, "ds-mode", "tools", "query.py")
DEFAULT_REVIEWERS = [
    {"family": "gpt", "model": "-", "cmd": ["sh", "{tools}/reviewers/codex.sh", "{model}", "{prompt_file}"]},
    {"family": "claude", "model": "-", "cmd": ["sh", "{tools}/reviewers/claude.sh", "{model}", "{prompt_file}"]},
]
# A model slug's family, for --analyst-model and reviewers.json entries without a "family".
FAMILY_PREFIXES = (("claude", "claude"), ("opus", "claude"), ("sonnet", "claude"), ("haiku", "claude"),
                   ("gpt", "gpt"), ("o1", "gpt"), ("o3", "gpt"), ("o4", "gpt"), ("codex", "gpt"),
                   ("grok", "grok"), ("cursor-grok", "grok"), ("composer", "grok"), ("gemini", "gemini"))
KEYS = ("title", "readout_quote", "query_id", "shows", "why_it_matters")
# What a reviewer CLI needs from the environment: login, network, locale. Nothing else is passed.
ENV_KEEP = ("PATH", "HOME", "USER", "LOGNAME", "SHELL", "LANG", "LC_ALL", "LC_CTYPE", "TERM", "TMPDIR",
            "CODEX_HOME", "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "CLAUDE_CODE_OAUTH_TOKEN", "ANTHROPIC_BASE_URL",
            "CURSOR_API_KEY", "HTTPS_PROXY", "HTTP_PROXY", "NO_PROXY", "https_proxy", "http_proxy", "no_proxy",
            "SSL_CERT_FILE", "NODE_EXTRA_CA_CERTS", "REQUESTS_CA_BUNDLE", "DS_OVERLAY_DIR")
NUMBER_IN_TEXT = re.compile(r"(?<![A-Za-z_#\d.])([-+−]?\d+(?:[.,]\d+)*)\s*(%|％|pp\b|pts?\b|points?\b|个?百分点)?", re.I)


def family_of(model):
    model = (model or "").lower()
    return next((family for prefix, family in FAMILY_PREFIXES if model.startswith(prefix)), None)


def load_reviewers():
    overlay = os.environ.get("DS_OVERLAY_DIR")
    path = os.path.join(overlay, "reviewers.json") if overlay else None
    base = os.path.dirname(path) if path else HERE
    if path and os.path.exists(path):
        with open(path) as handle:
            entries = json.load(handle).get("reviewers", [])
    else:
        entries = DEFAULT_REVIEWERS
    reviewers = []
    for entry in entries:
        if not isinstance(entry, dict) or not entry.get("cmd"):
            print(f"ds-interrogate: skipping a reviewers.json entry without a command: {entry}", file=sys.stderr)
            continue
        family = (entry.get("family") or family_of(entry.get("model")) or "").lower() or None
        cmd = [str(tok).replace("{tools}", HERE) for tok in entry["cmd"]]
        if cmd[0] in ("sh", "bash") and len(cmd) > 1 and not os.path.isabs(cmd[1]):
            cmd[1] = os.path.join(base, cmd[1])
        reviewers.append({"family": family, "model": str(entry.get("model", "-")), "cmd": cmd})
    return reviewers


def installed(reviewer):
    """True when the command the reviewer finally runs is on PATH (the agent a wrapper script calls)."""
    cmd = reviewer["cmd"]
    if cmd[0] in ("sh", "bash") and len(cmd) > 1:
        if not os.path.exists(cmd[1]):
            return False
        programs = re.findall(r"^\s*(?:exec\s+)?(codex|claude|cursor-agent)\b", open(cmd[1]).read(), re.M)
        return all(shutil.which(p) for p in set(programs)) if programs else shutil.which(cmd[0]) is not None
    return shutil.which(cmd[0]) is not None


def choose(reviewers, analyst_family, count):
    """(chosen reviewers, independence note)."""
    available = [r for r in reviewers if installed(r)]
    if not available:
        return [], "no reviewer command is installed"
    if not analyst_family:
        return available[:count], "the analyst's family is unknown, so the family check didn't run"
    other = [r for r in available if r["family"] and r["family"] != analyst_family]
    if other:
        return other[:count], f"independent: reviewer family differs from the analyst's ({analyst_family})"
    unknown = [r for r in available if not r["family"]]
    if unknown:
        return unknown[:count], "a reviewer's family is unknown, so the family check didn't run"
    return available[:count], f"not independent: every installed reviewer is in the analyst's family ({analyst_family})"


# --- one reviewer --------------------------------------------------------------------------------------------

def private_database(db, dest):
    """Copy the database for a reviewer to query and write to, without the analysis's scratch tables."""
    with tempfile.TemporaryDirectory(prefix="ds-interrogate-") as workdir:
        conn = dv.scratch_copy(db, workdir, dv.scratch_prefix())
        try:
            target = sqlite3.connect(dest)
            conn.backup(target)
            target.close()
        finally:
            conn.close()


def prepare(workdir, readout, request, queries, checks, db):
    shutil.copy(readout, os.path.join(workdir, "readout.md"))
    with open(os.path.join(workdir, "request.md"), "w", encoding="utf-8") as handle:
        handle.write(request)
    for source, name in ((queries, "evidence.queries.log"), (checks, "evidence.checks.log")):
        if source and os.path.exists(source):
            shutil.copy(source, os.path.join(workdir, name))
        else:
            open(os.path.join(workdir, name), "w").close()
    private_database(db, os.path.join(workdir, "warehouse.db"))
    query_cmd = f"python3 {shlex.quote(QUERY_PY)} --db warehouse.db"
    with open(os.path.join(SKILL, "references", "brief.md"), encoding="utf-8") as handle:
        brief = handle.read().replace("{query_cmd}", query_cmd)
    prompt_file = os.path.join(workdir, ".brief.md")
    with open(prompt_file, "w", encoding="utf-8") as handle:
        handle.write(brief)
    return prompt_file


def reviewer_env(workdir):
    env = {k: os.environ[k] for k in ENV_KEEP if k in os.environ}
    env.update(DS_QUERIES_LOG=os.path.join(workdir, "review.queries.log"), DS_QUERY_PY=QUERY_PY,
               DS_CHECKS_LOG=os.path.join(workdir, "review.checks.log"), DS_RUN_ID="review")
    return env


SERVED_MODEL = re.compile(r"^model:\s*([\w.:/-]+)\s*$", re.M)  # the header Codex prints on stderr


def served_model(log_text):
    """The model a reviewer CLI says it ran, when it prints one, else None."""
    match = SERVED_MODEL.search(log_text or "")
    return match.group(1) if match else None


def run_reviewer(reviewer, workdir, prompt_file, timeout):
    cmd = [tok.replace("{model}", reviewer["model"] or "-").replace("{prompt_file}", prompt_file) for tok in reviewer["cmd"]]
    started = time.time()
    proc = subprocess.Popen(cmd, cwd=workdir, env=reviewer_env(workdir), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            stdin=subprocess.DEVNULL, start_new_session=True)
    try:
        out, err = proc.communicate(timeout=timeout)
        code = proc.returncode
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGKILL)  # the agent and everything it started
        out, err = proc.communicate()
        code = "timeout"
    stdout, stderr = (b.decode("utf-8", errors="replace") for b in (out or b"", err or b""))
    with open(os.path.join(workdir, "reviewer.log"), "w", encoding="utf-8") as handle:
        handle.write(f"$ {shlex.join(cmd)}\nexit {code} after {time.time() - started:.0f}s\n\n{stderr}\n\n{stdout}")
    return stdout, code, served_model(stderr) if reviewer["model"] in (None, "", "-") else None


def read_findings(workdir, stdout):
    """The findings list from findings.json, else the last JSON list in the reply, else None."""
    path = os.path.join(workdir, "findings.json")
    candidates = [open(path, encoding="utf-8", errors="replace").read()] if os.path.exists(path) else []
    candidates += re.findall(r"```(?:json)?\s*(\[.*?\])\s*```", stdout or "", re.S)[::-1]
    for text in candidates:
        try:
            data = json.loads(text)
        except ValueError:
            continue
        if isinstance(data, dict):
            data = data.get("findings")
        if isinstance(data, list):
            return [f for f in data if isinstance(f, dict)]
    return None


# --- the four rules ------------------------------------------------------------------------------------------

def normal(text):
    return re.sub(r"\s+", " ", dv.vr._clean(str(text))).strip().lower()


def data_tables(db):
    """The tables and views a proof may read: everything in the database but the scratch area."""
    conn = sqlite3.connect(f"file:{os.path.abspath(db)}?mode=ro", uri=True)
    try:
        names = [n for (n,) in conn.execute("select name from sqlite_master where type in ('table', 'view')")]
    finally:
        conn.close()
    return [n for n in names if not n.startswith(dv.scratch_prefix())]


def reads_a_table(sql, tables):
    bare = re.sub(r"'(?:[^']|'')*'|\"(?:[^\"]|\"\")*\"", " ", str(sql))  # string literals don't count
    return any(re.search(rf"(?<![\w.]){re.escape(t)}(?!\w)", bare, re.I) for t in tables)


def cell_values(rows):
    """Numbers in the output: numeric cells, and numbers in text cells once dates are removed."""
    values = []
    for row in rows or []:
        for cell in row:
            if isinstance(cell, bool) or cell is None:
                continue
            if isinstance(cell, (int, float)):
                values.append(float(cell))
            else:
                text = dv.vr.DATE.sub(" ", str(cell))
                values += [float(m) for m in re.findall(r"(?<![\d.])[-+]?\d+(?:\.\d+)?", text)]
    return values


def shown_numbers(text):
    """[(token, percent)] in a "shows" text, once each, without dates, date ranges and CI levels."""
    cleaned = dv.vr.CI_LEVEL.sub(" ", dv.vr.DATE.sub(" ", re.sub(r"\b\d{2}-\d{2}\b", " ", str(text))))
    seen, found = set(), []
    for match in NUMBER_IN_TEXT.finditer(cleaned):
        token = match.group(1).replace(",", "") if re.fullmatch(r"[-+−]?\d{1,3}(?:,\d{3})+", match.group(1)) else match.group(1)
        if token.lstrip("+-−") not in seen:
            seen.add(token.lstrip("+-−"))
            found.append((token, bool(match.group(2))))
    return found


def specific(token):
    """A number that can't match by chance: a decimal, or an integer of 3+ digits that isn't a year."""
    digits = token.lstrip("+-−")
    if "." in digits:
        return True
    return len(digits) >= 3 and not (len(digits) == 4 and 1900 <= int(digits) <= 2100)


def in_values(token, percent, values):
    return any(dv.close(token, v) or (percent and dv.close(token, v * 100)) for v in values)


def verify_findings(findings, readout_text, review_queries, db, evidence=()):
    """(kept, dropped): each kept finding carries its query; each dropped one its reason."""
    replay = {f.get("ref"): f for f in dv.check_replay(review_queries, db)} if review_queries else {}
    by_id = {str(q.get("id") or "").lower(): q for q in review_queries if isinstance(q, dict) and q.get("id")}
    tables = data_tables(db)
    readout = normal(readout_text)
    context = cell_values([[readout_text]]) + list(evidence)  # numbers the reviewer may quote back
    kept, dropped = [], []
    for finding in findings:
        finding = {k: v if isinstance(v, str) else json.dumps(v, ensure_ascii=False) for k, v in finding.items()}
        missing = [k for k in KEYS if not finding.get(k, "").strip()]
        quote = normal(finding.get("readout_quote", ""))
        qid = finding.get("query_id", "").strip().strip("[]").lower()
        query = by_id.get(qid)
        numbers = shown_numbers(finding.get("shows", ""))
        reason = None
        if missing:
            reason = f"missing {', '.join(missing)}"
        elif len(quote) < 15 or not re.search(r"[a-z一-鿿]", quote):
            reason = "its quote is too short to name a claim (15 characters or more, with words)"
        elif quote not in readout:
            reason = "its quote isn't in the readout"
        elif not query or query.get("status") != "ok":
            reason = f"{qid or 'no id'} isn't a query that ran in the reviewer's log"
        elif not reads_a_table(query.get("sql"), tables):
            reason = f"{query['id']} reads no data table, so its output proves nothing about the data"
        elif replay.get(query["id"], {}).get("status") != "pass":
            reason = f"{query['id']} didn't reproduce: {replay.get(query['id'], {}).get('message', 'not replayed')}"
        elif not numbers:
            reason = "its shows text quotes no number from the query's output"
        else:
            rows = cell_values(query.get("rows"))
            anchors = [t for t, pct in numbers if specific(t) and in_values(t, pct, rows)]
            in_rows = [t for t, pct in numbers if in_values(t, pct, rows)]
            others = [t for t, pct in numbers if t not in in_rows and not in_values(t, True, context)]
            if not anchors:
                reason = f"none of its specific numbers is in the output of {query['id']} ({', '.join(t for t, _ in numbers[:6])})"
            elif len(others) > len(in_rows):
                reason = f"most of its numbers aren't in the output of {query['id']}: {', '.join(others[:6])}"
            else:
                finding["unmatched"] = others
        if reason:
            dropped.append({"title": finding.get("title", "")[:120], "reason": reason})
        else:
            kept.append({**{k: finding[k] for k in KEYS}, "sql": query.get("sql"), "rows": (query.get("rows") or [])[:8],
                         "columns": query.get("columns"), "unmatched": finding.get("unmatched", [])})
    return kept, dropped


# --- running -------------------------------------------------------------------------------------------------

def review(reviewer, args, request, out_dir, index):
    name = f"reviewer-{index}-{reviewer['family'] or 'unknown'}"
    result = {"reviewer": f"{reviewer['family']}:{reviewer['model']}", "dir": os.path.join(out_dir, name)}
    # The reviewer works outside the project, so it can't reach the analysis files by relative path and
    # doesn't inherit the project's AGENTS.md or CLAUDE.md. Only its record comes back, never the data.
    workdir = tempfile.mkdtemp(prefix="ds-interrogate-review-")
    try:
        prompt_file = prepare(workdir, args.readout, request, args.queries, args.checks, args.db)
        stdout, code, served = run_reviewer(reviewer, workdir, prompt_file, args.timeout)
        result["exit"] = code
        if served:  # "-" means the CLI's default model; record which one it was
            result["reviewer"] = f"{reviewer['family']}:{served}"
        findings = read_findings(workdir, stdout)
        review_queries = dv.vr.read_jsonl(os.path.join(workdir, "review.queries.log"))
        if findings is None:
            return {**result, "ran": False, "kept": [], "dropped": [],
                    "problem": "no findings.json and no JSON list in its reply" + (f" (exit {code})" if code != 0 else "")}
        evidence = dv.values_in([q.get("rows") for q in dv.vr.read_jsonl(args.queries)]
                                + [{"s": c.get("summary"), "d": c.get("details")} for c in dv.vr.read_jsonl(args.checks)], [])
        with open(args.readout, encoding="utf-8") as handle:
            kept, dropped = verify_findings(findings, handle.read(), review_queries, args.db, evidence)
        return {**result, "ran": True, "kept": kept, "dropped": dropped}
    except Exception as err:  # noqa: BLE001 - one reviewer's failure is reported, not fatal
        return {**result, "ran": False, "kept": [], "dropped": [], "problem": f"{type(err).__name__}: {err}"}
    finally:
        os.makedirs(result["dir"], exist_ok=True)
        for kept_file in ("reviewer.log", "findings.json", "review.queries.log", "review.checks.log", ".brief.md"):
            if os.path.exists(os.path.join(workdir, kept_file)):
                shutil.copy(os.path.join(workdir, kept_file), result["dir"])
        shutil.rmtree(workdir, ignore_errors=True)


def merge(results):
    """Verified findings, one per readout quote and title, with the reviewers that found each."""
    groups = {}
    for result in results:
        for finding in result["kept"]:
            key = (normal(finding["readout_quote"]), normal(finding["title"]))
            group = groups.setdefault(key, {**finding, "reviewers": []})
            if result["reviewer"] not in group["reviewers"]:
                group["reviewers"].append(result["reviewer"])
    return list(groups.values())


def render(report):
    lines = [f"ds-interrogate: {len(report['findings'])} verified finding(s) from "
             f"{', '.join(r['reviewer'] for r in report['results'] if r['ran']) or 'no reviewer'}; {report['independence']}"]
    for i, finding in enumerate(report["findings"], 1):
        lines += [f"{i}. {finding['title']}  ({', '.join(finding['reviewers'])})",
                  f"   readout says: {finding['readout_quote']}",
                  f"   query: {finding['sql']}",
                  f"   rows: {json.dumps(finding['rows'], default=str)[:300]}",
                  f"   shows: {finding['shows']}"]
        if finding.get("unmatched"):
            lines.append(f"   not in the rows (derived or unproven): {', '.join(finding['unmatched'])}")
        lines.append(f"   why it matters (the reviewer's claim, for you to judge): {finding['why_it_matters']}")
    for result in report["results"]:
        if not result["ran"]:
            lines.append(f"{result['reviewer']} didn't run: {result['problem']}; see {result['dir']}/reviewer.log")
        elif result["dropped"]:
            reasons = "; ".join(f"{d['title'][:60]}: {d['reason']}" for d in result["dropped"])
            lines.append(f"{result['reviewer']} dropped {len(result['dropped'])}: {reasons}")
    if not report["findings"] and any(r["ran"] for r in report["results"]):
        lines.append("No verified findings. That doesn't prove the readout right; it means no reviewer proved it wrong.")
    return "\n".join(lines)


def run(args):
    try:
        with open(args.request, encoding="utf-8") as handle:
            request = handle.read()
        open(args.readout).close()
    except OSError as err:
        print(f"ds-interrogate: {err}", file=sys.stderr)
        return 3
    if not os.path.exists(args.db):
        print(f"ds-interrogate: no database at {args.db}; pass --db", file=sys.stderr)
        return 3
    analyst = (args.analyst_family or family_of(args.analyst_model) or "").lower() or None
    chosen, independence = choose(load_reviewers(), analyst, args.reviewers)
    os.makedirs(args.out, exist_ok=True)
    ignore = os.path.join(args.out, ".gitignore")
    if not os.path.exists(ignore):
        with open(ignore, "w") as handle:
            handle.write("# Reviewer records hold query results; keep them out of git.\n*\n")
    # A unique, absolute directory per run, so two runs in the same second don't collide.
    out_dir = os.path.abspath(tempfile.mkdtemp(prefix=time.strftime("%Y%m%d-%H%M%S-"), dir=args.out))
    with futures.ThreadPoolExecutor(max_workers=max(1, len(chosen))) as pool:
        results = list(pool.map(lambda pair: review(pair[1], args, request, out_dir, pair[0]), enumerate(chosen, 1)))
    report = {"independence": independence, "results": results, "findings": merge(results)}
    print(render(report))
    if args.json:
        with open(args.json, "w") as handle:
            json.dump(report, handle, indent=2, default=str)
    if not any(r["ran"] for r in results):
        return 2
    return 1 if report["findings"] else 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("readout")
    parser.add_argument("--request", required=True, help="a file holding the original request")
    parser.add_argument("--queries", default=os.environ.get("DS_QUERIES_LOG") or ".ds-queries.log")
    parser.add_argument("--checks", default=os.environ.get("DS_CHECKS_LOG") or ".ds-checks.log")
    parser.add_argument("--db", default=os.environ.get("DS_WAREHOUSE") or "warehouse.db")
    parser.add_argument("--analyst-family", default=os.environ.get("DS_ANALYST_FAMILY"),
                        help="the analyst's model family: claude, gpt, grok, gemini, ...")
    parser.add_argument("--analyst-model", default=os.environ.get("DS_ANALYST_MODEL"),
                        help="the analyst's model slug, when its family isn't given")
    parser.add_argument("--reviewers", type=int, default=1, help="how many reviewers to run, in config order")
    parser.add_argument("--timeout", type=int, default=1200)
    parser.add_argument("--out", default="ds-interrogate", help="where each reviewer's record is kept")
    parser.add_argument("--json", help="also write the report as JSON")
    args = parser.parse_args(argv)
    try:
        return run(args)
    except Exception:  # noqa: BLE001 - an internal error must not read as "1: a verified finding"
        traceback.print_exc()
        return 4


if __name__ == "__main__":
    sys.exit(main())
