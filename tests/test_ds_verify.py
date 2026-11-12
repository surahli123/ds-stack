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

QUERIES = [{"id": "q1", "status": "ok", "source": "runner", "rows": [[0.3012, 0.2876]],
            "sql": "select sum(searches_with_click), sum(searches_with_results) from search_daily"}]
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


F6_DB = os.path.join(FIXTURES, "f6", "warehouse.db")  # has searches_with_click, searches_with_results, traffic_type
CTR_OVERLAY = {"ctr": {"numerator": "searches_with_click", "denominator": "searches_with_results",
                       "filters": ["traffic_type = 'external'"]}}
EXTERNAL = [{"id": "q1", "status": "ok", "source": "runner", "rows": [[0.3012, 0.2876]],
             "sql": "select sum(searches_with_click), sum(searches_with_results) from search_daily_v "
                    "where traffic_type = 'external'"}]


def overlay_findings(tmp_path, queries, text=None):
    (tmp_path / "metrics.json").write_text(json.dumps(CTR_OVERLAY))
    text = text or readout().replace("from metrics.json", "traffic_type = 'external', from metrics.json")
    report = ds_verify.run_all(text, queries, CHECKS, F6_DB, str(tmp_path), "What was CTR?")
    return [(f["status"], f["message"]) for f in report["findings"] if f["check"] == "overlay"]


def test_the_query_behind_the_headline_must_use_the_overlay_definition(tmp_path):
    assert all(s == "pass" for s, _ in overlay_findings(tmp_path, EXTERNAL))
    # The Metric line copied from metrics.json, the number computed another way: rewording doesn't pass.
    other = [{**EXTERNAL[0], "sql": "select sum(clicks), sum(searches) from search_daily_v"}]
    found = overlay_findings(tmp_path, other)
    assert any(s == "fail" and "searches_with_click, searches_with_results, traffic_type from" in m
               and "rewording" in m for s, m in found), found


def test_a_pasted_interval_is_followed_to_the_query_it_names(tmp_path):
    pasted = {"id": "q2", "status": "ok", "source": "pasted", "sql": "Wilson interval computed from q1", "rows": [[1]]}
    text = readout().replace("from metrics.json", "traffic_type = 'external', from metrics.json") \
                    .replace("Headline: -1.36 pp (-1.5 to -1.2) [q1]", "Headline: -1.36 pp (-1.5 to -1.2) [q2]")
    assert all(s == "pass" for s, _ in overlay_findings(tmp_path, [*EXTERNAL, pasted], text))
    lone = {**pasted, "sql": "Wilson interval, by hand"}
    assert ds_verify.sql_behind_estimates("## Answer\nHeadline: 50.1% [q2]\n", [*EXTERNAL, lone], []) == []


def test_not_ruled_out_is_the_verdict_for_an_open_alternative():
    lines = ("  - v2: not ruled out; a holdout would decide it [q1] [guess]", "  - Mix: cannot be ruled out [q1] [guess]")
    found = statuses(readout(alternatives=lines), "alternatives")
    assert [s for s, _ in found] == ["pass", "pass"] and found[0][1].startswith("not ruled out")


def test_not_ruled_in_alone_is_no_verdict():
    found = statuses(readout(alternatives=("  - v2: not ruled in [q1] [guess]",)), "alternatives")
    assert ("fail", "none of the 1 alternatives says 'ruled in', 'ruled out' or 'not ruled out'") in found


def test_a_hedged_ruled_in_points_to_not_ruled_out():
    # The Codex wording on 2026-11-02: an open alternative written as "ruled in".
    line = "  - Logging changes: ruled in as unresolved possibilities; no audit exists [q1] [inferred]"
    status, message = statuses(readout(alternatives=(line,)), "alternatives")[-1]
    assert status == "fail" and "Write 'not ruled out'" in message


ONLY_MIX = [{"id": "mix_shift#1", "check": "mix_shift", "status": "flag", "from": ["q1"], "summary": "mix -1.36 pp"},
            {"id": "completeness#1", "check": "completeness", "status": "pass", "from": ["q1"], "summary": "100%"}]


def test_abstaining_only_because_the_cause_is_unidentified_fails():
    # Codex, 2026-11-02, f1 and f3 in Chinese: "Headline: can't tell" next to a computed Adjusted.
    found = statuses(readout(headline="Headline: can't tell [inferred]"), "estimand", checks=ONLY_MIX)
    assert found[-1][0] == "fail" and "not a reason to abstain" in found[-1][1]


@pytest.mark.parametrize("checks, adjusted, causal", [
    (CHECKS, None, None),                                                             # srm failed: a data problem
    ([*ONLY_MIX, {"id": "completeness#2", "check": "completeness", "status": "could not run"}], None, None),
    (ONLY_MIX, "- Adjusted: not computed (one week only, 7 days)", None),
    (ONLY_MIX, None, "- Causal effect: -1.36 pp, from the randomized test [q1]"),
    (None, None, None),                                                               # no check log: not judged here
])
def test_abstaining_is_left_alone_when_the_data_or_design_explains_it(checks, adjusted, causal):
    text = readout(headline="Headline: can't tell", causal=causal or "- Causal effect: not identified (a holdout would)")
    if adjusted:
        text = "\n".join(adjusted if l.startswith("- Adjusted") else l for l in text.splitlines())
    found = statuses(text, "estimand", checks=checks)
    assert not any("not a reason to abstain" in m for _, m in found), found


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


