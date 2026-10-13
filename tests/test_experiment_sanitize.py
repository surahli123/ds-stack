"""port/sanitize.py: material sanitized on the work laptop must give the same answers
at home (call, verdicts, checks, readiness, mechanisms), and nothing it was told to
remove may survive."""

import contextlib
import io
import json
import os
import shutil
import sys
from datetime import date

import pytest

from conftest import ROOT

sys.path.insert(0, os.path.join(ROOT, "skills", "ds-experiment", "port"))

import adapters  # noqa: E402
import checks  # noqa: E402
import decide  # noqa: E402
import explain  # noqa: E402
import sanitize  # noqa: E402

EVAL = os.path.join(ROOT, "eval", "experiment")
CASES = [os.path.join(sub, c) for sub in ("cases", "mechanisms", "regressions", "regressions_deepdive")
         for c in sorted(os.listdir(os.path.join(EVAL, sub)))]
STANDARDS = os.path.join(ROOT, "overlay.example", "standards.json")


@pytest.fixture(autouse=True)
def quiet_log(monkeypatch, tmp_path):
    monkeypatch.setenv("DS_CHECKS_LOG", str(tmp_path / "checks.log"))
    monkeypatch.delenv("DS_DENYLIST", raising=False)
    monkeypatch.delenv("DS_OVERLAY_DIR", raising=False)


def answers(d, overlay=None, groups_to=None):
    plan = json.load(open(os.path.join(d, "run.json"))) if os.path.exists(os.path.join(d, "run.json")) else {}
    pulses = plan.get("pulse", ["pulse.json"])
    groups = [p.split(":")[1] for p in pulses] if all(":" in p for p in pulses) else None
    if groups and groups_to:
        groups = [groups_to.get(g, g) for g in groups]
    sc = adapters.statsig_pulse([adapters.load_json(os.path.join(d, p.split(":")[0])) for p in pulses],
                                adapters.load_json(os.path.join(d, "request.json")), groups)
    cfg = adapters.statsig_config(adapters.load_json(os.path.join(d, "experiment.json")),
                                  adapters.load_json(os.path.join(d, "audit_logs.json")))
    pre = adapters.load_json(os.path.join(d, "prereg.json"))
    daily = os.path.join(d, plan.get("daily", "daily_by_exposure_day.json"))
    std = adapters.load_json(os.path.join(overlay, "standards.json") if overlay else STANDARDS)
    try:
        dec = decide.decide(sc, pre, cfg, std, adapters.load_json(daily) if os.path.exists(daily) else None)
    except decide.InputError:
        return {"error": "InputError"}
    ex = explain.explain(dec, sc, pre, explain.load_library(overlay), None, cfg)
    metrics = [m for c in sc["comparisons"] for m in c["metrics"]]
    return {"call": dec["call"], "decider": dec["decider"].get("metric") or dec["decider"].get("check"),
            "verdicts": [(v["metric"], v["role"], v["verdict"]) for v in dec["verdicts"]],
            "checks": [(c["check"], c["status"]) for c in dec["checks"]],
            "significant": [(m["metric"], m["rel_ci"][0] > 0 or m["rel_ci"][1] < 0) for m in metrics if m.get("rel_ci")],
            "readiness": ex["readiness"]["verdict"],
            "mechanisms": [(q["metric"], q["candidates"][0] if q["candidates"] else None) for q in ex["questions"]],
            "patterns": [p["id"] for p in ex["patterns"]]}


def real_names(obj, reverse):
    """Tokens back to names, compared the way decide.py matches names."""
    if isinstance(obj, str):
        for token in sorted(reverse, key=len, reverse=True):
            obj = obj.replace(token, reverse[token])
        return decide._key(obj)
    if isinstance(obj, (list, tuple)):
        out = [real_names(x, reverse) for x in obj]
        return sorted(out, key=repr) if isinstance(obj, list) else tuple(out)
    if isinstance(obj, dict):
        return {k: real_names(v, reverse) for k, v in obj.items()}
    return obj


