"""ds-verify checks a ds-mode readout against its logs, its data and the metric overlay, without gold."""

import hashlib
import json
import os
import shutil
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
                      "", "## Provenance", "- Metric: CTR = clicks / searches, from metrics.json",
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
    assert ("fail", "srm#1 failed and the readout doesn't report it: 51.2/48.8 against 50/50") in statuses(silent, "flags")


def test_the_overlay_definition_must_be_used(tmp_path):
    (tmp_path / "metrics.json").write_text(json.dumps({
        "ctr": {"numerator": "searches_with_click", "denominator": "searches_with_results"},
        "search_purchase_rate": {"available": False, "note": "orders aren't in this warehouse"}}))
    assert statuses(readout(), "overlay", "What was CTR?", overlay=str(tmp_path))[0][0] == "pass"
    own = readout().replace("from metrics.json", "stated here [guess]")
    assert statuses(own, "overlay", "What was CTR?", overlay=str(tmp_path))[0][0] == "fail"
    assert statuses(readout(), "overlay", "What share of searches led to a purchase?", overlay=str(tmp_path))[-1][0] == "fail"
    abstains = readout(headline="Headline: can't tell")
    assert statuses(abstains, "overlay", "What share of searches led to a purchase?", overlay=str(tmp_path))[-1][0] == "pass"
    assert statuses(readout(), "overlay", "What was CTR?", overlay=None)[0][0] == "skipped"


def test_a_derived_number_goes_on_the_check_by_hand_list():
    derived = readout().replace("- Observed: -1.36 pp", "- Observed: -1.37 pp").replace("Headline: -1.36", "Headline: -1.37")
    report = ds_verify.run_all(derived, QUERIES, CHECKS + [{"id": "x#1"}], None, None, "")
    rendered = ds_verify.render(report)
    assert "Check by hand" in rendered and "-1.37 [q1]" in rendered


# --- the command line ----------------------------------------------------------------------------------------

def test_cli_exit_codes_and_json(tmp_path):
    ok = run("2026-10-14-claude-en", "f1__full__2")
    proc = subprocess.run([sys.executable, SCRIPT, "--run-dir", ok, "--db", os.path.join(FIXTURES, "f1", "warehouse.db"),
                           "--json", str(tmp_path / "r.json")], capture_output=True, text=True)
    assert proc.returncode == 0 and proc.stdout.startswith("ds-verify: pass")
    assert json.loads((tmp_path / "r.json").read_text())["verdict"] == "pass"
    bad = run("2026-10-14-claude-zh", "f2__full__1")
    proc = subprocess.run([sys.executable, SCRIPT, "--run-dir", bad, "--request", os.path.join(FIXTURES, "f2", "task.md")],
                          capture_output=True, text=True)
    assert proc.returncode == 1 and "asks for percent" in proc.stdout
    assert subprocess.run([sys.executable, SCRIPT], capture_output=True).returncode == 3
