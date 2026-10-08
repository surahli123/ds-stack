"""The readout parser extracts graded fields; the grader applies gold and the pass rule."""

import json
import os

import grade
from readout import parse

GOOD = """Some analysis first.

## Answer
Headline: **-0.1 pp** (95% CI -0.4 to 0.2)
Ranker v2 did not cause the drop; mobile's share grew.

## What it means for the rollback decision
Don't roll back.

## Why we believe it
- Alternatives considered:
  - **Mix-shift (mobile share 40% -> 55%)**: ruled in by mix_shift check [measured]
  - Ranker v2: ruled out by flat within-platform CTR [measured]
- Checks run:
  - `mix_shift`: fail mix share 100%
  - completeness: pass all days loaded

## Caveats, and what would change the answer
- None material.
"""

ABSTAIN = """## Answer
Headline: can’t tell
Yesterday is only partly loaded.

## Why we believe it
- Checks run:
  - completeness: fail 42% of trailing median
"""


def test_parse_extracts_headline_interval_alternatives_and_checks():
    readout = parse(GOOD)
    assert readout.ok
    assert readout.value == -0.1 and readout.interval == (-0.4, 0.2)
    assert readout.alternatives[0]["verdict"] == "in" and "mix" in readout.alternatives[0]["name"]
    assert readout.alternatives[0]["label"] == "measured"
    assert readout.checks == {"mix_shift": "fail", "completeness": "pass"}


def test_parse_recognises_abstention_with_curly_apostrophe():
    readout = parse(ABSTAIN)
    assert readout.ok and readout.abstained and readout.value is None


def test_parse_reports_missing_parts_instead_of_guessing():
    assert not parse("The answer is -2.1 pp.").ok
    assert not parse("## Answer\nCTR fell 2.1 pp\n").ok
    assert not parse("## Answer\nHeadline: about the same\n").ok


def test_parse_handles_unicode_minus_and_code_fences():
    readout = parse("```\n## Answer\nHeadline: −1.8 pp\n```")
    assert readout.value == -1.8


def gold(**overrides):
    base = {"kind": "error", "accept_values": [{"value": 0.0, "tol": 0.3}], "accept_abstain": False,
            "must_rule_in": [["mix"]], "must_not_rule_in": [["ranker"]]}
    return {**base, **overrides}


def test_grade_accepts_right_number_and_right_cause():
    assert grade.grade_readout(parse(GOOD), gold())[0]


def test_grade_rejects_the_naive_number():
    readout = parse(GOOD.replace("-0.1 pp", "-2.1 pp"))
    correct, reason, _ = grade.grade_readout(readout, gold())
    assert not correct and "outside" in reason


def test_grade_rejects_a_ruled_in_false_cause():
    readout = parse(GOOD.replace("Ranker v2: ruled out", "Ranker v2: ruled in"))
    assert not grade.grade_readout(readout, gold())[0]


def test_grade_counts_abstaining_on_a_clean_case_as_a_false_alarm():
    correct, _, miss = grade.grade_readout(parse(ABSTAIN), gold(kind="clean", must_rule_in=[]))
    assert not correct and miss == "false_alarm"


def test_grade_counts_a_number_on_an_abstain_only_case():
    correct, _, miss = grade.grade_readout(parse(GOOD), gold(kind="abstain", accept_values=[], accept_abstain=True))
    assert not correct and miss == "answered_abstain_case"


def test_grade_accepts_abstention_where_allowed():
    assert grade.grade_readout(parse(ABSTAIN), gold(kind="abstain", accept_abstain=True))[0]


def make_run(tmp_path, fixture, arm, run, text, checks=None, transcript=""):
    run_dir = tmp_path / f"{fixture}__{arm}__{run}"
    run_dir.mkdir()
    (run_dir / "meta.json").write_text(json.dumps({"fixture": fixture, "arm": arm, "run": run, "cost_usd": 0.1}))
    (run_dir / "result.md").write_text(text)
    (run_dir / "transcript.jsonl").write_text(transcript)
    if checks:
        (run_dir / ".." / f"{fixture}__{arm}__{run}" / "checks.log").write_text(
            "\n".join(json.dumps({"check": c, "status": s}) for c, s in checks))


def test_grade_dir_flags_contamination_and_reads_the_check_log(tmp_path):
    make_run(tmp_path, "f5", "full", 1, ABSTAIN, checks=[("srm", "fail")])
    make_run(tmp_path, "f5", "baseline", 1, ABSTAIN, transcript='{"cmd": "cat /home/user/ds-stack/eval/gold/f5.json"}')
    runs = {r["arm"]: r for r in grade.grade_dir(str(tmp_path))}
    assert runs["full"]["correct"] and runs["full"]["checks_ran"] == {"srm": ["fail"]}
    assert not runs["baseline"]["correct"] and runs["baseline"]["miss"] == "contaminated"


def test_pass_rule_refuses_a_verdict_below_the_minimum_n(tmp_path):
    with open(os.path.join(grade.HERE, "pass_rule.json")) as handle:
        rule = json.load(handle)
    runs = [{"fixture": "f5", "arm": arm, "run": i, "correct": True, "miss": None, "checks_ran": {},
             "skill_read": False, "cost_usd": 0, "kind": "abstain", "headline": "can't tell"}
            for arm in ("baseline", "full") for i in (1, 2, 3)]
    *_, verdict = grade.summarize(runs, rule)
    assert verdict["verdict"].startswith("INSUFFICIENT_N")
