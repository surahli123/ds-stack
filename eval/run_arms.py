#!/usr/bin/env python3
"""Run fixtures through the three arms with `claude -p` in clean profiles.

    python3 eval/run_arms.py --runs 3 --model sonnet --parallel 6
    DS_AGENT_CMD='my-agent --print --model {model}' python3 eval/run_arms.py --model auto

Each job gets a fresh working directory holding only the fixture's warehouse.db
and its arm's assets, plus a fresh, empty Claude config dir (no personal
CLAUDE.md, memory, skills or hooks). Gold answers are never copied in.

Other agents (Cursor, RovoDev, ...): set --agent-cmd or DS_AGENT_CMD to a command
template. The prompt is written to a temp file; `{prompt_file}` becomes its path
and `{model}` the --model value. If the template has no `{prompt_file}`, the
prompt goes on stdin. The template is split with shlex and run without a shell
(use `sh -c '...'` for redirection or $(...)). The agent runs in the job's
analysis directory and its stdout is the final reply, saved as result.md.
A custom agent has no stream-json transcript, so no transcript.jsonl is written,
cost and turns are null, and meta.json records "agent_cmd" and "transcript": false.
The job's DS_CHECKS_LOG and DS_QUERIES_LOG still point into the analysis
directory and are copied out as checks.log and queries.log. Isolation can't be
audited without a transcript, and the agent keeps your real HOME so it stays
logged in (the clean Claude profile applies only to the default `claude -p`),
so grade such runs with `grade.py --allow-no-transcript`.

Arms:
  baseline  plain prompting
  checks    checks/ plus a one-line instruction to run them
  full      the ds-mode skill (method + checks + readout), pointed to by CLAUDE.md and AGENTS.md

Every arm gets the identical prompt: the fixture's task plus the readout format.
A fixture with an overlay/ folder (the team's metric definitions) gets it copied
outside the analysis directory, with $DS_OVERLAY_DIR pointing at it, in every arm.
"""

import argparse
import concurrent.futures as futures
import json
import os
import re
import shlex
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
                   "REQUESTS_CA_BUNDLE", "ANTHROPIC_API_KEY", "CLAUDE_CODE_OAUTH_TOKEN")
# A custom agent keeps its real login, so it also gets these (the default arm runs with HOME set to an empty dir).
CUSTOM_AGENT_ENV = ("HOME", "USER", "LOGNAME", "XDG_CONFIG_HOME", "XDG_DATA_HOME", "XDG_CACHE_HOME", "CURSOR_API_KEY")
SKIP_IN_COPY = shutil.ignore_patterns("__pycache__", "registry.json", ".ds-checks.log", ".ds-queries.log")
CHECKS_ONLY_NOTE = ("Before reporting any number computed from data, run the checks in checks/ that apply "
                    "(python3 checks/run.py --list shows them) and include their results.\n")
FULL_NOTE = "For any data analysis request, read and follow .claude/skills/ds-mode/SKILL.md.\n"


# Tag placeholders the full arm's skill asks for: [q<n>], [check:<name>#<n>], [given], or "|"-joined mixes.
# `[measured|inferred|guess]` and the like don't start with one of these, so they stay.
_TAG_TERM = r"(?:q(?:<[^<>\]|]*>|\d+)|check:[^\]|]+|given)"
_TAG = rf"\[\s*{_TAG_TERM}(?:\s*\|\s*{_TAG_TERM})*\s*\]"


def strip_tag_placeholders(text):
    """Drop evidence-tag placeholders and the spaces before them, so every arm sees the same format text."""
    text = re.sub(rf"(?m)^([ \t]*){_TAG}[ \t]?", r"\1", text)
    return re.sub(rf"[ \t]*{_TAG}", "", text)


def readout_format():
    """The readout block from SKILL.md, without tag syntax, so every arm sees the same format text."""
    with open(os.path.join(SKILL_DIR, "SKILL.md")) as handle:
        text = handle.read()
    section = text.split("## Readout", 1)[1]
    return strip_tag_placeholders(re.search(r"```\n(.*?)```", section, re.S).group(1))


