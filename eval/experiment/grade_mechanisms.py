#!/usr/bin/env python3
"""Grade deep-dive runs on the planted-mechanism cases.

    python3 eval/experiment/grade_mechanisms.py eval/experiment/results/<run>

Per run, by script: whether the reply names the planted mechanism (its gold
keywords), whether it proposes the cut that tests it (cut keywords), whether its
"Ready for triage:" line matches gold, words, and stat-speak. Keyword grading is
coarse by design and reported as such; read the replies before trusting a gap.
"""

import json
import os
import re
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "skills", "ds-experiment", "tools"))
import render  # noqa: E402

READINESS = [("not_ready", r"not ready"), ("open_questions", r"open questions"), ("ready", r"\bready\b")]


def readiness(text):
    m = re.search(r"ready for triage\W*[:\-]\s*(.+)$", text.replace("**", ""), re.I | re.M)
    if not m:
        return None
    for verdict, pattern in READINESS:
        if re.search(pattern, m.group(1), re.I):
            return verdict
    return None


def main():
    run = sys.argv[1]
    rows = []
    for name in sorted(os.listdir(run)):
        if "__" not in name:
            continue
        cid, arm, r = name.split("__")
        gold = json.load(open(os.path.join(HERE, "gold_mechanisms", f"{cid}.json")))
        text = open(os.path.join(run, name, "result.md")).read()
        low = text.lower()
        transcript = os.path.join(run, name, "transcript.jsonl")
        contaminated = not os.path.exists(transcript) or any(
            k in open(transcript, errors="replace").read() for k in ("gold_mechanisms", "make_mechanisms", "mechanism_check"))
        rows.append({"case": cid, "arm": arm, "run": int(r), "contaminated": contaminated,
                     "mechanism": any(k in low for k in gold["mechanism_keywords"]),
                     "cut": any(k in low for k in gold["cut_keywords"]),
                     "readiness": readiness(text) == gold["readiness"], "readiness_said": readiness(text),
                     "words": len(text.split()), "stat_speak": len(render.STAT_SPEAK.findall(text))})
    rows = [r for r in rows if not r["contaminated"]]
    summary = {}
    for arm in sorted({r["arm"] for r in rows}):
        mine = [r for r in rows if r["arm"] == arm]
        share = lambda k: sum(r[k] for r in mine) / len(mine)  # noqa: E731
        summary[arm] = {"runs": len(mine), "mechanism": share("mechanism"), "cut": share("cut"), "readiness": share("readiness"),
                        "words": sum(r["words"] for r in mine) / len(mine),
                        "stat_speak": sum(r["stat_speak"] for r in mine) / len(mine)}
    lines = [f"# Deep-dive eval: {os.path.basename(run.rstrip('/'))}", "",
             "Per run. Mechanism and cut are keyword matches against gold, so read the replies before trusting a gap.", "",
             "| Arm | Runs | Names the mechanism | Proposes the cut | Readiness right | Words | Stat-speak |",
             "|---|---|---|---|---|---|---|"]
    for arm, s in summary.items():
        lines.append(f"| {arm} | {s['runs']} | {s['mechanism']:.0%} | {s['cut']:.0%} | {s['readiness']:.0%} | {s['words']:.0f} | {s['stat_speak']:.1f} |")
    lines += ["", "| Case | " + " | ".join(summary) + " |", "|---|" + "---|" * len(summary)]
    for cid in sorted({r["case"] for r in rows}):
        cells = []
        for arm in summary:
            hit = [r for r in rows if r["case"] == cid and r["arm"] == arm]
            cells.append(", ".join(f"{'M' if r['mechanism'] else 'm'}{'C' if r['cut'] else 'c'}{'R' if r['readiness'] else 'r'}" for r in hit))
        lines.append(f"| {cid} | " + " | ".join(cells) + " |")
    lines += ["", "M/C/R: mechanism, cut, readiness right (lower case: missed)."]
    with open(os.path.join(run, "summary.md"), "w") as handle:
        handle.write("\n".join(lines) + "\n")
    with open(os.path.join(run, "summary.json"), "w") as handle:
        json.dump({"arms": summary, "rows": rows}, handle, indent=2)
    print("\n".join(lines))


if __name__ == "__main__":
    main()
