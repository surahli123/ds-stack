"""ds-step keeps a long project on its aim: the card, the run gate and the hooks refuse the moves that caused drift.

The scenarios replay the failure modes from the 2026-11-09 to 11-17 intent-labeling pilot retro
(docs/drift-research.md) and the ways around the first version found in review of PR #32.
"""

import json
import os
import subprocess
import sys

import pytest
from conftest import ROOT

TOOLS = os.path.join(ROOT, "skills", "ds-step", "tools")
HOOK = os.path.join(ROOT, "hooks", "ds_step_hook.py")
STEP = os.path.join(TOOLS, "step.py")
sys.path.insert(0, TOOLS)
import step  # noqa: E402

CARD = ["card", "--aim", "compare prompt v2 and v3 on the held-out set", "--done", "a verdict on v2 vs v3",
        "--scope", "run both prompts on the 300 held-out rows", "--scope", "record the verdict",
        "--out", "boundary cases of fields the success bar does not use", "--budget", "60m",
        "--ask", "the held-out set has fewer than 300 rows", "--freeze", "prompts/v3.md"]


@pytest.fixture
def project(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    for name in ("DS_STEP_ROOT", "DS_SESSION_ID", "CLAUDE_PROJECT_DIR"):
        monkeypatch.delenv(name, raising=False)
    (tmp_path / "prompts").mkdir()
    (tmp_path / "prompts" / "v3.md").write_text("Label the query's intent.\n")
    assert step.main(["init", "--aim", "Rank three search bets", "--bar", "Precision on 300 held-out rows"]) == 0
    return tmp_path


def started(project):
    assert step.main(CARD) == 0
    assert step.main(["start"]) == 0
    assert step.main(["decide", "ship prompt v2 or v3"]) == 0


def run(*args, decision="D1"):
    return step.main(["run", "--decision", decision, "--if", "v3 >= 2pp better -> ship v3", *args])


def printer(text):
    return [sys.executable, "-c", f"print({text!r})"]


# --- blocking 1: the instructions can't change under a running step -----------------------------

def test_a_frozen_file_changed_by_any_route_stops_run_and_end(project, capsys):
    started(project)
    (project / "prompts" / "v3.md").write_text("Label the intent. Also label secondary intent.\n")  # sed, git pull
    assert run("--", "true") == 1 and step.main(["end", "done"]) == 1
    err = capsys.readouterr().err
    assert "frozen file prompts/v3.md changed" in err and "--abandon" in err
    assert step.main(["end", "prompt changed mid-step", "--abandon"]) == 0
    assert "abandoned" in (project / "DS-STATE.md").read_text()


def test_dropping_the_frozen_entry_or_rewriting_the_aim_in_the_state_file_is_caught(project, capsys):
    started(project)
    state = project / "DS-STATE.md"
    text = state.read_text()
    state.write_text(text.replace("- prompts/v3.md\n", "").replace("Rank three search bets", "Explore labels"))
    assert step.main(["brief"]) == 1 and run("--", "true") == 1
    assert "DS-STATE.md was changed outside step.py" in capsys.readouterr().err
    assert step.main(["render"]) == 0 and step.main(["brief"]) == 0
    assert "- prompts/v3.md" in state.read_text()


def test_editing_the_card_inside_the_event_log_is_caught(project, capsys):
    started(project)
    events = project / ".ds-step" / "events.jsonl"
    events.write_text(events.read_text().replace('"budget": "60m"', '"budget": "600m"'))
    step.main(["render"])
    assert run("--", "true") == 1
    assert "Step card changed in the event log since start" in capsys.readouterr().err


# --- blocking 3: the run gate counts decisions, not wording -------------------------------------

def test_a_run_needs_an_open_decision_id_and_an_if_line(project, capsys):
    started(project)
    assert step.main(["run", "--decision", "ship prompt v2 or v3", "--if", "x", "--", "true"]) == 1
    assert step.main(["run", "--decision", "D1", "--", "true"]) == 1
    err = capsys.readouterr().err
    assert "no decision ship prompt v2 or v3" in err and "--if" in err


def test_a_conclusive_verdict_closes_the_decision(project, capsys):
    started(project)
    assert run("--", *printer("SUMMARY v3-v2 +0.4pp, CI +-3pp")) == 0
    assert step.main(["verdict", "R1", "no-change", "within noise, keep v2"]) == 0
    assert run("--", "true") == 1
    assert "D1 is closed by C1" in capsys.readouterr().err
    assert "- C1: ship prompt v2 or v3 -> within noise, keep v2" in (project / "DS-STATE.md").read_text()


def test_tuning_on_noise_stops_at_the_third_run_whatever_the_verdicts_or_wording(project, capsys):
    """The pilot ran about ten tuning rounds ending 'within noise'. Rewording or switching verdicts doesn't help."""
    started(project)
    allowed, verdicts = 0, ["inconclusive", "no-change", "inconclusive", "no-change"]
    for attempt in range(10):
        decision = f"D{step.fold(step.load(str(project)))['n']['D']}"
        if run("--", *printer("SUMMARY within noise"), decision=decision) != 0:
            break
        allowed += 1
        step.main(["verdict", f"R{attempt + 1}", verdicts[attempt % 4], "within noise"])
        step.main(["decide", f"ship prompt v2 or v3, take {attempt + 2}"])
    assert allowed == 2
    assert "changed nothing" in capsys.readouterr().err
    assert run("--new-design", "1,000 held-out rows, not 100", "--", "true", decision="D3") == 0


# --- should-fix 4 and 5: every run leaves a record ----------------------------------------------

def test_two_runs_started_together_get_one_id_and_one_refusal(project):
    started(project)
    cmd = [sys.executable, STEP, "run", "--decision", "D1", "--if", "x", "--", sys.executable, "-c",
           "import time; time.sleep(1)"]
    procs = [subprocess.Popen(cmd, cwd=project, stdout=subprocess.PIPE, stderr=subprocess.PIPE) for _ in range(2)]
    codes = sorted(p.wait(timeout=30) for p in procs)
    assert codes == [0, 1]
    assert list(step.fold(step.load(str(project)))["runs"]) == ["R1"]


def test_failed_killed_and_binary_runs_are_all_recorded(project, capsys):
    started(project)
    assert run("--", "no-such-command-xyz") == 1
    assert "did not launch" in capsys.readouterr().err
    assert run("--", "sh", "-c", "printf 'SUMMARY \\377 bytes\\n'; kill -9 $$") == 0
    assert "SUMMARY" in capsys.readouterr().out
    assert (project / ".ds-step" / "runs" / "R2.log").exists()
    assert run("--", "true") == 1
    assert "R2 has no verdict" in capsys.readouterr().err


def test_run_prints_the_summary_and_keeps_rows_out_of_context(project, capsys):
    started(project)
    script = "for i in range(500): print(f'row {i}: query, label, confidence')\nprint('SUMMARY precision v3 0.81 vs v2 0.77')"
    assert run("--", sys.executable, "-c", script) == 0
    out = capsys.readouterr().out
    assert "SUMMARY precision v3 0.81 vs v2 0.77" in out and "row 1:" not in out and len(out) < 1000
    assert (project / ".ds-step" / "runs" / "R1.log").read_text().count("row ") == 500


# --- should-fix 6, 7, 8 and 11: the card, discovery, one step per session -----------------------

def test_the_card_takes_real_values_and_refuses_bad_ones(project, capsys):
    ok = CARD[:4] + ["CI half-width < 2pp on < 300 rows"] + CARD[5:]
    assert step.main(ok) == 0
    assert "Done when: CI half-width < 2pp on < 300 rows" in (project / "DS-STATE.md").read_text()
    too_many = CARD + [x for i in range(5) for x in ("--scope", f"task {i}")]
    assert step.main(too_many) == 1
    assert step.main([*CARD[:-2], "--budget", "as long as it takes", "--freeze", "prompts"]) == 1
    err = capsys.readouterr().err
    assert "7 in-scope steps" in err and "time box" in err and "not a file" in err


def test_one_state_file_found_from_any_subfolder(project, monkeypatch, capsys):
    (project / "notebooks").mkdir()
    monkeypatch.chdir(project / "notebooks")
    assert step.main(["init", "--aim", "a", "--bar", "b"]) == 1
    assert "already exists" in capsys.readouterr().err
    assert step.main(["park", "secondary-intent boundary cases"]) == 0
    assert "secondary-intent" in (project / "DS-STATE.md").read_text()
    assert STEP in (project / "DS-STATE.md").read_text()


def test_one_step_per_session(project, monkeypatch, capsys):
    monkeypatch.setenv("DS_SESSION_ID", "session-a")
    started(project)
    assert step.main(["start"]) == 1
    assert step.main(["end", "compared v2 and v3"]) == 0
    assert step.main(["start"]) == 1
    assert "no card" in capsys.readouterr().err
    assert step.main(CARD) == 0 and step.main(["start"]) == 1
    assert "this session already ended a step" in capsys.readouterr().err
    monkeypatch.setenv("DS_SESSION_ID", "session-b")
    assert step.main(["start"]) == 0


def test_closed_ids_are_never_reused(project):
    step.main(["close", "Which dataset?", "held-out v3"])
    step.main(["reopen", "C1", "--reason", "120 duplicate rows"])
    step.main(["close", "Which dataset?", "held-out v4"])
    text = (project / "DS-STATE.md").read_text()
    assert "- C2: Which dataset? -> held-out v4" in text and "- C1:" not in text


# --- blocking 2 and should-fix 10: the hooks ----------------------------------------------------

def hook(mode, payload, project, env_file=None):
    env = {**os.environ, "CLAUDE_PROJECT_DIR": str(project)}
    env.pop("DS_STEP_ROOT", None)
    if env_file:
        env["CLAUDE_ENV_FILE"] = str(env_file)
    proc = subprocess.run([sys.executable, HOOK, mode], input=json.dumps(payload), capture_output=True,
                          text=True, env=env, timeout=30)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout) if proc.stdout.strip() else None


