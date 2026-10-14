#!/usr/bin/env python3
"""One-command pass/fail for a ds-mode smoke test, whichever agent ran it.

    python3 eval/smoke_check.py <run dir> [--fixture f1]

<run dir> is where the agent worked: it holds the fixture's warehouse.db and,
after the run, readout.md, .ds-queries.log and .ds-checks.log. Prints one line
per check, then PASS or FAIL. Exit code: 0 pass, 1 fail, 3 usage error.

The checks: the readout exists; queries were logged; at least one check names
its source query; verify_readout.py passes (every number traces to a log; this
says nothing about whether the number is right); the estimand the fixture asks
for and the causes match its gold answer, which is loaded only here, after the
agent has finished.
"""

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "skills", "ds-mode", "tools"))

import verify_readout  # noqa: E402
from grade import grade_readout, load_gold  # noqa: E402
from readout import parse  # noqa: E402


def check(run_dir, fixture):
    """Return a list of (ok, line)."""
    results = []
    path = os.path.join(run_dir, "readout.md")
    text = open(path).read() if os.path.exists(path) else ""
    results.append((bool(text), "readout.md exists" if text else "readout.md is missing: the agent didn't finish ds-mode step 7"))
    queries = verify_readout.read_jsonl(os.path.join(run_dir, ".ds-queries.log"))
    ran = [q for q in queries if q.get("status") == "ok"]
    results.append((bool(ran), f"{len(ran)} logged queries ran" if ran
                    else "no logged queries: the agent queried the data without tools/query.py"))
    checks = verify_readout.read_jsonl(os.path.join(run_dir, ".ds-checks.log"))
    completed = [c for c in checks if c.get("status") != "could_not_run"]
    sourced = [c for c in completed if c.get("from")]
    skipped = len(checks) - len(completed)
    note = f" ({skipped} more could not run, kept in the log)" if skipped else ""
    results.append((bool(sourced), f"{len(sourced)} of {len(completed)} completed checks name their source query{note}" if sourced
                    else f"no completed check names its source query ({len(checks)} checks logged)"))
    if text:
        problems, _, _ = verify_readout.verify(text, queries, checks)
        results.append((not problems, "verify_readout (trace only): pass" if not problems
                        else "verify_readout (trace only): fail: " + "; ".join(problems[:3])))
        correct, reason, _ = grade_readout(parse(text), load_gold(fixture))
        results.append((correct, f"answer vs gold: {reason}"))
    return results


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("run_dir")
    parser.add_argument("--fixture", default="f1")
    args = parser.parse_args(argv)
    if not os.path.isdir(args.run_dir):
        print(f"smoke_check: no directory at {args.run_dir}", file=sys.stderr)
        return 3
    results = check(args.run_dir, args.fixture)
    for ok, line in results:
        print(f"{'ok  ' if ok else 'FAIL'} {line}")
    failed = sum(not ok for ok, _ in results)
    print("PASS" if not failed else f"FAIL ({failed} of {len(results)} checks)")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
