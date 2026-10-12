#!/usr/bin/env python3
"""Backtest decide.py against past triage decisions and print the confusion matrix only.

    python3 backtest.py cases.csv [--standards standards.json]

cases.csv has one row per past experiment: scorecard,config,prereg,triage_call[,daily]
(paths to canonical files from normalize.py, a prereg.json, and the call the
triage meeting actually made: ship, dont_ship, escalate, keep_running,
no_effect, cant_tell). Prints the 7 x 7 matrix (rows: triage, columns:
decide.py) and agreement. No metric names or numbers are printed, so the output
is safe to copy off a work machine. Disagreements are the cases to read
locally: each is either a rule to change in standards.json or a triage call
the rule would have caught.
"""

import argparse
import csv
import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools"))

import decide  # noqa: E402

CALLS = ["ship", "dont_ship", "escalate", "keep_running", "no_effect", "cant_tell", "not_ab"]


def load(path):
    if not path:
        return None
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("cases")
    parser.add_argument("--standards")
    parser.add_argument("--show-rows", action="store_true", help="print row numbers of disagreements (local use only)")
    args = parser.parse_args()
    os.environ.setdefault("DS_CHECKS_LOG", os.devnull)
    standards = load(args.standards)
    matrix, errors, disagree = Counter(), 0, []
    with open(args.cases, newline="", encoding="utf-8") as handle:
        for i, row in enumerate(csv.DictReader(handle), 1):
            try:
                made = decide.decide(load(row["scorecard"]), load(row["prereg"]), load(row.get("config")), standards,
                                     load(row.get("daily")))["call"]
            except (OSError, ValueError, KeyError):
                errors += 1
                continue
            truth = row["triage_call"].strip().lower()
            matrix[(truth, made)] += 1
            if truth != made:
                disagree.append(i)
    total = sum(matrix.values())
    print("rows = triage call, columns = decide.py call")
    print("              " + " ".join(f"{c[:10]:>10}" for c in CALLS))
    for truth in CALLS:
        print(f"{truth[:12]:>12}  " + " ".join(f"{matrix[(truth, made)]:>10}" for made in CALLS))
    agree = sum(matrix[(c, c)] for c in CALLS)
    print(f"agreement: {agree}/{total}; could not run: {errors}")
    if args.show_rows:
        print(f"disagreeing rows (read these locally): {disagree}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
