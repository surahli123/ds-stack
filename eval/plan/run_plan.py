#!/usr/bin/env python3
"""Run the plan tasks through two arms with `claude -p` in clean profiles.

    python3 eval/plan/run_plan.py --runs 3 --model sonnet --parallel 6

Arms:
  baseline  plain prompting
  full      ds-plan installed, pointed to by CLAUDE.md

Each run has two turns in one session. Turn 1 is the task plus the task's
closing lines and "save it as plan.md". Turn 2 is the task's objection
(followup.md), answered in the same session; the reply is saved as reply.md.
Both arms get identical prompts. Gold is never copied in.
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
FULL_NOTE = "When asked to plan, frame, scope or brainstorm an analysis, read and follow .claude/skills/ds-plan/SKILL.md.\n"
ARMS = ("baseline", "full")
TOOLS = "Bash,Read,Write,Edit,Glob,Grep,Task,Agent"


def read(task, name):
    path = os.path.join(TASKS, task, name)
    if not os.path.exists(path):
        return ""
    with open(path) as handle:
        return handle.read().strip()


def ask(prompt, model, work, env, timeout, resume=None):
    cmd = ["claude", "-p", prompt, "--model", model, "--output-format", "stream-json", "--verbose",
           "--allowedTools", TOOLS, "--max-turns", "60"] + (["--resume", resume] if resume else [])
    try:
        proc = subprocess.run(cmd, cwd=work, env=env, capture_output=True, text=True, timeout=timeout)
        stdout, code = proc.stdout, proc.returncode
    except subprocess.TimeoutExpired as err:
        stdout = err.stdout.decode() if isinstance(err.stdout, bytes) else (err.stdout or "")
        code = "timeout"
    session = reply = cost = turns = None
    for line in stdout.splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        session = session or event.get("session_id")
        if event.get("type") == "result":
            reply, cost, turns = event.get("result"), event.get("total_cost_usd"), event.get("num_turns")
    return stdout, code, session, reply, cost, turns


def run_job(job, model, out_dir, timeout):
    task, arm, run = job
    job_root = os.path.join(os.environ.get("DS_RUN_ROOT", "/tmp/ds-runs"), uuid.uuid4().hex[:10])
    work = os.path.join(job_root, "project")
    config = os.path.join(job_root, "config")
    os.makedirs(work)
    os.makedirs(config)
    for name in os.listdir(os.path.join(TASKS, task)):
        if name not in ("task.md", "closing.md", "followup.md"):
            shutil.copy(os.path.join(TASKS, task, name), work)
    if arm == "full":
        shutil.copytree(os.path.join(ROOT, "skills", "ds-plan"), os.path.join(work, ".claude", "skills", "ds-plan"))
        with open(os.path.join(work, "CLAUDE.md"), "w") as handle:
            handle.write(FULL_NOTE)
    env = {k: os.environ[k] for k in PASSTHROUGH_ENV if k in os.environ}
    env.update(HOME=config, CLAUDE_CONFIG_DIR=config)
    closing = read(task, "closing.md")
    first = (read(task, "task.md") + "\n\nSave the plan as plan.md in the current directory. End it with these lines, filled in:\n"
             + closing + "\n\nReply with one line when it is saved.\n")
    started = time.time()
    out1, code1, session, _, cost1, turns1 = ask(first, model, work, env, timeout)
    out2 = code2 = reply = cost2 = turns2 = None
    if session and read(task, "followup.md"):
        second = read(task, "followup.md") + "\n\nAnswer in a short paragraph, then repeat the closing lines, updated if your plan changed.\n"
        out2, code2, _, reply, cost2, turns2 = ask(second, model, work, env, timeout, resume=session)

    dest = os.path.join(out_dir, f"{task}__{arm}__{run}")
    os.makedirs(dest, exist_ok=True)
    with open(os.path.join(dest, "transcript.jsonl"), "w") as handle:
        handle.write(out1 + (out2 or ""))
    if os.path.exists(os.path.join(work, "plan.md")):
        shutil.copy(os.path.join(work, "plan.md"), os.path.join(dest, "plan.md"))
    if reply:
        with open(os.path.join(dest, "reply.md"), "w") as handle:
            handle.write(reply)
    meta = {"task": task, "arm": arm, "run": run, "model": model, "exit": [code1, code2],
            "seconds": round(time.time() - started, 1), "cost_usd": round((cost1 or 0) + (cost2 or 0), 4),
            "turns": [turns1, turns2]}
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
    parser.add_argument("--timeout", type=int, default=900)
    parser.add_argument("--out", default=os.path.join(HERE, "results", time.strftime("%Y%m%d-%H%M%S")))
    args = parser.parse_args()
    jobs = [(t, a, r) for t in args.tasks.split(",") for a in args.arms.split(",") for r in range(1, args.runs + 1)]
    os.makedirs(args.out, exist_ok=True)
    print(f"{len(jobs)} jobs -> {args.out}", flush=True)
    with futures.ThreadPoolExecutor(max_workers=args.parallel) as pool:
        for done in futures.as_completed([pool.submit(run_job, j, args.model, args.out, args.timeout) for j in jobs]):
            m = done.result()
            print(f"{m['task']} {m['arm']:8} run {m['run']}: exit {m['exit']}, {m['seconds']}s, ${m['cost_usd']}", flush=True)
    print(f"done: {args.out}")


if __name__ == "__main__":
    main()
