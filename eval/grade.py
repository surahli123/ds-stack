#!/usr/bin/env python3
"""Grade a results directory against gold, by script, and apply the pass rule.

    python3 eval/grade.py eval/results/<run> [--allow-no-transcript]

Mechanics are graded by code: the headline number in the gold unit, abstention,
and which alternatives were ruled in. Whether checks ran comes from each run's
.ds-checks.log, not from the readout. Every pass-rule input is counted per
fixture by majority vote, never per run. Writes summary.md and summary.json.

A run with no transcript fails closed: isolation can't be verified. Runs made
with a custom agent (run_arms.py --agent-cmd) have no transcript by design and
say so in meta.json ("transcript": false). With --allow-no-transcript those runs
are graded on their readout and reported as "unverified (custom agent)" for
isolation and skill-read instead of failing, and counted per arm in
runs_unverified_isolation. Without the flag nothing changes.
"""

import json
import os
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from readout import parse  # noqa: E402

ARMS = ("baseline", "checks", "full")
CONTAMINATION_MARKERS = (ROOT, "/home/user/notes", "make_fixtures", "pass_rule", "/gold/")
UNVERIFIED = "unverified (custom agent)"


def load_gold(fixture):
    with open(os.path.join(HERE, "gold", f"{fixture}.json")) as handle:
        return json.load(handle)


def _ruled_in(readout, words, unless=()):
    return [a["name"] for a in readout.alternatives
            if a["verdict"] == "in" and any(w in a["name"] for w in words)
            and not any(u in a["name"] for u in unless)]


def grade_readout(readout, gold):
    """Return (correct, reason, kind_of_miss)."""
    if not readout.ok:
        return False, "unparseable: " + "; ".join(readout.errors), "unparseable"
    if readout.abstained:
        if gold["accept_abstain"]:
            return True, "abstained (accepted)", None
        return False, "abstained on a case with a valid answer", "false_alarm" if gold["kind"] == "clean" else "miss"
    value = readout.value_in(gold["unit"])
    if value is None:
        return False, f"headline has no number in {gold['unit']}", "unparseable"
    if gold["kind"] == "abstain" and not gold["accept_values"]:
        return False, f"answered {value:g} where the right answer is can't tell", "answered_abstain_case"
    if not any(abs(value - v["value"]) <= v["tol"] for v in gold["accept_values"]):
        targets = ", ".join(f"{v['value']:g}±{v['tol']:g}" for v in gold["accept_values"])
        miss = "answered_abstain_case" if gold["kind"] == "abstain" else "miss"
        return False, f"headline {value:g} outside {targets}", miss
    true_words = gold.get("true_cause_words", [])
    for words in gold["must_rule_in"]:
        if not _ruled_in(readout, words):
            return False, f"true cause not ruled in (expected one of {words[:3]})", "miss"
    for words in gold["must_not_rule_in"]:
        hits = _ruled_in(readout, words, unless=true_words)
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


def contamination(run_dir):
    """None if clean, else the reason. A missing transcript is not clean."""
    path = os.path.join(run_dir, "transcript.jsonl")
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return "no transcript, so isolation can't be verified"
    with open(path) as handle:
        text = handle.read()
    for marker in CONTAMINATION_MARKERS:
        if marker in text:
            return f"touched the eval or notes tree ({marker})"
    return None


def skill_read(run_dir):
    path = os.path.join(run_dir, "transcript.jsonl")
    if not os.path.exists(path):
        return False
    with open(path) as handle:
        for line in handle:
            if '"name":"Read"' in line.replace(" ", "") and "ds-mode/SKILL.md" in line:
                return True
    return False


def grade_dir(results_dir, allow_no_transcript=False):
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
        if allow_no_transcript and meta.get("transcript") is False:
            isolation = skill = UNVERIFIED
        else:
            tainted = contamination(run_dir)
            if tainted:
                correct, reason, miss = False, "contaminated: " + tainted, "contaminated"
            isolation, skill = tainted or "ok", skill_read(run_dir)
        runs.append({**meta, "correct": correct, "reason": reason, "miss": miss, "headline": readout.headline,
                     "dropped_alternative_lines": len(readout.dropped),
                     "checks_ran": checks_that_ran(run_dir), "skill_read": skill, "isolation": isolation,
                     "kind": gold["kind"]})
    return runs


def majority_needed(rule):
    return rule["runs_per_fixture"] // 2 + 1


def cell_outcome(group, rule):
    """Majority outcome of one fixture x arm cell: 'correct', a miss kind, or 'incomplete'."""
    if len(group) != rule["runs_per_fixture"]:
        return "incomplete"
    if sum(r["correct"] for r in group) >= majority_needed(rule):
        return "correct"
    misses = Counter(r["miss"] for r in group if not r["correct"])
    kind, count = misses.most_common(1)[0]
    return kind if count >= majority_needed(rule) else "miss"


