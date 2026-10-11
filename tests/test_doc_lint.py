"""doc_lint passes a clean doc and fails each planted structure, format or length mistake."""

import os
import subprocess
import sys

import doc_lint
from conftest import ROOT

LINT = os.path.join(ROOT, "skills", "doc-tighten", "tools", "doc_lint.py")

CLEAN = """# Ranker v2 rollout readout

## Answer
Keep ranker v2. The 2.1 pp CTR drop after launch comes from more mobile traffic, not from the ranker: CTR inside each platform did not move.

## What it means
Rolling back would not recover CTR. The open question is why mobile share rose from 40% to 55%, which belongs to the growth team.

## Evidence
Within-platform CTR was 36.0% on desktop and 22.0% on mobile in both weeks. A mix decomposition attributes all of the change to the platform shift. Every day in both weeks is fully loaded.

## Caveats
This is a before and after comparison with no holdout, so a ranker effect smaller than 0.3 pp would not show.
"""


def rules(text, doc_type="readout"):
    found, _ = doc_lint.check(text, doc_type)
    return {f.rule for f in found}


def test_clean_doc_passes():
    found, words = doc_lint.check(CLEAN, "readout")
    assert found == [] and words < 600


def test_answer_buried_under_method_fails():
    method = "## Data sources\n" + "We pulled logs from three tables and joined them on query id. " * 20 + "\n\n"
    assert "D1" in rules("# Readout\n\n" + method + CLEAN.split("# Ranker v2 rollout readout")[1])


def test_handover_accepts_a_status_line_first():
    assert "D1" not in rules("# Handover\n\n## Current state\nThe hook is live and tests pass.\n", "handover")


def test_bold_as_default_voice_fails():
    noisy = CLEAN.replace("Keep ranker v2.", "**Keep** **ranker** **v2**. **CTR** **drop** **is** **mix**.")
    assert "D2" in rules(noisy)


def test_bold_label_bullets_and_caps_warn():
    bullets = "\n".join(f"- **Item {i}:** detail {i}" for i in range(6))
    text = CLEAN + "\n## List\n" + bullets + "\nThis is NOT optional and you MUST NEVER skip it.\n"
    assert {"D3", "D4"} <= rules(text)


def test_log_drift_fails():
    text = CLEAN + "\n## Execution record\n- ~~old plan~~\n- DONE 2026-07-08 shipped the fix\n"
    assert "D5" in rules(text)


def test_restated_sections_warn():
    para = ("mobile share rose from forty to fifty five percent while desktop clickthrough stayed flat across both weeks, "
            "so the decline reflects traffic composition rather than ranking quality changes in either platform segment. "
            "Marketing campaigns, app store placement, seasonal travel demand, notification experiments, onboarding funnels, "
            "referral bonuses, partner integrations and regional holidays could explain growth; engineering should audit "
            "logging pipelines, sampling configuration, bot filtering thresholds and dashboard definitions before escalation. ")
    text = f"# Doc\n\n## Answer\n{para}\n\n## Summary again\n{para}\n"
    assert "D6" in rules(text)


def test_process_clutter_warns():
    text = "# Doc\n**Status:** draft\n**Workflow:** wf_943d3676 with 1.68M tokens\n\n" + CLEAN + "\nI ran the query. I checked the logs.\n"
    assert "D7" in rules(text)


def test_undefined_id_codes_and_arrows_warn():
    text = CLEAN + "\nCut A#12, A#13 and B3-5; defer C4, D6 and P1. " + "x -> y " * 10 + "\n"
    assert "D8" in rules(text)


def test_prose_in_tables_and_empty_templates_fail():
    long_cell = " ".join(["word"] * 30)
    assert "D9" in rules(CLEAN + f"\n| a | b |\n|---|---|\n| {long_cell} | 1 |\n")
    assert "D9" in rules(CLEAN + "\n| a | b |\n|---|---|\n| <the number> | <reason> |\n")


def test_mixed_reader_warns():
    assert "D10" in rules(CLEAN + "\nYou should check this before the owner decides; the user may disagree.\n")


def test_thinking_out_loud_warns():
    assert "D11" in rules(CLEAN + "\nHmm, the verify lane earned its keep here.\n")


def test_length_budget_by_type():
    long = CLEAN + "\n## More\n" + ("Extra sentence about the analysis that adds words. " * 80) + "\n"
    assert "D12" in rules(long, "readout")
    assert "D12" not in rules(long, "other")


def test_appendix_counts_at_half_weight():
    small = CLEAN + "\n## Appendix\n" + ("Raw detail line for reference. " * 40) + "\n"
    huge = CLEAN + "\n## Appendix\n" + ("Raw detail line for reference. " * 200) + "\n"
    assert "D12" not in rules(small, "readout") and "D12" in rules(huge, "readout")


def test_unsupported_causal_language_warns_and_supported_does_not():
    assert "D13" in rules(CLEAN + "\nThe new layout drives engagement.\n")
    assert "D13" not in rules(CLEAN + "\nIn the randomized experiment the new layout drives engagement (p < 0.01).\n")


def test_hedged_answer_warns():
    hedged = CLEAN.replace("Keep ranker v2.", "It seems we might possibly keep ranker v2, perhaps.")
    assert "D14" in rules(hedged)


def test_code_blocks_are_ignored():
    text = CLEAN + "\n```\n**bold** **bold** **bold** DONE 2026-01-01 ~~x~~\n```\n"
    assert rules(text) == set()