def run_sanitize(files, out, overlay, *extra):
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()) as err:
        rc = sanitize.main([str(f) for f in files] + ["--out-dir", str(out), "--overlay", str(overlay), "--seed", "7",
                                                       *extra])
    return rc, err.getvalue()


def sanitize_case(d, tmp_path, *extra):
    overlay, out, home = tmp_path / "overlay", tmp_path / "out", tmp_path / "home"
    overlay.mkdir()
    home.mkdir()
    (overlay / "denylist.txt").write_text("acmecorp\n")
    shutil.copy(STANDARDS, tmp_path / "standards.json")
    files = [os.path.join(d, f) for f in os.listdir(d) if f.endswith(".json") and f not in ("expected.json", "run.json")]
    rc, err = run_sanitize(files + [tmp_path / "standards.json"], out, overlay, *extra)
    assert rc == 0, err
    if os.path.exists(os.path.join(d, "run.json")):
        shutil.copy(os.path.join(d, "run.json"), out / "run.json")
    (out / "standards.json").rename(home / "standards.json")
    if (out / "metric_families.json").exists():
        (out / "metric_families.json").rename(home / "metric_families.json")
    key = json.load(open(overlay / "sanitize_key.json"))
    reverse = {}
    for real, token in key["strings"].items():
        reverse.setdefault(token, real)
    return out, home, key, reverse


@pytest.mark.parametrize("cid", CASES)
def test_sanitized_case_gives_the_same_answers(cid, tmp_path):
    d = os.path.join(EVAL, cid)
    out, home, key, reverse = sanitize_case(d, tmp_path)
    before = real_names(answers(d), {})
    after = real_names(answers(str(out), str(home), key["strings"]), reverse)
    assert after == before


@pytest.mark.parametrize("cid", ["cases/c1", "cases/c4", "mechanisms/m3", "regressions/f07_multi_arm"])
def test_scaled_lifts_keep_signs_significance_and_checks(cid, tmp_path):
    d = os.path.join(EVAL, cid)
    out, home, key, reverse = sanitize_case(d, tmp_path, "--scale-lifts")
    assert key["factors"]["lift"] != 1
    before, after = answers(d), answers(str(out), str(home), key["strings"])
    for field in ("significant", "checks"):
        assert real_names(after[field], reverse) == real_names(before[field], {})


def test_counts_scale_without_changing_the_split_test():
    counts, shares = [1_010_000, 990_000], [50, 50]
    _, p_before = checks.chi_square_p(counts, [0.5, 0.5])
    new = sanitize.scale_counts(counts, shares, 0.73)
    _, p_after = checks.chi_square_p(new, [0.5, 0.5])
    assert abs(sum(new) - 0.73 * sum(counts)) <= 1
    assert p_after == pytest.approx(p_before, rel=0.01)
    three = sanitize.scale_counts([500_400, 249_100, 251_000], [50, 25, 25], 1.3)
    assert checks.chi_square_p(three, [0.5, 0.25, 0.25])[1] == pytest.approx(
        checks.chi_square_p([500_400, 249_100, 251_000], [0.5, 0.25, 0.25])[1], rel=0.01)


