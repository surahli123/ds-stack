#!/usr/bin/env python3
"""Fill in the acceptance table in docs/acceptance.md from results directories.

    python3 eval/acceptance.py eval/results/<dir> [<dir> ...] [--allow-no-transcript] [--diagnostic]

Each directory is one harness and one language (zh when its runs carry a prompt
suffix). For each, prints the Plumbing, Correctness and Value levels with their
counts and PASS or FAIL. The thresholds below are the ones docs/acceptance.md
fixed before the first acceptance run; changing one restarts the count.

A directory where any run didn't execute (rate-limited, at capacity, not isolated,
crashed, or an API error), or where run_arms.py left jobs unstarted, is
INVALID: its levels aren't computed, because they would measure the failures,
not the agent. --diagnostic prints them anyway, marked as diagnostic only. A
directory named in eval/never_grade.txt is refused, and one with no runs is
skipped. Exit code: 0 when every directory was assessed, 2 when any was INVALID
or refused, 3 when none exists.
"""

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "skills", "ds-mode", "tools"))

import grade  # noqa: E402
import verify_readout  # noqa: E402

FIXTURES = [f"f{i}" for i in range(1, 9)]
VALUE_FIXTURES = ["f6", "f7", "f8"]
MIN_BASELINE_MISS = 0.30


def plumbing_ok(run_dir):
    """Every full-arm run: a query ran, every completed check names its source, the trace resolves."""
    queries = verify_readout.read_jsonl(os.path.join(run_dir, "queries.log"))
    checks = verify_readout.read_jsonl(os.path.join(run_dir, "checks.log"))
    completed = [c for c in checks if c.get("status") != "could_not_run"]
    with open(os.path.join(run_dir, "result.md")) as handle:
        problems, _, _ = verify_readout.verify(handle.read(), queries, checks)
    reasons = []
    if not any(q.get("status") == "ok" for q in queries):
        reasons.append("no logged query ran")
    if any(not c.get("from") for c in completed):
        reasons.append("a completed check has no source query")
    if problems:
        reasons.append("verify_readout: " + problems[0])
    return reasons


def not_started(results_dir):
    path = os.path.join(results_dir, "run-status.json")
    if not os.path.exists(path):
        return []
    with open(path) as handle:
        return json.load(handle).get("not_started", [])


def invalid_reason(runs, results_dir):
    """Why a directory's levels can't be computed, or None."""
    failed = {}
    for r in runs:
        if r["miss"] == "not_executed":
            failed[r["execution"]] = failed.get(r["execution"], 0) + 1
    unstarted = not_started(results_dir)
    if not failed and not unstarted:
        return None
    kinds = ", ".join(f"{kind} {n}" for kind, n in sorted(failed.items(), key=lambda kv: -kv[1]))
    parts = [f"{sum(failed.values())} of {len(runs)} runs didn't execute" + (f" ({kinds})" if kinds else "")]
    if unstarted:
        parts.append(f"{len(unstarted)} jobs never started")
    return "; ".join(parts)


def assess(results_dir, allow_no_transcript):
    runs = grade.grade_dir(results_dir, allow_no_transcript)
    with open(os.path.join(HERE, "pass_rule.json")) as handle:
        rule = json.load(handle)
    _, _, cells, _, _ = grade.summarize(runs, rule)
    language = "zh" if any(r.get("prompt_suffix") for r in runs) else "en"
    harness = next((r.get("agent_cmd") for r in runs if r.get("agent_cmd")), None) or "claude -p"

    full_runs = [r for r in runs if r["arm"] == "full"]
    plumbing_fail = {}
    for r in full_runs:
        reasons = plumbing_ok(os.path.join(results_dir, f"{r['fixture']}__full__{r['run']}"))
        if reasons:
            plumbing_fail[f"{r['fixture']}#{r['run']}"] = reasons[0]

    def correct(fixture, arm):
        return cells.get((fixture, arm), {}).get("outcome") == "correct"

    present = [f for f in FIXTURES if (f, "full") in cells]
    wrong = [f for f in present if not correct(f, "full")]
    base_value = [r for r in runs if r["arm"] == "baseline" and r["fixture"] in VALUE_FIXTURES]
    miss_rate = sum(not r["correct"] for r in base_value) / len(base_value) if base_value else None
    full_value = sum(correct(f, "full") for f in VALUE_FIXTURES)
    base_fixtures = sum(correct(f, "baseline") for f in VALUE_FIXTURES)
    return {
        "dir": os.path.basename(results_dir.rstrip("/")), "harness": harness, "language": language,
        "invalid": invalid_reason(runs, results_dir),
        "plumbing": (len(full_runs) - len(plumbing_fail), len(full_runs), plumbing_fail),
        "correctness": (len(present) - len(wrong), len(present), wrong, present == FIXTURES),
        "value": (miss_rate, full_value, base_fixtures, len(base_value)),
    }


