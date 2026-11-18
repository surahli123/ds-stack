"""ds-step keeps a long project on its aim: the card, the run gate and the hooks refuse the moves that caused drift.

The scenarios replay the failure modes from the 2026-11-09 to 11-17 intent-labeling pilot retro
(docs/drift-research.md) and the ways around earlier versions found in review of PR #32.
"""

import json
import os
import shutil
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


def state(project):
    return step.fold(step.load(str(project)))


def decide(capsys, question="ship prompt v2 or v3", *extra):
    capsys.readouterr()
    assert step.main(["decide", question, *extra]) == 0
    return capsys.readouterr().out.strip()


def started(project, capsys):
    assert step.main(CARD) == 0 and step.main(["start"]) == 0
    return decide(capsys)


def run(decision, *args):
    return step.main(["run", "--decision", decision, "--if", "v3 >= 2pp better -> ship v3", *args])


def printer(text):
    return [sys.executable, "-c", f"print({text!r})"]


def last_run(project):
    return list(state(project)["runs"])[-1]


# --- the freeze: instructions can't change under a running step ---------------------------------

def test_a_frozen_file_changed_by_any_route_stops_run_and_end_but_not_the_verdict(project, capsys):
    d1 = started(project, capsys)
    assert run(d1, "--", "true") == 0
    (project / "prompts" / "v3.md").write_text("Label the intent. Also label secondary intent.\n")  # sed, git pull
    assert step.main(["verdict", last_run(project), "inconclusive", "noise"]) == 0
    assert run(d1, "--", "true") == 1 and step.main(["end", "done"]) == 1
    assert "frozen file prompts/v3.md changed" in capsys.readouterr().err
    assert step.main(["brief"]) == 0
    assert "WARNING: frozen file prompts/v3.md changed" in capsys.readouterr().out
    assert step.main(["end", "prompt changed mid-step", "--abandon"]) == 0


def test_abandoning_a_step_closes_its_unjudged_runs(project, capsys):
    d1 = started(project, capsys)
    run(d1, "--", "true")
    assert step.main(["end", "stop", "--abandon"]) == 0
    assert [r["verdict"] for r in state(project)["runs"].values()] == ["abandoned"]


def test_editing_the_card_inside_the_event_log_is_caught(project, capsys):
    d1 = started(project, capsys)
    events = project / ".ds-step" / "events.jsonl"
    events.write_text(events.read_text().replace('"budget": "60m"', '"budget": "600m"'))
    assert run(d1, "--", "true") == 1
    assert "card changed in the event log since start" in capsys.readouterr().err


