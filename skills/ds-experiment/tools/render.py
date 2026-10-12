#!/usr/bin/env python3
"""Render the launch-review readout from decide.py's decision and the model's notes.

    python3 render.py --decision decision.json --scorecard scorecard.json --notes notes.json [--out-dir DIR]

notes.json is the only part the model writes:

    {"why_it_moved": [{"text": "...", "label": "measured|inferred|guess"}],   # at most 3
     "would_change": ["...", "..."],                                          # at most 3
     "analyst_view": null or {"call": "<one of the calls>", "reason": "..."}}

The notes are checked before anything is written: bullet and word caps, no
stat-speak, no call words in "Why it moved", and every number must be one the
scorecard or the decision contains. On any problem it prints them and exits 1.
Writes readout.md, all_metrics.md and spine.json (the cold-read answer key,
built from the decision, never from the readout). Exit 0 on success, 2 on bad input.
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from decide import CALL_TEXT, describe, threshold_text  # noqa: E402

STAT_SPEAK = re.compile(r"p[- ]?values?|\bp\s*[<=>]|statistical|significan|\balpha\b|z[- ]?score|t[- ]?stat|"
                        r"\bpower(ed)?\b|variance|cuped|bonferroni|sequential|\bsrm\b|null hypothesis|"
                        r"confidence interval|\bci\b", re.I)
CALL_WORDS = re.compile(r"\bship\b|don'?t ship|escalat|keep running|no effect found|can'?t tell", re.I)
NUMBER = re.compile(r"(?<![\w.])([-+−]?\d+(?:,\d{3})*(?:\.\d+)?)\s*(%|pp\b)?")
LABELS = ("measured", "inferred", "guess")
MAX_BULLETS, MAX_WORDS, MAX_VIEW_WORDS = 3, 35, 45
GLOSSARY = ("Calls: Can't tell means the test is broken. Keep running means not enough data yet. "
            "No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.")


def allowed_numbers(decision, scorecard):
    percents, plain = set(), set()
    for comparison in scorecard.get("comparisons", []):
        for m in comparison["metrics"]:
            for key in ("rel_delta",):
                if m.get(key) is not None:
                    percents.add(100 * m[key])
            for ci in (m.get("rel_ci"), m.get("seq_rel_ci")):
                for b in ci or []:
                    percents.add(100 * b)
            for key in ("control_mean", "test_mean", "abs_delta", "control_units", "test_units"):
                if m.get(key) is not None:
                    plain.add(m[key])
                    if key in ("control_mean", "test_mean") and 0 < abs(m[key]) <= 1:
                        percents.add(100 * m[key])
            if m.get("abs_delta") is not None and m.get("control_mean") is not None and abs(m["control_mean"]) <= 1:
                percents.add(100 * m["abs_delta"])  # a rate's change in percentage points
            for b in m.get("abs_ci") or []:
                plain.add(b)
    for v in decision["verdicts"]:
        for key in ("point", "low", "high", "threshold"):
            if v.get(key) is not None:
                (percents if v.get("unit") == "relative" else plain).add(100 * v[key] if v.get("unit") == "relative" else v[key])
                if key == "threshold" and v.get("unit") == "relative":
                    percents.add(100 * v[key])
    for s in decision["secondaries"]["survivors"]:
        if s.get("rel_delta") is not None:
            percents.add(100 * s["rel_delta"])
    for key, value in decision["status"].items():
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            plain.add(value)
    plain.add(100 * decision["settings"]["ci_level"])
    return percents, plain


def number_ok(text_value, unit, percents, plain):
    value = abs(float(text_value.replace(",", "").replace("−", "-")))
    if unit in ("%", "pp"):
        return any(abs(value - abs(p)) <= 0.0051 + 1e-9 or abs(value - abs(p)) <= 0.051 and len(text_value.split(".")[-1]) == 1
                   for p in percents) or any(abs(value - abs(p)) <= 0.0051 for p in plain)
    if value <= 10 and float(value).is_integer():
        return True
    return any(abs(value - abs(p)) <= max(0.005 * abs(p), 0.0051) for p in plain | percents)


def check_notes(notes, decision, scorecard):
    problems = []
    percents, plain = allowed_numbers(decision, scorecard)
    why = notes.get("why_it_moved") or []
    change = notes.get("would_change") or []
    view = notes.get("analyst_view")
    if not isinstance(why, list) or not isinstance(change, list):
        return ["why_it_moved and would_change must be lists"]
    if len(why) > MAX_BULLETS:
        problems.append(f"why_it_moved has {len(why)} bullets; at most {MAX_BULLETS}")
    if len(change) > MAX_BULLETS:
        problems.append(f"would_change has {len(change)} bullets; at most {MAX_BULLETS}")
    texts = []
    for i, item in enumerate(why, 1):
        if not isinstance(item, dict) or item.get("label") not in LABELS:
            problems.append(f"why_it_moved #{i} needs a label: measured, inferred or guess")
            continue
        texts.append((f"why_it_moved #{i}", item.get("text", ""), MAX_WORDS))
        if CALL_WORDS.search(item.get("text", "")):
            problems.append(f"why_it_moved #{i} uses a call word ('{CALL_WORDS.search(item['text']).group(0)}'); "
                            "the call is made once, in the title")
    texts += [(f"would_change #{i}", t, MAX_WORDS) for i, t in enumerate(change, 1)]
    if view:
        if view.get("call") not in CALL_TEXT or view.get("call") == decision["call"]:
            problems.append(f"analyst_view.call must be one of {sorted(CALL_TEXT)} and differ from the scripted call")
        texts.append(("analyst_view", view.get("reason", ""), MAX_VIEW_WORDS))
    for where, text, cap in texts:
        if not isinstance(text, str) or not text.strip():
            problems.append(f"{where} is empty")
            continue
        words = len(text.split())
        if words > cap:
            problems.append(f"{where} has {words} words; at most {cap}")
        speak = STAT_SPEAK.search(text)
        if speak:
            problems.append(f"{where} uses stat-speak ('{speak.group(0)}'); say what it means for the decision instead")
        for match in NUMBER.finditer(re.sub(r"\b[A-Za-z]+\d+\w*\b|\d{4}-\d{2}-\d{2}", " ", text)):
            if not number_ok(match.group(1), match.group(2), percents, plain):
                problems.append(f"{where}: {match.group(0).strip()} is not a number in the scorecard or the decision")
    return problems


def bar_text(v):
    if v.get("threshold") is None:
        return "no worse than zero" if v["role"] == "guardrail" else "none registered"
    shown = threshold_text(v["threshold"], v.get("unit", "relative"), v.get("display_unit", ""))
    if v["role"] == "primary":
        return f"at least {shown}"
    if v["role"] == "guardrail":
        return f"no worse than {shown}"
    return "no change"


VERDICT_TEXT = {"better": "better", "below_bar": "better, below the bar", "worse": "worse", "undetermined": "unclear",
                "within": "within margin", "harm_within_margin": "worse, within margin", "breached": "past its margin",
                "no_harm_detected": "no harm found", "missing": "not in the scorecard", "no_interval": "no interval",
                "no_direction": "no direction registered", "moved": "moved", "held": "held"}


def row(v):
    change = describe(v) if v.get("point") is not None else ""
    return f"| {v['metric']} | {v['role']} | {change} | {bar_text(v)} | {VERDICT_TEXT.get(v['verdict'], v['verdict'])} |"


def metric_rows(decision):
    verdicts = decision["verdicts"]
    decider = decision["decider"].get("metric")
    flagged = {"breached", "undetermined", "harm_within_margin", "missing", "no_interval", "no_direction", "moved", "worse",
               "below_bar"}
    first = [v for v in verdicts if v["metric"] == decider]
    alarms = [v for v in verdicts if v not in first and v["verdict"] in flagged]
    primaries = [v for v in verdicts if v not in first and v not in alarms and v["role"] == "primary"]
    quiet = [v for v in verdicts if v not in first and v not in alarms and v not in primaries]
    lines = [row(v) for v in first + alarms + primaries]
    quiet_guards = [v["metric"] for v in quiet if v["role"] == "guardrail"]
    if quiet_guards:
        lines.append(f"| Other guardrails | guardrail | {', '.join(quiet_guards)} | | within margin |")
    for v in quiet:
        if v["role"] == "invariant":
            lines.append(row(v))
    return lines


def status_line(status):
    parts = []
    if status.get("days_run") is not None:
        parts.append(f"day {status['days_run']} of {status['planned_days']}" if status.get("planned_days") else f"{status['days_run']} days")
    if status.get("units_per_arm"):
        units = f"{status['units_per_arm']:,} users per arm"
        if status.get("planned_units"):
            units += f" (planned {status['planned_units']:,})"
        parts.append(units)
    if status.get("whole_weeks") is not None:
        parts.append("whole weeks" if status["whole_weeks"] else "not whole weeks")
    return ", ".join(parts) or "unknown"


def checks_line(checks):
    order = {"fail": 0, "flag": 1, "could_not_run": 2, "pass": 3}
    shown = sorted(checks, key=lambda c: order.get(c["status"], 4))
    return "; ".join(f"{c['check'].replace('_', ' ')} {c['status'].replace('_', ' ')}" for c in shown)


def reversal(decision):
    """What could change this call, by call type."""
    d, call, items = decision["decider"], decision["call"], decision["open_items"]
    if call == "dont_ship" and d.get("metric"):
        limit = bar_text(d) if d.get("role") == "guardrail" else "an improvement"
        return f"only a version that keeps {d['metric']} at {limit}" if d.get("role") == "guardrail" else \
            f"only a version where {d['metric']} improves"
    if call == "cant_tell":
        return f"fixing the {d.get('check', 'failed check').replace('_', ' ')} problem and rerunning"
    if call == "keep_running":
        return "the remaining data; the call is made at the planned sample"
    if call == "not_ab":
        return "nothing here; this design needs its own readout"
    if call == "escalate":
        others = [i for i in items if not d.get("metric") or d["metric"] not in i]
        return others[0] if others else "triage's judgment on the trade-off; nothing else is open"
    return items[0] if items else "nothing open; every registered check ran and passed"


def readout(decision, notes, scorecard):
    exp = decision["experiment"]
    lines = [f"# {exp.get('name') or exp.get('id') or 'Experiment'}: {decision['call_text']}", "",
             f"Decision: {decision['call_text']}. {decision['reason']}", "",
             f"Ask: {decision['ask']}", "",
             f"Status: {status_line(decision['status'])}.", "",
             f"Could reverse it: {reversal(decision)}.", ""]
    if decision["call"] != "not_ab":
        lines += [f"| Metric | Role | Change ({round(100 * decision['settings']['ci_level'])}% interval) | Bar | Verdict |",
                  "|---|---|---|---|---|"] + metric_rows(decision) + [""]
    lines += [f"Checks: {checks_line(decision['checks'])}.", ""]
    change = notes.get("would_change") or []
    lines += ["## What would change the call", ""] + ([f"- {t}" for t in change] or ["- Nothing short of new data."]) + [""]
    why = notes.get("why_it_moved") or []
    lines += ["## Why it moved", ""] + ([f"- [{w['label']}] {w['text']}" for w in why]
                                         or ["- [guess] No segment cuts were read, so the mechanism is not known."]) + [""]
    view = notes.get("analyst_view")
    if view:
        lines += ["## Analyst's view", "", f"The analyst would call this {CALL_TEXT[view['call']]}: {view['reason']}", ""]
    sec = decision["secondaries"]
    survivors = sec["survivors"]
    lines += ["## Appendix", ""]
    if survivors:
        names = ", ".join(f"{s['metric']} ({100 * s['rel_delta']:+.2f}%)" for s in survivors if s.get("rel_delta") is not None)
        lines.append(f"- Secondary metrics: {sec['tested']} tested; after a false-discovery correction these moved: {names}. "
                     "They are exploratory and don't change the call.")
    else:
        lines.append(f"- Secondary metrics: {sec['tested']} tested; none moved after a false-discovery correction.")
    settings = decision["settings"]
    cuped = {True: "on (changes are adjusted for pre-test behaviour)", False: "off", None: "not recorded"}[settings.get("cuped")]
    lines.append(f"- Settings: {round(100 * settings['ci_level'])}% intervals; variance reduction {cuped}; "
                 f"harm inside a margin goes to {settings['standards']['harm_within_margin']}.")
    for item in decision["fallbacks"]:
        lines.append(f"- Fallback: {item}.")
    lines += ["- Every metric, with means and p-values: all_metrics.md.", f"- {GLOSSARY}", ""]
    return "\n".join(lines)


def all_metrics(decision, scorecard):
    lines = [f"# {decision['experiment'].get('name')}: every metric", "",
             "| Metric | Listed as | Control | Test | Change | Interval | p |", "|---|---|---|---|---|---|---|"]
    for comparison in scorecard["comparisons"]:
        if comparison.get("test_group") != decision["experiment"].get("test_group"):
            continue
        for m in comparison["metrics"]:
            ci = m.get("rel_ci")
            lines.append(f"| {m['metric']} | {m.get('listed_as')} | {m.get('control_mean')} | {m.get('test_mean')} | "
                         f"{'' if m.get('rel_delta') is None else f'{100 * m['rel_delta']:+.2f}%'} | "
                         f"{'' if not ci else f'{100 * ci[0]:+.2f}% to {100 * ci[1]:+.2f}%'} | {m.get('p_value')} |")
    return "\n".join(lines) + "\n"


def spine(decision):
    """The cold-read answer key, from the decision only."""
    answer = f"{decision['call_text']}: {decision['reason']}"
    if len(answer.split()) > 30:
        d = decision["decider"]
        answer = f"{decision['call_text']}, decided by {d.get('metric') or d.get('check', '').replace('_', ' ')}."
    verdicts = decision["verdicts"]
    decider = decision["decider"]
    lead = next((v for v in verdicts if v["role"] == "primary" and v.get("point") is not None), None)
    takeaways = []
    if decider.get("metric") and decider.get("point") is not None:
        takeaways.append(f"{decider['metric']} {VERDICT_TEXT.get(decider['verdict'], decider['verdict'])}: {describe(decider)}.")
    elif decider.get("summary"):
        takeaways.append(_first_words(decider["summary"], 25))
    if lead and lead["metric"] != decider.get("metric"):
        takeaways.append(f"{lead['metric']} {describe(lead)} against a bar of {bar_text(lead)}.")
    takeaways.append(f"Could reverse it: {reversal(decision)}.")
    guards = [v for v in verdicts if v["role"] == "guardrail"]
    if len(takeaways) < 3:
        takeaways.insert(1, f"Guardrails: {', '.join(v['metric'] + ' ' + VERDICT_TEXT.get(v['verdict'], v['verdict']) for v in guards[:3])}."
                         if guards else f"Status: {status_line(decision['status'])}.")
    while len(takeaways) < 3:
        takeaways.append(f"Status: {status_line(decision['status'])}.")
    return {"type": "readout", "reader": "the launch review (product, engineering and data science leads) deciding whether to launch",
            "answer": answer, "decision": decision["ask"], "takeaways": [_first_words(t, 40) for t in takeaways[:3]]}


def _first_words(text, n):
    words = text.split()
    return " ".join(words[:n]) + ("..." if len(words) > n else "")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--decision", required=True)
    parser.add_argument("--scorecard", required=True)
    parser.add_argument("--notes", help="the model's notes.json; omit for a readout with no mechanism")
    parser.add_argument("--out-dir")
    args = parser.parse_args(argv)
    try:
        with open(args.decision, encoding="utf-8") as handle:
            decision = json.load(handle)
        with open(args.scorecard, encoding="utf-8") as handle:
            scorecard = json.load(handle)
        notes = {}
        if args.notes:
            with open(args.notes, encoding="utf-8") as handle:
                notes = json.load(handle)
    except (OSError, ValueError) as err:
        print(f"render: {err}", file=sys.stderr)
        return 2
    problems = check_notes(notes, decision, scorecard)
    if problems:
        print("render: notes.json was not accepted:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1
    out = args.out_dir or os.path.dirname(os.path.abspath(args.decision))
    files = {"readout.md": readout(decision, notes, scorecard), "all_metrics.md": all_metrics(decision, scorecard),
             "spine.json": json.dumps(spine(decision), indent=2)}
    for name, text in files.items():
        with open(os.path.join(out, name), "w", encoding="utf-8") as handle:
            handle.write(text)
    print(f"render: wrote readout.md, all_metrics.md and spine.json to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