def test_the_headline_column_must_be_the_overlay_definition_when_a_query_computes_both(tmp_path):
    # From the arm without the overlay step: one query computed both rates and the Headline took the wrong one.
    (tmp_path / "metrics.json").write_text(json.dumps(CTR_OVERLAY))
    both = [{"id": "q1", "status": "ok", "source": "runner", "columns": ["p", "p_res"], "rows": [[46.05, 50.05]],
             "sql": "select 100.0*sum(searches_with_click)/sum(searches) p, "
                    "100.0*sum(searches_with_click)/sum(searches_with_results) as p_res "
                    "from search_daily_v where traffic_type = 'external'"}]
    metric = "- Metric: CTR = searches_with_click / searches_with_results, traffic_type = 'external', from metrics.json"
    db = os.path.join(FIXTURES, "f6", "warehouse.db")

    def overlay_of(value):
        text = "\n".join(["## Answer", f"Headline: {value}% [q1]", "CTR was this. [q1]", f"- Observed: {value}% [q1]",
                          "- Adjusted: not computed (a level)", "- Causal effect: not identified (no design)",
                          "## Provenance", metric])
        report = ds_verify.run_all(text, both, [], db, str(tmp_path), "What was CTR?")
        return [(f["status"], f["message"]) for f in report["findings"] if f["check"] == "overlay"]

    wrong = overlay_of("46.05")
    assert any(s == "fail" and "column p of q1" in m and "searches_with_results" in m for s, m in wrong), wrong
    assert all(s == "pass" for s, _ in overlay_of("50.05"))


@pytest.mark.parametrize("sql, expected", [
    ("select a*1.0/b as ctr, count(*) from t", {"ctr": "a*1.0/b"}),
    ("with x as (select 1 as a from z) select k*100.0/n ctr from x where s = 'from here'", {"ctr": "k*100.0/n"}),
    ("select case when a then b end, distinct_x from t", {"distinct_x": "distinct_x"}),
])
def test_select_items_reads_the_top_level_select_list(sql, expected):
    items = ds_verify.select_items(sql)
    assert {k: v for k, v in items.items() if k in expected} == expected
    assert "end" not in items and "a" not in items


# --- the adversarial review of the SQL definition check (2026-11-02) -----------------------------------------

WRONG_AND_RIGHT = ("select 100.0*sum(searches_with_click)/sum(searches) p, "
                   "100.0*sum(searches_with_click)/sum(searches_with_results) p_res "
                   "from search_daily_v where traffic_type = 'external'")
METRIC = "- Metric: CTR = searches_with_click / searches_with_results, traffic_type = 'external', from metrics.json"


def runner(qid, sql, columns, rows):
    return {"id": qid, "status": "ok", "source": "runner", "sql": sql, "columns": columns, "rows": rows}


def overlay_of(tmp_path, headline, observed, queries, checks=()):
    (tmp_path / "metrics.json").write_text(json.dumps(CTR_OVERLAY))
    text = "\n".join(["## Answer", f"Headline: {headline}", "CTR was this. [q1]", f"- Observed: {observed}",
                      "- Adjusted: not computed (a level)", "- Causal effect: not identified (no design)",
                      "## Provenance", METRIC])
    report = ds_verify.run_all(text, queries, list(checks), F6_DB, str(tmp_path), "What was CTR?")
    return [(f["status"], f["message"]) for f in report["findings"] if f["check"] == "overlay"]


def failed(found):
    return any(s == "fail" for s, _ in found)


def test_a_pasted_detour_does_not_hide_the_wrong_column(tmp_path):
    both = runner("q6", WRONG_AND_RIGHT, ["p", "p_res"], [[46.05, 50.05]])
    pasted = {"id": "q7", "status": "ok", "source": "pasted", "sql": "Wilson interval computed from q6",
              "columns": ["p", "lo", "hi"], "rows": [[46.05, 45.93, 46.17]]}
    assert failed(overlay_of(tmp_path, "46.05 % (45.93 to 46.17) [q7]", "46.05 % [q6]", [both, pasted]))
    assert not failed(overlay_of(tmp_path, "50.05 % [q7]", "50.05 % [q6]",
                                 [both, {**pasted, "rows": [[50.05, 49.93, 50.17]]}]))


@pytest.mark.parametrize("sql, columns, row", [
    (WRONG_AND_RIGHT.replace(" p_res", " p_res, round(100.0*sum(searches_with_click)/sum(searches), 2) p_rounded"),
     ["p", "p_res", "p_rounded"], [46.0512, 50.0529, 46.05]),
    (WRONG_AND_RIGHT.replace("100.0*sum(searches_with_click)/sum(searches) p",
                             "printf('%.2f', 100.0*sum(searches_with_click)/sum(searches)) p"),
     ["p", "p_res"], ["46.05", 50.0529]),
])
def test_several_matching_columns_or_text_cells_still_get_judged(tmp_path, sql, columns, row):
    assert failed(overlay_of(tmp_path, "46.05 % [q1]", "46.05 % [q1]", [runner("q1", sql, columns, [row])]))