def write_inputs(tmp_path):
    src = tmp_path / "in"
    shutil.copytree(os.path.join(EVAL, "cases", "c1"), src)
    (src / "task.md").unlink()
    (src / "readout.md").write_text(
        "# Ranker v7 readout (AcmeCorp search, Zephyr answers)\n"
        "Owner: jane.doe@acmecorp.com, @jdoe. Dashboard: https://statsig.example.com/exp/ranker_v7\n"
        "Ran 2026-09-10 to Sep 24, 2026 on 2,013,442 users ($1.2M at stake, 450 ms p95).\n"
        "Successful Search Rate rose 0.81% (95% CI 0.41% to 1.21%) over 14 days in group g_test.\n"
        "Run 3f2a9c1e5b7d4a6f8e9c0b1a2d3e4f5a.\n")
    (src / "scorecard.csv").write_text(
        "Metric,Variant,Relative Delta %,Control Mean,Control Units,P-Value\n"
        "Successful Search Rate,Test,0.81%,0.412,\"1,000,000\",<0.001\n"
        "Zephyr Answer CTR,Test,-1.2%,0.0831,\"1,000,000\",0.003\n")
    overlay = tmp_path / "overlay"
    overlay.mkdir()
    (overlay / "denylist.txt").write_text("acmecorp\nzephyr\n")
    (tmp_path / "names.txt").write_text("AcmeCorp\nZephyr answers\n")
    return sorted(src.iterdir()), overlay


def test_denylist_blocks_and_writes_nothing(tmp_path):
    files, overlay = write_inputs(tmp_path)
    rc, err = run_sanitize(files, tmp_path / "out", overlay)
    assert rc == 1 and "readout.md: acmecorp, zephyr" in err
    assert not (tmp_path / "out").exists() and not (overlay / "sanitize_key.json").exists()


def test_refuses_without_a_denylist_or_with_the_key_in_the_output(tmp_path):
    files, overlay = write_inputs(tmp_path)
    (overlay / "denylist.txt").unlink()
    assert run_sanitize(files, tmp_path / "out", overlay)[0] == 2
    (overlay / "denylist.txt").write_text("acmecorp\n")
    rc, err = run_sanitize(files, tmp_path / "out", overlay, "--key", str(tmp_path / "out" / "key.json"))
    assert rc == 2 and "output folder" in err


def test_text_and_csv_are_scrubbed(tmp_path):
    files, overlay = write_inputs(tmp_path)
    rc, err = run_sanitize(files, tmp_path / "out", overlay, "--names", str(tmp_path / "names.txt"))
    assert rc == 0, err
    text = (tmp_path / "out" / "readout.md").read_text()
    for gone in ("Ranker v7", "jane.doe", "@jdoe", "statsig.example", "3f2a9c1e", "2,013,442", "$1.2M",
                 "Successful Search Rate", "g_test", "450 ms"):
        assert gone not in text, gone
    for kept in ("experiment_1", "<email>", "<url>", "<handle>", "<id>", "success_metric_1", "0.81%",
                 "(95% CI 0.41% to 1.21%)", "14 days"):
        assert kept in text, kept
    shift = json.load(open(overlay / "sanitize_key.json"))["date_shift_days"]
    assert shift % 7 == 0 and shift < 0
    moved = date(2026, 9, 10).toordinal() + shift
    assert date.fromordinal(moved).isoformat() in text  # weekday kept
    table = (tmp_path / "out" / "scorecard.csv").read_text().splitlines()
    assert table[0] == "Metric,Variant,Relative Delta %,Control Mean,Control Units,P-Value"
    assert table[1].startswith("success_metric_1,Test,0.") and table[2].startswith("ctr_metric_")
    assert "<0.00" in table[1] and "1,000,000" not in table[1]
    families = json.load(open(tmp_path / "out" / "metric_families.json"))
    assert "success_metric_1" in families["success"]


def test_tokens_are_stable_across_runs(tmp_path):
    files, overlay = write_inputs(tmp_path)
    names = str(tmp_path / "names.txt")
    assert run_sanitize(files, tmp_path / "a", overlay, "--names", names)[0] == 0
    first = json.load(open(overlay / "sanitize_key.json"))
    assert run_sanitize(files[:2], tmp_path / "b", overlay, "--names", names)[0] == 0
    second = json.load(open(overlay / "sanitize_key.json"))
    assert second["strings"] == first["strings"] and second["factors"] == first["factors"]
    name = os.path.basename(str(files[0]))
    assert (tmp_path / "a" / name).read_text() == (tmp_path / "b" / name).read_text()
