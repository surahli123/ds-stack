"""ds-verify checks a ds-mode readout against its logs, its data and the metric overlay, without gold."""

import hashlib
import json
import os
import shutil
import sqlite3
import subprocess
import sys

import pytest
from conftest import ROOT

sys.path.insert(0, os.path.join(ROOT, "skills", "ds-verify", "tools"))
import ds_verify  # noqa: E402

RESULTS = os.path.join(ROOT, "eval", "results")
FIXTURES = os.path.join(ROOT, "eval", "fixtures")
SCRIPT = os.path.join(ROOT, "skills", "ds-verify", "tools", "ds_verify.py")


def verify(run_dir, fixture, **overrides):
    with open(os.path.join(run_dir, "result.md"), encoding="utf-8") as handle:
        text = overrides.pop("text", handle.read())
    overlay = os.path.join(FIXTURES, fixture, "overlay")
    with open(os.path.join(FIXTURES, fixture, "task.md"), encoding="utf-8") as handle:
        request = handle.read()
    return ds_verify.run_all(text, ds_verify.vr.read_jsonl(os.path.join(run_dir, "queries.log")),
                             ds_verify.vr.read_jsonl(os.path.join(run_dir, "checks.log")),
                             overrides.get("db", os.path.join(FIXTURES, fixture, "warehouse.db")),
                             overlay if os.path.isdir(overlay) else None, request)


def fails(report):
    return [f for f in report["findings"] if f["status"] == "fail"]


def run(results, name):
    return os.path.join(RESULTS, results, name)


# --- real graded runs ----------------------------------------------------------------------------------------

def test_a_right_readout_passes_and_every_query_replays():
    report = verify(run("2026-10-14-claude-en", "f1__full__2"), "f1")
    assert report["verdict"] == "pass", fails(report)
    replays = [f for f in report["findings"] if f["check"] == "replay"]
    assert replays and all(f["status"] == "pass" for f in replays)


@pytest.mark.parametrize("results, name, fixture, check, words", [
    ("2026-10-14-claude-zh", "f2__full__1", "f2", "estimand", "asks for percent"),
    ("2026-10-14-claude-en", "f2__full__3", "f2", "alternatives", "none of the"),
    ("2026-10-14-teeth-no-overlay-step", "f6__full__2", "f6", "overlay", "searches_with_click / searches_with_results"),
    ("2026-10-14-teeth-no-overlay-step", "f7__full__1", "f7", "overlay", "unavailable"),
])
def test_the_wrong_readouts_fail_on_the_right_check(results, name, fixture, check, words):
    report = verify(run(results, name), fixture)
    assert report["verdict"] == "fail"
    assert any(f["check"] == check and words in f["message"] for f in fails(report)), fails(report)


def test_replay_catches_a_logged_result_that_the_data_does_not_give(tmp_path):
    source = run("2026-10-14-claude-en", "f1__full__2")
    shutil.copytree(source, tmp_path / "run")
    log = tmp_path / "run" / "queries.log"
    entries = [json.loads(line) for line in log.read_text().splitlines()]
    target = next(e for e in entries if e.get("status") == "ok" and any(
        isinstance(v, (int, float)) and not isinstance(v, bool) for row in e["rows"] for v in row))
    row = next(r for r in target["rows"] if any(isinstance(v, (int, float)) and not isinstance(v, bool) for v in r))
    i = next(k for k, v in enumerate(row) if isinstance(v, (int, float)) and not isinstance(v, bool))
    row[i] = row[i] + 7
    log.write_text("".join(json.dumps(e) + "\n" for e in entries))
    report = verify(tmp_path / "run", "f1")
    assert any(f["check"] == "replay" and f["ref"] == target["id"] and "different rows" in f["message"]
               for f in fails(report))


def test_replay_never_touches_the_database():
    db = os.path.join(FIXTURES, "f1", "warehouse.db")
    before = hashlib.sha256(open(db, "rb").read()).hexdigest()
    verify(run("2026-10-14-claude-en", "f1__full__2"), "f1")
    assert hashlib.sha256(open(db, "rb").read()).hexdigest() == before


def test_without_a_database_replay_could_not_verify_and_a_pasted_result_never_passes():
    report = verify(run("2026-10-14-claude-en", "f1__full__2"), "f1", db=None)
    assert [f["status"] for f in report["findings"] if f["check"] == "replay"] == ["could_not_verify"]
    report = verify(run("2026-10-14-claude-en", "f5__full__1"), "f5")
    assert any(f["check"] == "replay" and f["status"] == "could_not_verify" and "pasted" in f["message"]
               for f in report["findings"])


