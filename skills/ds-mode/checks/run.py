#!/usr/bin/env python3
"""Run one ds-mode check on a JSON spec of aggregates.

    python3 checks/run.py <check> --json '<spec>'
    python3 checks/run.py <check> --file spec.json
    python3 checks/run.py --list

Prints one JSON line and appends it to .ds-checks.log in the working directory.
Add "from": "q3" (or a list of query ids) to the spec to record which logged
queries the aggregates came from; the readout cites the printed id, such as
[check:mix_shift#1].
Statuses: pass; flag (a finding the answer must report, not a data defect);
fail (a data or query defect); could_not_run.
Exit code: 0 pass, 1 flag or fail, 2 could not run, 3 usage error.
"""

import argparse
import importlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _common import COULD_NOT_RUN, Result, emit  # noqa: E402

QUERY_ID = re.compile(r"^q\d+$")

CHECKS = ("completeness", "fanout", "mix_shift", "srm")

USAGE = {
    "completeness": ("before reporting any period: is it fully loaded?",
                     '{"series": [{"period": "2026-10-01", "rows": 100}, ...], "target": "2026-10-07"}'),
    "fanout": ("after any join: did it add or lose rows?",
               '{"left_rows": 1000, "joined_rows": 1000, "relationship": "many_to_one", "join": "left", '
               '"right_rows": 1000, "right_distinct_keys": 1000, "matched_left_rows": 1000}'),
    "mix_shift": ("when a rate moved: how much is segment mix vs within-segment change?",
                  '{"segments": [{"name": "web", "before": {"n": 800, "k": 240}, '
                  '"after": {"n": 820, "k": 250}}, ...]}  (n = denominator, k = numerator)'),
    "srm": ("before reading any experiment lift: is the assignment split as planned?",
            '{"observed": [10120, 9880], "expected_ratio": [0.5, 0.5]}'),
}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("check", nargs="?", choices=CHECKS)
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--json", help="the spec as a JSON string")
    source.add_argument("--file", help="path to a JSON spec")
    parser.add_argument("--list", action="store_true", help="list checks, when to run them, and a spec example")
    args = parser.parse_args(argv)

    if args.list:
        for name in CHECKS:
            when, example = USAGE[name]
            print(f"{name}: {when}\n  spec: {example}\n")
        return 0
    if not args.check or not (args.json or args.file):
        parser.print_usage(sys.stderr)
        return 3

    try:
        if args.file:
            with open(args.file) as handle:
                spec = json.load(handle)
        else:
            spec = json.loads(args.json)
        if not isinstance(spec, dict):
            raise ValueError("the spec must be a JSON object")
    except (OSError, ValueError) as err:
        return emit(Result(args.check, COULD_NOT_RUN, f"could not run: unreadable spec ({err})"))

    sources = spec.pop("from", [])
    if isinstance(sources, str):
        sources = [sources]
    if not isinstance(sources, list) or not all(isinstance(s, str) and QUERY_ID.match(s) for s in sources):
        return emit(Result(args.check, COULD_NOT_RUN, "could not run: 'from' must be a query id like \"q3\" or a list of them"))

    module = importlib.import_module(args.check)
    return emit(module.run(spec), sources=sources)


if __name__ == "__main__":
    sys.exit(main())
