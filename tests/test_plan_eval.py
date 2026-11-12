"""The plan eval grades a plan's closing lines by script: right plans pass, the real mistake fails."""

import json
import os
import sys

from conftest import ROOT

sys.path.insert(0, os.path.join(ROOT, "eval", "plan"))

import grade_plan  # noqa: E402

with open(os.path.join(ROOT, "eval", "plan", "gold", "p2.json")) as handle:
    GOLD = json.load(handle)

RIGHT = """# Plan

Estimate the effect per user, stratified by tenant.

**Unit:** user, since users were randomized; tenant only as a stratum
**Segment:** users whose own sessions used 3P results in June to August, before the test
**Tenants:** stratify by tenant and report heterogeneity; not the unit of analysis
"""

THE_MISTAKE = """# Plan

Unit: tenant, because tenant-level analysis gives more power
Segment: users in tenants with segment = '3P power'
Tenants: unit of analysis is the tenant; aggregate to tenant means
"""


def test_a_right_plan_passes_every_item():
    assert grade_plan.score(RIGHT, GOLD) == (1.0, [item["name"] for item in GOLD["items"]])


def test_the_real_mistake_fails_every_item():
    assert grade_plan.score(THE_MISTAKE, GOLD) == (0.0, [])


def test_negated_phrases_do_not_trip_none_of():
    lines = "Unit: user-level, not tenant level\nTenants: strata, rather than the unit of analysis is the tenant\n"
    assert grade_plan.score(lines, GOLD)[1] == ["estimates at the user level", "tenants only as a stratum or for clustering"]


def test_the_last_closing_line_wins_and_full_width_colons_parse():
    text = "Unit: tenant\n\nAfter your point:\n\nUnit： user\n"
    assert grade_plan.closing_lines(text)["unit"] == "user"


def test_a_missing_plan_scores_zero():
    assert grade_plan.score(None, GOLD) == (0.0, [])


def test_one_task_is_insufficient_n():
    rows = [{"task": "p2", "arm": arm, "run": 1, "plan": True, "turn1": t, "turn2": t, "words": 300,
             "contaminated": None, "cost_usd": 0.1} for arm, t in (("baseline", 0.0), ("full", 1.0))]
    per_arm, _, verdict = grade_plan.summarize(rows, {"min_tasks": 10, "turn1_margin": 0.2, "turn2_margin": 0.2,
                                                     "max_words_ratio": 1.0})
    assert verdict["verdict"].startswith("INSUFFICIENT_N") and verdict["rule_outcome_if_n_were_enough"] == "PASS"
    assert per_arm["full"]["turn1_score"] == 1.0
