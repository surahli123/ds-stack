"""acceptance.py turns results directories into the acceptance table, with the thresholds fixed in docs/acceptance.md."""

import os
import shutil

import acceptance
from conftest import ROOT

RESULTS = os.path.join(ROOT, "eval", "results", "2026-10-14-estimand")


def test_the_estimand_run_passes_plumbing_and_is_incomplete_elsewhere(capsys):
    assert acceptance.main([RESULTS]) == 0
    out = capsys.readouterr().out
    assert "| Plumbing | PASS | 15 of 15 full-arm runs |" in out
    assert "| Correctness | INCOMPLETE (not all of f1-f8 ran) |" in out
    assert "| Value | INCOMPLETE (no baseline runs on f6-f8) |" in out


def test_a_run_without_its_query_log_fails_plumbing(tmp_path):
    run = tmp_path / "f1__full__1"
    shutil.copytree(os.path.join(RESULTS, "f1__full__1"), run)
    assert acceptance.plumbing_ok(str(run)) == []
    os.remove(run / "queries.log")
    reasons = acceptance.plumbing_ok(str(run))
    assert reasons[0] == "no logged query ran" and reasons[-1].startswith("verify_readout:")


def test_a_missing_directory_is_a_usage_error(tmp_path):
    assert acceptance.main([str(tmp_path / "missing")]) == 3


def test_a_harness_that_did_not_run_is_skipped_not_fatal(capsys):
    assert acceptance.main([RESULTS, os.path.join(ROOT, "eval", "results", "nope-cursor-*")]) == 0
    captured = capsys.readouterr()
    assert "skipping" in captured.err and "| Plumbing | PASS |" in captured.out
