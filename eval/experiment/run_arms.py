#!/usr/bin/env python3
"""Run the experiment cases through two arms with `claude -p` in clean profiles.

    python3 eval/experiment/run_arms.py --runs 1 --model sonnet --parallel 6 [--cases s1,d3]

baseline  the case files and the task, nothing else
full      plus the ds-experiment skill (and the ds-mode, doc-tighten and cold-read
          tools it calls), pointed to by CLAUDE.md

Every arm gets the identical prompt: task.md. Gold is never copied in.
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
sys.path.insert(0, os.path.join(ROOT, "eval"))
from run_arms import PASSTHROUGH_ENV  # noqa: E402

CASES = os.path.join(HERE, "cases")
SKILLS = ("ds-experiment", "ds-mode", "doc-tighten", "cold-read")
SKIP = shutil.ignore_patterns("__pycache__", ".ds-checks.log", "registry.json")
FULL_NOTE = "For any experiment readout or launch decision, read and follow .claude/skills/ds-experiment/SKILL.md.\n"


def run_job(job, model, out_dir, timeout):
    cid, arm, run = job
    root = os.path.join(os.environ.get("DS_RUN_ROOT", "/tmp/ds-runs"), uuid.uuid4().hex[:10])
    work = os.path.join(root, "work")
    shutil.copytree(os.path.join(CASES, cid), work)
    if arm == "full":
        for skill in SKILLS:
            shutil.copytree(os.path.join(ROOT, "skills", skill), os.path.join(work, ".claude", "skills", skill), ignore=SKIP)
        with open(os.path.join(work, "CLAUDE.md"), "w") as handle:
            handle.write(FULL_NOTE)
        os.makedirs(os.path.join(work, "overlay"))
        shutil.copy(os.path.join(ROOT, "overlay.example", "standards.json"), os.path.join(work, "overlay", "standards.json"))
    config = os.path.join(root, "config")
    os.makedirs(config)
    env = {k: os.environ[k] for k in PASSTHROUGH_ENV if k in os.environ}
    env.update(HOME=config, CLAUDE_CONFIG_DIR=config, DS_CHECKS_LOG=os.path.join(work, ".ds-checks.log"))
    if arm == "full":
        env["DS_OVERLAY_DIR"] = os.path.join(work, "overlay")
    with open(os.path.join(work, "task.md")) as handle:
        prompt = handle.read()
    cmd = ["claude", "-p", prompt, "--model", model, "--output-format", "stream-json", "--verbose",
           "--allowedTools", "Bash,Read,Write,Edit,Glob,Grep", "--max-turns", "60"]
    started = time.time()
    try:
        proc = subprocess.run(cmd, cwd=work, env=env, capture_output=True, text=True, timeout=timeout)
        stdout, code = proc.stdout, proc.returncode
    except subprocess.TimeoutExpired as err:
        stdout = err.stdout.decode() if isinstance(err.stdout, bytes) else (err.stdout or "")
        code = "timeout"
    dest = os.path.join(out_dir, f"{cid}__{arm}__{run}")
    os.makedirs(dest, exist_ok=True)
    final = cost = turns = None
    for line in stdout.splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if event.get("type") == "result":
            final, cost, turns = event.get("result", ""), event.get("total_cost_usd"), event.get("num_turns")
    with open(os.path.join(dest, "transcript.jsonl"), "w") as handle:
        handle.write(stdout)
    with open(os.path.join(dest, "result.md"), "w") as handle:
        handle.write(final or "")
    for name in (".ds-checks.log", "readout.md", "notes.json", "prereg.json", "decision.json", "cold_read.json"):
        if os.path.exists(os.path.join(work, name)):
            shutil.copy(os.path.join(work, name), os.path.join(dest, name.lstrip(".")))
    meta = {"case": cid, "arm": arm, "run": run, "model": model, "exit": code,
            "seconds": round(time.time() - started, 1), "cost_usd": cost, "turns": turns}
    with open(os.path.join(dest, "meta.json"), "w") as handle:
        json.dump(meta, handle, indent=2)
    shutil.rmtree(root, ignore_errors=True)
    return meta


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--runs", type=int, default=1)
    parser.add_argument("--model", default="sonnet")
    parser.add_argument("--parallel", type=int, default=6)
    parser.add_argument("--timeout", type=int, default=1500)
    parser.add_argument("--cases")
    parser.add_argument("--arms", default="baseline,full")
    parser.add_argument("--out", default=os.path.join(HERE, "results", time.strftime("%Y-%m-%d-%H%M")))
    args = parser.parse_args()
    cases = args.cases.split(",") if args.cases else sorted(os.listdir(CASES))
    jobs = [(c, a, r) for c in cases for a in args.arms.split(",") for r in range(1, args.runs + 1)]
    os.makedirs(args.out, exist_ok=True)
    with futures.ThreadPoolExecutor(max_workers=args.parallel) as pool:
        for done in futures.as_completed([pool.submit(run_job, j, args.model, args.out, args.timeout) for j in jobs]):
            m = done.result()
            print(f"{m['case']:3} {m['arm']:8} run {m['run']}: exit {m['exit']}, {m['seconds']}s, turns {m['turns']}, ${m['cost_usd']}",
                  flush=True)
    print(f"results in {args.out}")


if __name__ == "__main__":
    main()
