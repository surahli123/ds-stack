#!/usr/bin/env python3
"""Grade a results directory against gold, by script, and apply the pass rule.

    python3 eval/grade.py eval/results/<run>

Mechanics are graded by code: the headline number against gold, abstention,
and which alternatives were ruled in. Whether checks ran comes from each run's
.ds-checks.log, not from the readout. Writes summary.md and summary.json.
"""

import json
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from readout import parse  # noqa: E402

ARMS = ("baseline", "checks", "full")
CONTAMINATION_MARKERS = ("ds-stack/eval", "/gold/", "make_fixtures", "pass_rule")


def load_gold(fixture):
    with open(os.path.join(HERE, "gold", f"{fixture}.json")) as handle:
        return json.load(handle)


def _ruled_in(readout, words):
    return [a["name"] for a in readout.alternatives
            if a["verdict"] == "in" and any(w in a["name"] for w in words)]


def grade_readout(readout, gold):
    """Return (correct, reason, kind_of_miss)."""
    if not readout.ok:
        return False, "unparseable: " + "; ".join(readout.errors), "unparseable"
    if readout.abstained:
        if gold["accept_abstain"]:
            return True, "abstained (accepted)", None
        return False, "abstained on a case with a valid answer", "false_alarm" if gold["kind"] == "clean" else "miss"
    if gold["kind"] == "abstain" and not gold["accept_values"]:
        return False, f"answered {readout.value:g} where the right answer is can't tell", "answered_abstain_case"
    if not any(abs(readout.value - v["value"]) <= v["tol"] for v in gold["accept_values"]):
        targets = ", ".join(f"{v['value']:g}±{v['tol']:g}" for v in gold["accept_values"])
        miss = "answered_abstain_case" if gold["kind"] == "abstain" else "miss"
        return False, f"headline {readout.value:g} outside {targets}", miss
    for words in gold["must_rule_in"]:
        if not _ruled_in(readout, words):
            return False, f"true cause not ruled in (expected one of {words[:3]})", "miss"
    for words in gold["must_not_rule_in"]:
        hits = _ruled_in(readout, words)
        if hits:
            return False, f"ruled in a false cause: {hits[0]!r}", "false_alarm" if gold["kind"] == "clean" else "miss"
    return True, "number within tolerance; causes consistent with gold", None


def checks_that_ran(run_dir):
    path = os.path.join(run_dir, "checks.log")
    if not os.path.exists(path):
        return {}
    ran = {}
    with open(path) as handle:
        for line in handle:
            try:
                event = json.loads(line)
            except ValueError:
                continue
            ran.setdefault(event.get("check"), []).append(event.get("status"))
    return ran


def contaminated(run_dir):
    path = os.path.join(run_dir, "transcript.jsonl")
    if not os.path.exists(path):
        return False
    with open(path) as handle:
        text = handle.read()
    return any(marker in text for marker in CONTAMINATION_MARKERS)


def skill_read(run_dir):
    path = os.path.join(run_dir, "transcript.jsonl")
    if not os.path.exists(path):
        return False
    with open(path) as handle:
        for line in handle:
            if '"name":"Read"' in line.replace(" ", "") and "ds-mode/SKILL.md" in line:
                return True
    return False


def grade_dir(results_dir):
    runs = []
    for name in sorted(os.listdir(results_dir)):
        run_dir = os.path.join(results_dir, name)
        meta_path = os.path.join(run_dir, "meta.json")
        if not os.path.isfile(meta_path):
            continue
        with open(meta_path) as handle:
            meta = json.load(handle)
        with open(os.path.join(run_dir, "result.md")) as handle:
            readout = parse(handle.read())
        gold = load_gold(meta["fixture"])
        correct, reason, miss = grade_readout(readout, gold)
        tainted = contaminated(run_dir)
        runs.append({**meta, "correct": correct and not tainted, "reason": reason if not tainted else "contaminated: touched eval files",
                     "miss": miss if not tainted else "contaminated", "headline": readout.headline,
                     "checks_ran": checks_that_ran(run_dir), "skill_read": skill_read(run_dir),
                     "kind": gold["kind"]})
    return runs


