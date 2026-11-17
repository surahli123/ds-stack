"""ds-step keeps a long project on its aim: the card, the run gate and the hooks refuse the moves that caused drift.

The scenarios replay the failure modes from the 2026-11-09 to 11-17 intent-labeling pilot retro
(docs/drift-research.md): tuning on noise, rewriting instructions mid-run, reopening settled questions,
and reading row-level output into context.
"""

import json
import os
import subprocess
import sys

import pytest
from conftest import ROOT

TOOLS = os.path.join(ROOT, "skills", "ds-step", "tools")
HOOK = os.path.join(ROOT, "hooks", "ds_step_hook.py")
sys.path.insert(0, TOOLS)
import step  # noqa: E402

CARD = """## Step
Aim: compare prompt v2 and v3 on the held-out set
Done when: a verdict on v2 vs v3 is in the Log
In scope:
1. run both prompts on the 300 held-out rows
2. record the verdict
Out of scope: boundary cases of fields the success bar does not use
Budget: 60m
Stop and ask: the held-out set has fewer than 300 rows

## Frozen
- prompts/v3.md

"""


@pytest.fixture
def project(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("DS_STATE", raising=False)
    monkeypatch.delenv("CLAUDE_PROJECT_DIR", raising=False)
    assert step.main(["init", "--aim", "Rank three search bets", "--bar", "Precision on 300 held-out rows"]) == 0
    return tmp_path


def fill_card(path, card=CARD):
    text = (path / "DS-STATE.md").read_text()
    start, end = text.index("## Step"), text.index("## Closed")
    (path / "DS-STATE.md").write_text(text[:start] + card + text[end:])


def gate(*args):
    return step.main(["run", "--decision", "ship prompt v2 or v3", "--if", "v3 >= 2pp better -> ship v3", *args])


# --- the task card ------------------------------------------------------------------------------

def test_start_refuses_a_card_with_placeholders(project, capsys):
    assert step.main(["start"]) == 1
    err = capsys.readouterr().err
    assert "Done when is not filled in" in err and "Budget is not filled in" in err


def test_start_refuses_more_than_five_in_scope_steps_and_a_budget_that_is_not_a_time_box(project, capsys):
    many = CARD.replace("2. record the verdict", "\n".join(f"{i}. task {i}" for i in range(2, 8)))
    fill_card(project, many.replace("Budget: 60m", "Budget: as long as it takes"))
    assert step.main(["start"]) == 1
    err = capsys.readouterr().err
    assert "7 in-scope steps; at most 5" in err and "time box" in err


def test_one_step_per_session(project, capsys):
    fill_card(project)
    assert step.main(["start"]) == 0
    assert "Aim: Rank three search bets" in capsys.readouterr().out
    assert step.main(["start"]) == 1
    assert "One step per session" in capsys.readouterr().err
    assert step.main(["start", "--resume"]) == 0
    assert step.main(["end", "compared v2 and v3"]) == 0
    assert "ended after 0 min: compared v2 and v3" in (project / "DS-STATE.md").read_text()


# --- the run gate -------------------------------------------------------------------------------

def test_no_run_without_a_started_step_or_a_named_decision(project, capsys):
    assert gate("--", "true") == 1
    assert "no step is started" in capsys.readouterr().err
    fill_card(project)
    step.main(["start"])
    assert step.main(["run", "--", "true"]) == 1
    assert "don't run it" in capsys.readouterr().err


def test_tuning_on_noise_stops_at_the_third_run(project, capsys):
    """The pilot ran about ten tuning rounds that each ended 'within noise'. The gate allows two."""
    fill_card(project)
    step.main(["start"])
    allowed = 0
    for attempt in range(10):
        if gate("--", sys.executable, "-c", "print('SUMMARY v3-v2 +0.4pp, 95% CI +-3pp')") != 0:
            break
        allowed += 1
        step.main(["verdict", f"R{attempt + 1}", "inconclusive", "within noise, can't choose"])
    assert allowed == 2
    assert "noise is larger than the effect" in capsys.readouterr().err
    assert gate("--new-design", "1,000 held-out rows instead of 100", "--", "true") == 0


def test_the_next_run_waits_for_a_verdict_and_a_step_cannot_end_without_one(project, capsys):
    fill_card(project)
    step.main(["start"])
    assert gate("--", "true") == 0
    assert gate("--", "true") == 1
    assert "R1 has no verdict" in capsys.readouterr().err
    assert step.main(["end", "done"]) == 1
    assert step.main(["verdict", "R1", "changed", "v3 wins by 4pp"]) == 0
    assert step.main(["verdict", "R1", "no-change", "rewrite history"]) == 1


def test_run_prints_the_summary_and_keeps_rows_out_of_context(project, capsys):
    fill_card(project)
    step.main(["start"])
    script = "for i in range(500): print(f'row {i}: query text, label, confidence')\nprint('SUMMARY precision v3 0.81 vs v2 0.77')"
    assert gate("--", sys.executable, "-c", script) == 0
    out = capsys.readouterr().out
    assert "SUMMARY precision v3 0.81 vs v2 0.77" in out and "row 1:" not in out and len(out) < 1000
    assert (project / ".ds-runs" / "R1.log").read_text().count("row ") == 500
    rows = step.ledger_rows()
    assert rows[0]["decision"] == "ship prompt v2 or v3" and rows[0]["verdict"] == ""


# --- closed questions and the parking lot -------------------------------------------------------

def test_close_park_and_reopen_leave_a_trail(project, capsys):
    assert step.main(["close", "Which dataset?", "held-out v3, 300 rows", "--evidence", "data/README.md"]) == 0
    assert step.main(["park", "boundary cases of the secondary-intent field"]) == 0
    text = (project / "DS-STATE.md").read_text()
    assert "- C1: Which dataset? -> held-out v3, 300 rows" in text and "secondary-intent" in text
    assert "## Closed\n- C1:" in text
    assert step.main(["reopen", "C1", "--reason", "the held-out file has 120 duplicate rows"]) == 0
    text = (project / "DS-STATE.md").read_text()
    assert "- C1:" not in step.sections(text)["Closed"] and "because: the held-out file has 120" in text


# --- the hooks ----------------------------------------------------------------------------------

def hook(mode, payload, project):
    env = {**os.environ, "CLAUDE_PROJECT_DIR": str(project)}
    env.pop("DS_STATE", None)
    proc = subprocess.run([sys.executable, HOOK, mode], input=json.dumps(payload), capture_output=True,
                          text=True, env=env, timeout=30)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout) if proc.stdout.strip() else None


