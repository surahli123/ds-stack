"""Runs that didn't execute are never graded as answers.

The real logs come from dots' Codex attempt 2026-10-13-2343 (results/2026-10-13-2343-codex): 137 of 144 runs
died on HTTP 429 or "model at capacity" within seconds, every one carried the old wrapper's isolation warning,
run_arms.py exited 0, and grading scored the empty replies as model misses.
"""

import json
import os
import shlex
import shutil
import subprocess
import sys

import acceptance
import execution
import grade
import pytest
import run_arms
from conftest import ROOT

DATA = os.path.join(ROOT, "tests", "data")
CODEX_SH = os.path.join(ROOT, "eval", "agents", "codex.sh")
READOUT = """## Answer
Headline: can't tell
The split is 51.2/48.8 on every day, so the lift is not trustworthy.

## Why we believe it
- Alternatives considered:
  - Sample ratio mismatch: ruled in by the srm check [measured]
- Checks run:
  - srm: fail 51.2/48.8 against a planned 50/50
"""


def read(name):
    with open(os.path.join(DATA, name)) as handle:
        return handle.read()


# --- classify ------------------------------------------------------------------------------------------------

def test_the_real_429_run_was_an_execution_failure_not_a_miss():
    run_dir = os.path.join(DATA, "codex-2343-en-f1-baseline-1")
    assert execution.run_execution(run_dir) == "not_isolated+rate_limited"
    log = read("codex-2343-en-f1-baseline-1/agent.log").replace(
        "ds-stack: <HOME>/.codex/skills is present, so this run is not isolated\n", "")
    assert execution.classify(1, "", log) == "rate_limited"


def test_the_real_capacity_log_is_capacity():
    assert execution.classify(1, "", read("codex-2343-en-f5-full-2-capacity-head.log").split("\n", 2)[2]) == "capacity"


def test_a_run_that_finished_after_codex_retried_a_429_itself_is_ok():
    log = "model: gpt-x\nERROR: Reconnecting... 2/5\nstream error: 429 Too Many Requests, retrying\n"
    assert execution.classify(0, READOUT, log) == "ok"


@pytest.mark.parametrize("code, reply, log, error, expected", [
    ("timeout", READOUT, "", None, "timeout"),
    ("timeout", "", "ERROR: exceeded retry limit, last status: 429 Too Many Requests", None, "rate_limited"),
    (0, "   \n", "", None, "empty_reply"),
    (3, READOUT, "Traceback ...", None, "exit_3"),
    (0, "API Error: 529 Overloaded", "", "API Error: 529 Overloaded", "capacity"),
    (0, "Claude AI usage limit reached", "", "Claude AI usage limit reached", "rate_limited"),
    (0, "", "", "error_max_turns", "max_turns"),
    (0, "", "", "error_during_execution", "agent_error"),
    (4, "", "ds-stack: /h/.codex/AGENTS.md is present, so this run is not isolated; Codex was not started\n", None,
     "not_isolated"),
])
def test_classify(code, reply, log, error, expected):
    assert execution.classify(code, reply, log, error) == expected


def test_the_agents_own_limits_are_graded_and_provider_failures_are_not():
    assert all(execution.executed(kind) for kind in ("ok", "timeout", "max_turns", "empty_reply"))
    assert not any(execution.executed(kind) for kind in ("rate_limited", "capacity", "not_isolated", "exit_1",
                                                         "agent_error", "not_isolated+rate_limited"))


def test_a_timed_out_run_is_graded_as_a_miss_not_invalid(tmp_path):
    run_dir = make_run(tmp_path, "f5", "full", 1, code="timeout", text="")
    (run,) = grade.grade_dir(str(tmp_path), allow_no_transcript=True)
    assert run["execution"] == "timeout" and run["miss"] == "unparseable" and run["reason"].startswith("timeout: ")
    assert run_dir.exists()


def test_an_analysis_that_says_not_isolated_is_not_an_isolation_failure():
    assert execution.classify(0, "The effect is not isolated from seasonality.\n" + READOUT, "") == "ok"


