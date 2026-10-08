"""Every check passes on clean input, fails on its planted mistake, and refuses bad specs."""

import json
import os
import sqlite3
import subprocess
import sys

import completeness
import fanout
import mix_shift
import srm
from _common import COULD_NOT_RUN, FAIL, PASS
from conftest import ROOT

CHECKS_DIR = os.path.join(ROOT, "skills", "ds-mode", "checks")
FIXTURES = os.path.join(ROOT, "eval", "fixtures")


def seg(name, nb, kb, na, ka):
    return {"name": name, "before": {"n": nb, "k": kb}, "after": {"n": na, "k": ka}}


# mix_shift

def test_mix_shift_fails_when_mix_explains_the_move():
    result = mix_shift.run({"segments": [seg("desktop", 600, 216, 450, 162), seg("mobile", 400, 88, 550, 121)]})
    assert result.status == FAIL
    assert abs(result.details["rate_effect_pp"]) < 1e-9
    assert result.details["delta_pp"] == result.details["mix_effect_pp"]


def test_mix_shift_passes_when_rates_moved_within_segments():
    result = mix_shift.run({"segments": [seg("desktop", 600, 216, 600, 198), seg("mobile", 400, 88, 400, 88)]})
    assert result.status == PASS
    assert result.details["mix_share"] == 0


def test_mix_shift_effects_sum_to_the_overall_change():
    result = mix_shift.run({"segments": [seg("a", 500, 100, 700, 210), seg("b", 300, 90, 200, 50), seg("c", 200, 20, 150, 30)]})
    d = result.details
    assert abs(d["rate_effect_pp"] + d["mix_effect_pp"] - d["delta_pp"]) < 1e-3


def test_mix_shift_flags_offsetting_effects():
    # Overall CTR flat, but only because a mix shift hides a real within-segment drop (Simpson).
    result = mix_shift.run({"segments": [seg("desktop", 500, 180, 700, 238), seg("mobile", 500, 110, 300, 52)]})
    assert result.status == FAIL


def test_mix_shift_does_not_flag_noise_on_a_flat_metric():
    result = mix_shift.run({"segments": [seg("a", 100000, 30000, 100010, 30003), seg("b", 100000, 20000, 99990, 19998)]})
    assert result.status == PASS and abs(result.details["delta_pp"]) < 0.01


def test_mix_shift_cannot_run_on_bad_specs():
    assert mix_shift.run({"segments": [seg("only", 10, 1, 10, 2)]}).status == COULD_NOT_RUN
    assert mix_shift.run({"segments": [seg("a", 10, 11, 10, 2), seg("b", 10, 1, 10, 1)]}).status == COULD_NOT_RUN
    assert mix_shift.run({"segments": [seg("a", 0, 0, 10, 2), seg("b", 10, 1, 10, 1)]}).status == COULD_NOT_RUN
    assert mix_shift.run({}).status == COULD_NOT_RUN


def test_mix_shift_catches_the_planted_f1_mistake_from_the_warehouse():
    conn = sqlite3.connect(os.path.join(FIXTURES, "f1", "warehouse.db"))
    rows = conn.execute("""SELECT platform, date < '2026-09-28' AS before, SUM(searches), SUM(clicks)
                           FROM search_daily GROUP BY 1, 2""").fetchall()
    parts = {}
    for platform, before, n, k in rows:
        parts.setdefault(platform, {"name": platform})["before" if before else "after"] = {"n": n, "k": k}
    result = mix_shift.run({"segments": list(parts.values())})
    assert result.status == FAIL
    assert abs(result.details["rate_effect_pp"]) < 0.05


# fanout

def test_fanout_fails_on_duplicate_right_keys():
    result = fanout.run({"left_rows": 1000, "joined_rows": 1000, "right_rows": 1300, "right_distinct_keys": 1000})
    assert result.status == FAIL and "duplicate" in result.summary