def denied(result):
    return bool(result) and result["hookSpecificOutput"]["permissionDecision"] == "deny"


def write(path):
    return {"tool_name": "Write", "tool_input": {"file_path": str(path), "content": "x"}}


def test_the_hooks_do_nothing_without_a_project(tmp_path):
    assert hook("session-start", {"source": "startup"}, tmp_path) is None
    assert hook("pre-tool-use", write(tmp_path / "DS-STATE.md"), tmp_path) is None


def test_state_files_take_no_file_tool_edits_and_shell_commands_are_not_judged(project):
    for path in (project / "DS-STATE.md", project / ".ds-step" / "events.jsonl"):
        assert denied(hook("pre-tool-use", write(path), project))
    shell = {"tool_name": "Bash", "tool_input": {"command": "git diff DS-STATE.md 2>&1 | head"}}
    assert hook("pre-tool-use", shell, project) is None
    assert hook("pre-tool-use", write(project / "notes" / "v3.md"), project) is None


def test_frozen_files_take_no_edits_while_a_step_runs_and_any_edit_between_steps(project):
    notebook = {"tool_name": "NotebookEdit", "tool_input": {"notebook_path": str(project / "prompts" / "v3.md")}}
    assert hook("pre-tool-use", write(project / "prompts" / "v3.md"), project) is None
    started(project)
    assert denied(hook("pre-tool-use", write(project / "prompts" / "v3.md"), project))
    assert denied(hook("pre-tool-use", notebook, project))
    assert step.main(["end", "done"]) == 0
    assert hook("pre-tool-use", write(project / "prompts" / "v3.md"), project) is None