def test_claude_result_reads_is_error():
    ok = json.dumps({"type": "result", "result": "R", "is_error": False, "total_cost_usd": 0.1, "num_turns": 3})
    bad = json.dumps({"type": "result", "result": "API Error: 429 rate_limit_error", "is_error": True})
    assert execution.claude_result(ok) == ("R", None, 0.1, 3)
    assert execution.classify(0, *execution.claude_result(bad)[:1], "", execution.claude_result(bad)[1]) == "rate_limited"


def test_agent_details_reads_the_codex_header():
    assert execution.agent_details(read("codex-2343-en-f1-baseline-1/agent.log")) == {
        "agent_model": "gpt-6-astra", "reasoning_effort": "none"}


# --- codex.sh's isolation guard -----------------------------------------------------------------------------

@pytest.fixture
def fake_codex(tmp_path, monkeypatch):
    """A `codex` on PATH that records its arguments, so codex.sh can run without the real CLI."""
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    codex = bin_dir / "codex"
    codex.write_text('#!/bin/sh\nif [ "$2" = "--help" ]; then echo "--approve-for-me"; exit 0; fi\n'
                     'for a in "$@"; do echo "arg:$a"; done\n')
    codex.chmod(0o755)
    home = tmp_path / "codex-home"
    home.mkdir()
    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ['PATH']}")
    monkeypatch.setenv("CODEX_HOME", str(home))
    monkeypatch.delenv("DS_CODEX_MODEL", raising=False)
    monkeypatch.delenv("DS_CODEX_EFFORT", raising=False)
    prompt = tmp_path / "prompt.md"
    prompt.write_text("PROMPT TEXT")

    def run():
        return subprocess.run(["sh", CODEX_SH, str(prompt)], capture_output=True, text=True)
    return home, run


def test_codex_rebuilt_system_skills_are_allowed(fake_codex):
    home, run = fake_codex
    (home / "skills" / ".system" / "imagegen").mkdir(parents=True)
    (home / "auth.json").write_text("{}")
    (home / "plugins").mkdir()
    proc = run()
    assert proc.returncode == 0 and proc.stderr == ""
    assert "arg:PROMPT TEXT" in proc.stdout and "arg:--approve-for-me" in proc.stdout


@pytest.mark.parametrize("leftover", ["AGENTS.md", "AGENTS.override.md", "prompts/p.md", "skills/my-skill/SKILL.md",
                                      "skills/.hidden-skill/SKILL.md"])
def test_any_other_leftover_stops_the_run_before_codex_starts(fake_codex, leftover):
    home, run = fake_codex
    (home / "skills" / ".system").mkdir(parents=True)
    path = home / leftover
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("x")
    proc = run()
    assert proc.returncode == 4 and proc.stdout == ""
    assert "not isolated; Codex was not started" in proc.stderr and leftover.split("/")[0] in proc.stderr
    assert execution.classify(proc.returncode, proc.stdout, proc.stderr) == "not_isolated"


def test_a_symlinked_system_folder_is_a_leftover(fake_codex, tmp_path):
    home, run = fake_codex
    (tmp_path / "elsewhere").mkdir()
    (home / "skills").mkdir()
    os.symlink(tmp_path / "elsewhere", home / "skills" / ".system")
    assert run().returncode == 4


def test_model_and_effort_are_pinned_only_when_set(fake_codex, monkeypatch):
    home, run = fake_codex
    assert "arg:--model" not in run().stdout
    monkeypatch.setenv("DS_CODEX_MODEL", "gpt-x")
    monkeypatch.setenv("DS_CODEX_EFFORT", "high")
    out = run().stdout.splitlines()
    assert out[out.index("arg:--model") + 1] == "arg:gpt-x"
    assert out[out.index("arg:-c") + 1] == 'arg:model_reasoning_effort="high"'
    assert out[-1] == "arg:PROMPT TEXT"


# --- run_arms.py: retries, the shared pause and the stop rule ----------------------------------------------

def counting_agent(tmp_path, failures, stderr="ERROR: exceeded retry limit, last status: 429 Too Many Requests",
                   code=1):
    """Fails `failures` times with `stderr`, then answers. Counts its calls in a file."""
    counter = tmp_path / "calls"
    script = (
        "import pathlib, sys\n"
        f"c = pathlib.Path({str(counter)!r})\n"
        "n = int(c.read_text()) + 1 if c.exists() else 1\n"
        "c.write_text(str(n))\n"
        f"if n <= {failures}:\n"
        f"    sys.stderr.write({stderr!r} + '\\n'); sys.exit({code})\n"
        "sys.stderr.write('model: fake-1\\nreasoning effort: high\\n')\n"
        f"sys.stdout.write({READOUT!r})\n")
    return shlex.join([sys.executable, "-c", script, "{prompt_file}"]), counter