def test_the_same_wrong_query_cited_twice_fails(tmp_path):
    q6 = runner("q6", WRONG_AND_RIGHT, ["p", "p_res"], [[46.05, 50.05]])
    assert failed(overlay_of(tmp_path, "46.05 % [q6, q7]", "46.05 % [q6]", [q6, {**q6, "id": "q7"}]))


def test_an_analysis_through_a_scratch_table_passes(tmp_path):
    made = runner("q1", "create table scratch_dsmode_abc_agg as select sum(searches_with_click) as c, "
                        "sum(searches_with_results) as r from search_daily_v where traffic_type = 'external'", [], [])
    read = runner("q2", "select 100.0*c/r as ctr from scratch_dsmode_abc_agg", ["ctr"], [[50.0529]])
    for cited in ("[q2]", "[q1, q2]"):
        found = overlay_of(tmp_path, f"50.05 % {cited}", f"50.05 % {cited}", [made, read])
        assert not failed(found), found


@pytest.mark.parametrize("sql", [
    # A CTE alias that equals a base column name.
    "with t as (select sum(searches_with_click) as clicked, sum(searches_with_results) as searches from search_daily_v "
    "where traffic_type = 'external') select 100.0*clicked/searches as ctr from t",
    # Aliases mixed with a base column.
    "with a as (select date, sum(searches_with_click) c, sum(searches_with_results) r from search_daily_v "
    "where traffic_type = 'external' group by date) select 100.0*sum(case when date >= '2026-10-05' then c end)"
    "/sum(case when date >= '2026-10-05' then r end) as ctr from a",
])
def test_an_expression_of_aliases_is_left_alone(tmp_path, sql):
    found = overlay_of(tmp_path, "50.05 % [q1]", "50.05 % [q1]", [runner("q1", sql, ["ctr"], [[50.0529]])])
    assert not failed(found), found


@pytest.mark.parametrize("change, status", [
    ({"numerator": "searches with at least one click"}, "could_not_verify"),
    ({"filters": ["lower(traffic_type) = 'external'"]}, "pass"),
    ({"numerator": "search_daily_v.searches_with_click"}, "pass"),
    ({"filters": None}, "pass"),
    ({"numerator": ["searches_with_click"]}, None),
])
def test_overlay_forms_people_write_do_not_block_an_honest_analysis(tmp_path, change, status):
    overlay = {"ctr": {**CTR_OVERLAY["ctr"], **change}}
    (tmp_path / "metrics.json").write_text(json.dumps(overlay))
    text = "\n".join(["## Answer", "Headline: 50.05 % [q1]", "CTR. [q1]", "- Observed: 50.05 % [q1]",
                      "- Adjusted: not computed (a level)", "- Causal effect: not identified (no design)", METRIC])
    report = ds_verify.run_all(text, [runner("q1", WRONG_AND_RIGHT, ["p", "p_res"], [[46.05, 50.05]])], [], F6_DB,
                               str(tmp_path), "What was CTR?")
    found = [(f["status"], f["message"]) for f in report["findings"] if f["check"] == "overlay"]
    assert not any("internal error" in m for _, m in found), found
    if status == "could_not_verify":
        assert any(s == status and "names no column" in m for s, m in found), found
    elif status == "pass":
        assert not any(s == "fail" and ("query behind" in m or "column p" in m) for s, m in found), found


def test_a_null_row_or_a_broken_log_line_does_not_crash(tmp_path):
    (tmp_path / "metrics.json").write_text(json.dumps(CTR_OVERLAY))
    text = readout().replace("from metrics.json", "traffic_type = 'external', from metrics.json")
    queries = [{**EXTERNAL[0], "columns": ["a", "b"], "rows": [None, [0.3012, 0.2876]]}, "not an object", 5]
    checks = [*CHECKS, {"id": "x#1", "check": "x", "status": "pass", "from": 5}, ["junk"]]
    report = ds_verify.run_all(text, queries, checks, F6_DB, str(tmp_path), "What was CTR?")
    assert report["verdict"] in ("pass", "fail", "unverified")


def test_an_exception_inside_a_check_is_reported_not_raised(monkeypatch):
    monkeypatch.setattr(ds_verify, "check_flags", lambda *a: 1 / 0)
    report = ds_verify.run_all(readout(), QUERIES, CHECKS, None, None, "")
    assert ("flags", "could_not_verify") in {(f["check"], f["status"]) for f in report["findings"]}
    assert report["verdict"] in ("fail", "unverified")


def test_an_unaliased_expression_ending_in_a_column_is_not_an_alias():
    assert ds_verify.select_items("select n, k * 100.0 / n from x")["n"] == "n"