def summarize(runs, rule):
    by_cell = defaultdict(list)
    for run in runs:
        by_cell[(run["fixture"], run["arm"])].append(run)
    fixtures = sorted({r["fixture"] for r in runs})
    arms = [a for a in ARMS if any(r["arm"] == a for r in runs)]
    cells = {key: {"outcome": cell_outcome(group, rule), "correct_runs": sum(r["correct"] for r in group),
                   "runs": len(group)} for key, group in by_cell.items()}

    per_arm = {}
    for arm in arms:
        arm_runs = [r for r in runs if r["arm"] == arm]
        outcomes = [cells[(f, arm)]["outcome"] for f in fixtures if (f, arm) in cells]
        per_arm[arm] = {
            "fixtures_correct": outcomes.count("correct"),
            "fixtures_false_alarm": outcomes.count("false_alarm"),
            "fixtures_abstain_answered": outcomes.count("answered_abstain_case"),
            "fixtures_incomplete": outcomes.count("incomplete"),
            "runs_correct": sum(r["correct"] for r in arm_runs),
            "runs": len(arm_runs),
            "runs_unparseable": sum(r["miss"] == "unparseable" for r in arm_runs),
            "runs_contaminated": sum(r["miss"] == "contaminated" for r in arm_runs),
            "runs_unverified_isolation": sum(r.get("isolation") == UNVERIFIED for r in arm_runs),
            "dropped_alternative_lines": sum(r["dropped_alternative_lines"] for r in arm_runs),
            "runs_with_any_check": sum(bool(r["checks_ran"]) for r in arm_runs),
            "runs_reading_skill": sum(r["skill_read"] is True for r in arm_runs),
            "cost_usd": round(sum(r.get("cost_usd") or 0 for r in arm_runs), 2),
        }

    verdict = {"n_fixtures": len(fixtures), "min_required": rule["min_holdout_fixtures"]}
    if "full" in per_arm and "baseline" in per_arm:
        verdict["rule_outcome_if_n_were_enough"] = "PASS" if passes(per_arm["full"], per_arm["baseline"], rule) else "FAIL"
    if any(p["fixtures_incomplete"] for p in per_arm.values()):
        verdict["verdict"] = "INCOMPLETE (some cells lack the pre-registered run count)"
    elif len(fixtures) < rule["min_holdout_fixtures"]:
        verdict["verdict"] = "INSUFFICIENT_N (smoke test, not a decision)"
    else:
        verdict["verdict"] = verdict.get("rule_outcome_if_n_were_enough", "INCOMPLETE")
    return fixtures, arms, cells, per_arm, verdict


def passes(full, base, rule):
    return (full["fixtures_correct"] - base["fixtures_correct"] >= rule["margin_vs_baseline"]
            and full["fixtures_false_alarm"] - base["fixtures_false_alarm"] <= rule["max_extra_false_alarms_vs_baseline"]
            and full["fixtures_abstain_answered"] <= rule["max_abstain_cases_answered_with_number"])


def render(results_dir, runs, fixtures, arms, cells, per_arm, verdict):
    lines = [f"# Eval summary: {os.path.basename(results_dir)}", ""]
    if not runs:
        return "\n".join(lines + ["No runs found."]) + "\n"
    lines += [f"**Verdict:** {verdict['verdict']}. {verdict['n_fixtures']} fixtures; the pass rule needs "
              f"{verdict['min_required']}. Rule outcome at this n: {verdict.get('rule_outcome_if_n_were_enough', 'n/a')}.", "",
              "## Fixtures by majority vote", "",
              "| Fixture | Kind | " + " | ".join(arms) + " |", "|---|---|" + "---|" * len(arms)]
    kinds = {r["fixture"]: r["kind"] for r in runs}
    for fixture in fixtures:
        row = [fixture, kinds[fixture]]
        for arm in arms:
            cell = cells.get((fixture, arm))
            if not cell:
                row.append("—")
                continue
            mark = "✓" if cell["outcome"] == "correct" else f"✗ {cell['outcome']}"
            row.append(f"{mark} ({cell['correct_runs']}/{cell['runs']})")
        lines.append("| " + " | ".join(row) + " |")
    lines += ["", "## Per arm", "", "| Metric | " + " | ".join(arms) + " |", "|---|" + "---|" * len(arms)]
    for metric in next(iter(per_arm.values())).keys():
        lines.append(f"| {metric} | " + " | ".join(str(per_arm[a][metric]) for a in arms) + " |")
    unverified = any(r.get("isolation") == UNVERIFIED for r in runs)
    head = "| Run | Correct | Headline | Reason | Checks that ran |" + (" Isolation | Skill read |" if unverified else "")
    lines += ["", "## Every run", "", head, "|---|" + "---|" * (6 if unverified else 4)]
    for run in sorted(runs, key=lambda r: (r["fixture"], ARMS.index(r["arm"]), r["run"])):
        ran = ", ".join(f"{k}:{'/'.join(v)}" for k, v in run["checks_ran"].items()) or "none"
        headline = run["headline"].replace("|", "/")[:70]
        row = f"| {run['fixture']} {run['arm']} #{run['run']} | {'✓' if run['correct'] else '✗'} | {headline} | {run['reason']} | {ran} |"
        if unverified:
            iso = run.get("isolation", "ok")
            row += f" {iso if iso in ('ok', UNVERIFIED) else 'contaminated'} | {run['skill_read']} |"
        lines.append(row)
    return "\n".join(lines) + "\n"


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    allow = "--allow-no-transcript" in argv
    paths = [a for a in argv if a != "--allow-no-transcript"]
    if len(paths) != 1:
        print(__doc__)
        return 3
    results_dir = paths[0]
    with open(os.path.join(HERE, "pass_rule.json")) as handle:
        rule = json.load(handle)
    runs = grade_dir(results_dir, allow_no_transcript=allow)
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