def build_prompt(fixture, suffix=""):
    """The fixture's task plus the readout format. `suffix` (for example "Write the prose in Chinese.")
    goes last, identically for every arm."""
    with open(os.path.join(FIXTURES, fixture, "task.md")) as handle:
        task = handle.read().strip()
    prompt = (f"{task}\n\nThe data is in warehouse.db (SQLite) in the current directory.\n\n"
              "End with exactly this readout as your final reply. Label each claim "
              "measured (computed from data here), inferred, or guess:\n\n"
              f"```\n{readout_format()}```\n")
    return prompt + (f"\n{suffix.strip()}\n" if suffix.strip() else "")


def write_note(work, note):
    """The arm's one-line instruction, for Claude Code (CLAUDE.md) and for Codex and Cursor (AGENTS.md)."""
    for name in ("CLAUDE.md", "AGENTS.md"):
        with open(os.path.join(work, name), "w") as handle:
            handle.write(note)


def prepare_workdir(job_root, fixture, arm):
    work = os.path.join(job_root, "analysis")
    os.makedirs(work)
    shutil.copy(os.path.join(FIXTURES, fixture, "warehouse.db"), work)
    if arm == "checks":
        shutil.copytree(os.path.join(SKILL_DIR, "checks"), os.path.join(work, "checks"), ignore=SKIP_IN_COPY)
        write_note(work, CHECKS_ONLY_NOTE)
    elif arm == "full":
        shutil.copytree(SKILL_DIR, os.path.join(work, ".claude", "skills", "ds-mode"), ignore=SKIP_IN_COPY)
        write_note(work, FULL_NOTE)
    return work


def claude_argv(prompt, model):
    return ["claude", "-p", prompt, "--model", model, "--output-format", "stream-json",
            "--verbose", "--allowedTools", "Bash,Read,Write,Edit,Glob,Grep", "--max-turns", "60"]


def agent_argv(template, prompt_file, model):
    """Expand an --agent-cmd template into (argv, prompt_on_stdin).

    The template is split with shlex first and `{prompt_file}` / `{model}` are filled in token by token, so a
    path with spaces or backslashes stays one argument. Never goes through a shell.
    """
    argv = [tok.replace("{prompt_file}", prompt_file).replace("{model}", model) for tok in shlex.split(template)]
    if not argv:
        raise ValueError("the agent command is empty")
    return argv, "{prompt_file}" not in template


