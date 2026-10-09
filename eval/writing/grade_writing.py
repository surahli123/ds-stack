#!/usr/bin/env python3
"""Grade writing runs: a fresh reader's comprehension first, lint second.

    python3 eval/writing/grade_writing.py eval/writing/results/<run> [--reader-model haiku]

For each doc, a fresh reader (claude -p in a clean profile, no tools) answers
the cold-read questions twice: once from the skim view (first 120 words plus
headings and section leads) and once from the whole doc. A script grades each
answer line against the task's gold facts. The reader never sees the notes,
the gold or which arm wrote the doc. Lint fails and word counts are reported
too, but the lint is part of the full arm's skill, so they are secondary.
"""

import argparse
import concurrent.futures as futures
import json
import os
import re
import shutil
import subprocess
import sys
import uuid
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
for sub in ("skills/doc-tighten/tools", "skills/cold-read/tools", "eval"):
    sys.path.insert(0, os.path.join(ROOT, sub))

import doc_lint  # noqa: E402
import skim_view  # noqa: E402
from run_arms import PASSTHROUGH_ENV  # noqa: E402

PROMPTS = os.path.join(ROOT, "skills", "cold-read", "references", "reader-prompts.md")
KEYS = {1: "answer", 2: "decision", 3: "number", 4: "caveat", 5: "lost", 6: "question"}
CONTAMINATION_MARKERS = (ROOT, "/home/user/notes", "/gold/", "grade_writing")


def reader_prompts():
    with open(PROMPTS) as handle:
        text = handle.read()
    blocks = re.findall(r"```\n(.*?)```", text, re.S)
    return {"skim": blocks[0], "full": blocks[1]}


def ask_reader(prompt, model):
    root = os.path.join(os.environ.get("DS_RUN_ROOT", "/tmp/ds-runs"), "reader-" + uuid.uuid4().hex[:10])
    os.makedirs(root)
    env = {k: os.environ[k] for k in PASSTHROUGH_ENV if k in os.environ}
    env.update(HOME=root, CLAUDE_CONFIG_DIR=root)
    try:
        proc = subprocess.run(["claude", "-p", prompt, "--model", model, "--disallowedTools",
                               "Bash,Read,Write,Edit,Glob,Grep,Task,Agent,WebFetch,WebSearch"],
                              cwd=root, env=env, capture_output=True, text=True, timeout=300)
        return proc.stdout
    finally:
        shutil.rmtree(root, ignore_errors=True)


def answer_lines(reply):
    lines = {}
    for line in reply.splitlines():
        match = re.match(r"^\s*\**\s*([1-6])[.)]\s*(.*)$", line)
        if match:
            lines[KEYS[int(match.group(1))]] = match.group(2).lower()
    return lines


def fact_found(fact, lines):
    pools = {"answer": ("answer", "decision"), "decision": ("decision", "answer"),
             "number": ("number", "answer"), "caveat": ("caveat",)}
    text = " ".join(lines.get(k, "") for k in pools[fact["key"]]).replace("−", "-")
    return all(any(word in text for word in group) for group in fact["all_of"])


def contamination(run_dir):
    path = os.path.join(run_dir, "transcript.jsonl")
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return "no transcript"
    with open(path) as handle:
        text = handle.read()
    return next((m for m in CONTAMINATION_MARKERS if m in text), None)


def grade_run(run_dir, model, prompts):
    with open(os.path.join(run_dir, "meta.json")) as handle:
        meta = json.load(handle)
    with open(os.path.join(HERE, "gold", f"{meta['task']}.json")) as handle:
        gold = json.load(handle)
    result = {**meta, "doc": False, "skim": 0.0, "full": 0.0, "lint_fails": None, "words": None,
              "contaminated": contamination(run_dir)}
    doc_path = os.path.join(run_dir, "doc.md")
    if not os.path.exists(doc_path):
        return result
    with open(doc_path) as handle:
        doc = handle.read()
    findings, words = doc_lint.check(doc, gold["type"])
    result.update(doc=True, words=words, lint_fails=sum(f.severity == "fail" for f in findings),
                  lint_rules=sorted({f.rule for f in findings}))
    skim_facts = [f for f in gold["facts"] if f["key"] in ("answer", "decision", "number")]
    for mode, text, facts in (("skim", skim_view.skim(doc), skim_facts), ("full", doc, gold["facts"])):
        reply = ask_reader(prompts[mode].replace("{role}", gold["reader_role"]).replace("{text}", text), model)
        lines = answer_lines(reply)
        got = [f["name"] for f in facts if fact_found(f, lines)]
        result[mode] = round(len(got) / len(facts), 3)
        result[f"{mode}_got"] = got
        with open(os.path.join(run_dir, f"reader_{mode}.txt"), "w") as handle:
            handle.write(reply)
    if result["contaminated"]:
        result["skim"] = result["full"] = 0.0
    return result


