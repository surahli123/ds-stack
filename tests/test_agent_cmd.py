"""--agent-cmd / DS_AGENT_CMD: cold_read.py and run_arms.py can drive any headless agent, and grade.py
can score the runs that leave no transcript. A tiny fake agent (python3 -c ...) stands in for the model."""

import json
import os
import shlex
import sys

import cold_read
import grade
import pytest
import run_arms

READOUT = """Some work first.

## Answer
Headline: can't tell
The 50/50 split is really 51.2/48.8 on every day, so the lift is not trustworthy.

## Why we believe it
- Alternatives considered:
  - Sample ratio mismatch: ruled in by the srm check [measured]
- Checks run:
  - srm: fail 51.2/48.8 against a planned 50/50
"""
SPINE = {"type": "readout", "reader": "Dana, the PM",
         "answer": "Keep ranker v2: the 2.1 pp CTR drop is a mobile traffic mix shift.",
         "decision": "Do not roll back v2; ask growth to explain the mobile jump.",
         "takeaways": ["CTR fell 2.1 pp but did not move within desktop or mobile.",
                       "Mobile share of searches rose from 40% to 55%.",
                       "There is no holdout, so a small v2 effect would not show."]}
REPLY = ("1. Answer: keep v2, the 2.1 pp drop is a mobile traffic mix shift\n2. Decision: do not roll back; ask growth\n"
         "3. Number: mobile share rose from 40% to 55%; CTR did not move within desktop or mobile\n"
         "4. Caveat: no holdout, so a small v2 effect would not show\n5. Lost: nowhere\n6. Question: why did mobile grow?")

BOTH = pytest.mark.parametrize("tool", [cold_read, run_arms], ids=["cold_read", "run_arms"])


def fake_agent(code, *args):
    """A command template that runs a python one-liner, quoted the way a user would write it."""
    return shlex.join([sys.executable, "-c", code, *args])


# Echo whatever arrives on stdin, or the file named by the first argument, after a header with the model.
ECHO_STDIN = "import sys; print('model=' + sys.argv[1]); sys.stdout.write(sys.stdin.read())"
ECHO_FILE = "import sys; print('model=' + sys.argv[2]); sys.stdout.write(open(sys.argv[1]).read())"


# --- template expansion -------------------------------------------------------------------------------------

@BOTH
def test_template_with_prompt_file_fills_both_placeholders(tool):
    argv, on_stdin = tool.agent_argv("my-agent --file {prompt_file} --model {model} --quiet", "/tmp/p.txt", "auto")
    assert argv == ["my-agent", "--file", "/tmp/p.txt", "--model", "auto", "--quiet"]
    assert on_stdin is False


@BOTH
def test_template_without_prompt_file_sends_the_prompt_on_stdin(tool):
    argv, on_stdin = tool.agent_argv("my-agent -p --model {model}", "/tmp/p.txt", "auto")
    assert argv == ["my-agent", "-p", "--model", "auto"]
    assert on_stdin is True


@BOTH
def test_a_path_with_spaces_stays_one_argument_and_braces_elsewhere_are_left_alone(tool):
    argv, _ = tool.agent_argv("agent --json '{\"k\": 1}' {prompt_file}", "/tmp/a b/p.txt", "m")
    assert argv == ["agent", "--json", '{"k": 1}', "/tmp/a b/p.txt"]


@BOTH
def test_an_empty_template_is_refused(tool):
    with pytest.raises(ValueError):
        tool.agent_argv("   ", "/tmp/p.txt", "m")


# --- the default is still claude, with the same flags ---------------------------------------------------------

def test_default_cold_read_argv_is_unchanged():
    assert cold_read.claude_argv("PROMPT", "haiku") == [
        "claude", "-p", "PROMPT", "--model", "haiku", "--disallowedTools",
        "Bash,Read,Write,Edit,Glob,Grep,Task,Agent,WebFetch,WebSearch"]


def test_default_run_arms_argv_is_unchanged():
    assert run_arms.claude_argv("PROMPT", "sonnet") == [
        "claude", "-p", "PROMPT", "--model", "sonnet", "--output-format", "stream-json", "--verbose",
        "--allowedTools", "Bash,Read,Write,Edit,Glob,Grep", "--max-turns", "60"]


def test_cold_read_ask_without_agent_cmd_runs_claude(monkeypatch):
    seen = {}

    def fake_run(argv, **kwargs):
        seen["argv"], seen["kwargs"] = argv, kwargs
        return type("Proc", (), {"stdout": "reply", "stderr": "", "returncode": 0})()

    monkeypatch.setattr(cold_read.subprocess, "run", fake_run)
    assert cold_read.ask("PROMPT", "haiku") == "reply"
    assert seen["argv"] == cold_read.claude_argv("PROMPT", "haiku")
    assert "input" not in seen["kwargs"] and "stdin" not in seen["kwargs"]


