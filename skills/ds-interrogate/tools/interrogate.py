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
same family runs and the report says the review is not independent. When the analyst's family is unknown,
the report says the family check didn't run.

Each reviewer works in a fresh directory with the readout, the request, the analyst's logs and a private
copy of the database, and runs SQL only through ds-mode's query runner, which logs it. It writes
findings.json (references/brief.md). A finding is kept only when all four hold:
  1. its readout_quote is in the readout;
  2. its query_id is a query that ran in the reviewer's log;
  3. that query, replayed on a fresh copy of the data, gives the logged rows;
  4. every number in its "shows" text is in that query's output.
Whether a kept finding breaks the answer is for a person to judge; the report says so.

Exit code: 0 no verified finding, 1 at least one, 2 no reviewer could run, 3 usage error.
"""

import argparse
import concurrent.futures as futures
import json
import os
import re
import shlex
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time

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
FAMILY_PREFIXES = (("claude", "claude"), ("gpt", "gpt"), ("o1", "gpt"), ("o3", "gpt"), ("o4", "gpt"),
                   ("codex", "gpt"), ("grok", "grok"), ("cursor-grok", "grok"), ("composer", "grok"),
                   ("gemini", "gemini"))
KEYS = ("title", "readout_quote", "query_id", "shows", "why_it_matters")


def family_of(model):
    model = (model or "").lower()
    return next((family for prefix, family in FAMILY_PREFIXES if model.startswith(prefix)), None)


def load_reviewers():
    overlay = os.environ.get("DS_OVERLAY_DIR")
    path = os.path.join(overlay, "reviewers.json") if overlay else None
    if path and os.path.exists(path):
        with open(path) as handle:
            entries = json.load(handle).get("reviewers", [])
    else:
        entries = DEFAULT_REVIEWERS
    reviewers = []
    for entry in entries:
        family = entry.get("family") or family_of(entry.get("model"))
        cmd = [tok.replace("{tools}", HERE) for tok in entry["cmd"]]
        reviewers.append({"family": family, "model": entry.get("model", "-"), "cmd": cmd})
    return reviewers


def installed(reviewer):
    """True when the command the reviewer finally runs is on PATH (the script after `sh`, else the program)."""
    cmd = reviewer["cmd"]
    if cmd[0] in ("sh", "bash") and len(cmd) > 1 and os.path.exists(cmd[1]):
        wrapper = open(cmd[1]).read()
        programs = re.findall(r"^\s*(?:exec\s+)?(codex|claude|cursor-agent)\b", wrapper, re.M)
        return all(shutil.which(p) for p in set(programs)) if programs else True
    return shutil.which(cmd[0]) is not None


def choose(reviewers, analyst_family, count):
    """(chosen reviewers, independence note)."""
    available = [r for r in reviewers if installed(r)]
    if not available:
        return [], "no reviewer command is installed"
    if not analyst_family:
        return available[:count], "the analyst's family is unknown, so the family check didn't run"
    other = [r for r in available if r["family"] != analyst_family]
    if other:
        return other[:count], f"independent: reviewer family differs from the analyst's ({analyst_family})"
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


def run_reviewer(reviewer, workdir, prompt_file, timeout):
    cmd = [tok.replace("{model}", reviewer["model"] or "-").replace("{prompt_file}", prompt_file) for tok in reviewer["cmd"]]
    env = dict(os.environ, DS_QUERIES_LOG=os.path.join(workdir, "review.queries.log"),
               DS_CHECKS_LOG=os.path.join(workdir, "review.checks.log"), DS_RUN_ID="review")
    env.pop("DS_WAREHOUSE", None)
    started = time.time()
    try:
        proc = subprocess.run(cmd, cwd=workdir, env=env, capture_output=True, text=True, timeout=timeout,
                              stdin=subprocess.DEVNULL)
        stdout, stderr, code = proc.stdout, proc.stderr, proc.returncode
    except subprocess.TimeoutExpired as err:
        stdout = err.stdout.decode() if isinstance(err.stdout, bytes) else (err.stdout or "")
        stderr, code = "", "timeout"
    except OSError as err:
        stdout, stderr, code = "", str(err), f"error: {err}"
    with open(os.path.join(workdir, "reviewer.log"), "w", encoding="utf-8") as handle:
        handle.write(f"$ {shlex.join(cmd)}\nexit {code} after {time.time() - started:.0f}s\n\n{stderr}\n\n{stdout}")
    return stdout, code


def read_findings(workdir, stdout):
    """The findings list from findings.json, else the last JSON list in the reply, else None."""
    path = os.path.join(workdir, "findings.json")
    candidates = [open(path, encoding="utf-8").read()] if os.path.exists(path) else []
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


def normal(text):
    return re.sub(r"\s+", " ", vr_clean(str(text))).strip().lower()


def vr_clean(text):
    return dv.vr._clean(text)


def verify_findings(findings, readout_text, review_queries, db):
    """(kept, dropped): each kept finding carries its query; each dropped one its reason."""
    replay = {f.get("ref"): f for f in dv.check_replay(review_queries, db)} if review_queries else {}
    by_id = {q["id"].lower(): q for q in review_queries if q.get("id")}
    readout = normal(readout_text)
    kept, dropped = [], []
    for finding in findings:
        missing = [k for k in KEYS if not str(finding.get(k, "")).strip()]
        qid = str(finding.get("query_id", "")).strip().strip("[]").lower()
        query = by_id.get(qid)
        if missing:
            reason = f"missing {', '.join(missing)}"
        elif normal(finding["readout_quote"]) not in readout:
            reason = "its quote isn't in the readout"
        elif not query or query.get("status") != "ok":
            reason = f"{qid or 'no id'} isn't a query that ran in the reviewer's log"
        elif replay.get(query["id"], {}).get("status") != "pass":
            reason = f"{query['id']} didn't reproduce: {replay.get(query['id'], {}).get('message', 'not replayed')}"
        else:
            numbers = dv.vr.numbers_in(str(finding["shows"]))
            values = dv.values_in(query.get("rows"), [])
            unmatched = [n for n in numbers if not any(dv.close(n, v) or dv.close(n, v * 100) for v in values)]
            reason = f"its output doesn't show {', '.join(unmatched)}" if unmatched else None
        if reason:
            dropped.append({"title": str(finding.get("title", ""))[:120], "reason": reason})
        else:
            kept.append({**{k: finding[k] for k in KEYS}, "sql": query.get("sql"), "rows": (query.get("rows") or [])[:8],
                         "columns": query.get("columns")})
    return kept, dropped


def review(reviewer, args, request, out_dir, index):
    workdir = os.path.join(out_dir, f"reviewer-{index}-{reviewer['family'] or 'unknown'}")
    os.makedirs(workdir)
    prompt_file = prepare(workdir, args.readout, request, args.queries, args.checks, args.db)
    stdout, code = run_reviewer(reviewer, workdir, prompt_file, args.timeout)
    findings = read_findings(workdir, stdout)
    result = {"reviewer": f"{reviewer['family']}:{reviewer['model']}", "exit": code, "dir": workdir}
    if findings is None:
        return {**result, "ran": False, "kept": [], "dropped": [],
                "problem": "no findings.json and no JSON list in its reply" + (f" (exit {code})" if code != 0 else "")}
    review_queries = dv.vr.read_jsonl(os.path.join(workdir, "review.queries.log"))
    with open(args.readout, encoding="utf-8") as handle:
        kept, dropped = verify_findings(findings, handle.read(), review_queries, args.db)
    return {**result, "ran": True, "kept": kept, "dropped": dropped}


# --- report --------------------------------------------------------------------------------------------------

def merge(results):
    """Verified findings grouped by the readout words they challenge, with the reviewers that found each."""
    groups = {}
    for result in results:
        for finding in result["kept"]:
            key = normal(finding["readout_quote"])
            group = groups.setdefault(key, {**finding, "reviewers": []})
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
                  f"   shows: {finding['shows']}",
                  f"   why it matters (the reviewer's claim, for you to judge): {finding['why_it_matters']}"]
    for result in report["results"]:
        if not result["ran"]:
            lines.append(f"{result['reviewer']} didn't run: {result['problem']}; see {result['dir']}/reviewer.log")
        elif result["dropped"]:
            reasons = "; ".join(f"{d['title'][:60]}: {d['reason']}" for d in result["dropped"])
            lines.append(f"{result['reviewer']} dropped {len(result['dropped'])}: {reasons}")
    if not report["findings"] and any(r["ran"] for r in report["results"]):
        lines.append("No verified findings. That doesn't prove the readout right; it means no reviewer proved it wrong.")
    return "\n".join(lines)


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
    parser.add_argument("--out", default="ds-interrogate", help="where each reviewer's directory is kept")
    parser.add_argument("--json", help="also write the report as JSON")
    args = parser.parse_args(argv)
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
    # Absolute, because each reviewer runs with its own directory as the working directory.
    out_dir = os.path.abspath(os.path.join(args.out, time.strftime("%Y%m%d-%H%M%S")))
    os.makedirs(out_dir, exist_ok=True)
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


if __name__ == "__main__":
    sys.exit(main())