def summarize(runs, rule):
    by_cell = defaultdict(list)
    for run in runs:
        by_cell[(run["fixture"], run["arm"])].append(run)
    fixtures = sorted({r["fixture"] for r in runs})
    arms = [a for a in ARMS if any(r["arm"] == a for r in runs)]
    cells = {}
    for (fixture, arm), group in by_cell.items():
        wins = sum(r["correct"] for r in group)
        cells[(fixture, arm)] = {"correct_runs": wins, "runs": len(group),
                                 "majority_correct": wins >= rule["majority"] and len(group) >= rule["majority"]}

    per_arm = {}
    for arm in arms:
        arm_runs = [r for r in runs if r["arm"] == arm]
        per_arm[arm] = {
            "fixtures_correct": sum(cells[(f, arm)]["majority_correct"] for f in fixtures if (f, arm) in cells),
            "runs_correct": sum(r["correct"] for r in arm_runs),
            "runs": len(arm_runs),
            "false_alarms": sum(r["miss"] == "false_alarm" for r in arm_runs),
            "abstain_cases_answered": sum(r["miss"] == "answered_abstain_case" for r in arm_runs),
            "unparseable": sum(r["miss"] == "unparseable" for r in arm_runs),
            "contaminated": sum(r["miss"] == "contaminated" for r in arm_runs),
            "runs_with_any_check": sum(bool(r["checks_ran"]) for r in arm_runs),
            "runs_reading_skill": sum(r["skill_read"] for r in arm_runs),
            "cost_usd": round(sum(r["cost_usd"] or 0 for r in arm_runs), 2),
        }

    verdict = {"n_fixtures": len(fixtures), "min_required": rule["min_holdout_fixtures"]}
    if "full" in per_arm and "baseline" in per_arm:
        full, base = per_arm["full"], per_arm["baseline"]
        would_pass = (full["fixtures_correct"] - base["fixtures_correct"] >= rule["margin_vs_baseline"]
                      and full["false_alarms"] - base["false_alarms"] <= rule["max_extra_false_alarms_vs_baseline"]
                      and full["abstain_cases_answered"] <= rule["max_abstain_cases_answered_with_number"])
        verdict["rule_outcome_if_n_were_enough"] = "PASS" if would_pass else "FAIL"
    verdict["verdict"] = ("INSUFFICIENT_N (smoke test, not a decision)" if len(fixtures) < rule["min_holdout_fixtures"]
                          else verdict.get("rule_outcome_if_n_were_enough", "INCOMPLETE"))
    return fixtures, arms, cells, per_arm, verdict


def render(results_dir, runs, fixtures, arms, cells, per_arm, verdict):
    lines = [f"# Eval summary: {os.path.basename(results_dir)}", "",
             f"**Verdict:** {verdict['verdict']}. {verdict['n_fixtures']} fixtures; the pass rule needs "
             f"{verdict['min_required']}. Rule outcome at this n: {verdict.get('rule_outcome_if_n_were_enough', 'n/a')}.", "",
             "## Fixtures correct by majority vote", "",
             "| Fixture | Kind | " + " | ".join(arms) + " |", "|---|---|" + "---|" * len(arms)]
    kinds = {r["fixture"]: r["kind"] for r in runs}
    for fixture in fixtures:
        row = [fixture, kinds[fixture]]
        for arm in arms:
            cell = cells.get((fixture, arm))
            row.append(f"{'✓' if cell['majority_correct'] else '✗'} {cell['correct_runs']}/{cell['runs']}" if cell else "—")
        lines.append("| " + " | ".join(row) + " |")
    lines += ["", "## Per arm", "", "| Metric | " + " | ".join(arms) + " |", "|---|" + "---|" * len(arms)]
    for metric in next(iter(per_arm.values())).keys():
        lines.append(f"| {metric} | " + " | ".join(str(per_arm[a][metric]) for a in arms) + " |")
    lines += ["", "## Every run", "", "| Run | Correct | Headline | Reason | Checks that ran |", "|---|---|---|---|---|"]
    for run in sorted(runs, key=lambda r: (r["fixture"], ARMS.index(r["arm"]), r["run"])):
        ran = ", ".join(f"{k}:{'/'.join(v)}" for k, v in run["checks_ran"].items()) or "none"
        headline = run["headline"].replace("|", "/")[:60]
        lines.append(f"| {run['fixture']} {run['arm']} #{run['run']} | {'✓' if run['correct'] else '✗'} | {headline} | {run['reason']} | {ran} |")
    return "\n".join(lines) + "\n"


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 3
    results_dir = sys.argv[1]
    with open(os.path.join(HERE, "pass_rule.json")) as handle:
        rule = json.load(handle)
    runs = grade_dir(results_dir)
    fixtures, arms, cells, per_arm, verdict = summarize(runs, rule)
    report = render(results_dir, runs, fixtures, arms, cells, per_arm, verdict)
    with open(os.path.join(results_dir, "summary.md"), "w") as handle:
        handle.write(report)
    with open(os.path.join(results_dir, "summary.json"), "w") as handle:
        json.dump({"verdict": verdict, "per_arm": per_arm, "runs": runs}, handle, indent=2, default=str)
    print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