# --- each rule on a small readout ----------------------------------------------------------------------------

QUERIES = [{"id": "q1", "status": "ok", "source": "runner", "sql": "select 1", "rows": [[0.3012, 0.2876]]}]
CHECKS = [{"id": "srm#1", "check": "srm", "status": "fail", "from": ["q1"], "summary": "51.2/48.8 against 50/50"},
          {"id": "mix_shift#1", "check": "mix_shift", "status": "flag", "from": ["q1"], "summary": "mix -1.36 pp"}]


def readout(headline="Headline: -1.36 pp (-1.5 to -1.2) [q1]", causal="- Causal effect: not identified (a holdout would)",
            alternatives=("  - Mix shift: ruled in by the mix_shift check [check:mix_shift#1] [measured]",),
            checks=("  - srm: fail 51.2/48.8 [check:srm#1]", "  - mix_shift: flag mix -1.36 pp [check:mix_shift#1]")):
    return "\n".join(["## Answer", headline, "CTR fell. [q1]", "- Observed: -1.36 pp (-1.5 to -1.2) [q1]",
                      "- Adjusted: +0.02 pp (-0.1 to +0.1), holding platform fixed [check:mix_shift#1]", causal,
                      "", "## Why we believe it", "- Alternatives considered:", *alternatives, "- Checks run:", *checks,
                      "", "## Provenance", "- Metric: CTR = searches_with_click / searches_with_results, from metrics.json",
                      "- Reconciled: not done (no dashboard)"])


def statuses(text, check, request="", checks=CHECKS, overlay=None):
    report = ds_verify.run_all(text, QUERIES, checks, None, overlay, request)
    return [(f["status"], f["message"]) for f in report["findings"] if f["check"] == check]


def test_a_causal_number_needs_a_design():
    no_design = readout(causal="- Causal effect: -1.36 pp (-1.5 to -1.2) [q1]")
    assert statuses(no_design, "estimand")[0][0] == "fail"
    designed = readout(causal="- Causal effect: -1.36 pp (-1.5 to -1.2), from the randomized 50/50 test [q1]")
    assert all(s == "pass" for s, _ in statuses(designed, "estimand"))


def test_the_headline_must_be_one_of_the_estimates():
    assert all(s == "pass" for s, _ in statuses(readout(), "estimand"))
    assert statuses(readout(headline="Headline: -2.10 pp (-2.3 to -1.9) [q1]"), "estimand")[-1][0] == "fail"
    assert all(s == "pass" for s, _ in statuses(readout(headline="Headline: can't tell"), "estimand"))


def test_the_headline_unit_must_match_the_request():
    assert statuses(readout(), "estimand", "What was CTR, in percent?")[0][0] == "fail"
    assert statuses(readout(), "estimand", "How much did CTR change, in percentage points?")[0][0] == "pass"


@pytest.mark.parametrize("line, status", [
    ("  - v2 as the cause: ruled in as an unresolved possibility [q1] [inferred]", "fail"),
    ("  - Logging loss: ruled in as a possible cause [check:srm#1] [inferred]", "warn"),
    ("  - Bots: ruled in by the share of bot traffic [inferred]", "warn"),
    ("  - Bots: ruled out by the bot filter [q1] [measured]", "pass"),
    ("  - 搜索量变化：ruled out，两周搜索量持平 [q1] [measured]", "pass"),
])
def test_ruled_in_means_the_evidence_shows_it(line, status):
    assert statuses(readout(alternatives=(line,)), "alternatives")[-1][0] == status


def test_a_flag_left_out_of_the_readout_fails():
    assert all(s == "pass" for s, _ in statuses(readout(), "flags"))
    silent = readout(checks=("  - mix_shift: flag mix -1.36 pp [check:mix_shift#1]",),
                     alternatives=("  - Mix shift: ruled in [check:mix_shift#1] [measured]",))
    assert ("fail", "srm#1 failed and the readout doesn't report it by its tag: 51.2/48.8 against 50/50") in statuses(silent, "flags")


