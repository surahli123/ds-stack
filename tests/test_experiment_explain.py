"""explain.py finds the mechanism behind co-movements, splits ratios and segments, and judges triage readiness."""

import json
import os
import subprocess
import sys

import pytest

from conftest import ROOT

sys.path.insert(0, os.path.join(ROOT, "eval", "experiment"))
import adapters  # noqa: E402
import decide  # noqa: E402
import explain  # noqa: E402
import make_cases as mc  # noqa: E402
import pipeline_cases  # noqa: E402
import random  # noqa: E402

LIB = explain.load_library(None)


@pytest.fixture(autouse=True)
def quiet_log(monkeypatch, tmp_path):
    monkeypatch.setenv("DS_CHECKS_LOG", str(tmp_path / "log"))


def run(overrides, prereg=None, segments=None, seed=7, daily=None):
    pulse = mc.scorecard(random.Random(seed), {**mc.GUARDS, **overrides})
    scorecard = adapters.statsig_pulse([pulse], {"control": "g_control", "test": "g_test", "cuped": "false", "confidence": "95"})
    config = adapters.statsig_config(mc.experiment("Ranker v7"))
    pre = prereg or mc.prereg()
    pre.setdefault("hypothesis", "The new ranker raises the share of searches that end in a successful click.")
    decision = decide.decide(scorecard, pre, config, None, daily)
    return decision, explain.explain(decision, scorecard, pre, LIB, segments)


def test_volume_primary_with_retries_is_not_ready_and_names_the_separating_cut():
    case = os.path.join(ROOT, "eval", "experiment", "cases", "e6")
    pre = json.load(open(os.path.join(case, "prereg.json")))
    pre["hypothesis"] = "More queries per user means users engage more with search."
    decision = pipeline_cases.run_case("e6")
    scorecard = adapters.statsig_pulse([json.load(open(os.path.join(case, "pulse.json")))],
                                       json.load(open(os.path.join(case, "request.json"))))
    result = explain.explain(decision, scorecard, pre, LIB)
    assert result["readiness"]["verdict"] == "not_ready"
    assert result["readiness"]["first"]["cut"] == "success per query vs per user"
    first = result["questions"][0]
    assert first["metric"] == "Queries per User" and first["candidates"][0] == "struggling_users"


def test_ctr_up_because_searches_fell_is_measured_as_denominator_driven():
    _, result = run({**mc.WIN, "CTR": {"rel": 0.021, "half": 0.005}, "Clicks per User": {"rel": 0.001, "half": 0.008},
                     "Queries per User": {"rel": -0.019, "half": 0.008}})
    ratio = [p for p in result["patterns"] if p["id"] == "denominator_driven"]
    assert ratio and ratio[0]["label"] == "measured" and "Queries per User" in ratio[0]["mechanism"]


def test_clicks_without_long_clicks_reads_as_attractiveness_and_rules_out_relevance():
    _, result = run({"Successful Search Rate": {"rel": 0.0, "half": 0.004}, "CTR": {"rel": 0.024, "half": 0.005},
                     "Long Click Rate": {"rel": -0.001, "half": 0.006}})
    ids = [p["id"] for p in result["patterns"]]
    assert "attractive_not_relevant" in ids and "relevance_gain" not in ids


def test_abandonment_up_with_ctr_up_is_not_good_abandonment():
    _, result = run({"Successful Search Rate": {"rel": 0.0124}, "Abandonment Rate": {"rel": 0.022, "half": 0.007},
                     "CTR": {"rel": 0.019}})
    assert "good_abandonment" in [p["id"] for p in result["ruled_out"]]
    assert "mixed_wins_losses" in [p["id"] for p in result["patterns"]]


