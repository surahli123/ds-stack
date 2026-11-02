"""ds-retro finds the mistakes that repeat across runs and proposes where each fix belongs; it changes nothing."""

import json
import os
import re
import shutil
import sys

from conftest import ROOT

sys.path.insert(0, os.path.join(ROOT, "skills", "ds-retro", "tools"))
import retro  # noqa: E402

RESULTS = os.path.join(ROOT, "eval", "results")
FIXTURES = os.path.join(ROOT, "eval", "fixtures")


def analysis(tmp_path, name, run, fixture, headline_unit=None):
    """A finished analysis folder copied from an eval run, with its request and database."""
    folder = tmp_path / name
    folder.mkdir()
    source = os.path.join(RESULTS, run)
    text = open(os.path.join(source, "result.md"), encoding="utf-8").read()
    if headline_unit:
        text = re.sub(r"Headline: \+?50\.05 (?:%|percent)", f"Headline: +50.05 {headline_unit}", text)
    (folder / "readout.md").write_text(text, encoding="utf-8")
    shutil.copy(os.path.join(source, "queries.log"), folder / ".ds-queries.log")
    shutil.copy(os.path.join(source, "checks.log"), folder / ".ds-checks.log")
    shutil.copy(os.path.join(FIXTURES, fixture, "task.md"), folder / "request.md")
    shutil.copy(os.path.join(FIXTURES, fixture, "warehouse.db"), folder / "warehouse.db")
    return str(folder)


def run(tmp_path, *args):
    out = tmp_path / "out"
    code = retro.main([*args, "--out", str(out), "--json", str(tmp_path / "r.json")])
    return code, json.loads((tmp_path / "r.json").read_text()), out


def test_a_mistake_in_two_analyses_becomes_a_proposal(tmp_path, monkeypatch):
    monkeypatch.setenv("DS_OVERLAY_DIR", os.path.join(FIXTURES, "f6", "overlay"))
    folders = [analysis(tmp_path, f"a{i}", f"2026-10-14-claude-en/f6__full__{i}", "f6", headline_unit="pp") for i in (1, 3)]
    code, report, out = run(tmp_path, "--analyses", *folders)
    unit = [p for p in report["proposals"] if p["pattern"].startswith("estimand: the request asks for percent")]
    assert code == 1 and unit and unit[0]["runs"] == 2
    assert unit[0]["layer"] == "ds-mode skill" and "unit the request asks for" in unit[0]["proposal"]
    text = (out / "proposals.md").read_text()
    assert "Fixture for the eval gate" in text and (out / ".gitignore").read_text().endswith("*\n")


def test_a_mistake_in_one_analysis_is_not_proposed(tmp_path, monkeypatch):
    monkeypatch.setenv("DS_OVERLAY_DIR", os.path.join(FIXTURES, "f6", "overlay"))
    folders = [analysis(tmp_path, "a1", "2026-10-14-claude-en/f6__full__1", "f6", headline_unit="pp"),
               analysis(tmp_path, "a2", "2026-10-14-claude-en/f6__full__3", "f6")]
    _, report, _ = run(tmp_path, "--analyses", *folders)
    assert not any(p["pattern"].startswith("estimand: the request asks for percent") for p in report["proposals"])
    assert any(k.startswith("estimand: the request asks for percent") and n == 1 for k, n in report["counts"].items())


def test_eval_runs_add_the_graders_reasons_and_say_whether_ds_verify_caught_them():
    code, report, _ = run_in_tmp("--results", os.path.join(RESULTS, "2026-10-14-teeth-no-overlay-step"))
    graded = [p for p in report["proposals"] if p["pattern"].startswith("grade: headline # outside")]
    assert graded and graded[0]["runs"] == 3 and graded[0]["caught"] == 3


def run_in_tmp(*args):
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        from pathlib import Path
        return run(Path(tmp), *args)


def test_a_broken_existing_rule_becomes_a_gate_not_more_text():
    _, report, _ = run_in_tmp("--results", os.path.join(RESULTS, "2026-10-14-claude-en"), os.path.join(RESULTS, "2026-10-14-estimand"))
    pasted = [p for p in report["proposals"] if p["pattern"].startswith("replay: [q#] is a pasted result")]
    assert pasted and pasted[0]["covered"] is True


def test_patterns_drop_the_quoted_line_and_the_metric_name():
    a = retro.normalize("overlay: the overlay defines ctr as a / b with filters []; the Metric line lacks b: - Metric: x")
    b = retro.normalize("overlay: the overlay defines zrr as c / d with filters ['x']; the Metric line lacks d, e: - Metric: y")
    assert a == b == "overlay: the overlay defines <metric>; the metric line lacks <columns>"
    hedged = retro.normalize("alternatives: 'ruled in' is hedged and no flagged check backs it: an alternative that wasn't "
                             "ruled out is not ruled in. Say what would decide it: - v2: ruled in as possible [q1]")
    assert hedged == "alternatives: 'ruled in' is hedged without a flagged check"
    assert retro.normalize("replay: [q12] is a pasted result") == retro.normalize("replay: [q4] is a pasted result")


def test_unknown_patterns_go_to_a_person():
    assert retro.lesson_for("something new: never seen")["layer"] == "a person decides"


def test_it_changes_nothing_outside_its_output(tmp_path, monkeypatch):
    monkeypatch.setenv("DS_OVERLAY_DIR", os.path.join(FIXTURES, "f6", "overlay"))
    folder = analysis(tmp_path, "a1", "2026-10-14-claude-en/f6__full__1", "f6")
    before = {name: open(os.path.join(folder, name), "rb").read() for name in os.listdir(folder)}
    skill = open(retro.DS_MODE_SKILL, "rb").read()
    run(tmp_path, "--analyses", folder)
    assert {name: open(os.path.join(folder, name), "rb").read() for name in os.listdir(folder)} == before
    assert open(retro.DS_MODE_SKILL, "rb").read() == skill


def test_usage_errors(tmp_path):
    assert retro.main([]) == 3
    assert retro.main(["--analyses", str(tmp_path / "nope")]) == 3