def denied(result):
    return result and result["hookSpecificOutput"]["permissionDecision"] == "deny"


def test_the_hooks_do_nothing_without_a_state_file(tmp_path):
    assert hook("session-start", {"source": "startup"}, tmp_path) is None
    edit = {"tool_name": "Write", "tool_input": {"file_path": str(tmp_path / "x.md"), "content": ""}}
    assert hook("pre-tool-use", edit, tmp_path) is None


def test_session_start_puts_the_brief_in_context(project):
    step.main(["close", "Which dataset?", "held-out v3, 300 rows"])
    context = hook("session-start", {"source": "startup"}, project)["hookSpecificOutput"]["additionalContext"]
    assert "Rank three search bets" in context and "C1: Which dataset?" in context
    assert "No step is running" in context and len(context) < 3000
    fill_card(project)
    step.main(["start"])
    context = hook("session-start", {"source": "startup"}, project)["hookSpecificOutput"]["additionalContext"]
    assert "still open" in context and "compare prompt v2 and v3" in context


def test_an_edit_that_changes_a_closed_answer_is_blocked(project):
    step.main(["close", "Which dataset?", "held-out v3, 300 rows"])
    state = str(project / "DS-STATE.md")
    text = (project / "DS-STATE.md").read_text()
    edit = {"tool_name": "Edit", "cwd": str(project),
            "tool_input": {"file_path": state, "old_string": "held-out v3, 300 rows", "new_string": "the 100 invented rows"}}
    result = hook("pre-tool-use", edit, project)
    assert denied(result) and "step.py reopen" in result["hookSpecificOutput"]["permissionDecisionReason"]
    rewrite = {"tool_name": "Write", "tool_input": {"file_path": state, "content": text.replace("- C1:", "- C9:")}}
    assert denied(hook("pre-tool-use", rewrite, project))
    park = {"tool_name": "Edit", "tool_input": {"file_path": state, "old_string": "## Parking lot\n",
                                                 "new_string": "## Parking lot\n- an idea\n"}}
    assert hook("pre-tool-use", park, project) is None


def test_instructions_are_frozen_while_a_step_runs_and_free_between_steps(project):
    fill_card(project)
    state = str(project / "DS-STATE.md")
    card_edit = {"tool_name": "Edit", "tool_input": {"file_path": state, "old_string": "Budget: 60m",
                                                      "new_string": "Budget: 240m"}}
    prompt_edit = {"tool_name": "Write", "tool_input": {"file_path": str(project / "prompts" / "v3.md"), "content": "x"}}
    sed = {"tool_name": "Bash", "tool_input": {"command": "sed -i 's/a/b/' prompts/v3.md"}}
    assert hook("pre-tool-use", card_edit, project) is None
    assert hook("pre-tool-use", prompt_edit, project) is None
    step.main(["start"])
    assert denied(hook("pre-tool-use", card_edit, project))
    assert denied(hook("pre-tool-use", prompt_edit, project))
    assert denied(hook("pre-tool-use", sed, project))
    read_only = {"tool_name": "Bash", "tool_input": {"command": "wc -l prompts/v3.md"}}
    via_tool = {"tool_name": "Bash", "tool_input": {"command": "python3 step.py park 'try v4' > /dev/null"}}
    assert hook("pre-tool-use", read_only, project) is None
    assert hook("pre-tool-use", via_tool, project) is None
    step.main(["end", "done"])
    assert hook("pre-tool-use", prompt_edit, project) is None


def test_a_broken_payload_never_blocks_the_agent(project):
    env = {**os.environ, "CLAUDE_PROJECT_DIR": str(project)}
    proc = subprocess.run([sys.executable, HOOK, "pre-tool-use"], input="not json", capture_output=True, text=True, env=env)
    assert proc.returncode == 0 and proc.stdout == "" and "allowing" in proc.stderr


def test_the_plugin_registers_both_hooks_on_the_shipped_script():
    with open(os.path.join(ROOT, "hooks", "hooks.json")) as handle:
        config = json.load(handle)["hooks"]
    commands = [h["command"] for event in ("SessionStart", "PreToolUse") for m in config[event] for h in m["hooks"]]
    assert all("${CLAUDE_PLUGIN_ROOT}/hooks/ds_step_hook.py" in c for c in commands)
    assert set(config["PreToolUse"][0]["matcher"].split("|")) == {"Write", "Edit", "MultiEdit", "Bash"}