# --- cold_read.py with a fake agent --------------------------------------------------------------------------

def test_cold_read_ask_feeds_stdin_when_the_template_has_no_prompt_file():
    reply = cold_read.ask("hello reader", "m1", fake_agent(ECHO_STDIN, "{model}"))
    assert reply == "model=m1\nhello reader"


def test_cold_read_ask_writes_the_prompt_file_when_the_template_names_it():
    reply = cold_read.ask("hello reader", "m1", fake_agent(ECHO_FILE, "{prompt_file}", "{model}"))
    assert reply == "model=m1\nhello reader"


def test_cold_read_main_runs_end_to_end_with_agent_cmd_flag_and_env(tmp_path, monkeypatch, capsys):
    doc, spine = tmp_path / "doc.md", tmp_path / "spine.json"
    doc.write_text("# Readout\n\n## Answer\nKeep ranker v2.\n")
    spine.write_text(json.dumps(SPINE))
    monkeypatch.setenv("PATH", "/nonexistent")  # no claude: only the custom command can answer
    canned = fake_agent("import sys; sys.stdin.read(); print(" + repr(REPLY) + ")")
    assert cold_read.main([str(doc), "--spine", str(spine), "--agent-cmd", canned]) == 0
    assert "cold-read: skim 2/2, full 3/3 - pass" in capsys.readouterr().out

    (tmp_path / "cold_read.json").unlink()
    from_file = fake_agent("import sys; open(sys.argv[1]).read(); print(" + repr(REPLY) + ")", "{prompt_file}")
    monkeypatch.setenv("DS_AGENT_CMD", from_file)
    assert cold_read.main([str(doc), "--spine", str(spine)]) == 0
    assert json.loads((tmp_path / "cold_read.json").read_text())["pass"]


def test_cold_read_main_reports_a_missing_agent_program(tmp_path, monkeypatch, capsys):
    doc, spine = tmp_path / "doc.md", tmp_path / "spine.json"
    doc.write_text("# Readout\n\nKeep ranker v2.\n")
    spine.write_text(json.dumps(SPINE))
    monkeypatch.delenv("DS_AGENT_CMD", raising=False)
    assert cold_read.main([str(doc), "--spine", str(spine), "--agent-cmd", "no-such-agent-xyz -p"]) == 2
    assert "no-such-agent-xyz" in capsys.readouterr().err


# --- run_arms.py: readout_format strips tag syntax -----------------------------------------------------------

TAGGED = """## Answer
Headline: <signed number> <unit> (<95% interval>) [q<n>]   or   Headline: can't tell
<one plain sentence: what happened and how big> [q<n> | check:<name>#<n>]

## Why we believe it
- Alternatives considered:
  - <alternative>: ruled <in|out> by <evidence> [measured|inferred|guess] [check:<name>#<n>]
  - [given] <the premise you were handed>
    [q<n>] indented tag at the start of a line
- Checks run:
  - <check>: <pass|flag|fail|could not run|skipped> <one-line result or reason> [q<n>|check:<name>#<n>|given]

## Provenance
- Metric: <definition>, from <metrics.json | stated here [guess]> [ given ]
"""
UNTAGGED = """## Answer
Headline: <signed number> <unit> (<95% interval>)   or   Headline: can't tell
<one plain sentence: what happened and how big>

## Why we believe it
- Alternatives considered:
  - <alternative>: ruled <in|out> by <evidence> [measured|inferred|guess]
  - <the premise you were handed>
    indented tag at the start of a line
- Checks run:
  - <check>: <pass|flag|fail|could not run|skipped> <one-line result or reason>

## Provenance
- Metric: <definition>, from <metrics.json | stated here [guess]>
"""


def test_strip_tag_placeholders_removes_tags_and_the_space_before_them():
    assert run_arms.strip_tag_placeholders(TAGGED) == UNTAGGED


def test_strip_tag_placeholders_leaves_an_untagged_block_alone():
    assert run_arms.strip_tag_placeholders(UNTAGGED) == UNTAGGED
    for keep in ("[measured|inferred|guess]", "[guess]", "[quality]", "[given name]", "[check]", "[x] done"):
        assert run_arms.strip_tag_placeholders(f"- a {keep} b") == f"- a {keep} b"