def summarize(results, rule):
    arms = sorted({r["arm"] for r in results}, key=lambda a: ("baseline", "full").index(a))
    tasks = sorted({r["task"] for r in results})
    per_arm = {}
    for arm in arms:
        rows = [r for r in results if r["arm"] == arm]
        docs = [r for r in rows if r["doc"]]
        per_arm[arm] = {
            "runs": len(rows), "docs_written": len(docs),
            "skim_score": round(sum(r["skim"] for r in rows) / len(rows), 3),
            "full_score": round(sum(r["full"] for r in rows) / len(rows), 3),
            "docs_with_no_lint_fail": sum(r["lint_fails"] == 0 for r in docs),
            "mean_lint_fails": round(sum(r["lint_fails"] for r in docs) / max(len(docs), 1), 2),
            "mean_words": round(sum(r["words"] for r in docs) / max(len(docs), 1)),
            "contaminated": sum(bool(r["contaminated"]) for r in rows),
            "cost_usd": round(sum(r.get("cost_usd") or 0 for r in rows), 2),
        }
    verdict = {"n_tasks": len(tasks), "min_required": rule["min_tasks"]}
    if {"baseline", "full"} <= set(per_arm):
        full, base = per_arm["full"], per_arm["baseline"]
        ok = (full["skim_score"] - base["skim_score"] >= rule["skim_margin"]
              and full["full_score"] - base["full_score"] >= rule["full_margin"]
              and full["mean_lint_fails"] <= rule["max_lint_fails_full_arm"])
        verdict["rule_outcome_if_n_were_enough"] = "PASS" if ok else "FAIL"
    verdict["verdict"] = ("INSUFFICIENT_N (smoke test, not a decision)" if len(tasks) < rule["min_tasks"]
                          else verdict.get("rule_outcome_if_n_were_enough", "INCOMPLETE"))
    by_task = defaultdict(dict)
    for task in tasks:
        for arm in arms:
            rows = [r for r in results if r["task"] == task and r["arm"] == arm]
            by_task[task][arm] = {"skim": round(sum(r["skim"] for r in rows) / len(rows), 2),
                                  "full": round(sum(r["full"] for r in rows) / len(rows), 2),
                                  "words": [r["words"] for r in rows], "lint_fails": [r["lint_fails"] for r in rows]}
    return per_arm, dict(by_task), verdict


def render(name, per_arm, by_task, verdict, results):
    arms = list(per_arm)
    out = [f"# Writing eval: {name}", "",
           f"**Verdict:** {verdict['verdict']}. {verdict['n_tasks']} tasks; the rule needs {verdict['min_required']}. "
           f"Rule outcome at this n: {verdict.get('rule_outcome_if_n_were_enough', 'n/a')}.", "",
           "## Per arm", "", "| Metric | " + " | ".join(arms) + " |", "|---|" + "---|" * len(arms)]
    for metric in next(iter(per_arm.values())):
        out.append(f"| {metric} | " + " | ".join(str(per_arm[a][metric]) for a in arms) + " |")
    out += ["", "## Per task (mean reader score: skim / full)", "", "| Task | " + " | ".join(arms) + " |", "|---|" + "---|" * len(arms)]
    for task, cells in by_task.items():
        out.append(f"| {task} | " + " | ".join(f"{cells[a]['skim']:.2f} / {cells[a]['full']:.2f} · words {cells[a]['words']}" for a in arms) + " |")
    out += ["", "## Every run", "", "| Run | Skim got | Full got | Lint | Words |", "|---|---|---|---|---|"]
    for r in sorted(results, key=lambda r: (r["task"], r["arm"], r["run"])):
        out.append(f"| {r['task']} {r['arm']} #{r['run']} | {', '.join(r.get('skim_got', [])) or '-'} | "
                   f"{', '.join(r.get('full_got', [])) or '-'} | {' '.join(r.get('lint_rules', [])) or '-'} | {r['words']} |")
    return "\n".join(out) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("results_dir")
    parser.add_argument("--reader-model", default="haiku")
    parser.add_argument("--parallel", type=int, default=6)
    args = parser.parse_args()
    with open(os.path.join(HERE, "pass_rule.json")) as handle:
        rule = json.load(handle)
    prompts = reader_prompts()
    dirs = [os.path.join(args.results_dir, d) for d in sorted(os.listdir(args.results_dir))
            if os.path.isfile(os.path.join(args.results_dir, d, "meta.json"))]
    with futures.ThreadPoolExecutor(max_workers=args.parallel) as pool:
        results = list(pool.map(lambda d: grade_run(d, args.reader_model, prompts), dirs))
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
