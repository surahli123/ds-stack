"""smoke_check gives one pass/fail line per piece of a ds-mode run, judged from its files."""

import os
import shutil

import pytest
import smoke_check
from conftest import ROOT

RUN = os.path.join(ROOT, "eval", "results", "2026-10-13-seed", "f1__full__1")


@pytest.fixture
def run_dir(tmp_path):
    shutil.copy(os.path.join(RUN, "result.md"), tmp_path / "readout.md")
    shutil.copy(os.path.join(RUN, "queries.log"), tmp_path / ".ds-queries.log")
    shutil.copy(os.path.join(RUN, "checks.log"), tmp_path / ".ds-checks.log")
    return tmp_path


def test_a_traced_correct_run_passes(run_dir, capsys):
    assert smoke_check.main([str(run_dir)]) == 0
    assert capsys.readouterr().out.strip().endswith("PASS")


def test_a_wrong_answer_fails_on_the_gold_check_only(run_dir):
    results = smoke_check.check(str(run_dir), "f3")
    assert [ok for ok, _ in results] == [True, True, True, True, False]


def test_missing_logs_fail_the_trace(run_dir):
    os.remove(run_dir / ".ds-queries.log")
    results = dict((line.split(":")[0], ok) for ok, line in smoke_check.check(str(run_dir), "f1"))
    assert not results["no logged queries"] and not results["verify_readout (trace only)"]


def test_no_readout_and_no_directory(tmp_path):
    assert smoke_check.check(str(tmp_path), "f1")[0] == (False, "readout.md is missing: the agent didn't finish ds-mode step 7")
    assert smoke_check.main([str(tmp_path / "missing")]) == 3