def test_fanout_fails_when_join_adds_rows():
    assert fanout.run({"left_rows": 1000, "joined_rows": 1300}).status == FAIL


def test_fanout_fails_when_left_join_loses_rows():
    assert fanout.run({"left_rows": 1000, "joined_rows": 990, "join": "left"}).status == FAIL


def test_fanout_inner_join_drop_passes_unless_over_limit():
    assert fanout.run({"left_rows": 1000, "joined_rows": 990, "join": "inner"}).status == PASS
    assert fanout.run({"left_rows": 1000, "joined_rows": 900, "join": "inner", "max_drop_fraction": 0.05}).status == FAIL


def test_fanout_one_to_one_needs_unique_left_keys():
    spec = {"left_rows": 1000, "joined_rows": 1000, "relationship": "one_to_one", "left_distinct_keys": 990}
    assert fanout.run(spec).status == FAIL
    assert fanout.run({**spec, "relationship": "many_to_one"}).status == PASS


def test_fanout_passes_a_clean_join():
    assert fanout.run({"left_rows": 1000, "joined_rows": 1000, "right_rows": 1000, "right_distinct_keys": 1000}).status == PASS


def test_fanout_cannot_run_on_bad_specs():
    assert fanout.run({"left_rows": -1, "joined_rows": 3}).status == COULD_NOT_RUN
    assert fanout.run({"left_rows": 1, "joined_rows": 1, "relationship": "many_to_many"}).status == COULD_NOT_RUN
    assert fanout.run({"left_rows": 1, "joined_rows": 1, "right_rows": 5}).status == COULD_NOT_RUN


def test_fanout_catches_the_planted_f2_mistake_from_the_warehouse():
    conn = sqlite3.connect(os.path.join(FIXTURES, "f2", "warehouse.db"))
    right_rows, right_keys = conn.execute("SELECT COUNT(*), COUNT(DISTINCT query_id) FROM query_labels").fetchone()
    left_rows = conn.execute("SELECT COUNT(*) FROM query_stats").fetchone()[0]
    joined = conn.execute("SELECT COUNT(*) FROM query_stats s JOIN query_labels l USING (query_id)").fetchone()[0]
    result = fanout.run({"left_rows": left_rows, "joined_rows": joined, "right_rows": right_rows, "right_distinct_keys": right_keys})
    assert result.status == FAIL


# srm

def test_srm_fails_on_a_mismatched_split():
    result = srm.run({"observed": [50000, 47600], "expected_ratio": [0.5, 0.5]})
    assert result.status == FAIL and result.details["p_value"] < 1e-10


def test_srm_passes_a_balanced_split():
    assert srm.run({"observed": [50000, 50100], "expected_ratio": [0.5, 0.5]}).status == PASS


def test_srm_p_values_match_chi_square_tables():
    assert abs(srm._gamma_q(0.5, 3.841459 / 2) - 0.05) < 1e-6
    assert abs(srm._gamma_q(1.0, 5.991465 / 2) - 0.05) < 1e-6
    assert abs(srm._gamma_q(1.5, 11.344867 / 2) - 0.01) < 1e-6


def test_srm_cannot_run_on_bad_specs():
    assert srm.run({"observed": [1, 2], "expected_ratio": [0.6, 0.6]}).status == COULD_NOT_RUN
    assert srm.run({"observed": [1], "expected_ratio": [1.0]}).status == COULD_NOT_RUN
    assert srm.run({"observed": [0, 0], "expected_ratio": [0.5, 0.5]}).status == COULD_NOT_RUN
    assert srm.run({"observed": [1.5, 2], "expected_ratio": [0.5, 0.5]}).status == COULD_NOT_RUN


def test_srm_catches_the_planted_f5_mistake_from_the_warehouse():
    conn = sqlite3.connect(os.path.join(FIXTURES, "f5", "warehouse.db"))
    users = dict(conn.execute("SELECT arm, SUM(users) FROM experiment_daily GROUP BY arm").fetchall())
    assert srm.run({"observed": [users["control"], users["treatment"]], "expected_ratio": [0.5, 0.5]}).status == FAIL