def test_the_overlay_definition_must_be_used(tmp_path):
    (tmp_path / "metrics.json").write_text(json.dumps({
        "ctr": {"numerator": "searches_with_click", "denominator": "searches_with_results"},
        "search_purchase_rate": {"available": False, "note": "orders aren't in this warehouse"}}))
    assert statuses(readout(), "overlay", "What was CTR?", overlay=str(tmp_path))[0][0] == "pass"
    own = readout().replace("searches_with_click / searches_with_results, from metrics.json", "clicks / searches, stated here [guess]")
    assert statuses(own, "overlay", "What was CTR?", overlay=str(tmp_path))[0][0] == "fail"
    # Saying "from metrics.json" is not using it.
    claimed = readout().replace("searches_with_click / searches_with_results", "clicks / searches")
    status, message = statuses(claimed, "overlay", "What was CTR?", overlay=str(tmp_path))[0]
    assert status == "fail" and "although it says metrics.json" in message
    assert statuses(readout(), "overlay", "What share of searches led to a purchase?", overlay=str(tmp_path))[-1][0] == "fail"
    abstains = readout(headline="Headline: can't tell")
    # A number on any estimate line counts, unless the line says it is not computed (a labelled proxy).
    assert statuses(abstains, "overlay", "What share of searches led to a purchase?", overlay=str(tmp_path))[-1][0] == "fail"
    proxy = "\n".join(l if not l.startswith(("- Observed", "- Adjusted")) else
                       "- Observed: not computed (no purchases; add-to-cart per search was 8.30%, a proxy) [q1]"
                       for l in abstains.splitlines())
    assert statuses(proxy, "overlay", "What share of searches led to a purchase?", overlay=str(tmp_path))[-1][0] == "pass"
    assert statuses(readout(), "overlay", "What was CTR?", overlay=None)[0][0] == "skipped"


def test_a_derived_number_goes_on_the_check_by_hand_list():
    derived = readout().replace("- Observed: -1.36 pp", "- Observed: -1.37 pp").replace("Headline: -1.36", "Headline: -1.37")
    report = ds_verify.run_all(derived, QUERIES, CHECKS, None, None, "")
    assert report["verdict"] == "unverified"
    assert any("headline: -1.37 isn't in q1" in item for item in report["needs_human"])
    assert any(item.startswith("check by hand: -1.37 [q1]") for item in report["needs_human"])


# --- the command line ----------------------------------------------------------------------------------------

def test_cli_exit_codes_and_json(tmp_path):
    ok = run("2026-10-14-claude-en", "f1__full__2")
    proc = subprocess.run([sys.executable, SCRIPT, "--run-dir", ok, "--db", os.path.join(FIXTURES, "f1", "warehouse.db"),
                           "--request", os.path.join(FIXTURES, "f1", "task.md"), "--json", str(tmp_path / "r.json")],
                          capture_output=True, text=True)
    assert proc.returncode == 0 and proc.stdout.startswith("ds-verify: pass")
    assert json.loads((tmp_path / "r.json").read_text())["verdict"] == "pass"
    bad = run("2026-10-14-claude-zh", "f2__full__1")
    proc = subprocess.run([sys.executable, SCRIPT, "--run-dir", bad, "--request", os.path.join(FIXTURES, "f2", "task.md")],
                          capture_output=True, text=True)
    assert proc.returncode == 1 and "asks for percent" in proc.stdout
    assert subprocess.run([sys.executable, SCRIPT], capture_output=True).returncode == 3
    # Without the request or the database, nothing fails, but the readout isn't verified either.
    proc = subprocess.run([sys.executable, SCRIPT, "--run-dir", ok], capture_output=True, text=True)
    assert proc.returncode == 2 and proc.stdout.startswith("ds-verify: unverified")


# --- regressions from the adversarial review ----------------------------------------------------------------

def verdict(text, queries=QUERIES, checks=CHECKS, db=None, overlay=None, request=""):
    return ds_verify.run_all(text, queries, checks, db, overlay, request)


def test_overlay_aliases_catch_a_chinese_request(tmp_path):
    (tmp_path / "metrics.json").write_text(json.dumps({"ctr": {
        "numerator": "searches_with_click", "denominator": "searches_with_results", "aliases": ["点击率"]}}))
    zh = readout().replace("CTR = searches_with_click / searches_with_results, from metrics.json", "点击率 = clicks / searches")
    assert statuses(zh, "overlay", "上周搜索点击率是多少？", overlay=str(tmp_path))[0][0] == "fail"


