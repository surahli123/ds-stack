#!/usr/bin/env python3
"""Measure an existing agent's readouts and print counts only. No text leaves.

    python3 audit_readouts.py DIR [--glob '*.md']

For each readout: words, lint fails per rule (readout type), stat-speak terms,
the line where a launch call first appears, whether the structure (the heading
sequence) matches other readouts, and how many metrics it mentions. Prints
aggregate counts: medians, shares and the number of distinct structures. Safe to
copy off a work machine because no document text is printed.
"""

import argparse
import glob
import hashlib
import os
import re
import statistics
import subprocess
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.join(os.path.dirname(HERE), "tools")
LINT = os.path.join(os.path.dirname(os.path.dirname(HERE)), "doc-tighten", "tools", "doc_lint.py")
sys.path.insert(0, TOOLS)

from render import CALL_WORDS, STAT_SPEAK  # noqa: E402

PERCENT = re.compile(r"[-+]?\d+(?:\.\d+)?\s*%")


def measure(path):
    text = open(path, encoding="utf-8", errors="replace").read()
    lines = text.splitlines()
    call_line = next((i + 1 for i, line in enumerate(lines) if CALL_WORDS.search(line)), None)
    headings = tuple(re.sub(r"\W+", " ", line.lstrip("#").strip().lower()) for line in lines if line.startswith("#"))
    proc = subprocess.run([sys.executable, LINT, path, "--type", "readout"], capture_output=True, text=True)
    rules = Counter(m.group(1) for m in re.finditer(r" fail (D\d+) ", proc.stdout))
    return {"words": len(text.split()), "stat_speak": len(STAT_SPEAK.findall(text)), "call_line": call_line,
            "skeleton": hashlib.sha1(repr(headings).encode()).hexdigest()[:8], "percent_figures": len(PERCENT.findall(text)),
            "lint_rules": rules}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("dir")
    parser.add_argument("--glob", default="*.md")
    args = parser.parse_args()
    paths = sorted(glob.glob(os.path.join(args.dir, args.glob)))
    if not paths:
        print("audit: no files matched", file=sys.stderr)
        return 2
    rows = [measure(p) for p in paths]
    median = lambda key: statistics.median(r[key] for r in rows if r[key] is not None)  # noqa: E731
    rules = sum((r["lint_rules"] for r in rows), Counter())
    calls = [r["call_line"] for r in rows if r["call_line"]]
    print(f"readouts: {len(rows)}")
    print(f"median words: {median('words'):.0f}; median stat-speak terms: {median('stat_speak'):.0f}; "
          f"median percent figures: {median('percent_figures'):.0f}")
    print(f"call word present: {len(calls)}/{len(rows)}; median line of first call word: "
          f"{statistics.median(calls) if calls else 'n/a'}; call in first 5 lines: {sum(c <= 5 for c in calls)}/{len(rows)}")
    print(f"distinct structures: {len(set(r['skeleton'] for r in rows))} across {len(rows)} readouts")
    print("lint fails by rule: " + (", ".join(f"{k} {v}" for k, v in sorted(rules.items())) or "none"))
    print(f"lint-clean: {sum(not r['lint_rules'] for r in rows)}/{len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
