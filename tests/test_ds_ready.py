"""ds-ready audits a work project for what ds-stack needs and writes questions for the metric owners."""

import hashlib
import json
import os
import shutil
import sys

import pytest
from conftest import ROOT

sys.path.insert(0, os.path.join(ROOT, "skills", "ds-ready", "tools"))
import audit  # noqa: E402

FIXTURES = os.path.join(ROOT, "eval", "fixtures")
RESULTS = os.path.join(ROOT, "eval", "results")
CTR = json.load(open(os.path.join(FIXTURES, "f6", "overlay", "metrics.json")))["ctr"]


def overlay(tmp_path, metrics=None, extra=("runner.json", "reviewers.json", "denylist.txt", "tables.json")):
    folder = tmp_path / "overlay"
    folder.mkdir()
    (folder / "metrics.json").write_text(json.dumps(metrics if metrics is not None else {"ctr": {**CTR, "aliases": ["点击率"]}}))
    for name in extra:
        src = os.path.join(ROOT, "overlay.example", name)
        shutil.copy(src, folder / name) if os.path.exists(src) else (folder / name).write_text("internal_codename\n")
    return folder


def project(tmp_path, agents=True, runs=()):
    folder = tmp_path / "project"
    folder.mkdir()
    if agents:
        (folder / "AGENTS.md").write_text(f"For any data analysis request, read and follow {ROOT}/skills/ds-mode/SKILL.md\n"
                                          f"To check a finished readout, read and follow {ROOT}/skills/ds-verify/SKILL.md\n")
    for i, run in enumerate(runs, 1):
        dest = folder / f"analysis-{i}"
        dest.mkdir()
        shutil.copy(os.path.join(RESULTS, run, "result.md"), dest / "readout.md")
        if os.path.exists(os.path.join(RESULTS, run, "queries.log")):
            shutil.copy(os.path.join(RESULTS, run, "queries.log"), dest / ".ds-queries.log")
    return folder


def audit_of(tmp_path, ov, proj, db=None):
    out = tmp_path / "ds-ready"
    args = ["--project", str(proj), "--out", str(out), "--json", str(tmp_path / "r.json")]
    args += ["--overlay", str(ov)] if ov else []
    args += ["--db", db] if db else []
    code = audit.main(args)
    return code, json.loads((tmp_path / "r.json").read_text()), out


def messages(report, severity=None):
    return [g["message"] for g in report["gaps"] if severity in (None, g["severity"])]


def test_a_complete_project_is_ready(tmp_path, monkeypatch):
    monkeypatch.delenv("DS_OVERLAY_DIR", raising=False)
    ov = overlay(tmp_path)
    tables = json.loads((ov / "tables.json").read_text())
    tables["search_daily_v"] = tables.pop("search_daily")
    (ov / "tables.json").write_text(json.dumps(tables))
    proj = project(tmp_path, runs=["2026-10-14-claude-en/f6__full__1"])
    code, report, _ = audit_of(tmp_path, ov, proj, os.path.join(FIXTURES, "f6", "warehouse.db"))
    assert code == 0 and messages(report, "blocking") == []
    assert report["usage"]["readouts"] == 1 and report["usage"]["query_logs"] == 1


def test_no_overlay_is_blocking(tmp_path, monkeypatch):
    monkeypatch.delenv("DS_OVERLAY_DIR", raising=False)
    code, report, _ = audit_of(tmp_path, None, project(tmp_path))
    assert code == 1 and "DS_OVERLAY_DIR isn't set" in messages(report, "blocking")[0]


@pytest.mark.parametrize("metrics, words", [
    ({"ctr": {"numerator": "clicks"}}, "ctr lacks denominator, filters, grain, source, owner"),
    ({"spr": {"available": False}}, "spr is marked unavailable without note, owner"),
    ({}, "metrics.json defines no metric"),
])
def test_incomplete_definitions_are_blocking(tmp_path, metrics, words):
    code, report, _ = audit_of(tmp_path, overlay(tmp_path, metrics), project(tmp_path))
    assert code == 1 and any(words in m for m in messages(report, "blocking"))