@pytest.mark.parametrize("queries, words", [
    ([{"id": "q1", "status": "ok", "source": "pasted", "sql": "by hand", "rows": [[-1.36]]}], "only pasted results"),
    ([{"id": "q1", "status": "ok", "source": "runner", "sql": "select name from sqlite_master", "rows": [["t"]]}], "no numbers"),
    ([{"id": "q1", "status": "ok", "source": "runner", "sql": "select 1", "rows": [[0.2101]]}], "check it by hand"),
])
def test_a_headline_nobody_can_check_is_unverified_not_pass(queries, words):
    report = verdict(readout(), queries=queries)
    assert report["verdict"] == "unverified"
    assert any(f["check"] == "sources" and f["status"] == "could_not_verify" and words in f["message"]
               for f in report["findings"])


def scratch_db(path, wal=False):
    conn = sqlite3.connect(path)
    if wal:
        conn.execute("pragma journal_mode=wal")
    conn.execute("create table t (k integer, b blob)")
    conn.executemany("insert into t values (?, ?)", [(1, b"\x01"), (2, b"\x02")])
    conn.commit()
    return conn


SCRATCH_LOG = [
    {"id": "q1", "status": "ok", "source": "runner", "sql": "create table scratch_dsmode_run7_s as select k * 10 k from t",
     "rows": []},
    {"id": "q2", "status": "ok", "source": "runner", "sql": "select sum(k) from scratch_dsmode_run7_s", "rows": [[30]]},
    {"id": "q3", "status": "ok", "source": "runner", "sql": "select b from t where k = 1", "rows": [[str(b"\x01")]]},
]


@pytest.mark.parametrize("leave_scratch", [True, False])
def test_replay_handles_scratch_tables_and_blobs(tmp_path, leave_scratch):
    conn = scratch_db(tmp_path / "w.db")
    if leave_scratch:  # the analysis left its scratch table in the database
        conn.execute("create table scratch_dsmode_run7_s as select k * 10 k from t")
        conn.commit()
    conn.close()
    results = ds_verify.check_replay(SCRATCH_LOG, str(tmp_path / "w.db"))
    assert [r["status"] for r in results] == ["pass", "pass", "pass"], results


def test_replay_reads_a_wal_database_that_a_writer_still_holds(tmp_path):
    writer = scratch_db(tmp_path / "w.db", wal=True)  # open, no checkpoint: the rows sit in the -wal file
    try:
        results = ds_verify.check_replay([{"id": "q1", "status": "ok", "source": "runner",
                                           "sql": "select count(*), sum(k) from t", "rows": [[2, 3]]}], str(tmp_path / "w.db"))
    finally:
        writer.close()
    assert results[0]["status"] == "pass", results


@pytest.mark.parametrize("causal, status", [
    ("- Causal effect: -1.36 pp (-1.5 to -1.2), before/after only; there was no randomized holdout [q1]", "fail"),
    ("- Causal effect: -1.36 pp (-1.5 to -1.2), from a comparison without a holdout [q1]", "fail"),
    ("- Causal effect: -1.36 pp (-1.5 to -1.2), from the 50/50 split test, treatment vs control [q1]", "pass"),
    ("- Causal effect: -1.36 pp (-1.5 to -1.2)，来自随机分流实验 [q1]", "pass"),
])
def test_a_causal_number_needs_an_unnegated_design(causal, status):
    found = [s for s, m in statuses(readout(causal=causal), "estimand") if "Causal" in m]
    assert found == [status]


@pytest.mark.parametrize("headline, asked, status", [
    ("Headline: 50.05% (49.9 to 50.2) [q1]", "What was CTR, in percent? Flag it if it moved more than 0.5 percentage points.", "pass"),
    ("Headline: CTR 从 30.42% 降到 28.32%，下降 1.36 pp (-1.5 至 -1.2) [q1]", "How much did CTR change, in percentage points?", "pass"),
    ("Headline: 下降 1.36 个百分点 (-1.5 至 -1.2) [q1]", "CTR 变化了多少个百分点？", "pass"),
    ("Headline: -1.4 pp (-1.5 to -1.2) [q1]", "", "pass"),
    ("Headline: +1.36 pp (1.2 to 1.5) [q1]", "", "fail"),
    ("Headline: 上升 1.36 pp (1.2 to 1.5) [q1]", "", "fail"),
])
def test_units_signs_and_directions(headline, asked, status):
    text = readout(headline=headline)
    if "50.05%" in headline:
        text = text.replace("- Observed: -1.36 pp (-1.5 to -1.2) [q1]", "- Observed: 50.05% (49.9 to 50.2) [q1]")
    worst = sorted(s for s, _ in statuses(text, "estimand", asked))[0]
    assert worst == status, statuses(text, "estimand", asked)