# completeness

def series(*rows):
    return [{"period": f"2026-10-0{i + 1}", "rows": r} for i, r in enumerate(rows)]


def test_completeness_fails_on_a_partial_period():
    assert completeness.run({"series": series(24, 24, 24, 24, 10), "target": "2026-10-05"}).status == FAIL


def test_completeness_fails_on_a_missing_period():
    assert completeness.run({"series": series(24, 24, 24, 24), "target": "2026-10-05"}).status == FAIL


def test_completeness_flags_double_loads_only_when_asked():
    spec = {"series": series(24, 24, 24, 24, 48), "target": "2026-10-05"}
    assert completeness.run(spec).status == PASS
    assert completeness.run({**spec, "max_ratio": 1.5}).status == FAIL


def test_completeness_cannot_run_without_enough_history():
    assert completeness.run({"series": series(24, 24), "target": "2026-10-03"}).status == COULD_NOT_RUN
    assert completeness.run({"series": series(24, 24, 24), "target": "2026-10-03"}).status == COULD_NOT_RUN


def test_completeness_rejects_duplicate_periods():
    assert completeness.run({"series": series(24, 24, 24, 24) + series(1)[:1], "target": "2026-10-04"}).status == COULD_NOT_RUN


def test_completeness_catches_the_planted_f4_mistake_from_the_warehouse():
    conn = sqlite3.connect(os.path.join(FIXTURES, "f4", "warehouse.db"))
    rows = conn.execute("SELECT date, COUNT(*) FROM search_hourly GROUP BY date").fetchall()
    spec = {"series": [{"period": d, "rows": n} for d, n in rows], "target": "2026-10-07"}
    assert completeness.run(spec).status == FAIL


# CLI and run log

def test_cli_log_follows_DS_CHECKS_LOG(tmp_path):
    log = tmp_path / "pinned.log"
    sub = tmp_path / "elsewhere"
    sub.mkdir()
    subprocess.run([sys.executable, os.path.join(CHECKS_DIR, "run.py"), "srm", "--json", '{"observed": [10, 10], "expected_ratio": [0.5, 0.5]}'],
                   cwd=sub, env={**os.environ, "DS_CHECKS_LOG": str(log)}, capture_output=True, check=True)
    assert log.exists() and not (sub / ".ds-checks.log").exists()


def test_cli_logs_every_run_and_uses_exit_codes(tmp_path):
    runner = os.path.join(CHECKS_DIR, "run.py")
    ok = subprocess.run([sys.executable, runner, "srm", "--json", '{"observed": [10, 10], "expected_ratio": [0.5, 0.5]}'],
                        cwd=tmp_path, capture_output=True, text=True)
    bad = subprocess.run([sys.executable, runner, "srm", "--json", "not json"], cwd=tmp_path, capture_output=True, text=True)
    assert ok.returncode == 0 and bad.returncode == 2
    logged = [json.loads(line) for line in (tmp_path / ".ds-checks.log").read_text().splitlines()]
    assert [entry["status"] for entry in logged] == ["pass", "could_not_run"]


def test_registry_covers_every_check_and_enforces_the_evidence_rule():
    with open(os.path.join(CHECKS_DIR, "registry.json")) as handle:
        registry = json.load(handle)
    modules = {f[:-3] for f in os.listdir(CHECKS_DIR) if f.endswith(".py") and f not in ("run.py", "_common.py")}
    assert modules == {k for k in registry if not k.startswith("_")}
    for name, entry in registry.items():
        if name.startswith("_"):
            continue
        assert entry["status"] in ("evidenced", "provisional")
        if entry["status"] == "evidenced":
            assert entry["incidents"] >= 2 and entry["evidence"], name