def test_a_rate_limited_attempt_is_retried_and_kept(tmp_path, monkeypatch):
    monkeypatch.setenv("DS_RUN_ROOT", str(tmp_path / "runs"))
    template, counter = counting_agent(tmp_path, failures=1)
    out = tmp_path / "out"
    meta = run_arms.run_job(("f5", "baseline", 1), "auto", str(out), 60, agent_cmd=template,
                            pacer=run_arms.Pacer(backoff=0), retries=2)
    assert meta["execution"] == "ok" and meta["attempts"] == 2 and meta["earlier_attempts"] == ["rate_limited"]
    assert meta["agent_model"] == "fake-1" and meta["reasoning_effort"] == "high" and meta["model"] is None
    dest = out / "f5__baseline__1"
    assert "429" in (dest / "attempt1.log").read_text() and (dest / "result.md").read_text() == READOUT
    assert counter.read_text() == "2"


def test_retries_run_out(tmp_path, monkeypatch):
    monkeypatch.setenv("DS_RUN_ROOT", str(tmp_path / "runs"))
    template, counter = counting_agent(tmp_path, failures=99)
    meta = run_arms.run_job(("f5", "baseline", 1), "auto", str(tmp_path / "out"), 60, agent_cmd=template,
                            pacer=run_arms.Pacer(backoff=0), retries=2)
    assert meta["execution"] == "rate_limited" and meta["attempts"] == 3 and counter.read_text() == "3"


def test_a_crash_is_not_retried(tmp_path, monkeypatch):
    monkeypatch.setenv("DS_RUN_ROOT", str(tmp_path / "runs"))
    template, counter = counting_agent(tmp_path, failures=99, stderr="Traceback: boom")
    meta = run_arms.run_job(("f5", "baseline", 1), "auto", str(tmp_path / "out"), 60, agent_cmd=template,
                            pacer=run_arms.Pacer(backoff=0), retries=2)
    assert meta["execution"] == "exit_1" and meta["attempts"] == 1


def test_the_pacer_stops_new_jobs_after_failures_in_a_row_and_after_any_isolation_failure():
    pacer = run_arms.Pacer(backoff=0, max_failed=2)
    pacer.finished("rate_limited")
    pacer.finished("ok")
    pacer.finished("capacity")
    assert pacer.stopped is None
    pacer.finished("capacity")
    assert "2 jobs in a row" in pacer.stopped
    pacer = run_arms.Pacer()
    pacer.finished("not_isolated")
    assert pacer.stopped == "a run was not isolated"
    assert run_arms.run_job(("f5", "baseline", 1), "auto", "/nonexistent", 60, agent_cmd="x", pacer=pacer) == {
        "fixture": "f5", "arm": "baseline", "run": 1, "execution": "not_started"}


def test_the_pause_holds_every_worker(monkeypatch):
    pacer = run_arms.Pacer(backoff=10)
    now = [1000.0]
    slept = []
    monkeypatch.setattr(run_arms.time, "time", lambda: now[0])

    def fake_sleep(seconds):
        slept.append(seconds)
        now[0] += seconds
    monkeypatch.setattr(run_arms.time, "sleep", fake_sleep)
    pacer.pause(2)
    pacer.wait()
    assert sum(slept) == 20


def test_run_arms_exits_2_and_records_what_did_not_run(tmp_path):
    template, _ = counting_agent(tmp_path, failures=99)
    out = tmp_path / "out"
    env = {**os.environ, "DS_RUN_ROOT": str(tmp_path / "runs")}
    proc = subprocess.run([sys.executable, os.path.join(ROOT, "eval", "run_arms.py"), "--fixtures", "f5",
                           "--arms", "baseline", "--runs", "3", "--parallel", "1", "--retries", "0",
                           "--backoff", "0", "--max-failed-in-row", "2", "--agent-cmd", template, "--out", str(out)],
                          capture_output=True, text=True, env=env)
    assert proc.returncode == 2, proc.stderr
    status = json.loads((out / "run-status.json").read_text())
    assert status["executed"] == 0 and status["failed"] == {"rate_limited": 2} and len(status["not_started"]) == 1
    assert "jobs in a row" in status["stopped"] and "not a result" in proc.stdout
    assert len([p for p in out.iterdir() if p.is_dir()]) == 2