def test_measured_segment_cut_from_a_deep_dive_names_the_segment():
    segments = {"Successful Search Rate": {"by": "query class", "parts": [
        {"segment": "Head", "rel_delta": 0.0004, "rel_ci": [-0.003, 0.004], "weight": 0.6},
        {"segment": "Torso", "rel_delta": 0.003, "rel_ci": [-0.004, 0.010], "weight": 0.25},
        {"segment": "Tail", "rel_delta": 0.031, "rel_ci": [0.021, 0.041], "weight": 0.15}]}}
    _, result = run({"Successful Search Rate": {"rel": 0.005, "half": 0.003}}, segments=segments)
    seg = [p for p in result["patterns"] if p["id"] == "concentrated_segment" and p.get("dimension") == "query class"]
    assert seg and seg[0]["segment"] == "Tail" and seg[0]["label"] == "measured"


def test_clean_win_is_ready_only_once_durability_is_known_and_a_broken_test_is_not():
    _, unknown = run(mc.WIN)
    assert unknown["readiness"]["verdict"] == "open_questions" and "durability" in unknown["readiness"]["reasons"][0]
    _, result = run(mc.WIN, daily=mc.daily([0.0081, 0.0079, 0.0083, 0.0080, 0.0082, 0.0080, 0.0081, 0.0079]))
    assert result["readiness"]["verdict"] == "ready"
    assert [q["question"] for q in result["standard"]][:3] == ["Is the data trustworthy?", "Is the effect real, or chance?",
                                                               "Will it last?"]
    assert result["chance"]["tested"] >= 50 and result["chance"]["expected_by_chance"] > 2
    decision = pipeline_cases.run_case("c1")
    case = os.path.join(ROOT, "eval", "experiment", "cases", "c1")
    scorecard = adapters.statsig_pulse([json.load(open(os.path.join(case, "pulse.json")))],
                                       json.load(open(os.path.join(case, "request.json"))))
    broken = explain.explain(decision, scorecard, json.load(open(os.path.join(case, "prereg.json"))), LIB)
    assert broken["readiness"]["verdict"] == "not_ready" and broken["readiness"]["first"]


def test_triage_prep_renders_lint_clean(tmp_path):
    decision, result = run({"Queries per User": {"rel": 0.024}, "Reformulation Rate": {"rel": 0.051, "half": 0.008}})
    scorecard_path, decision_path, explain_path = tmp_path / "s.json", tmp_path / "d.json", tmp_path / "e.json"
    pulse = mc.scorecard(random.Random(7), {**mc.GUARDS, "Queries per User": {"rel": 0.024},
                                            "Reformulation Rate": {"rel": 0.051, "half": 0.008}})
    scorecard_path.write_text(json.dumps(adapters.statsig_pulse([pulse], {"control": "g_control", "test": "g_test", "cuped": "false", "confidence": "95"})))
    decision_path.write_text(json.dumps(decision))
    explain_path.write_text(json.dumps(result))
    tools = os.path.join(ROOT, "skills", "ds-experiment", "tools")
    proc = subprocess.run([sys.executable, os.path.join(tools, "render.py"), "--decision", str(decision_path),
                           "--scorecard", str(scorecard_path), "--explain", str(explain_path)], capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    prep = (tmp_path / "triage_prep.md").read_text()
    assert "## Questions triage will ask" in prep and "## Cuts to run before triage, in order" in prep
    assert "Triage: " in (tmp_path / "readout.md").read_text()
    lint = subprocess.run([sys.executable, os.path.join(ROOT, "skills", "doc-tighten", "tools", "doc_lint.py"),
                           str(tmp_path / "triage_prep.md"), "--type", "reference"], capture_output=True, text=True)
    assert lint.returncode == 0, lint.stdout


MECHANISMS = sorted(os.listdir(os.path.join(ROOT, "eval", "experiment", "mechanisms")))


@pytest.mark.parametrize("cid", MECHANISMS)
def test_mechanism_case_matches_gold(cid):
    import mechanism_check
    ok, gold, top, result = mechanism_check.compare(cid)
    assert ok, f"{cid}: gold {gold['mechanism']}/{gold['readiness']}, got {top}/{result['readiness']['verdict']}"
