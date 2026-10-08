#!/usr/bin/env python3
"""Run fixtures through the three arms with `claude -p` in clean profiles.

    python3 eval/run_arms.py --runs 3 --model sonnet --parallel 6

Each job gets a fresh working directory holding only the fixture's warehouse.db
and its arm's assets, plus a fresh, empty Claude config dir (no personal
CLAUDE.md, memory, skills or hooks). Gold answers are never copied in.

Arms:
  baseline  plain prompting
  checks    checks/ plus a one-line instruction to run them
  full      the ds-mode skill (method + checks + readout), pointed to by CLAUDE.md

Every arm gets the identical prompt: the fixture's task plus the readout format.
"""

import argparse
import concurrent.futures as futures
import json
import os
import re
import shutil
import subprocess
import time
import uuid

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SKILL_DIR = os.path.join(ROOT, "skills", "ds-mode")
FIXTURES = os.path.join(HERE, "fixtures")
ARMS = ("baseline", "checks", "full")
PASSTHROUGH_ENV = ("PATH", "ANTHROPIC_BASE_URL", "HTTPS_PROXY", "HTTP_PROXY", "NO_PROXY",
                   "https_proxy", "http_proxy", "no_proxy", "NODE_EXTRA_CA_CERTS", "SSL_CERT_FILE",
                   "REQUESTS_CA_BUNDLE", "ANTHROPIC_API_KEY")
SKIP_IN_COPY = shutil.ignore_patterns("__pycache__", "registry.json", ".ds-checks.log")
CHECKS_ONLY_NOTE = ("Before reporting any number computed from data, run the checks in checks/ that apply "
                    "(python3 checks/run.py --list shows them) and include their results.\n")
FULL_NOTE = "For any data analysis request, read and follow .claude/skills/ds-mode/SKILL.md.\n"


def readout_format():
    """The readout block from SKILL.md, so every arm sees the same format text."""
    with open(os.path.join(SKILL_DIR, "SKILL.md")) as handle:
        text = handle.read()
    section = text.split("## Readout", 1)[1]
    return re.search(r"```\n(.*?)```", section, re.S).group(1)


def build_prompt(fixture):
    with open(os.path.join(FIXTURES, fixture, "task.md")) as handle:
        task = handle.read().strip()
    return (f"{task}\n\nThe data is in warehouse.db (SQLite) in the current directory.\n\n"
            "End with exactly this readout as your final reply. Label each claim "
            "measured (computed from data here), inferred, or guess:\n\n"
            f"```\n{readout_format()}```\n")


def prepare_workdir(job_root, fixture, arm):
    work = os.path.join(job_root, "analysis")
    os.makedirs(work)
    shutil.copy(os.path.join(FIXTURES, fixture, "warehouse.db"), work)
    if arm == "checks":
        shutil.copytree(os.path.join(SKILL_DIR, "checks"), os.path.join(work, "checks"), ignore=SKIP_IN_COPY)
        with open(os.path.join(work, "CLAUDE.md"), "w") as handle:
            handle.write(CHECKS_ONLY_NOTE)
    elif arm == "full":
        shutil.copytree(SKILL_DIR, os.path.join(work, ".claude", "skills", "ds-mode"), ignore=SKIP_IN_COPY)
        with open(os.path.join(work, "CLAUDE.md"), "w") as handle:
            handle.write(FULL_NOTE)
    return work


def run_job(job, model, out_dir, timeout):
    fixture, arm, run = job
    job_root = os.path.join(os.environ.get("DS_RUN_ROOT", "/tmp/ds-runs"), uuid.uuid4().hex[:10])
    work = prepare_workdir(job_root, fixture, arm)
    config = os.path.join(job_root, "config")
    os.makedirs(config)
    env = {k: os.environ[k] for k in PASSTHROUGH_ENV if k in os.environ}
    env.update(HOME=config, CLAUDE_CONFIG_DIR=config, DS_CHECKS_LOG=os.path.join(work, ".ds-checks.log"))
    cmd = ["claude", "-p", build_prompt(fixture), "--model", model, "--output-format", "stream-json",
           "--verbose", "--allowedTools", "Bash,Read,Write,Edit,Glob,Grep", "--max-turns", "60"]
    started = time.time()
    try:
        proc = subprocess.run(cmd, cwd=work, env=env, capture_output=True, text=True, timeout=timeout)
        stdout, code = proc.stdout, proc.returncode
    except subprocess.TimeoutExpired as err:
        stdout, code = (err.stdout or b"").decode() if isinstance(err.stdout, bytes) else (err.stdout or ""), "timeout"

    dest = os.path.join(out_dir, f"{fixture}__{arm}__{run}")
    os.makedirs(dest, exist_ok=True)
    with open(os.path.join(dest, "transcript.jsonl"), "w") as handle:
        handle.write(stdout)
    result_text, cost, turns = "", None, None
    for line in stdout.splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if event.get("type") == "result":
            result_text = event.get("result") or ""
            cost = event.get("total_cost_usd")
            turns = event.get("num_turns")
    with open(os.path.join(dest, "result.md"), "w") as handle:
        handle.write(result_text)
    log = os.path.join(work, ".ds-checks.log")
    if os.path.exists(log):
        shutil.copy(log, os.path.join(dest, "checks.log"))
    meta = {"fixture": fixture, "arm": arm, "run": run, "model": model, "exit": code,
            "seconds": round(time.time() - started, 1), "cost_usd": cost, "turns": turns}
    with open(os.path.join(dest, "meta.json"), "w") as handle:
        json.dump(meta, handle, indent=2)
    shutil.rmtree(job_root, ignore_errors=True)
    return meta


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--fixtures", default=",".join(sorted(os.listdir(FIXTURES))))
    parser.add_argument("--arms", default=",".join(ARMS))
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--model", default="sonnet")
    parser.add_argument("--parallel", type=int, default=6)
    parser.add_argument("--timeout", type=int, default=900)
    parser.add_argument("--out", default=os.path.join(HERE, "results", time.strftime("%Y%m%d-%H%M%S")))
    args = parser.parse_args()

    jobs = [(f, a, r) for f in args.fixtures.split(",") for a in args.arms.split(",") for r in range(1, args.runs + 1)]
    os.makedirs(args.out, exist_ok=True)
    print(f"{len(jobs)} jobs -> {args.out}", flush=True)
    with futures.ThreadPoolExecutor(max_workers=args.parallel) as pool:
        pending = {pool.submit(run_job, job, args.model, args.out, args.timeout): job for job in jobs}
        for done in futures.as_completed(pending):
            meta = done.result()
            print(f"{meta['fixture']} {meta['arm']:8} run {meta['run']}: exit {meta['exit']}, "
                  f"{meta['seconds']}s, turns {meta['turns']}, ${meta['cost_usd']}", flush=True)
    print(f"done: {args.out}")


if __name__ == "__main__":
    main()
