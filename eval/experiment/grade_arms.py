#!/usr/bin/env python3
"""Grade experiment-readout runs by script and apply the pre-registered pass rule.

    python3 eval/experiment/grade_arms.py eval/experiment/results/<run> [--cold-read]

Per run: the call (from the required "Decision:" line, or the analyst's view when
one is given), its cost from the pass rule's matrix, whether the deciding metric
or check appears in the first six lines, lint fails and words (readout type),
stat-speak before any appendix, and, with --cold-read, a fresh launch-review
reader graded against an answer key built from decide.py's decision for the case.
Writes summary.md and summary.json in the run directory.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "skills", "ds-experiment", "tools"))
sys.path.insert(0, os.path.join(ROOT, "skills", "doc-tighten", "tools"))

import pipeline_cases  # noqa: E402
import render  # noqa: E402

CALL_PATTERNS = [("dont_ship", r"don['’]?t ship|do not ship|no[- ]ship"), ("cant_tell", r"can['’]?t tell|cannot tell"),
                 ("no_effect", r"no effect"), ("keep_running", r"keep running|extend"), ("not_ab", r"not an a/?b"),
                 ("escalate", r"escalat"), ("ship", r"\bship\b")]
CONTAMINATION = ("eval/experiment/gold", "/gold/", "make_cases", "pipeline_cases", "make_regressions",
                 "eval/experiment/results", "eval/experiment/regressions", "grade_arms")
DECIDER_WORDS = {"sample_split": ["split", "sample ratio", "srm", "imbalance", "mismatch", "allocation"],
                 "config_params": ["snippet", "parameter"], "pre_period": ["pre-period", "pre-experiment", "before exposure",
                                                                           "pre period", "pre-exposure", "pre-test"],
                 "scorecard": ["percent", "fraction", "scorecard", "inconsistent", "units", "export"],
                 "config_edits": ["allocation", "mid-flight", "edited"], "design": ["interleav", "holdout"]}


def parse_call(text):
    clean = text.replace("**", "").replace("__", "")
    match = re.search(r"^\W*decision\W*[:\-]\s*(.+)$", clean, re.I | re.M)
    if not match:
        return None
    return to_call(match.group(1))


def to_call(phrase):
    for call, pattern in CALL_PATTERNS:
        if re.search(pattern, phrase, re.I):
            return call
    return None


def analyst_call(text):
    match = re.search(r"analyst would call this ([^:.\n]+)", text, re.I)
    return to_call(match.group(1)) if match else None


def top_lines(text, n=6):
    clean = text.replace("**", "")
    start = re.search(r"^\W*decision\W*:", clean, re.I | re.M)
    body = clean[start.start():] if start else clean
    return [line for line in body.splitlines() if line.strip()][:n]


def decider_near_top(text, gold):
    words = DECIDER_WORDS.get(gold["decider"], [gold["decider"].lower().split(" (")[0]])
    head = " ".join(top_lines(text)).lower()
    return any(w in head for w in words)


def lint(path):
    proc = subprocess.run([sys.executable, os.path.join(ROOT, "skills", "doc-tighten", "tools", "doc_lint.py"), path,
                           "--type", "readout"], capture_output=True, text=True)
    last = proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else ""
    match = re.search(r"(\d+) fail, (\d+) warn, (\d+) body words", last)
    return (int(match.group(1)), int(match.group(3))) if match else (None, None)


def stat_speak(text):
    before = re.split(r"^#+\s*appendix", text, flags=re.I | re.M)[0]
    before = re.split(r"^\s*(?:\*\*)?check results|^```", before, flags=re.I | re.M)[0]
    return len(render.STAT_SPEAK.findall(before))


def cold_read(run_dir, cid, doc="result.md"):
    decision = pipeline_cases.run_case(cid)
    spine_path = os.path.join(run_dir, "gold_spine.json")
    with open(spine_path, "w") as handle:
        json.dump(render.spine(decision), handle)
    proc = subprocess.run([sys.executable, os.path.join(ROOT, "skills", "cold-read", "tools", "cold_read.py"),
                           os.path.join(run_dir, doc), "--spine", spine_path], capture_output=True, text=True)
    match = re.search(r"skim (\d)/2, full (\d)/3", proc.stdout)
    return (int(match.group(1)), int(match.group(2))) if match else (None, None)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("run")
    parser.add_argument("--cold-read", action="store_true")
    args = parser.parse_args()
    with open(os.path.join(HERE, "pass_rule.json")) as handle:
        rule = json.load(handle)
    matrix = rule["cost_matrix_rows_true_cols_made"]
    os.environ.setdefault("DS_CHECKS_LOG", os.devnull)
    rows = []
    for name in sorted(os.listdir(args.run)):
        run_dir = os.path.join(args.run, name)
        if not os.path.isdir(run_dir) or "__" not in name:
            continue
        cid, arm, run = name.split("__")
        with open(os.path.join(HERE, "gold", f"{cid}.json")) as handle:
            gold = json.load(handle)
        full_text = open(os.path.join(run_dir, "result.md")).read()
        text = re.split(r"^# .*triage prep\s*$", full_text, flags=re.M)[0]  # the launch readout only
        if text != full_text:
            with open(os.path.join(run_dir, "readout_part.md"), "w") as handle:
                handle.write(text)
        call, view = parse_call(text), analyst_call(text)
        effective = view or call
        correct = effective in gold["accept_calls"]
        cost = 0 if correct else (matrix[gold["call"]].get(effective) if effective else max(matrix[gold["call"]].values()))
        fails, words = lint(os.path.join(run_dir, "readout_part.md" if text != full_text else "result.md"))
        meta = json.load(open(os.path.join(run_dir, "meta.json")))
        transcript_path = os.path.join(run_dir, "transcript.jsonl")
        transcript = open(transcript_path, encoding="utf-8", errors="replace").read() if os.path.exists(transcript_path) else None
        contaminated = transcript is None or any(marker in transcript for marker in CONTAMINATION)
        row = {"case": cid, "arm": arm, "run": int(run), "gold": gold["call"], "call": call, "analyst_view": view,
               "correct": correct, "cost": cost, "decider_near_top": decider_near_top(text, gold), "lint_fails": fails,
               "words": words, "stat_speak": stat_speak(text), "usd": meta.get("cost_usd"), "seconds": meta.get("seconds"),
               "contaminated": contaminated}
        if args.cold_read:
            row["skim"], row["full"] = cold_read(run_dir, cid, "readout_part.md" if text != full_text else "result.md")
        rows.append(row)

    dropped = [f"{r['case']}__{r['arm']}__{r['run']}" for r in rows if r["contaminated"]]
    rows = [r for r in rows if not r["contaminated"]]
    golds = {r["case"]: r["gold"] for r in rows}
    accept = {c: json.load(open(os.path.join(HERE, "gold", f"{c}.json")))["accept_calls"] for c in golds}
    constant = {c: sum(0 if c in accept[k] else matrix[g][c] for k, g in golds.items()) / len(golds) for c in matrix}
    best_constant = min(constant.items(), key=lambda kv: kv[1])
    summary = {"best_constant_policy": best_constant, "arms": {}, "contaminated": dropped}
    for arm in sorted({r["arm"] for r in rows}):
        mine = [r for r in rows if r["arm"] == arm]
        majority = {}
        for cid in sorted({r["case"] for r in mine}):
            runs_here = [r for r in mine if r["case"] == cid]
            calls = [r["analyst_view"] or r["call"] for r in runs_here]
            top = max(set(calls), key=lambda c: (calls.count(c), next(r["cost"] for r in runs_here if (r["analyst_view"] or r["call"]) == c)))
            pick = next(r for r in runs_here if (r["analyst_view"] or r["call"]) == top)
            majority[cid] = {"gold": pick["gold"], "call": top, "correct": pick["correct"], "cost": pick["cost"]}
        by_class = defaultdict(list)
        for m in majority.values():
            by_class[m["gold"]].append(m["correct"])
        mean = lambda key: sum(r[key] for r in mine if r.get(key) is not None) / max(1, sum(r.get(key) is not None for r in mine))  # noqa: E731
        runs = max(r["run"] for r in mine)
        result = {
            "runs": len(mine), "cases": len(majority),
            "accuracy": sum(m["correct"] for m in majority.values()) / len(majority),
            "mean_cost": sum(m["cost"] for m in majority.values()) / len(majority),
            "run_accuracy": sum(r["correct"] for r in mine) / len(mine), "run_mean_cost": mean("cost"),
            "ship_on_dont_ship_or_cant_tell": sum(1 for m in majority.values() if m["gold"] in ("dont_ship", "cant_tell")
                                                  and m["call"] == "ship"),
            "runs_shipping_a_blocker": sum(1 for r in mine if r["gold"] in ("dont_ship", "cant_tell") and
                                           (r["analyst_view"] or r["call"]) == "ship"),
            "per_class": {k: f"{sum(v)}/{len(v)}" for k, v in sorted(by_class.items())},
            "decider_near_top": mean("decider_near_top"), "lint_clean": sum(r["lint_fails"] == 0 for r in mine) / len(mine),
            "mean_words": mean("words"), "mean_stat_speak": mean("stat_speak"), "mean_usd": mean("usd"),
        }
        if args.cold_read:
            result["skim_2of2"] = sum(r.get("skim") == 2 for r in mine) / len(mine)
            result["full_3of3"] = sum(r.get("full") == 3 for r in mine) / len(mine)
        checks = {"mean_cost": result["mean_cost"] <= rule["max_mean_cost"],
                  "margin_below_best_constant": best_constant[1] - result["mean_cost"] >= rule["min_margin_below_best_constant"],
                  "no_ship_on_blockers": result["ship_on_dont_ship_or_cant_tell"] <= rule["max_ship_on_dont_ship_or_cant_tell"],
                  "per_class": all(sum(v) / len(v) >= rule["min_share_correct_per_class"] for v in by_class.values())}
        result["pass_rule"] = checks
        result["verdict"] = ("INSUFFICIENT_RUNS" if runs < rule["runs_per_case"] else ("PASS" if all(checks.values()) else "FAIL"))
        summary["arms"][arm] = result
    summary["rows"] = rows
    with open(os.path.join(args.run, "summary.json"), "w") as handle:
        json.dump(summary, handle, indent=2)
    lines = [f"# Experiment readout eval: {os.path.basename(args.run.rstrip('/'))}", "",
             f"Best constant policy: always '{best_constant[0]}', mean cost {best_constant[1]:.2f}.",
             f"Contaminated runs dropped (transcript missing or touches eval files): {len(dropped)}.", "",
             "Correct and mean cost are per case, on the majority call across runs; the rest are per run.", "",
             "| Arm | Correct | Mean cost | Ship on a blocker | Decider in first 6 lines | Lint-clean | Words | Stat-speak | $ per run | Verdict |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for arm, r in summary["arms"].items():
        lines.append(f"| {arm} | {r['accuracy']:.0%} | {r['mean_cost']:.2f} | {r['ship_on_dont_ship_or_cant_tell']} | "
                     f"{r['decider_near_top']:.0%} | {r['lint_clean']:.0%} | {r['mean_words']:.0f} | {r['mean_stat_speak']:.1f} | "
                     f"{r['mean_usd']:.3f} | {r['verdict']} |")
    if args.cold_read:
        lines += ["", "| Arm | Skim 2/2 | Full 3/3 |", "|---|---|---|"]
        for arm, r in summary["arms"].items():
            lines.append(f"| {arm} | {r['skim_2of2']:.0%} | {r['full_3of3']:.0%} |")
    lines += ["", "| Case | Gold | " + " | ".join(summary["arms"]) + " |", "|---|---|" + "---|" * len(summary["arms"])]
    for cid in sorted(golds):
        cells = []
        for arm in summary["arms"]:
            hit = [r for r in rows if r["case"] == cid and r["arm"] == arm]
            cells.append(", ".join(f"{'ok' if r['correct'] else 'MISS'} {r['call']}" + (f" (view {r['analyst_view']})" if r["analyst_view"] else "")
                                   for r in hit))
        lines.append(f"| {cid} | {golds[cid]} | " + " | ".join(cells) + " |")
    with open(os.path.join(args.run, "summary.md"), "w") as handle:
        handle.write("\n".join(lines) + "\n")
    print("\n".join(lines[:8 + len(summary["arms"])]))


if __name__ == "__main__":
    main()