def test_run_arms_exits_0_when_every_job_executed(tmp_path):
    template, _ = counting_agent(tmp_path, failures=0)
    out = tmp_path / "out"
    env = {**os.environ, "DS_RUN_ROOT": str(tmp_path / "runs")}
    proc = subprocess.run([sys.executable, os.path.join(ROOT, "eval", "run_arms.py"), "--fixtures", "f5",
                           "--arms", "baseline", "--runs", "1", "--agent-cmd", template, "--out", str(out)],
                          capture_output=True, text=True, env=env)
    assert proc.returncode == 0, proc.stderr
    assert json.loads((out / "run-status.json").read_text())["exit"] == 0


# --- grade.py and acceptance.py refuse to score what didn't run ------------------------------------------

def make_run(root, fixture, arm, run, code=0, text=READOUT, log=""):
    run_dir = root / f"{fixture}__{arm}__{run}"
    run_dir.mkdir(parents=True)
    (run_dir / "meta.json").write_text(json.dumps({"fixture": fixture, "arm": arm, "run": run, "exit": code,
                                                   "agent_cmd": "a", "transcript": False}))
    (run_dir / "result.md").write_text(text)
    (run_dir / "agent.log").write_text(log)
    return run_dir


def test_grade_marks_runs_that_did_not_execute_and_calls_the_directory_invalid(tmp_path, capsys):
    make_run(tmp_path, "f5", "full", 1)
    shutil.copytree(os.path.join(DATA, "codex-2343-en-f1-baseline-1"), tmp_path / "f1__baseline__1")
    runs = {r["fixture"]: r for r in grade.grade_dir(str(tmp_path), allow_no_transcript=True)}
    assert runs["f5"]["correct"] and runs["f5"]["execution"] == "ok"
    assert runs["f1"]["miss"] == "not_executed" and runs["f1"]["reason"] == "execution failed: not_isolated+rate_limited"
    assert grade.main([str(tmp_path), "--allow-no-transcript"]) == 2
    summary = json.loads((tmp_path / "summary.json").read_text())
    assert summary["verdict"]["verdict"].startswith("INVALID (1 of 2 runs didn't execute")
    assert summary["per_arm"]["baseline"]["runs_not_executed"] == 1
    assert summary["per_arm"]["baseline"]["runs_unparseable"] == 0
    capsys.readouterr()


def test_acceptance_refuses_levels_for_a_directory_with_failed_runs(tmp_path, capsys):
    make_run(tmp_path, "f5", "full", 1, code=1, text="", log="ERROR: 429 Too Many Requests\n")
    assert acceptance.main([str(tmp_path), "--allow-no-transcript"]) == 2
    out = capsys.readouterr().out
    assert "INVALID, not an acceptance result: 1 of 1 runs didn't execute (rate_limited 1)" in out
    assert "| Plumbing |" not in out
    assert acceptance.main([str(tmp_path), "--allow-no-transcript", "--diagnostic"]) == 2
    out = capsys.readouterr().out
    assert "DIAGNOSTIC ONLY" in out and "| Plumbing |" in out


def test_acceptance_counts_jobs_that_never_started(tmp_path, capsys):
    make_run(tmp_path, "f5", "full", 1)
    (tmp_path / "run-status.json").write_text(json.dumps({"not_started": ["f5__full__2"]}))
    assert acceptance.main([str(tmp_path), "--allow-no-transcript"]) == 2
    assert "1 jobs never started" in capsys.readouterr().out


def test_listed_directories_are_never_graded(tmp_path, capsys):
    results = tmp_path / "2026-10-14-codex-en"
    make_run(results, "f5", "full", 1)
    assert grade.main([str(results), "--allow-no-transcript"]) == 2
    assert not (results / "summary.md").exists()
    assert acceptance.main([str(results), "--allow-no-transcript"]) == 2
    assert "REFUSED" in capsys.readouterr().out
