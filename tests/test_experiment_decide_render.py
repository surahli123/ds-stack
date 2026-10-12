"""decide.py makes the gold call on every synthetic case; render.py enforces the notes contract."""

import json
import os
import subprocess
import sys

import pytest

from conftest import ROOT

sys.path.insert(0, os.path.join(ROOT, "eval", "experiment"))
import pipeline_cases  # noqa: E402
import render  # noqa: E402

CASES = sorted(os.listdir(os.path.join(ROOT, "eval", "experiment", "cases")))


@pytest.fixture(autouse=True)
def quiet_log(monkeypatch, tmp_path):
    monkeypatch.setenv("DS_CHECKS_LOG", str(tmp_path / "log"))


@pytest.mark.parametrize("cid", CASES)
def test_decide_matches_gold(cid):
    ok, gold, decision, decider = pipeline_cases.compare(cid)
    assert ok, f"{cid}: gold {gold['call']}/{gold['decider']}, got {decision['call']}/{decider}: {decision['reason']}"


def test_every_call_has_at_least_two_cases():
    calls = [json.load(open(os.path.join(ROOT, "eval", "experiment", "gold", f"{c}.json")))["call"] for c in CASES]
    counts = {call: calls.count(call) for call in set(calls)}
    assert set(counts) == {"ship", "dont_ship", "escalate", "keep_running", "no_effect", "cant_tell", "not_ab"}
    assert min(counts.values()) >= 2 and len(CASES) >= 20


def _case(cid):
    directory = os.path.join(ROOT, "eval", "experiment", "cases", cid)
    request = json.load(open(os.path.join(directory, "request.json")))
    scorecard = pipeline_cases.adapters.statsig_pulse([json.load(open(os.path.join(directory, "pulse.json")))], request)
    return pipeline_cases.run_case(cid), scorecard


def test_notes_with_invented_numbers_stat_speak_or_call_words_are_rejected():
    decision, scorecard = _case("s1")
    notes = {"why_it_moved": [{"text": "Tail queries gained 4.7% because the new model reads intent better.", "label": "inferred"},
                              {"text": "The lift is statistically significant.", "label": "measured"},
                              {"text": "We should ship it.", "label": "guess"}],
             "would_change": ["A latency regression."]}
    problems = " | ".join(render.check_notes(notes, decision, scorecard))
    assert "4.7%" in problems and "stat-speak" in problems and "call word" in problems


def test_notes_with_scorecard_numbers_pass_and_caps_hold():
    decision, scorecard = _case("s1")
    good = {"why_it_moved": [{"text": "Successful searches rose 0.81% while latency stayed flat.", "label": "measured"}],
            "would_change": ["Abandonment rising past its 1.00% margin in a longer run."],
            "analyst_view": None}
    assert render.check_notes(good, decision, scorecard) == []
    too_many = {"why_it_moved": [{"text": "x", "label": "guess"}] * 4, "would_change": []}
    assert any("at most 3" in p for p in render.check_notes(too_many, decision, scorecard))
    same_call = {"why_it_moved": [], "would_change": [], "analyst_view": {"call": "ship", "reason": "agree"}}
    assert any("differ" in p for p in render.check_notes(same_call, decision, scorecard))


def test_render_puts_the_decider_first_and_writes_the_spine(tmp_path):
    decision, scorecard = _case("d3")
    (tmp_path / "decision.json").write_text(json.dumps(decision))
    (tmp_path / "scorecard.json").write_text(json.dumps(scorecard))
    proc = subprocess.run([sys.executable, os.path.join(ROOT, "skills", "ds-experiment", "tools", "render.py"),
                           "--decision", str(tmp_path / "decision.json"), "--scorecard", str(tmp_path / "scorecard.json")],
                          capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    text = (tmp_path / "readout.md").read_text()
    table = [line for line in text.splitlines() if line.startswith("| ") and "Metric |" not in line]
    assert text.splitlines()[0] == "# Ranker v7: Don't ship"
    assert table[0].startswith("| Abandonment Rate | guardrail")
    spine = json.loads((tmp_path / "spine.json").read_text())
    assert spine["answer"].startswith("Don't ship") and len(spine["takeaways"]) == 3
    lint = subprocess.run([sys.executable, os.path.join(ROOT, "skills", "doc-tighten", "tools", "doc_lint.py"),
                           str(tmp_path / "readout.md"), "--spine", str(tmp_path / "spine.json")], capture_output=True, text=True)
    assert lint.returncode == 0, lint.stdout


def test_bad_notes_stop_the_render(tmp_path):
    decision, scorecard = _case("s1")
    for name, content in (("decision.json", decision), ("scorecard.json", scorecard),
                          ("notes.json", {"why_it_moved": [{"text": "p < 0.01", "label": "measured"}], "would_change": []})):
        (tmp_path / name).write_text(json.dumps(content))
    proc = subprocess.run([sys.executable, os.path.join(ROOT, "skills", "ds-experiment", "tools", "render.py"),
                           "--decision", str(tmp_path / "decision.json"), "--scorecard", str(tmp_path / "scorecard.json"),
                           "--notes", str(tmp_path / "notes.json")], capture_output=True, text=True)
    assert proc.returncode == 1 and "stat-speak" in proc.stderr and not (tmp_path / "readout.md").exists()