def run_job(job, model, out_dir, timeout, agent_cmd=None, suffix=""):
    fixture, arm, run = job
    job_root = os.path.join(os.environ.get("DS_RUN_ROOT", "/tmp/ds-runs"), uuid.uuid4().hex[:10])
    work = prepare_workdir(job_root, fixture, arm)
    config = os.path.join(job_root, "config")
    os.makedirs(config)
    env = {k: os.environ[k] for k in PASSTHROUGH_ENV if k in os.environ}
    if agent_cmd:
        env.update({k: os.environ[k] for k in CUSTOM_AGENT_ENV if k in os.environ})
        env.update(CLAUDE_CONFIG_DIR=config)
    else:
        env.update(HOME=config, CLAUDE_CONFIG_DIR=config)
    env.update(DS_CHECKS_LOG=os.path.join(work, ".ds-checks.log"), DS_QUERIES_LOG=os.path.join(work, ".ds-queries.log"))
    overlay = os.path.join(FIXTURES, fixture, "overlay")
    if os.path.isdir(overlay):
        # The team's definitions, outside the analysis directory and named only by $DS_OVERLAY_DIR, for every arm.
        shutil.copytree(overlay, os.path.join(job_root, "overlay"))
        env["DS_OVERLAY_DIR"] = os.path.join(job_root, "overlay")
    kwargs = {}
    if agent_cmd:
        prompt = build_prompt(fixture, suffix)
        prompt_file = os.path.join(job_root, "prompt.md")
        with open(prompt_file, "w", encoding="utf-8") as handle:
            handle.write(prompt)
        cmd, on_stdin = agent_argv(agent_cmd, prompt_file, model)
        kwargs = {"input": prompt} if on_stdin else {"stdin": subprocess.DEVNULL}
        kwargs.update(encoding="utf-8", errors="replace")
    else:
        cmd = claude_argv(build_prompt(fixture, suffix), model)
    started = time.time()
    try:
        proc = subprocess.run(cmd, cwd=work, env=env, capture_output=True, text=True, timeout=timeout, **kwargs)
        stdout, stderr, code = proc.stdout, proc.stderr or "", proc.returncode
    except subprocess.TimeoutExpired as err:
        stdout, code = (err.stdout or b"").decode() if isinstance(err.stdout, bytes) else (err.stdout or ""), "timeout"
        stderr = (err.stderr or b"").decode() if isinstance(err.stderr, bytes) else (err.stderr or "")
    except OSError as err:
        if not agent_cmd:
            raise
        stdout, stderr, code = "", str(err), f"error: {err}"

    dest = os.path.join(out_dir, f"{fixture}__{arm}__{run}")
    os.makedirs(dest, exist_ok=True)
    result_text, cost, turns = "", None, None
    if agent_cmd:
        result_text = stdout
        with open(os.path.join(dest, "agent.log"), "w") as handle:
            handle.write(stderr)
    else:
        with open(os.path.join(dest, "transcript.jsonl"), "w") as handle:
            handle.write(stdout)
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
    for name, copy in ((".ds-checks.log", "checks.log"), (".ds-queries.log", "queries.log")):
        log = os.path.join(work, name)
        if os.path.exists(log):
            shutil.copy(log, os.path.join(dest, copy))
    meta = {"fixture": fixture, "arm": arm, "run": run, "model": model, "exit": code,
            "seconds": round(time.time() - started, 1), "cost_usd": cost, "turns": turns}
    if agent_cmd:
        meta.update(agent_cmd=agent_cmd, transcript=False)
    if suffix.strip():
        meta.update(prompt_suffix=suffix.strip())
    with open(os.path.join(dest, "meta.json"), "w") as handle:
        json.dump(meta, handle, indent=2)
    shutil.rmtree(job_root, ignore_errors=True)
    return meta


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--fixtures", default=",".join(sorted(os.listdir(FIXTURES))))
    parser.add_argument("--arms", default=",".join(ARMS))
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--model", default="sonnet", help="passed to the agent as --model (claude) or {model} (custom)")
    parser.add_argument("--agent-cmd", default=os.environ.get("DS_AGENT_CMD") or None,
                        help="command template for a non-Claude agent, e.g. 'my-agent --model {model}'. {prompt_file} is "
                             "the prompt's path; without it the prompt goes on stdin. Its stdout is the final reply. "
                             "No transcript is recorded. Default: $DS_AGENT_CMD, else `claude -p`")
    parser.add_argument("--prompt-suffix", default="",
                        help='text appended to every arm\'s prompt, e.g. "Write the prose in Chinese." (recorded in meta.json)')
    parser.add_argument("--parallel", type=int, default=6)
    parser.add_argument("--timeout", type=int, default=900)
    parser.add_argument("--out", default=os.path.join(HERE, "results", time.strftime("%Y%m%d-%H%M%S")))
    args = parser.parse_args()
    agent_cmd = args.agent_cmd or None
    if agent_cmd:
        try:
            program = agent_argv(agent_cmd, "", "")[0][0]
        except ValueError as err:
            parser.error(f"--agent-cmd: {err}")
        if not shutil.which(program):
            parser.error(f"--agent-cmd: `{program}` is not on PATH")

    jobs = [(f, a, r) for f in args.fixtures.split(",") for a in args.arms.split(",") for r in range(1, args.runs + 1)]
    os.makedirs(args.out, exist_ok=True)
    print(f"{len(jobs)} jobs -> {args.out}", flush=True)
    with futures.ThreadPoolExecutor(max_workers=args.parallel) as pool:
        pending = {pool.submit(run_job, job, args.model, args.out, args.timeout, agent_cmd, args.prompt_suffix): job for job in jobs}
        for done in futures.as_completed(pending):
            meta = done.result()
            spend = "no transcript or cost data" if meta.get("transcript") is False else f"turns {meta['turns']}, ${meta['cost_usd']}"
            print(f"{meta['fixture']} {meta['arm']:8} run {meta['run']}: exit {meta['exit']}, "
                  f"{meta['seconds']}s, {spend}", flush=True)
    print(f"done: {args.out}")


if __name__ == "__main__":
    main()