def test_cli_exit_codes(tmp_path):
    good, bad = tmp_path / "good.md", tmp_path / "bad.md"
    good.write_text(CLEAN)
    bad.write_text("# Doc\n\n## Method\n" + "We did many things first. " * 60)
    assert subprocess.run([sys.executable, LINT, str(good), "--type", "readout"], capture_output=True).returncode == 0
    assert subprocess.run([sys.executable, LINT, str(bad), "--type", "readout"], capture_output=True).returncode == 1
    assert subprocess.run([sys.executable, LINT, str(tmp_path / "missing.md")], capture_output=True).returncode == 2


def test_every_rule_has_evidence():
    for rule_id, rule in doc_lint.load_rules().items():
        assert rule["severity"] in ("fail", "warn") and rule["evidence"], rule_id


# False positives found by linting this repo's own skill files.

def test_reference_pages_skip_the_answer_rule():
    text = "# Rules\n\n## Hedges\n" + "Use one hedge per claim and none in the answer. " * 30
    assert "D1" in rules(text, "other") and "D1" not in rules(text, "reference")


def test_restated_in_prose_is_not_thinking_out_loud():
    assert "D11" not in rules(CLEAN + "\nThe rule is restated in several sections of the old plan.\n")
    assert "D11" in rules(CLEAN + "\n## Biggest problem, restated\nSame as above.\n")


def test_prove_in_plain_english_is_not_a_stat_claim():
    assert "D13" not in rules(CLEAN + "\nA cold read can prove a reader gets the point.\n")
    assert "D13" in rules(CLEAN + "\nThis proves that the layout lifts CTR.\n")


def test_skim_view_shows_the_opening_and_each_section_lead():
    import skim_view
    out = skim_view.skim(CLEAN, limit=12)
    opening, outline = out.split("OUTLINE")
    assert len(opening.split()) <= 13
    assert "## Answer\n  Keep ranker v2." in outline
    assert "## Caveats\n  This is a before and after comparison" in outline


# Regressions from the real-case review (false positives and misses on real notes docs).

def test_claim_heading_counts_as_answer_first():
    doc = ("# Keep ranker v2: the drop is mobile mix\n\nThe 2.1 pp CTR drop comes from more mobile traffic, not the ranker.\n\n"
           "## Mix explains the whole drop\nWithin-platform CTR did not move.\n")
    assert "D1" not in rules(doc, "readout")


def test_status_h1_counts_for_a_handover():
    assert "D1" not in rules("# Hook rewrite shipped and verified, zero open findings\n\nDetails follow.\n", "handover")


def test_method_first_opening_still_fails():
    doc = "# Audit\n\nData sources: we pulled 14 days of hook logs and read 30 transcripts in full before writing anything.\n"
    assert "D1" in rules(doc, "readout")


def test_quoted_and_code_caps_are_not_emphasis():
    doc = CLEAN + '\nThe hook greps for `DONE` and `NEVER`. The guidance says "MUST", "NEVER" and "ALWAYS".\n'
    assert "D4" not in rules(doc)


def test_real_log_paths_and_checklist_wording_are_not_artifacts():
    doc = CLEAN + "\nErrors go to /tmp/cc-hook-errors.log. Each item was re-verified against source. Criteria were verified twice.\n"
    assert "D7" not in rules(doc)
    assert "D7" in rules(CLEAN + "\nSee /tmp/claude-0/session/x.md and wf_943d3676.\n")


def test_handover_paths_are_not_code_clutter():
    paths = " ".join(f"`src/module_{i}.py`" for i in range(20))
    doc = "# Handover\n\n## Current state\nThe job is failing. Open these: " + paths + "\n"
    assert "D8" not in rules(doc, "handover")


def test_causes_as_a_noun_is_not_a_stat_claim():
    assert "D13" not in rules(CLEAN + "\nWe listed the root causes and the likely causes of drift.\n")


def test_a_test_word_alone_does_not_excuse_causal_claims():
    assert "D13" in rules(CLEAN + "\nWe ran the unit test suite and the new ranker drives engagement.\n")


def test_restated_heading_and_executed_status_are_caught():
    assert "D6" in rules(CLEAN + "\n## Biggest problem, restated\nSame as the answer.\n")
    assert "D5" in rules(CLEAN + "\nStatus: EXECUTED 2026-08-11\n")
    assert "D5" in rules(CLEAN + "\n## Appendix: what actually happened\nWe did things.\n")


def test_common_and_defined_codes_are_not_flagged():
    doc = CLEAN + "\n| Code | Meaning |\n|---|---|\n| D1 | answer first |\n| D2 | bold |\n| D3 | labels |\n\nIn Q3 we fix D1, D2 and D3 (P0, H1).\n"
    assert "D8" not in rules(doc)


def test_cli_takes_the_type_from_the_spine(tmp_path):
    doc, spine = tmp_path / "doc.md", tmp_path / "spine.json"
    doc.write_text(CLEAN + "\n## More\n" + ("Extra sentence about the analysis that adds words. " * 80) + "\n")
    spine.write_text('{"type": "readout"}')
    assert subprocess.run([sys.executable, LINT, str(doc), "--spine", str(spine)], capture_output=True).returncode == 1
    assert subprocess.run([sys.executable, LINT, str(doc), "--spine", str(spine), "--type", "memo"], capture_output=True).returncode == 2


def test_skim_view_keeps_abbreviations_and_versions_inside_a_sentence():
    import skim_view
    assert skim_view.first_sentence("Run v1.2 of the gate, e.g. on staging, before the launch. Then ship.") == \
        "Run v1.2 of the gate, e.g. on staging, before the launch."
