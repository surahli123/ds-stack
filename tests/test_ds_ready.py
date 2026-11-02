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


# --- regressions from the adversarial review ----------------------------------------------------------------

def readout_with(folder, name, metric_line):
    path = folder / name
    path.mkdir(parents=True)
    (path / "readout.md").write_text(f"## Answer\nHeadline: 8.3 %\n\n## Provenance\n- Metric: {metric_line}\n", encoding="utf-8")


def test_an_out_folder_with_other_files_is_refused_and_never_overwritten(tmp_path):
    proj = project(tmp_path)
    (proj / ".gitignore").write_text("*.pyc\nsecrets.env\n")
    assert audit.main(["--project", str(proj), "--overlay", str(overlay(tmp_path)), "--out", str(proj)]) == 3
    assert (proj / ".gitignore").read_text() == "*.pyc\nsecrets.env\n"


def test_the_default_out_is_inside_the_project(tmp_path, monkeypatch):
    proj = project(tmp_path)
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    monkeypatch.chdir(elsewhere)
    audit.main(["--project", str(proj), "--overlay", str(overlay(tmp_path))])
    assert (proj / "ds-ready" / ".gitignore").exists() and not (elsewhere / "ds-ready").exists()


def test_one_metric_guessed_in_four_wordings_is_one_blocking_gap(tmp_path):
    proj = project(tmp_path)
    for i, line in enumerate(["conversions / searches, stated here [guess]. There is no metrics.json.",
                              "sum(conversions) / sum(searches), stated here [guess]",
                              "conversion rate = conversions ÷ searches over the week, stated here [guess]",
                              "转化率 = conversions ÷ searches（周合计），stated here [guess]"]):
        readout_with(proj, f"r{i}", line)
    code, report, _ = audit_of(tmp_path, overlay(tmp_path), proj)
    guessed = [m for m in messages(report, "blocking") if "defined a metric that metrics.json lacks" in m]
    assert code == 1 and len(guessed) == 1 and guessed[0].startswith("4 readout(s)")


def test_a_line_taken_from_metrics_json_is_not_a_guess(tmp_path):
    proj = project(tmp_path)
    for i in range(2):
        readout_with(proj, f"r{i}", "searches_with_click / searches_with_results, from metrics.json")
    _, report, _ = audit_of(tmp_path, overlay(tmp_path), proj)
    assert not any("defined a metric" in m or "wrote their own" in m for m in messages(report))


@pytest.mark.parametrize("change, words", [
    ({"numerator": []}, "wrongly typed numerator"),
    ({"denominator": "   "}, "wrongly typed denominator"),
    ({"filters": "traffic_type = 'external'"}, "filters (a list of strings)"),
    ({"available": "false"}, "available must be the JSON value true or false"),
])
def test_wrong_types_are_blocking(tmp_path, change, words):
    code, report, _ = audit_of(tmp_path, overlay(tmp_path, {"ctr": {**CTR, "aliases": ["x"], **change}}), project(tmp_path))
    assert code == 1 and any(words in m for m in messages(report, "blocking")), messages(report)


def test_odd_but_harmless_values_do_not_crash(tmp_path):
    metrics = {"ctr": {**CTR, "aliases": None, "owner": ["alice", "bob"]}}
    proj = project(tmp_path)
    readout_with(proj, "r1", "clicks / searches, stated here [guess]")
    code, report, _ = audit_of(tmp_path, overlay(tmp_path, metrics), proj)
    assert code in (0, 1) and report["gaps"]


def test_a_scan_cut_short_is_blocking(tmp_path):
    proj = project(tmp_path)
    for i in range(12):
        (proj / f"note{i}.md").write_text("notes")
    code = audit.main(["--project", str(proj), "--overlay", str(overlay(tmp_path)), "--max-files", "10",
                       "--out", str(tmp_path / "q"), "--json", str(tmp_path / "r.json")])
    report = json.loads((tmp_path / "r.json").read_text())
    assert code == 1 and any("scan stopped" in m for m in messages(report, "blocking"))


