#!/usr/bin/env python3
"""Run the writing tasks through two arms with `claude -p` in clean profiles.

    python3 eval/writing/run_writing.py --runs 3 --model sonnet --parallel 6

Arms:
  baseline  plain prompting
  full      ds-doc, doc-tighten and cold-read installed, pointed to by CLAUDE.md

Both arms get the identical prompt: the task plus "save it as doc.md".
"""

import argparse
import concurrent.futures as futures
import json
import os
import shutil
import subprocess
import sys
import time
import uuid

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.dirname(HERE))

from run_arms import PASSTHROUGH_ENV  # noqa: E402

TASKS = os.path.join(HERE, "tasks")
SKILLS = ("ds-doc", "doc-tighten", "cold-read")
FULL_NOTE = "When asked to write a document, read and follow .claude/skills/ds-doc/SKILL.md.\n"
ARMS = ("baseline", "full")


def clean_env(config, extra=None):
    env = {k: os.environ[k] for k in PASSTHROUGH_ENV if k in os.environ}
    env.update(HOME=config, CLAUDE_CONFIG_DIR=config, **(extra or {}))
    return env


def run_job(job, model, out_dir, timeout):
    task, arm, run = job
    job_root = os.path.join(os.environ.get("DS_RUN_ROOT", "/tmp/ds-runs"), uuid.uuid4().hex[:10])
    work = os.path.join(job_root, "project")
    config = os.path.join(job_root, "config")
    os.makedirs(work)
    os.makedirs(config)
    shutil.copy(os.path.join(TASKS, task, "notes.md"), work)
    if arm == "full":
        for skill in SKILLS:
            shutil.copytree(os.path.join(ROOT, "skills", skill), os.path.join(work, ".claude", "skills", skill),
                            ignore=shutil.ignore_patterns("__pycache__"))
        with open(os.path.join(work, "CLAUDE.md"), "w") as handle:
            handle.write(FULL_NOTE)
    with open(os.path.join(TASKS, task, "task.md")) as handle:
        prompt = handle.read().strip() + "\n\nSave the document as doc.md in the current directory. Reply with one line when it is saved.\n"
    cmd = ["claude", "-p", prompt, "--model", model, "--output-format", "stream-json", "--verbose",
           "--allowedTools", "Bash,Read,Write,Edit,Glob,Grep,Task,Agent", "--max-turns", "80"]
    started = time.time()
    try:
        proc = subprocess.run(cmd, cwd=work, env=clean_env(config), capture_output=True, text=True, timeout=timeout)
        stdout, code = proc.stdout, proc.returncode
    except subprocess.TimeoutExpired as err:
        stdout = err.stdout.decode() if isinstance(err.stdout, bytes) else (err.stdout or "")
        code = "timeout"

    dest = os.path.join(out_dir, f"{task}__{arm}__{run}")
    os.makedirs(dest, exist_ok=True)
    with open(os.path.join(dest, "transcript.jsonl"), "w") as handle:
        handle.write(stdout)
    doc = os.path.join(work, "doc.md")
    if os.path.exists(doc):
        shutil.copy(doc, os.path.join(dest, "doc.md"))
    cost = turns = None
    for line in stdout.splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if event.get("type") == "result":
            cost, turns = event.get("total_cost_usd"), event.get("num_turns")
    meta = {"task": task, "arm": arm, "run": run, "model": model, "exit": code,
            "seconds": round(time.time() - started, 1), "cost_usd": cost, "turns": turns}
    with open(os.path.join(dest, "meta.json"), "w") as handle:
        json.dump(meta, handle, indent=2)
    shutil.rmtree(job_root, ignore_errors=True)
    return meta


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--tasks", default=",".join(sorted(os.listdir(TASKS))))
    parser.add_argument("--arms", default=",".join(ARMS))
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--model", default="sonnet")
    parser.add_argument("--parallel", type=int, default=6)
    parser.add_argument("--timeout", type=int, default=1200)
    parser.add_argument("--out", default=os.path.join(HERE, "results", time.strftime("%Y%m%d-%H%M%S")))
    args = parser.parse_args()
    jobs = [(t, a, r) for t in args.tasks.split(",") for a in args.arms.split(",") for r in range(1, args.runs + 1)]
    os.makedirs(args.out, exist_ok=True)
    print(f"{len(jobs)} jobs -> {args.out}", flush=True)
    with futures.ThreadPoolExecutor(max_workers=args.parallel) as pool:
        for done in futures.as_completed([pool.submit(run_job, j, args.model, args.out, args.timeout) for j in jobs]):
            m = done.result()
            print(f"{m['task']} {m['arm']:8} run {m['run']}: exit {m['exit']}, {m['seconds']}s, turns {m['turns']}, ${m['cost_usd']}", flush=True)
    print(f"done: {args.out}")


if __name__ == "__main__":
    main()
