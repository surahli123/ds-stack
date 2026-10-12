"""The adversarial pressure-test cases: run the CLIs as the skill tells the model to, and
compare with expected.json (a call and decider, or a refusal with a hint)."""

import json
import os
import subprocess
import sys

import pytest

from conftest import ROOT

TOOLS = os.path.join(ROOT, "skills", "ds-experiment", "tools")
CASES = os.path.join(ROOT, "eval", "experiment", "regressions")
STANDARDS = os.path.join(ROOT, "overlay.example", "standards.json")


def run(args, cwd, env):
    return subprocess.run([sys.executable] + args, cwd=cwd, capture_output=True, text=True, env=env)


@pytest.mark.parametrize("cid", sorted(os.listdir(CASES)))
def test_regression_case(cid, tmp_path):
    case = os.path.join(CASES, cid)
    expected = json.load(open(os.path.join(case, "expected.json")))
    plan = json.load(open(os.path.join(case, "run.json"))) if os.path.exists(os.path.join(case, "run.json")) else {}
    env = {**os.environ, "DS_CHECKS_LOG": str(tmp_path / "log")}
    args = [os.path.join(TOOLS, "normalize.py")]
    for pulse in plan.get("pulse", ["pulse.json"]):
        args += ["--pulse", pulse]
    args += ["--request", "request.json", "--experiment", "experiment.json", "--audit", "audit_logs.json",
             "--out-dir", str(tmp_path)]
    proc = run(args, case, env)
    assert proc.returncode == 0, proc.stderr
    raw = json.load(open(os.path.join(case, "experiment.json")))["data"]
    if raw.get("exposures"):
        config = json.load(open(tmp_path / "config.json"))
        config["exposures"] = raw["exposures"]
        (tmp_path / "config.json").write_text(json.dumps(config))
    args = [os.path.join(TOOLS, "decide.py"), "--scorecard", str(tmp_path / "scorecard.json"),
            "--config", str(tmp_path / "config.json"), "--prereg", "prereg.json", "--standards", STANDARDS,
            "--out", str(tmp_path / "decision.json")]
    daily = plan.get("daily", "daily_by_exposure_day.json")
    if os.path.exists(os.path.join(case, daily)):
        args += ["--daily", daily]
    proc = run(args, case, env)
    if "exit" in expected:
        assert proc.returncode == expected["exit"] and expected["message"] in proc.stderr, proc.stderr
        return
    assert proc.returncode == 0, proc.stderr
    decision = json.load(open(tmp_path / "decision.json"))
    decider = decision["decider"].get("metric") or decision["decider"].get("check")
    assert (decision["call"], decider) == (expected["call"], expected["decider"]), decision["reason"]
