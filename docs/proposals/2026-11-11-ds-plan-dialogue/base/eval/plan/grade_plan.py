#!/usr/bin/env python3
"""Grade plan runs by script: the closing lines of the plan and of the reply to the objection.

    python3 eval/plan/grade_plan.py eval/plan/results/<run>

Each task asks every arm to end its plan with fixed lines (closing.md, such as
"Unit:" and "Segment:"), and to repeat them after the objection. Each gold
item reads one of those lines and passes when it holds a word from every
all_of group (or from any_of) and none from none_of, ignoring words after
"not", "rather than" or "instead of". Turn 1 grades plan.md;
turn 2 grades reply.md. No model judges anything. Plan length is counted with
doc_lint, so Chinese counts too.
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "skills", "doc-tighten", "tools"))

import doc_lint  # noqa: E402

CLOSING = re.compile(r"^[ \t]*(?:[-*>][ \t]*)?\**[ \t]*([A-Za-z][A-Za-z ]{0,20}?)[ \t]*\**[ \t]*[:：][ \t]*\**[ \t]*(\S.*?)[ \t]*$", re.M)
NEGATED = re.compile(r"\b(?:not|rather than|instead of|never|no)\b[^,;.()]*")
CONTAMINATION_MARKERS = ("/gold/", "grade_plan", "pass_rule.json")


def closing_lines(text):
    """The last value written for each closing key, lowercased: {'unit': 'user', ...}."""
    lines = {}
    for key, value in CLOSING.findall(text or ""):
        lines[key.strip().lower()] = value.lower().replace("’", "'")
    return lines


def item_passes(item, lines):
    text = lines.get(item["line"], "")
    if not text:
        return False
    groups = item.get("all_of") or [item.get("any_of", [])]
    affirmed = NEGATED.sub(" ", text)
    return (all(any(word in text for word in group) for group in groups)
            and not any(word in affirmed for word in item.get("none_of", [])))


def score(text, gold):
    lines = closing_lines(text)
    got = [item["name"] for item in gold["items"] if item_passes(item, lines)]
    return round(len(got) / len(gold["items"]), 3), got


def contamination(run_dir):
    path = os.path.join(run_dir, "transcript.jsonl")
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return "no transcript"
    with open(path) as handle:
        text = handle.read()
    return next((m for m in CONTAMINATION_MARKERS if m in text), None)


def read(path):
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def grade_run(run_dir):
    with open(os.path.join(run_dir, "meta.json")) as handle:
        meta = json.load(handle)
    with open(os.path.join(HERE, "gold", f"{meta['task']}.json")) as handle:
        gold = json.load(handle)
    plan, reply = read(os.path.join(run_dir, "plan.md")), read(os.path.join(run_dir, "reply.md"))
    turn1, got1 = score(plan, gold)
    turn2, got2 = score(reply, gold)
    result = {**meta, "plan": plan is not None, "turn1": turn1, "turn1_got": got1, "turn2": turn2, "turn2_got": got2,
              "words": doc_lint.check(plan, "plan")[1] if plan else None, "contaminated": contamination(run_dir)}
    if result["contaminated"]:
        result["turn1"] = result["turn2"] = 0.0
    return result


def summarize(results, rule):
    arms = sorted({r["arm"] for r in results}, key=lambda a: ("baseline", "full").index(a))
    tasks = sorted({r["task"] for r in results})
    per_arm = {}
    for arm in arms:
        rows = [r for r in results if r["arm"] == arm]
        plans = [r for r in rows if r["plan"]]
        per_arm[arm] = {
            "runs": len(rows), "plans_written": len(plans),
            "turn1_score": round(sum(r["turn1"] for r in rows) / len(rows), 3),
            "turn2_score": round(sum(r["turn2"] for r in rows) / len(rows), 3),
            "mean_words": round(sum(r["words"] for r in plans) / max(len(plans), 1)),
            "contaminated": sum(bool(r["contaminated"]) for r in rows),
            "cost_usd": round(sum(r.get("cost_usd") or 0 for r in rows), 2),
        }
    verdict = {"n_tasks": len(tasks), "min_required": rule["min_tasks"]}
    if {"baseline", "full"} <= set(per_arm):
        full, base = per_arm["full"], per_arm["baseline"]
        ok = (full["turn1_score"] - base["turn1_score"] >= rule["turn1_margin"]
              and full["turn2_score"] - base["turn2_score"] >= rule["turn2_margin"]
              and full["mean_words"] <= base["mean_words"] * rule["max_words_ratio"])
        verdict["rule_outcome_if_n_were_enough"] = "PASS" if ok else "FAIL"
    verdict["verdict"] = ("INSUFFICIENT_N (smoke test, not a decision)" if len(tasks) < rule["min_tasks"]
                          else verdict.get("rule_outcome_if_n_were_enough", "INCOMPLETE"))
    by_task = defaultdict(dict)
    for task in tasks:
        for arm in arms:
            rows = [r for r in results if r["task"] == task and r["arm"] == arm]
            by_task[task][arm] = {"turn1": round(sum(r["turn1"] for r in rows) / len(rows), 2),
                                  "turn2": round(sum(r["turn2"] for r in rows) / len(rows), 2),
                                  "words": [r["words"] for r in rows]}
    return per_arm, dict(by_task), verdict


def render(name, per_arm, by_task, verdict, results):
    arms = list(per_arm)
    out = [f"# Plan eval: {name}", "",
           f"Verdict: {verdict['verdict']}. {verdict['n_tasks']} tasks; the rule needs {verdict['min_required']}. "
           f"Rule outcome at this n: {verdict.get('rule_outcome_if_n_were_enough', 'n/a')}.", "",
           "## Per arm", "", "| Metric | " + " | ".join(arms) + " |", "|---|" + "---|" * len(arms)]
    for metric in next(iter(per_arm.values())):
        out.append(f"| {metric} | " + " | ".join(str(per_arm[a][metric]) for a in arms) + " |")
    out += ["", "## Per task (mean score: plan / after the objection)", "", "| Task | " + " | ".join(arms) + " |",
            "|---|" + "---|" * len(arms)]
    for task, cells in by_task.items():
        out.append(f"| {task} | " + " | ".join(f"{cells[a]['turn1']:.2f} / {cells[a]['turn2']:.2f} · words {cells[a]['words']}" for a in arms) + " |")
    out += ["", "## Every run", "", "| Run | Plan got | After the objection got | Words |", "|---|---|---|---|"]
    for r in sorted(results, key=lambda r: (r["task"], r["arm"], r["run"])):
        out.append(f"| {r['task']} {r['arm']} #{r['run']} | {', '.join(r['turn1_got']) or '-'} | "
                   f"{', '.join(r['turn2_got']) or '-'} | {r['words']} |")
    return "\n".join(out) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("results_dir")
    args = parser.parse_args()
    with open(os.path.join(HERE, "pass_rule.json")) as handle:
        rule = json.load(handle)
    dirs = [os.path.join(args.results_dir, d) for d in sorted(os.listdir(args.results_dir))
            if os.path.isfile(os.path.join(args.results_dir, d, "meta.json"))]
    results = [grade_run(d) for d in dirs]
    per_arm, by_task, verdict = summarize(results, rule)
    report = render(os.path.basename(args.results_dir.rstrip("/")), per_arm, by_task, verdict, results)
    with open(os.path.join(args.results_dir, "summary.md"), "w") as handle:
        handle.write(report)
    with open(os.path.join(args.results_dir, "summary.json"), "w") as handle:
        json.dump({"verdict": verdict, "per_arm": per_arm, "by_task": by_task, "runs": results}, handle, indent=2)
    print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