def test_a_second_install_and_a_hand_edited_view_change_nothing(project, tmp_path_factory, capsys):
    """The view is derived: another copy of step.py (plugin update, Codex's copy) must keep working."""
    d1 = started(project, capsys)
    (project / "DS-STATE.md").write_text("hand edit")
    other = tmp_path_factory.mktemp("other-install") / "step.py"
    shutil.copy(STEP, other)
    proc = subprocess.run([sys.executable, str(other), "run", "--decision", d1, "--if", "x", "--", "true"],
                          cwd=project, capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    assert "## Open decisions" in (project / "DS-STATE.md").read_text()
    assert "DS-STATE.md" in (project / ".gitignore").read_text()


# --- merging branches ---------------------------------------------------------------------------

def test_two_branches_merge_by_union_without_colliding_ids(project, capsys):
    events = project / ".ds-step" / "events.jsonl"
    base = events.read_text()
    decide(capsys, "which dataset?", "--answer", "held-out v3")
    branch_a = events.read_text()
    events.write_text(base)
    decide(capsys, "which metric?", "--answer", "precision")
    branch_b = events.read_text()
    events.write_text(base + branch_a[len(base):] + branch_b[len(base):])  # what merge=union produces
    assert len(step.settled(state(project))) == 2
    assert "events.jsonl merge=union" in (project / ".ds-step" / ".gitattributes").read_text()


def test_conflict_markers_and_duplicate_ids_are_refused_by_name(project, capsys):
    events = project / ".ds-step" / "events.jsonl"
    decide(capsys, "which dataset?", "--answer", "held-out v3")
    good = events.read_text()
    events.write_text(good + "<<<<<<< HEAD\n")
    assert step.main(["brief"]) == 1
    assert "line 3 is not an event" in capsys.readouterr().err
    events.write_text(good + good.splitlines(keepends=True)[-1])
    assert step.main(["brief"]) == 1
    err = capsys.readouterr().err
    assert "creates D-" in err and "twice" in err


# --- the run gate -------------------------------------------------------------------------------

def test_a_run_needs_an_open_decision_id_and_an_if_line(project, capsys):
    d1 = started(project, capsys)
    assert step.main(["run", "--decision", "ship prompt v2 or v3", "--if", "x", "--", "true"]) == 1
    assert step.main(["run", "--decision", d1, "--", "true"]) == 1
    err = capsys.readouterr().err
    assert "no decision ship prompt v2 or v3" in err and "--if" in err


def test_a_conclusive_verdict_settles_the_decision(project, capsys):
    d1 = started(project, capsys)
    assert run(d1, "--", *printer("SUMMARY v3-v2 +0.4pp, CI +-3pp")) == 0
    assert step.main(["verdict", last_run(project), "no-change", "within noise, keep v2"]) == 0
    assert run(d1, "--", "true") == 1
    assert "is settled: within noise, keep v2" in capsys.readouterr().err
    assert f"- {d1}: ship prompt v2 or v3 -> within noise, keep v2" in (project / "DS-STATE.md").read_text()
    assert step.main(["reopen", d1, "--reason", "the held-out file has 120 duplicate rows"]) == 0
    assert run(d1, "--", "true") == 0


def test_tuning_on_noise_stops_at_the_third_run_whatever_the_verdicts_or_wording(project, capsys):
    """The pilot ran about ten tuning rounds ending 'within noise'. Rewording or switching verdicts doesn't help."""
    decision = started(project, capsys)
    allowed, verdicts = 0, ["inconclusive", "no-change", "inconclusive", "no-change"]
    for attempt in range(10):
        if run(decision, "--", *printer("SUMMARY within noise")) != 0:
            break
        allowed += 1
        step.main(["verdict", last_run(project), verdicts[attempt % 4], "within noise"])
        decision = decide(capsys, f"ship prompt v2 or v3, take {attempt + 2}")
    assert allowed == 2
    assert "changed nothing" in capsys.readouterr().err
    assert run(decision, "--new-design", "1,000 held-out rows, not 100", "--", "true") == 0


# --- every run leaves a record ------------------------------------------------------------------

def test_two_runs_started_together_get_one_record_and_one_refusal(project, capsys):
    d1 = started(project, capsys)
    cmd = [sys.executable, STEP, "run", "--decision", d1, "--if", "x", "--", sys.executable, "-c",
           "import time; time.sleep(1)"]
    procs = [subprocess.Popen(cmd, cwd=project, stdout=subprocess.PIPE, stderr=subprocess.PIPE) for _ in range(2)]
    assert sorted(p.wait(timeout=30) for p in procs) == [0, 1]
    assert len(state(project)["runs"]) == 1


def test_no_verdict_while_the_run_is_still_going(project, capsys):
    d1 = started(project, capsys)
    proc = subprocess.Popen([sys.executable, STEP, "run", "--decision", d1, "--if", "x", "--", sys.executable,
                             "-c", "import time; time.sleep(3)"], cwd=project, stdout=subprocess.PIPE)
    for _ in range(50):
        if state(project)["runs"]:
            break
        subprocess.run([sys.executable, "-c", "import time; time.sleep(0.1)"])
    rid = last_run(project)
    assert step.main(["verdict", rid, "changed", "too early"]) == 1
    assert "still running" in capsys.readouterr().err
    proc.wait(timeout=30)
    assert step.main(["verdict", rid, "changed", "v3 wins by 4pp"]) == 0


def test_failed_killed_and_binary_runs_are_all_recorded(project, capsys):
    d1 = started(project, capsys)
    assert run(d1, "--", "no-such-command-xyz") == 1
    assert "did not launch" in capsys.readouterr().err
    assert run(d1, "--", "sh", "-c", "printf 'SUMMARY \\377 bytes\\n'; kill -9 $$") == 0
    assert "SUMMARY" in capsys.readouterr().out
    assert run(d1, "--", "true") == 1
    assert "has no verdict" in capsys.readouterr().err


def test_run_prints_the_summary_and_keeps_rows_out_of_context(project, capsys):
    d1 = started(project, capsys)
    capsys.readouterr()
    script = "for i in range(500): print(f'row {i}: query, label, confidence')\nprint('SUMMARY precision v3 0.81 vs v2 0.77')"
    assert run(d1, "--", sys.executable, "-c", script) == 0
    out = capsys.readouterr().out
    assert "SUMMARY precision v3 0.81 vs v2 0.77" in out and "row 1:" not in out and len(out) < 1500
    assert (project / ".ds-step" / "runs" / f"{last_run(project)}.log").read_text().count("row ") == 500


# --- the card, discovery, one step per session, the brief ---------------------------------------

def test_the_card_takes_real_values_and_refuses_bad_ones(project, capsys):
    assert step.main(CARD[:4] + ["CI half-width < 2pp on < 300 rows"] + CARD[5:]) == 0
    assert "Done when: CI half-width < 2pp on < 300 rows" in (project / "DS-STATE.md").read_text()
    assert step.main(CARD + [x for i in range(5) for x in ("--scope", f"task {i}")]) == 1
    assert step.main([*CARD[:-2], "--budget", "as long as it takes", "--freeze", "prompts"]) == 1
    err = capsys.readouterr().err
    assert "7 in-scope steps" in err and "time box" in err and "not a file" in err


def test_one_project_found_from_any_subfolder(project, monkeypatch, capsys):
    (project / "notebooks").mkdir()
    monkeypatch.chdir(project / "notebooks")
    assert step.main(["init", "--aim", "a", "--bar", "b"]) == 1
    assert "already exists" in capsys.readouterr().err
    assert step.main(["park", "secondary-intent boundary cases"]) == 0
    assert "secondary-intent" in (project / "DS-STATE.md").read_text()


def test_one_step_per_session_counting_the_session_that_ended_it(project, monkeypatch, capsys):
    monkeypatch.setenv("DS_SESSION_ID", "planner")
    started(project, capsys)
    monkeypatch.setenv("DS_SESSION_ID", "executor")
    assert step.main(["end", "compared v2 and v3"]) == 0
    assert step.main(["start"]) == 1
    assert "no card" in capsys.readouterr().err
    assert step.main(CARD) == 0 and step.main(["start"]) == 1
    assert "this session already ended a step" in capsys.readouterr().err
    monkeypatch.setenv("DS_SESSION_ID", "fresh")
    assert step.main(["start"]) == 0


def test_the_brief_stays_short_and_tool_first_on_a_busy_project(project, capsys):
    for i in range(20):
        decide(capsys, f"settled question {i} about the labeling rules", "--answer", f"answer {i} " * 6)
    for i in range(6):
        decide(capsys, f"open question {i}")
    for i in range(15):
        step.main(["park", f"parked idea number {i} with a long description of a side quest"])
    capsys.readouterr()
    assert step.main(["brief"]) == 0
    out = capsys.readouterr().out
    assert len(out) <= 2100 and out.startswith("Tool: python3 ") and "Parking lot: 15 idea(s)" in out
    assert "side quest" not in out and "settled question 19" in out and "older in DS-STATE.md" in out


def test_step_imports_without_fcntl_as_on_windows():
    code = f"import sys; sys.modules['fcntl'] = None; sys.path.insert(0, {TOOLS!r}); import step; print(step.fcntl)"
    assert subprocess.run([sys.executable, "-c", code], capture_output=True, text=True).stdout.strip() == "None"


# --- the hooks ----------------------------------------------------------------------------------

def hook(mode, payload, project_dir, env_file=None):
    env = {**os.environ, "CLAUDE_PROJECT_DIR": str(project_dir)}
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


def test_frozen_files_are_guarded_while_a_step_runs_even_from_a_parent_folder(project, capsys):
    target = project / "prompts" / "v3.md"
    notebook = {"tool_name": "NotebookEdit", "tool_input": {"notebook_path": str(target)}}
    assert hook("pre-tool-use", write(target), project.parent) is None
    started(project, capsys)
    assert denied(hook("pre-tool-use", write(target), project.parent))
    assert denied(hook("pre-tool-use", notebook, project))
    assert step.main(["end", "done"]) == 0
    assert hook("pre-tool-use", write(target), project) is None


def test_session_start_briefs_without_gating_discussion_and_stamps_the_session(project, tmp_path, capsys):
    decide(capsys, "which dataset?", "--answer", "held-out v3, 300 rows")
    env_file = tmp_path / "env"
    result = hook("session-start", {"source": "startup", "session_id": "abc", "cwd": str(project)}, project, env_file)
    context = result["hookSpecificOutput"]["additionalContext"]
    assert "Rank three search bets" in context and "which dataset? -> held-out v3" in context
    assert "Discussion, review and questions need nothing more" in context
    assert env_file.read_text() == "export DS_SESSION_ID=abc\n"
    (project / ".ds-step" / "events.jsonl").write_text("<<<<<<< HEAD\n")
    context = hook("session-start", {"source": "resume"}, project)["hookSpecificOutput"]["additionalContext"]
    assert "can't read its state" in context


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
    assert "fork" in config["SessionStart"][0]["matcher"]