@pytest.mark.parametrize("line, status", [
    ("  - 流量结构变化：ruled in，移动端占比从 40% 升到 55%，可能与新 app 推广有关 [check:mix_shift#1] [measured]", "pass"),
    ("  - Mix shift: ruled in; mobile share rose, possibly from the app campaign [check:mix_shift#1] [measured]", "pass"),
    ("  - v2: ruled in, possibly [q1] [inferred]", "fail"),
    ("  - v2: ruled in，可能 [q1] [inferred]", "fail"),
])
def test_a_hedge_counts_only_when_it_qualifies_the_verdict(line, status):
    assert statuses(readout(alternatives=(line,)), "alternatives")[-1][0] == status


def test_not_ruled_out_is_not_a_verdict():
    lines = ("  - v2: not ruled out; nothing separates it [q1] [guess]", "  - Mix: cannot be ruled out [q1] [guess]")
    assert ("fail", "none of the 2 alternatives says 'ruled in' or 'ruled out'") in statuses(readout(alternatives=lines), "alternatives")


@pytest.mark.parametrize("block", [
    ["- Alternatives considered:", "- Mix shift: ruled in [check:mix_shift#1] [measured]", "- Checks run:"],
    ["- 考虑过的其他解释：", "  - Mix shift: ruled in [check:mix_shift#1] [measured]", "- Checks run:"],
])
def test_alternatives_in_other_layouts_are_found(block):
    text = readout().replace("- Alternatives considered:\n  - Mix shift: ruled in by the mix_shift check "
                             "[check:mix_shift#1] [measured]\n- Checks run:", "\n".join(block))
    assert statuses(text, "alternatives")[-1][0] == "pass"
    headed = readout().replace("- Alternatives considered:", "### Alternatives considered")
    assert any(s == "pass" for s, _ in statuses(headed, "alternatives"))


def test_missing_inputs_are_could_not_verify():
    report = ds_verify.run_all(readout(), QUERIES, None, None, None, None)
    found = {(f["check"], f["status"]) for f in report["findings"]}
    assert ("flags", "could_not_verify") in found and ("estimand", "could_not_verify") in found
    assert report["verdict"] != "pass"  # here trace also fails: the check tags can't resolve without the log


def test_each_failed_id_needs_its_own_report_and_a_rerun_is_a_warn():
    checks = CHECKS + [
        {"id": "completeness#1", "check": "completeness", "status": "fail", "from": ["q1"], "details": {"target": "2026-10-04"}, "summary": "no rows"},
        {"id": "completeness#2", "check": "completeness", "status": "fail", "from": ["q1"], "details": {"target": "2026-10-03"}, "summary": "no rows"},
        {"id": "completeness#3", "check": "completeness", "status": "pass", "from": ["q1"], "details": {"target": "2026-10-04"}, "summary": "ok"}]
    text = readout(checks=("  - srm: fail [check:srm#1]", "  - mix_shift: flag [check:mix_shift#1]", "  - completeness: fail on a mis-call"))
    found = {f["message"].split(" ")[0]: f["status"] for f in ds_verify.check_flags(text, checks)}
    assert found["completeness#1"] == "warn" and found["completeness#2"] == "fail"


def test_the_cli_defaults_to_warehouse_db_in_the_analysis_directory(tmp_path):
    shutil.copy(os.path.join(FIXTURES, "f1", "warehouse.db"), tmp_path / "warehouse.db")
    source = run("2026-10-14-claude-en", "f1__full__2")
    shutil.copy(os.path.join(source, "result.md"), tmp_path / "readout.md")
    shutil.copy(os.path.join(source, "queries.log"), tmp_path / ".ds-queries.log")
    shutil.copy(os.path.join(source, "checks.log"), tmp_path / ".ds-checks.log")
    shutil.copy(os.path.join(FIXTURES, "f1", "task.md"), tmp_path / "request.md")
    env = {k: v for k, v in os.environ.items() if k not in ("DS_WAREHOUSE", "DS_QUERIES_LOG", "DS_CHECKS_LOG")}
    proc = subprocess.run([sys.executable, SCRIPT, "readout.md", "--request", "request.md"], cwd=tmp_path,
                          capture_output=True, text=True, env=env)
    assert proc.returncode == 0 and proc.stdout.startswith("ds-verify: pass"), proc.stdout
