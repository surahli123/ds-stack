#!/usr/bin/env python3
"""Measure ds-verify against graded runs: does it fail the runs grade.py marks wrong, and pass the right ones?

    python3 eval/verify_eval.py eval/results/<dir> [<dir> ...] [--arms full] [--allow-no-transcript]

ds-verify never sees gold. Each run is checked with its fixture's warehouse.db, overlay and task.md (the
request), the way it would be checked at work. The grade comes from grade.py. Prints, per arm, how many
wrong runs ds-verify failed (caught) and how many right runs it failed (false alarms), and which checks
fired on each side.
"""

import argparse
import collections
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "skills", "ds-verify", "tools"))

import ds_verify  # noqa: E402
import grade  # noqa: E402
from execution import executed  # noqa: E402

FIXTURES = os.path.join(HERE, "fixtures")


def verify_run(run_dir, fixture):
    fixture_dir = os.path.join(FIXTURES, fixture)
    overlay = os.path.join(fixture_dir, "overlay")
    with open(os.path.join(run_dir, "result.md"), encoding="utf-8") as handle:
        text = handle.read()
    with open(os.path.join(fixture_dir, "task.md"), encoding="utf-8") as handle:
        request = handle.read()
    return ds_verify.run_all(text, ds_verify.vr.read_jsonl(os.path.join(run_dir, "queries.log")),
                             ds_verify.vr.read_jsonl(os.path.join(run_dir, "checks.log")),
                             os.path.join(fixture_dir, "warehouse.db"),
                             overlay if os.path.isdir(overlay) else None, request)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("results_dirs", nargs="+")
    parser.add_argument("--arms", default="full")
    parser.add_argument("--allow-no-transcript", action="store_true")
    args = parser.parse_args(argv)
    arms = args.arms.split(",")
    table = collections.defaultdict(lambda: collections.Counter())
    fired = collections.defaultdict(collections.Counter)
    details = []
    for results_dir in args.results_dirs:
        for run in grade.grade_dir(results_dir, args.allow_no_transcript):
            if run["arm"] not in arms or not executed(run.get("execution", "ok")) or run["miss"] == "contaminated":
                continue
            run_dir = os.path.join(results_dir, f"{run['fixture']}__{run['arm']}__{run['run']}")
            report = verify_run(run_dir, run["fixture"])
            side = "right" if run["correct"] else "wrong"
            flagged = report["verdict"] == "fail"
            table[run["arm"]][(side, flagged)] += 1
            for check in sorted({f["check"] for f in report["findings"] if f["status"] == "fail"}):
                fired[(run["arm"], side)][check] += 1
            if flagged != (side == "wrong"):
                first = next(f for f in report["findings"] if f["status"] == "fail") if flagged else None
                details.append(f"{os.path.basename(results_dir)}/{os.path.basename(run_dir)}: grade {side}"
                               f" ({run['reason'][:60]}); ds-verify {'fail: ' + first['check'] + ': ' + first['message'][:90] if flagged else 'pass'}")
    for arm, counts in table.items():
        wrong = counts[("wrong", True)] + counts[("wrong", False)]
        right = counts[("right", True)] + counts[("right", False)]
        print(f"{arm}: caught {counts[('wrong', True)]} of {wrong} wrong runs; "
              f"false alarms on {counts[('right', True)]} of {right} right runs")
        for side in ("wrong", "right"):
            print(f"  checks that failed on {side} runs: {dict(fired[(arm, side)])}")
    print("Disagreements:")
    for line in details:
        print(f"  {line}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