def test_readout_format_shows_every_arm_the_same_text_without_tags():
    text = run_arms.readout_format()
    assert text.startswith("## Answer") and "## Provenance" in text
    for tag in ("[q<n>", "[q1", "[check:", "[given]"):
        assert tag not in text


def test_the_prompt_never_mentions_tag_syntax_even_if_the_skill_does(tmp_path, monkeypatch):
    skill = tmp_path / "ds-mode"
    skill.mkdir()
    (skill / "SKILL.md").write_text("# s\n\n## Readout\n\n```\n" + TAGGED + "```\n\nMore prose with [q1].\n")
    monkeypatch.setattr(run_arms, "SKILL_DIR", str(skill))
    prompt = run_arms.build_prompt("f5")
    assert UNTAGGED in prompt and "check:<name>" not in prompt and "[given]" not in prompt


# --- run_arms.py: a full job with a fake agent ----------------------------------------------------------------

# Writes a check line and a query line the way the real tools would, then answers with a canned readout.
JOB_AGENT = (
    "import json, os, sys\n"
    "src = sys.argv[1]\n"
    "text = sys.stdin.read() if src == '-' else open(src).read()\n"
    "assert 'warehouse.db' in text\n"
    "open(os.environ['DS_CHECKS_LOG'], 'a').write(json.dumps({'check': 'srm', 'status': 'fail'}) + '\\n')\n"
    "open(os.environ['DS_QUERIES_LOG'], 'a').write(json.dumps({'cwd': os.getcwd(), 'log': os.environ['DS_QUERIES_LOG']}) + '\\n')\n"
    "sys.stdout.write(" + repr(READOUT) + ")\n"
)


@pytest.mark.parametrize("source", ["-", "{prompt_file}"], ids=["stdin", "prompt_file"])
def test_run_job_with_a_custom_agent_writes_result_logs_and_meta(tmp_path, monkeypatch, source):
    monkeypatch.setenv("DS_RUN_ROOT", str(tmp_path / "runs"))
    template = fake_agent(JOB_AGENT, source)
    out = tmp_path / "out"
    meta = run_arms.run_job(("f5", "baseline", 1), "auto", str(out), 120, agent_cmd=template)

    dest = out / "f5__baseline__1"
    assert (dest / "result.md").read_text() == READOUT
    assert not (dest / "transcript.jsonl").exists()
    saved = json.loads((dest / "meta.json").read_text())
    assert saved == meta
    assert saved["agent_cmd"] == template and saved["transcript"] is False and saved["exit"] == 0
    assert saved["cost_usd"] is None and saved["turns"] is None
    assert json.loads((dest / "checks.log").read_text()) == {"check": "srm", "status": "fail"}
    query = json.loads((dest / "queries.log").read_text())
    assert query["log"] == os.path.join(query["cwd"], ".ds-queries.log")
    assert not (tmp_path / "runs").exists() or not list((tmp_path / "runs").iterdir())  # job dir cleaned up


def test_run_job_records_a_failing_custom_agent_instead_of_crashing(tmp_path, monkeypatch):
    monkeypatch.setenv("DS_RUN_ROOT", str(tmp_path / "runs"))
    out = tmp_path / "out"
    meta = run_arms.run_job(("f5", "baseline", 1), "auto", str(out), 120,
                            agent_cmd=fake_agent("import sys; sys.exit(3)"))
    assert meta["exit"] == 3 and (out / "f5__baseline__1" / "result.md").read_text() == ""


def test_custom_agent_keeps_the_real_home_but_claude_gets_an_empty_one(tmp_path, monkeypatch):
    monkeypatch.setenv("DS_RUN_ROOT", str(tmp_path / "runs"))
    monkeypatch.setenv("HOME", "/real/home")
    out = tmp_path / "out"
    echo_home = fake_agent("import os, sys; sys.stdout.write(os.environ['HOME'])")
    run_arms.run_job(("f5", "baseline", 1), "auto", str(out), 120, agent_cmd=echo_home)
    assert (out / "f5__baseline__1" / "result.md").read_text() == "/real/home"


# --- grade.py --allow-no-transcript ---------------------------------------------------------------------------

def make_custom_run(root, arm, run, transcript_flag=False, text=READOUT):
    """The minimal results dir grade.py reads: meta.json, result.md, optional checks.log, no transcript."""
    run_dir = root / f"f5__{arm}__{run}"
    run_dir.mkdir()
    meta = {"fixture": "f5", "arm": arm, "run": run, "model": "auto", "exit": 0, "cost_usd": None, "turns": None,
            "agent_cmd": "my-agent"}
    if transcript_flag is not None:
        meta["transcript"] = transcript_flag
    (run_dir / "meta.json").write_text(json.dumps(meta))
    (run_dir / "result.md").write_text(text)
    (run_dir / "checks.log").write_text(json.dumps({"check": "srm", "status": "fail"}) + "\n")
    return run_dir