def test_a_prose_numerator_is_a_recommendation(tmp_path):
    metrics = {"ctr": {**CTR, "numerator": "clicks on results", "aliases": ["x"]}}
    _, report, _ = audit_of(tmp_path, overlay(tmp_path, metrics), project(tmp_path))
    assert any("reads like prose" in m for m in messages(report, "recommended"))


def test_sources_are_checked_against_the_database(tmp_path):
    db = os.path.join(FIXTURES, "f6", "warehouse.db")
    metrics = {"ctr": {**CTR, "denominator": "searches_with_result"}, "old": {**CTR, "source": "search_daily_old"}}
    code, report, _ = audit_of(tmp_path, overlay(tmp_path, metrics), project(tmp_path), db)
    blocking = messages(report, "blocking")
    assert code == 1
    assert any("searches_with_result isn't a column of search_daily_v" in m for m in blocking)
    assert any("search_daily_old isn't in the database" in m for m in blocking)


def test_agents_md_must_load_ds_mode(tmp_path):
    code, report, _ = audit_of(tmp_path, overlay(tmp_path), project(tmp_path, agents=False))
    assert code == 1 and any("no AGENTS.md" in m for m in messages(report, "blocking"))
    proj = tmp_path / "project"
    (proj / "AGENTS.md").write_text("For any data analysis request, read and follow /nowhere/ds-mode/SKILL.md\n")
    _, report, _ = audit_of(tmp_path, tmp_path / "overlay", proj)
    assert any("/nowhere/ds-mode/SKILL.md, which doesn't exist" in m for m in messages(report, "blocking"))
    assert any("doesn't point to ds-verify" in m for m in messages(report, "recommended"))


def test_tables_used_without_notes_get_questions(tmp_path):
    ov = overlay(tmp_path, extra=("runner.json", "reviewers.json", "denylist.txt"))
    proj = project(tmp_path, runs=["2026-10-14-claude-en/f6__full__1"])
    _, report, out = audit_of(tmp_path, ov, proj)
    assert any(m.startswith("search_daily_v (in ") for m in messages(report, "recommended"))
    assert "search_daily_v: what are its grain" in (out / "questions-unknown-owner.md").read_text()


def test_readouts_that_ignored_the_overlay_are_flagged(tmp_path):
    runs = ["2026-10-14-teeth-no-overlay-step/f6__full__1", "2026-10-14-teeth-no-overlay-step/f6__full__2"]
    _, report, _ = audit_of(tmp_path, overlay(tmp_path), project(tmp_path, runs=runs))
    assert any("metrics.json defines ctr, but 2 readout(s) wrote their own definition" in m for m in messages(report))


def test_a_metric_readouts_keep_guessing_is_blocking(tmp_path):
    runs = ["2026-10-14-teeth-no-overlay-step/f7__full__1", "2026-10-14-teeth-no-overlay-step/f7__full__2"]
    code, report, out = audit_of(tmp_path, overlay(tmp_path), project(tmp_path, runs=runs))
    assert code == 1 and any("2 readout(s) defined a metric that metrics.json lacks" in m for m in messages(report, "blocking"))
    assert "conversions / searches" in (out / "questions-unknown-owner.md").read_text()


def test_questions_are_grouped_by_owner_and_kept_out_of_git(tmp_path):
    metrics = {"ctr": {**CTR}, "zrr": {**CTR, "owner": "Query Understanding", "aliases": ["无结果率"]}}
    _, report, out = audit_of(tmp_path, overlay(tmp_path, metrics), project(tmp_path))
    names = sorted(os.path.basename(p) for p in report["questions"])
    assert names == ["questions-search-analytics.md"]
    assert "ctr: what other names do people use" in (out / names[0]).read_text()
    assert (out / ".gitignore").read_text().endswith("*\n")


def test_the_audit_never_writes_to_the_overlay(tmp_path):
    ov = overlay(tmp_path)
    before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in ov.iterdir()}
    audit_of(tmp_path, ov, project(tmp_path, runs=["2026-10-14-teeth-no-overlay-step/f7__full__1"]))
    assert {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in ov.iterdir()} == before


def test_a_missing_project_is_a_usage_error(tmp_path):
    assert audit.main(["--project", str(tmp_path / "nope")]) == 3
