"""Regressions from the 2026-10-14 local Codex smoke run (docs/reports/2026-10-14-local-f1-smoke on
branch docs/local-f1-smoke-20261014): a Chinese readout must never grade its 95% CI level as the estimate."""

import os
import shutil

import grade
import smoke_check
import verify_readout as vr
from conftest import ROOT
from readout import parse

DATA = os.path.join(ROOT, "tests", "data")
ZH = open(os.path.join(DATA, "f1-codex-zh-readout.md")).read()


def test_the_saved_chinese_headline_reads_the_estimate_and_interval_not_95():
    readout = parse(ZH)
    assert readout.value_in("pp") == -2.0968
    assert readout.interval == (-2.248, -1.946)
    assert all(number != 95 for number, _ in readout.candidates)


def test_translated_alternatives_fail_loudly_instead_of_vanishing():
    readout = parse(ZH)
    assert len(readout.dropped) == 5 and not readout.alternatives
    assert readout.errors == ["none of the 5 alternative lines says 'ruled in' or 'ruled out'"]
    correct, reason, kind = grade.grade_readout(readout, grade.load_gold("f1"))
    assert not correct and kind == "unparseable" and "ruled in" in reason


def test_chinese_prose_with_the_fixed_english_words_parses():
    text = ZH.replace("流量构成：纳入解释。", "流量构成: ruled in.").replace("v2：不能确认或排除因果影响。", "v2: ruled out as the main driver.")
    readout = parse(text)
    assert readout.ok and [a["verdict"] for a in readout.alternatives] == ["in", "out"]


def test_full_width_punctuation_unicode_minus_and_bold():
    readout = parse("## Answer\nHeadline: **−2.10 pp**（95% CI：−2.25 至 −1.95）\n")
    assert readout.value_in("pp") == -2.10 and readout.interval == (-2.25, -1.95)
    readout = parse("## Answer\nHeadline: -0.00 个百分点（95% 置信区间 -0.15 至 0.15），假设 v2 没有改变流量构成\n")
    assert readout.value_in("pp") == 0.0 and readout.interval == (-0.15, 0.15)


def test_confidence_levels_dates_and_versions_are_not_estimates():
    readout = parse("## Answer\nHeadline: about 0 pp attributable to v2 (95% interval -0.15 to 0.15), 2026-09-28 rollout\n")
    assert readout.value_in("pp") == 0.0


def test_a_number_in_the_wrong_unit_is_never_taken():
    readout = parse("## Answer\nHeadline: 95% of the drop is mix\n")
    assert readout.value_in("pp") is None
    correct, reason, kind = grade.grade_readout(readout, grade.load_gold("f1"))
    assert not correct and reason == "headline has no number in pp" and kind == "unparseable"


def test_verify_readout_accepts_the_saved_run_and_its_logs():
    queries = vr.read_jsonl(os.path.join(DATA, "f1-codex-zh-queries.jsonl"))
    checks = vr.read_jsonl(os.path.join(DATA, "f1-codex-zh-checks.jsonl"))
    problems, stats, _ = vr.verify(ZH, queries, checks)
    assert problems == [] and stats["checks"] == {"mix_shift#1", "mix_shift#3", "completeness#1", "completeness#2"}
    assert vr.numbers_in("（95% 置信区间 −0.15 至 0.15）[q1]") == ["−0.15", "0.15"]


def test_smoke_check_counts_completed_checks_and_names_the_failure(tmp_path):
    shutil.copy(os.path.join(DATA, "f1-codex-zh-readout.md"), tmp_path / "readout.md")
    shutil.copy(os.path.join(DATA, "f1-codex-zh-queries.jsonl"), tmp_path / ".ds-queries.log")
    shutil.copy(os.path.join(DATA, "f1-codex-zh-checks.jsonl"), tmp_path / ".ds-checks.log")
    lines = [line for _, line in smoke_check.check(str(tmp_path), "f1")]
    assert "4 of 4 completed checks name their source query (1 more could not run, kept in the log)" in lines
    assert lines[-1].startswith("answer vs gold: unparseable: none of the 5 alternative lines")


THREE_LINES = """## Answer
Headline: -2.10 pp (95% CI -2.25 to -1.95) [check:mix_shift#1]
Overall CTR fell 2.10 pp; v2's effect isn't identified without a holdout. [check:mix_shift#1]
- Observed: -2.10 pp (95% CI -2.25 to -1.95) [check:mix_shift#1]
- Adjusted: -0.00 pp (95% CI -0.15 to 0.15), holding the platform mix fixed [check:mix_shift#1]
- Causal effect: not identified (a concurrent holdout would identify it)

## Why we believe it
- Alternatives considered:
  - Mix-shift: ruled in by mobile share rising from 40% to 55% [check:mix_shift#1] [measured]
  - Ranker v2: ruled out as the driver of the drop [check:mix_shift#1] [inferred]
- Checks run:
  - mix_shift (coarse): flag mix share 1.00 [check:mix_shift#2]
"""


def test_a_full_rollout_readout_can_headline_the_observed_drop_and_still_be_graded_on_the_adjusted_line():
    readout = parse(THREE_LINES)
    assert readout.ok and readout.estimates["causal effect"]["status"] == "not identified"
    assert readout.estimate_in("adjusted", "pp") == 0.0 and readout.estimate_in("observed", "pp") == -2.10
    assert grade.grade_readout(readout, grade.load_gold("f1"))[0]


def test_a_number_for_an_unidentified_causal_effect_fails():
    text = THREE_LINES.replace("- Causal effect: not identified (a concurrent holdout would identify it)",
                               "- Causal effect: -0.00 pp, from the decomposition")
    correct, reason, _ = grade.grade_readout(parse(text), grade.load_gold("f1"))
    assert not correct and reason == "gives a number for a causal effect the design can't identify"


def test_an_old_format_readout_is_graded_on_its_headline():
    text = "\n".join(line for line in THREE_LINES.splitlines() if not line.startswith(("- Observed", "- Adjusted", "- Causal")))
    correct, reason, _ = grade.grade_readout(parse(text), grade.load_gold("f1"))
    assert not correct and reason == "headline -2.1 outside 0±0.3"


def test_two_estimates_in_one_headline_are_a_parse_error():
    readout = parse("## Answer\nHeadline: 0.0 pp attributable to v2; the overall change was -2.1 pp (95% CI -2.2 to -2.0)\n")
    assert readout.errors == ["headline gives 2 different estimates before its parenthesis; give one"]


def test_a_check_label_with_a_qualifier_is_still_read():
    assert parse(THREE_LINES).checks == {"mix_shift": "flag"}
    assert parse(ZH).checks["mix_shift"] == "flag"


def test_a_translated_abstention_fails_explicitly():
    readout = parse("## Answer\nHeadline: 无法判断\n")
    assert not readout.ok and not readout.abstained
    assert parse("## Answer\nHeadline: can't tell\n昨天的数据只加载了一部分。\n").abstained