def render(row, diagnostic=False):
    title = f"### {row['dir']} ({row['harness']}, {row['language']})"
    if row["invalid"]:
        verdict = (f"INVALID, not an acceptance result: {row['invalid']}. The levels would measure these failures, "
                   "not the agent, so fix the cause and rerun into a new directory.")
        if not diagnostic:
            return f"{title}\n\n{verdict}\n"
        title = f"{title}: DIAGNOSTIC ONLY\n\n{verdict}"
    ok_runs, n_runs, failed = row["plumbing"]
    right, n_fix, wrong, complete = row["correctness"]
    miss_rate, full_value, base_value, n_base = row["value"]
    plumbing = "PASS" if n_runs and ok_runs == n_runs else "FAIL"
    correctness = "PASS" if complete and not wrong else ("FAIL" if complete else "INCOMPLETE (not all of f1-f8 ran)")
    if not n_base:
        value = "INCOMPLETE (no baseline runs on f6-f8)"
    else:
        value = "PASS" if miss_rate >= MIN_BASELINE_MISS and full_value > base_value else "FAIL"
    lines = [title, "",
             "| Level | Result | Counts |", "|---|---|---|",
             f"| Plumbing | {plumbing} | {ok_runs} of {n_runs} full-arm runs |",
             f"| Correctness | {correctness} | {right} of {n_fix} fixtures right by majority |",
             f"| Value | {value} | plain prompting missed {0 if miss_rate is None else round(100 * miss_rate)}% of "
             f"{n_base} runs on f6-f8; fixtures right: full {full_value}, plain {base_value} |", ""]
    for run, reason in failed.items():
        lines.append(f"- Plumbing failure {run}: {reason}")
    if wrong:
        lines.append(f"- Fixtures the full arm got wrong: {', '.join(wrong)}")
    return "\n".join(lines).rstrip() + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("results_dirs", nargs="+")
    parser.add_argument("--allow-no-transcript", action="store_true",
                        help="grade runs from a custom agent (Codex, Cursor) whose isolation can't be checked")
    parser.add_argument("--diagnostic", action="store_true",
                        help="also print the levels of an INVALID directory, marked diagnostic only")
    args = parser.parse_args(argv)
    found = [d for d in args.results_dirs if os.path.isdir(d)]
    for missing in sorted(set(args.results_dirs) - set(found)):
        print(f"acceptance: skipping {missing}: not a directory (a harness that didn't run?)", file=sys.stderr)
    if not found:
        return 3
    status = 0
    for results_dir in found:
        refused = grade.never_grade(results_dir)
        if refused:
            print(f"### {os.path.basename(os.path.normpath(results_dir))}\n\nREFUSED: {refused}\n")
            status = 2
            continue
        if not grade.grade_dir(results_dir, args.allow_no_transcript):
            print(f"acceptance: skipping {results_dir}: it holds no runs (a report directory?)", file=sys.stderr)
            continue
        row = assess(results_dir, args.allow_no_transcript)
        print(render(row, args.diagnostic))
        status = 2 if row["invalid"] else status
    return status


if __name__ == "__main__":
    sys.exit(main())
