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
    base = {"kind": "error", "unit": "pp", "accept_values": [{"value": 0.0, "tol": 0.3}], "accept_abstain": False,
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
    make_run(tmp_path, "f5", "full", 1, ABSTAIN, checks=[("srm", "fail")], transcript='{"type": "result"}')
    make_run(tmp_path, "f5", "baseline", 1, ABSTAIN, transcript='{"cmd": "cat /home/user/ds-stack/eval/gold/f5.json"}')
    runs = {r["arm"]: r for r in grade.grade_dir(str(tmp_path))}
    assert runs["full"]["correct"] and runs["full"]["checks_ran"] == {"srm": ["fail"]}
    assert not runs["baseline"]["correct"] and runs["baseline"]["miss"] == "contaminated"


def test_pass_rule_refuses_a_verdict_below_the_minimum_n(tmp_path):
    with open(os.path.join(grade.HERE, "pass_rule.json")) as handle:
        rule = json.load(handle)
    runs = [run_row("f5", arm, i, True, kind="abstain") for arm in ("baseline", "full") for i in (1, 2, 3)]
    *_, verdict = grade.summarize(runs, rule)
    assert verdict["verdict"].startswith("INSUFFICIENT_N")


# Regressions from the adversarial review: phrasings that used to misparse.

def answer(headline):
    return f"## Answer\nHeadline: {headline}\n"


def test_headline_ignores_identifiers_and_dates():
    assert parse(answer("v2 accounts for 0.0 pp of the -2.1 pp drop")).value_in("pp") == 0.0
    assert parse(answer("Ranker v3 caused -1.8 pp")).value_in("pp") == -1.8
    assert parse(answer("navigational CTR in 2026-W40 was 55.0%")).value_in("percent") == 55.0
    assert parse(answer("on 2026-10-07 CTR was flat at +0.0 pp")).value_in("pp") == 0.0


def test_headline_reads_direction_words_as_sign():
    assert parse(answer("CTR fell 1.8 pp")).value_in("pp") == -1.8
    assert parse(answer("CTR rose 1.2 pp")).value_in("pp") == 1.2


def test_headline_prefers_the_gold_unit():
    readout = parse(answer("CTR fell from 30.4% to 28.6% (-1.8 pp)"))
    assert readout.value_in("pp") == -1.8
    assert parse(answer("-1.8 pp, from 30.4% to 28.6%")).value_in("pp") == -1.8


def test_headline_abstention_without_the_exact_phrase():
    for text in ("insufficient data to say", "No reliable estimate (SRM)", "Cannot tell yet", "can't tell (need 14 more days)"):
        readout = parse(answer(text))
        assert readout.ok and readout.abstained, text


def test_other_heading_levels_parse():
    assert parse("### Answer\nHeadline: -0.1 pp\n").value == -0.1


def test_alternative_variants_parse_and_negations_are_undetermined():
    text = answer("-0.1 pp") + """
## Why we believe it
- Alternatives considered:
  - Mix-shift — ruled in by the decomposition [measured]
  - Seasonality: ruled-out, same weekdays [measured]
  - Ruled out: logging change, no schema diff [inferred]
  - Treatment effect: not ruled in [inferred]
  - Mix-shift: in.
"""
    readout = parse(text)
    verdicts = {a["name"]: a["verdict"] for a in readout.alternatives}
    assert verdicts["mix-shift"] == "in"
    assert verdicts["seasonality"] == "out"
    assert verdicts["logging change"] == "out"
    assert verdicts["treatment effect"] == "undetermined"
    assert readout.dropped == ["- Mix-shift: in."]


def test_a_mix_line_naming_the_launch_is_not_a_false_cause():
    text = answer("0.0 pp") + "\n## Why we believe it\n- Mix-shift after the v2 launch: ruled in [measured]\n"
    g = gold(true_cause_words=["mix"], must_not_rule_in=[["ranker", "v2"]])
    assert grade.grade_readout(parse(text), g)[0]


def run_row(fixture, arm, run, correct, miss=None, kind="clean"):
    return {"fixture": fixture, "arm": arm, "run": run, "correct": correct, "miss": miss, "checks_ran": {},
            "skill_read": False, "cost_usd": 0, "kind": kind, "headline": "", "dropped_alternative_lines": 0}


RULE = {"min_holdout_fixtures": 2, "runs_per_fixture": 3, "margin_vs_baseline": 1,
        "max_extra_false_alarms_vs_baseline": 0, "max_abstain_cases_answered_with_number": 0}


def test_majority_is_two_of_three_and_one_noisy_run_is_not_a_false_alarm():
    runs = [run_row("c1", "full", 1, True), run_row("c1", "full", 2, True), run_row("c1", "full", 3, False, "false_alarm"),
            run_row("c2", "full", 1, True), run_row("c2", "full", 2, False, "miss"), run_row("c2", "full", 3, False, "miss")]
    _, _, cells, per_arm, _ = grade.summarize(runs, RULE)
    assert cells[("c1", "full")]["outcome"] == "correct"
    assert cells[("c2", "full")]["outcome"] == "miss"
    assert per_arm["full"]["fixtures_false_alarm"] == 0


def test_cells_without_the_registered_run_count_are_incomplete():
    runs = [run_row("c1", "full", 1, True), run_row("c1", "full", 2, True)]
    *_, verdict = grade.summarize(runs, RULE)
    assert verdict["verdict"].startswith("INCOMPLETE")


def test_pass_rule_clauses():
    base = {"fixtures_correct": 1, "fixtures_false_alarm": 0, "fixtures_abstain_answered": 0}
    assert grade.passes({**base, "fixtures_correct": 2}, base, RULE)
    assert not grade.passes(base, base, RULE)
    assert not grade.passes({**base, "fixtures_correct": 2, "fixtures_false_alarm": 1}, base, RULE)
    assert not grade.passes({**base, "fixtures_correct": 2, "fixtures_abstain_answered": 1}, base, RULE)


def test_a_missing_transcript_counts_as_contaminated(tmp_path):
    run_dir = tmp_path / "f5__full__1"
    run_dir.mkdir()
    assert grade.contamination(str(run_dir)).startswith("no transcript")


CURRENT_FORMAT = """## Answer
Headline: -2.1 pp (95% CI -2.6 to -1.6)
CTR fell 2.1 pp; about 70% of it is mobile's growing share.

## What it means for the rollback decision
The interval excludes the 0.5 pp the rollback needs, so don't roll back.

## Why we believe it
- Alternatives considered:
  - Mix-shift: ruled in by mix_shift [measured]
- Checks run:
  - mix_shift: flag mix-dominant: overall change -2.10 pp
  - completeness: could not run no earlier periods

## Caveats, and what would change the answer
- None material.

## Provenance
- Metric: CTR, from metrics.json
- Data: search_daily, through 2026-10-07
- Queries and checks: .ds-checks.log
"""


def test_the_skill_readout_format_parses_with_flag_and_provenance():
    readout = parse(CURRENT_FORMAT)
    assert readout.ok and readout.value == -2.1 and readout.interval == (-2.6, -1.6)
    assert readout.checks == {"mix_shift": "flag", "completeness": "could_not_run"}
    assert "provenance" in readout.sections and len(readout.alternatives) == 1


def test_no_interval_with_a_reason_keeps_the_number():
    readout = parse("## Answer\nHeadline: +3.4% (no interval: a single total from the dashboard)\n")
    assert readout.ok and readout.value == 3.4 and readout.interval is None