def test_session_start_briefs_without_gating_discussion_and_stamps_the_session(project, tmp_path):
    step.main(["close", "Which dataset?", "held-out v3, 300 rows"])
    env_file = tmp_path / "env"
    result = hook("session-start", {"source": "startup", "session_id": "abc"}, project, env_file)
    context = result["hookSpecificOutput"]["additionalContext"]
    assert "Rank three search bets" in context and "C1: Which dataset?" in context and len(context) < 3000
    assert "Discussion, review and questions need nothing more" in context
    assert env_file.read_text() == "export DS_SESSION_ID=abc\n"
    (project / "DS-STATE.md").write_text("hand edit")
    context = hook("session-start", {"source": "resume"}, project)["hookSpecificOutput"]["additionalContext"]
    assert "refuses to brief" in context


def test_a_broken_payload_never_blocks_the_agent(project):
    env = {**os.environ, "CLAUDE_PROJECT_DIR": str(project)}
    proc = subprocess.run([sys.executable, HOOK, "pre-tool-use"], input="not json", capture_output=True, text=True, env=env)
    assert proc.returncode == 0 and proc.stdout == "" and "allowing" in proc.stderr


def test_the_plugin_registers_both_hooks_on_the_file_tools_only():
    with open(os.path.join(ROOT, "hooks", "hooks.json")) as handle:
        config = json.load(handle)["hooks"]
    commands = [h["command"] for event in ("SessionStart", "PreToolUse") for m in config[event] for h in m["hooks"]]
    assert all("${CLAUDE_PLUGIN_ROOT}/hooks/ds_step_hook.py" in c for c in commands)
    assert set(config["PreToolUse"][0]["matcher"].split("|")) == {"Write", "Edit", "MultiEdit", "NotebookEdit"}