def test_without_the_flag_a_missing_transcript_still_fails_closed(tmp_path):
    make_custom_run(tmp_path, "full", 1)
    (run,) = grade.grade_dir(str(tmp_path))
    assert not run["correct"] and run["miss"] == "contaminated" and "no transcript" in run["reason"]
    assert run["skill_read"] is False and run["isolation"].startswith("no transcript")


def test_allow_no_transcript_grades_the_readout_and_reports_unverified(tmp_path):
    make_custom_run(tmp_path, "full", 1)
    make_custom_run(tmp_path, "baseline", 1)
    runs = grade.grade_dir(str(tmp_path), allow_no_transcript=True)
    assert all(r["correct"] and r["miss"] is None for r in runs)
    assert all(r["isolation"] == "unverified (custom agent)" == r["skill_read"] for r in runs)
    assert runs[0]["checks_ran"] == {"srm": ["fail"]}

    with open(os.path.join(grade.HERE, "pass_rule.json")) as handle:
        rule = json.load(handle)
    fixtures, arms, cells, per_arm, verdict = grade.summarize(runs, rule)
    for arm in ("baseline", "full"):
        assert per_arm[arm]["runs_unverified_isolation"] == 1
        assert per_arm[arm]["runs_contaminated"] == 0 and per_arm[arm]["runs_reading_skill"] == 0
    report = grade.render("x", runs, fixtures, arms, cells, per_arm, verdict)
    assert "unverified (custom agent)" in report and "runs_unverified_isolation" in report


def test_allow_no_transcript_does_not_excuse_a_claude_run_that_lost_its_transcript(tmp_path):
    make_custom_run(tmp_path, "full", 1, transcript_flag=None)
    make_custom_run(tmp_path, "baseline", 1, transcript_flag=True)
    runs = grade.grade_dir(str(tmp_path), allow_no_transcript=True)
    assert all(r["miss"] == "contaminated" and r["isolation"] != "unverified (custom agent)" for r in runs)


def test_normal_runs_report_zero_unverified_and_keep_their_columns(tmp_path):
    run_dir = make_custom_run(tmp_path, "full", 1, transcript_flag=None)
    (run_dir / "transcript.jsonl").write_text('{"type": "result"}')
    runs = grade.grade_dir(str(tmp_path), allow_no_transcript=True)
    assert runs[0]["correct"] and runs[0]["isolation"] == "ok"
    with open(os.path.join(grade.HERE, "pass_rule.json")) as handle:
        rule = json.load(handle)
    fixtures, arms, cells, per_arm, verdict = grade.summarize(runs, rule)
    assert per_arm["full"]["runs_unverified_isolation"] == 0
    assert "Isolation" not in grade.render("x", runs, fixtures, arms, cells, per_arm, verdict)


def test_grade_cli_flag_end_to_end_from_a_run_arms_job(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("DS_RUN_ROOT", str(tmp_path / "runs"))
    results = tmp_path / "results"
    run_arms.run_job(("f5", "full", 1), "auto", str(results), 120, agent_cmd=fake_agent(JOB_AGENT, "-"))
    assert grade.main([str(results)]) == 0
    assert json.loads((results / "summary.json").read_text())["runs"][0]["miss"] == "contaminated"
    assert grade.main([str(results), "--allow-no-transcript"]) == 0
    summary = json.loads((results / "summary.json").read_text())
    assert summary["per_arm"]["full"]["runs_unverified_isolation"] == 1
    assert summary["runs"][0]["correct"] and summary["runs"][0]["skill_read"] == "unverified (custom agent)"
    assert "unverified (custom agent)" in (results / "summary.md").read_text()
    assert grade.main([]) == 3
    capsys.readouterr()


@pytest.mark.parametrize("arm, note", [("checks", run_arms.CHECKS_ONLY_NOTE), ("full", run_arms.FULL_NOTE)])
def test_the_arm_note_is_written_for_claude_codex_and_cursor(tmp_path, arm, note):
    work = run_arms.prepare_workdir(str(tmp_path), "f1", arm)
    for name in ("CLAUDE.md", "AGENTS.md"):
        assert open(os.path.join(work, name)).read() == note


def test_the_baseline_arm_gets_no_note(tmp_path):
    work = run_arms.prepare_workdir(str(tmp_path), "f1", "baseline")
    assert not any(os.path.exists(os.path.join(work, name)) for name in ("CLAUDE.md", "AGENTS.md"))