@pytest.mark.parametrize("line, blocking", [
    ("read and follow `{root}/skills/ds-mode/SKILL.md`.", False),
    ("read and follow [ds-mode]({root}/skills/ds-mode/SKILL.md)", False),
    ("read and follow skills/ds-mode/SKILL.md", False),
    ("<!-- read and follow {root}/skills/ds-mode/SKILL.md -->", True),
])
def test_agents_md_paths_are_read_like_a_person_would(tmp_path, line, blocking):
    proj = tmp_path / "project"
    proj.mkdir()
    if "skills/ds-mode" in line and "{root}" not in line:
        os.symlink(os.path.join(ROOT, "skills"), proj / "skills")
    (proj / "AGENTS.md").write_text(line.format(root=ROOT) + "\n")
    _, report, _ = audit_of(tmp_path, overlay(tmp_path), proj)
    assert any("ds-mode" in m for m in messages(report, "blocking")) == blocking


def test_home_in_agents_md_is_expanded_and_a_stale_ds_verify_is_only_recommended(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    os.makedirs(tmp_path / "home")
    os.symlink(os.path.join(ROOT, "skills"), tmp_path / "home" / "ds-skills")
    proj = tmp_path / "project"
    proj.mkdir()
    (proj / "AGENTS.md").write_text("Follow $HOME/ds-skills/ds-mode/SKILL.md\nCheck with /nowhere/ds-verify/SKILL.md\n")
    _, report, _ = audit_of(tmp_path, overlay(tmp_path), proj)
    assert not any("playbook" == g["area"] and g["severity"] == "blocking" for g in report["gaps"])
    assert any("ds-verify/SKILL.md, which doesn't exist" in m for m in messages(report, "recommended"))


def test_the_column_check_ignores_literals_functions_and_case(tmp_path):
    db = os.path.join(FIXTURES, "f6", "warehouse.db")
    good = {**CTR, "source": "main.search_daily_v", "numerator": "SEARCHES_WITH_CLICK",
            "filters": ["traffic_type = 'local_services'", "date >= date('now', '-7 day')"], "aliases": ["x"]}
    code, report, _ = audit_of(tmp_path, overlay(tmp_path, {"ctr": good}), project(tmp_path), db)
    assert not any(g["area"] == "data" for g in report["gaps"]), messages(report)
    typo = {**CTR, "numerator": "clickz", "aliases": ["x"]}
    _, report, _ = audit_of(tmp_path / "t2", overlay(mk(tmp_path / "t2"), {"ctr": typo}), project(tmp_path / "t2"), db)
    assert any("clickz isn't a column" in m for m in messages(report, "blocking"))


def mk(path):
    path.mkdir(parents=True, exist_ok=True)
    return path


def test_a_database_that_is_not_sqlite_is_a_gap_not_a_crash(tmp_path):
    bogus = tmp_path / "warehouse.db"
    bogus.write_text("this is not a database")
    code, report, _ = audit_of(tmp_path, overlay(tmp_path), project(tmp_path), str(bogus))
    assert code == 1 and any("can't be read as a SQLite database" in m for m in messages(report, "blocking"))


def test_a_denylist_in_another_encoding_does_not_crash(tmp_path):
    ov = overlay(tmp_path)
    (ov / "denylist.txt").write_bytes("内部代号\n".encode("gbk"))
    code, _, _ = audit_of(tmp_path, ov, project(tmp_path))
    assert code in (0, 1)


def test_an_internal_error_is_exit_3(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(audit, "audit_overlay", lambda *a: 1 / 0)
    assert audit.main(["--project", str(project(tmp_path)), "--out", str(tmp_path / "q")]) == 3
    assert "internal error: ZeroDivisionError" in capsys.readouterr().err


def test_only_real_tables_are_read_from_query_logs():
    sql = ("with t as (select * from search_daily), u as (select 1 from Search_Daily) "
           "select extract(day from ts), * from t join main.search_daily s on 1=1 -- from old_table\n"
           "join information_schema.columns c on 1=1 where x = 'from fake_table'")
    assert audit.tables_in(sql) == {"search_daily"}
