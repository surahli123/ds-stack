#!/usr/bin/env python3
"""Make the launch call: every call compares one named interval with one
pre-registered threshold.

    python3 decide.py --scorecard scorecard.json --prereg prereg.json \
        [--config config.json] [--standards standards.json] [--daily daily.json] [--out decision.json]

Each registered metric (primary, guardrail, invariant) gets a verdict from its
interval against its own bar or margin. The call is a fixed function of those
verdicts plus the sample and validity checks; the first rule that fires
decides, and its metric or check is the `decider`. Only registered metrics can
block. Secondaries get a Benjamini-Hochberg correction and are only noted
unless the team standard says otherwise.

Writes decision.json (default next to the scorecard) and appends one line to
.ds-checks.log (or $DS_CHECKS_LOG). Exit 0 on a call, 2 on unusable input.
"""

import argparse
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import checks as chk  # noqa: E402
import expstats  # noqa: E402

CALL_TEXT = {"not_ab": "Not an A/B test", "cant_tell": "Can't tell", "dont_ship": "Don't ship",
             "keep_running": "Keep running", "escalate": "Escalate", "no_effect": "No effect found", "ship": "Ship"}
ASK = {"ship": "Approve the launch to all traffic.",
       "dont_ship": "Agree not to launch; the owner decides whether to iterate.",
       "escalate": "Decide the trade-off at triage.",
       "keep_running": "Approve running the test longer.",
       "no_effect": "Agree to stop the test without launching.",
       "cant_tell": "Agree to fix the test and rerun; no launch decision from this data.",
       "not_ab": "Use the readout for this test design instead."}
DEFAULT_STANDARDS = {"srm_alpha": 0.001, "min_days": 7, "harm_within_margin": "escalate", "below_bar": "escalate",
                     "secondary_harm": "note", "secondary_q": 0.1, "max_extension_factor": 2.0,
                     "guardrails": [], "directions": {}}


class InputError(ValueError):
    """The inputs can't support a call."""


def find(metrics, name):
    """Exact, case-insensitive match on the metric name. No fuzzy matching: a near
    miss binds the wrong metric silently."""
    wanted = str(name).strip().lower()
    hits = [m for m in metrics if str(m["metric"]).strip().lower() == wanted]
    return hits[0] if hits else None


def interval(m, unit, level, base_level, sequential=False):
    """(point, low, high, se) for metric m in 'relative' or 'absolute' units at `level`."""
    rel_ci, abs_ci = (m.get("seq_rel_ci"), m.get("seq_abs_ci")) if sequential else (m.get("rel_ci"), m.get("abs_ci"))
    control = m.get("control_mean")
    if unit == "relative":
        point, ci = m.get("rel_delta"), rel_ci
        if ci is None and abs_ci and control:
            ci = [b / control for b in abs_ci]
        if point is None and m.get("abs_delta") is not None and control:
            point = m["abs_delta"] / control
    else:
        point, ci = m.get("abs_delta"), abs_ci
        if ci is None and rel_ci and control is not None:
            ci = [b * control for b in rel_ci]
        if point is None and m.get("rel_delta") is not None and control is not None:
            point = m["rel_delta"] * control
    if point is None or not ci:
        return None
    se = expstats.se_from_ci(min(ci), max(ci), base_level)
    z = expstats.z_for(level)
    return point, point - z * se, point + z * se, se


def oriented(iv, sign):
    """Flip so that positive is always good."""
    point, low, high, se = iv
    return (sign * point, min(sign * low, sign * high), max(sign * low, sign * high), se)


def zero_interval(m, level, base_level, sequential):
    """The interval used to test against zero: absolute when present (Statsig's advice), else relative."""
    return (interval(m, "absolute", level, base_level, sequential) if (m.get("seq_abs_ci") if sequential else m.get("abs_ci"))
            else interval(m, "relative", level, base_level, sequential))


def sign_of(direction):
    if direction in ("increase", "higher", "up", "higher_is_better"):
        return 1
    if direction in ("decrease", "lower", "down", "lower_is_better"):
        return -1
    return 0


def describe(entry):
    """'+0.81% (+0.36% to +1.26%)' in the entry's unit."""
    point, low, high = entry["point"], entry["low"], entry["high"]
    if entry["unit"] == "relative":
        return f"{100 * point:+.2f}% ({100 * low:+.2f}% to {100 * high:+.2f}%)"
    suffix = entry.get("display_unit", "")
    return f"{point:+.3g}{suffix} ({low:+.3g}{suffix} to {high:+.3g}{suffix})"


def threshold_text(value, unit, display_unit=""):
    return f"{100 * value:.2f}%" if unit == "relative" else f"{value:g}{display_unit}"


def judge_primary(spec, m, levels, base, sequential, ship_requires):
    sign = sign_of(spec.get("direction"))
    unit = spec.get("bar_unit", "relative")
    entry = {"metric": spec["metric"], "role": "primary", "unit": unit, "direction": spec.get("direction"),
             "threshold": spec.get("bar"), "threshold_kind": "bar", "listed_as": m.get("listed_as")}
    if sign == 0:
        return {**entry, "verdict": "no_direction"}
    iv = interval(m, unit, levels["primary"], base, sequential)
    zero = zero_interval(m, levels["primary"], base, sequential)
    if iv is None or zero is None:
        return {**entry, "verdict": "no_interval"}
    share = spec.get("mass_share")
    if share:  # triggered lift -> overall lift: scale by the triggered share of control metric mass
        iv = tuple(v * share for v in iv[:3]) + (iv[3] * share,)
        entry["scaled_from_triggered"] = share
    point, low, high, se = iv
    entry.update(point=point, low=low, high=high, se=se, level=levels["primary"])
    zpoint, zlow, zhigh, _ = oriented(zero, sign)
    gpoint, glow, ghigh, _ = oriented(iv, sign)
    bar = spec.get("bar")
    if zlow > 0:
        verdict = "better"
        if bar is not None and (ship_requires == "point_at_bar" and gpoint < bar or ship_requires == "ci_at_bar" and glow < bar):
            verdict = "below_bar"
    elif zhigh < 0:
        verdict = "worse"
    else:
        verdict = "undetermined"
    entry.update(verdict=verdict, rules_out_bar=bar is not None and ghigh < bar,
                 achieved_mde=expstats.achieved_mde(se, alpha=1 - levels["primary"]))
    return entry


def judge_guardrail(spec, m, levels, base, sequential):
    sign = sign_of(spec.get("direction"))
    margin, unit = spec.get("margin"), spec.get("margin_unit", "relative")
    entry = {"metric": spec["metric"], "role": "guardrail", "unit": unit, "direction": spec.get("direction"),
             "threshold": margin, "threshold_kind": "margin" if margin is not None else "zero",
             "display_unit": spec.get("display_unit", ""), "margin_source": spec.get("source", "pre-registration")}
    if sign == 0:
        return {**entry, "verdict": "no_direction"}
    if m is None:
        return {**entry, "verdict": "missing"}
    iv = interval(m, unit, levels["guardrail"], base, sequential)
    harm_iv = zero_interval(m, levels["harm"], base, sequential)
    zero = zero_interval(m, levels["guardrail"], base, sequential)
    if iv is None or harm_iv is None:
        return {**entry, "verdict": "no_interval"}
    point, low, high, se = iv
    entry.update(point=point, low=low, high=high, se=se, level=levels["guardrail"])
    gpoint, glow, _, _ = oriented(iv, sign)
    harm = oriented(harm_iv, sign)[2] < 0
    shown_worse = oriented(zero, sign)[2] < 0
    if margin is None:
        verdict = "breached" if harm else "no_harm_detected"
    elif glow >= -margin:
        verdict = "harm_within_margin" if harm else "within"
    elif gpoint < -margin and shown_worse:
        verdict = "breached"
    else:
        verdict = "undetermined"
    entry["verdict"] = verdict
    return entry


def judge_invariant(spec, m, level, base):
    entry = {"metric": spec["metric"], "role": "invariant", "unit": "relative", "threshold": 0, "threshold_kind": "zero"}
    if m is None:
        return {**entry, "verdict": "missing"}
    iv = interval(m, "relative", level, base)
    if iv is None:
        return {**entry, "verdict": "no_interval"}
    point, low, high, se = iv
    moved = low > 0 or high < 0
    return {**entry, "point": point, "low": low, "high": high, "se": se, "level": level,
            "verdict": "moved" if moved else "held"}


def merge_standards(standards):
    merged = dict(DEFAULT_STANDARDS)
    merged.update(standards or {})
    return merged


def pick_comparison(scorecard, prereg):
    comparisons = scorecard.get("comparisons") or []
    if not comparisons:
        raise InputError("the scorecard has no comparisons")
    wanted = prereg.get("test_group")
    if wanted:
        for c in comparisons:
            if str(c.get("test_group")).lower() == str(wanted).lower():
                return c
        raise InputError(f"test group '{wanted}' is not in the scorecard ({[c.get('test_group') for c in comparisons]})")
    if len(comparisons) > 1:
        raise InputError("the scorecard has several test groups; set 'test_group' in the pre-registration")
    return comparisons[0]


def decide(scorecard, prereg, config=None, standards=None, daily=None):
    std = merge_standards(standards)
    analysis = scorecard.get("analysis") or {}
    fallbacks = []
    if not prereg.get("confirmed"):
        fallbacks.append("the pre-registration was transcribed, not confirmed by the owner")
    base = prereg.get("ci_level") or analysis.get("ci_level") or ((config or {}).get("settings") or {}).get("ci_level")
    if not base:
        base = 0.95
        fallbacks.append("confidence level not stated anywhere; assumed 95%")
    comparison = pick_comparison(scorecard, prereg)
    metrics = comparison["metrics"]
    primaries = (prereg.get("primaries") or {}).get("metrics") or []
    if not primaries:
        raise InputError("the pre-registration names no primary metric")
    rule = (prereg.get("primaries") or {}).get("rule", "all")
    ship_requires = (prereg.get("primaries") or {}).get("ship_requires", "point_at_bar")
    guard_specs = prereg.get("guardrails")
    if guard_specs is None:
        guard_specs = [{**g, "source": "team standard"} for g in std["guardrails"]]
        if guard_specs:
            fallbacks.append("guardrails and margins from the team standard, not the pre-registration")
    for g in guard_specs:
        if not g.get("direction") and std["directions"].get(g["metric"]):
            g["direction"] = std["directions"][g["metric"]]
    registered = len(primaries) + len(guard_specs)
    alpha = 1 - base
    levels = {"primary": 1 - alpha / len(primaries) if rule == "any" and len(primaries) > 1 else base,
              "guardrail": base, "harm": 1 - alpha / max(registered, 1)}
    configured = ((config or {}).get("settings") or {}).get("sequential")
    sequential = bool(prereg.get("sequential") or (analysis.get("sequential") if analysis.get("sequential") is not None
                                                   else configured))
    if sequential and not any(m.get("seq_rel_ci") or m.get("seq_abs_ci") for m in metrics):
        fallbacks.append("sequential testing is on but the scorecard has no sequential intervals; used fixed-horizon ones")
        sequential = False

    checks = []
    design = (prereg.get("design") or "ab").lower()
    primary_metric = find(metrics, primaries[0]["metric"])
    registered_metrics = [m for m in (find(metrics, s["metric"]) for s in primaries + guard_specs) if m]
    checks.append(chk.scorecard_invariants(registered_metrics, analysis))
    checks.append(chk.sample_split(config, primary_metric, std["srm_alpha"], prereg.get("explanations")))
    checks.extend(chk.config_checks(config, prereg, analysis.get("as_of")))
    checks.append(chk.pre_period(prereg, config, primaries[0]["metric"]))

    verdicts = []
    for spec in primaries:
        m = find(metrics, spec["metric"])
        verdicts.append(judge_primary(spec, m, levels, base, sequential, ship_requires) if m else
                        {"metric": spec["metric"], "role": "primary", "verdict": "missing"})
    for spec in guard_specs:
        verdicts.append(judge_guardrail(spec, find(metrics, spec["metric"]), levels, base, sequential))
    for spec in prereg.get("invariants") or []:
        verdicts.append(judge_invariant(spec, find(metrics, spec["metric"]), base, base))
    prim = [v for v in verdicts if v["role"] == "primary"]
    guards = [v for v in verdicts if v["role"] == "guardrail"]

    lead = prim[0]
    lead_sign = sign_of(lead.get("direction")) or 1
    checks.append(chk.novelty(daily, lead_sign * (1 if lead.get("point", 0) >= 0 else -1)))

    registered_names = {s["metric"].strip().lower() for s in primaries + guard_specs + (prereg.get("invariants") or [])}
    secondaries = [m for m in metrics if m["metric"].strip().lower() not in registered_names and m.get("p_value") is not None]
    survivors = [secondaries[i] for i in expstats.benjamini_hochberg([m["p_value"] for m in secondaries], std["secondary_q"])]
    harmful = [m for m in survivors if sign_of(m.get("directionality")) * (m.get("rel_delta") or m.get("abs_delta") or 0) < 0]

    status = study_status(config, analysis, prereg, primary_metric, std, fallbacks)
    call, decider, reason = rule_chain(design, checks, prim, guards, verdicts, status, sequential, std, rule, harmful)
    open_items = collect_open_items(verdicts, checks, fallbacks, status, harmful, call)
    return {
        "call": call, "call_text": CALL_TEXT[call], "reason": reason, "ask": ASK[call], "decider": decider,
        "status": status, "verdicts": verdicts, "checks": checks,
        "secondaries": {"tested": len(secondaries), "q": std["secondary_q"],
                        "survivors": [{"metric": m["metric"], "rel_delta": m.get("rel_delta"), "rel_ci": m.get("rel_ci"),
                                       "p_value": m["p_value"], "directionality": m.get("directionality")} for m in survivors]},
        "open_items": open_items, "fallbacks": fallbacks,
        "settings": {"ci_level": base, "levels": levels, "sequential": sequential, "rule": rule,
                     "ship_requires": ship_requires, "cuped": analysis.get("cuped"),
                     "mc_correction": analysis.get("mc_correction"), "standards": {k: std[k] for k in (
                         "harm_within_margin", "below_bar", "secondary_harm", "srm_alpha", "min_days")}},
        "experiment": {"id": prereg.get("experiment_id") or scorecard.get("experiment_id"),
                       "name": prereg.get("name") or (config or {}).get("name") or prereg.get("experiment_id"),
                       "test_group": comparison.get("test_group"), "design": design},
    }


def study_status(config, analysis, prereg, primary_metric, std, fallbacks):
    planned = prereg.get("planned") or {}
    start = (config or {}).get("start") or prereg.get("start")
    restarts = [e["date"] for e in (config or {}).get("edits", []) if e.get("action") in chk.RESTARTS and e.get("date")]
    window_start = max(restarts + [start]) if start else None
    as_of = analysis.get("as_of")
    days = prereg.get("days_run") or (chk.days_between(window_start, as_of) if window_start and as_of else None)
    units = None
    if primary_metric and primary_metric.get("control_units") and primary_metric.get("test_units"):
        units = int(min(primary_metric["control_units"], primary_metric["test_units"]))
    planned_days, planned_units = planned.get("days"), planned.get("units_per_arm")
    if planned_days is None and planned_units is None:
        planned_days = std["min_days"]
        fallbacks.append(f"no planned duration registered; used the team minimum of {planned_days} days")
    reached = True
    if planned_days is not None:
        reached = reached and days is not None and days >= planned_days
    if planned_units is not None:
        reached = reached and units is not None and units >= planned_units
    if days is None:
        fallbacks.append("days run unknown (no start date or results date)")
    return {"days_run": days, "planned_days": planned_days, "units_per_arm": units, "planned_units": planned_units,
            "reached": reached, "whole_weeks": None if days is None else days % 7 == 0,
            "window_start": window_start, "as_of": as_of}


def rule_chain(design, checks, prim, guards, verdicts, status, sequential, std, rule, harmful):
    """The ordered rules. Returns (call, decider, reason)."""
    lead = prim[0]
    if design != "ab":
        return "not_ab", {"check": "design", "summary": design}, f"This is a {design} test; the A/B launch rule doesn't apply."
    blocking = [c for c in checks if c["status"] == chk.FAIL and c["check"] != "novelty"]
    if blocking:
        c = blocking[0]
        return "cant_tell", {"check": c["check"], "summary": c["summary"]}, f"{_sentence(c['summary'])} No launch decision from this data until it's fixed."
    for v in prim:
        if v["verdict"] in ("missing", "no_interval"):
            return "cant_tell", {"metric": v["metric"], "role": "primary", "verdict": v["verdict"]}, \
                f"The primary metric {v['metric']} is {'not in the scorecard' if v['verdict'] == 'missing' else 'missing an interval'}."
    moved = [v for v in verdicts if v["role"] == "invariant" and v["verdict"] == "moved"]
    if moved:
        v = moved[0]
        return "cant_tell", v, f"{v['metric']} moved {describe(v)} though the change shouldn't touch it, so the arms aren't comparable."

    breached = [v for v in guards if v["verdict"] == "breached"]
    if breached:
        v = max(breached, key=lambda g: abs(g["point"]) / (g["threshold"] or abs(g["point"]) or 1))
        limit = f"past its {threshold_text(v['threshold'], v['unit'], v.get('display_unit', ''))} margin" if v["threshold"] is not None \
            else "and the change is clearly worse than zero"
        return "dont_ship", v, f"{v['metric']} moved the wrong way, {describe(v)}, {limit}."
    worse = [v for v in prim if v["verdict"] == "worse"]
    if worse:
        v = worse[0]
        return "dont_ship", v, f"{v['metric']} moved the wrong way, {describe(v)}."

    early = not status["reached"] and (not sequential or lead["verdict"] == "undetermined")
    if early:
        where = (f"day {status['days_run']} of {status['planned_days']}" if status["days_run"] is not None
                 and status["planned_days"] else "before the planned sample")
        return "keep_running", lead, f"It's {where}; {lead['metric']} reads {describe(lead)} so far, too early to call."
    novelty = next((c for c in checks if c["check"] == "novelty"), None)
    if novelty and novelty["status"] == chk.FLAG and lead["verdict"] in ("better", "below_bar"):
        return "keep_running", {"check": "novelty", "summary": novelty["summary"], "metric": lead["metric"]}, \
            f"{lead['metric']} reads {describe(lead)} overall, but the effect is fading over the days of the test."

    no_dir = [v for v in verdicts if v["verdict"] == "no_direction"]
    if no_dir:
        return "escalate", no_dir[0], f"{no_dir[0]['metric']} has no registered direction, so the rule can't say whether its move is good."
    flagged = [c for c in checks if c["status"] == chk.FLAG and c["check"] in ("sample_split", "pre_period")]
    if flagged:
        return "escalate", {"check": flagged[0]["check"], "summary": flagged[0]["summary"]}, \
            f"{_sentence(flagged[0]['summary'])} Triage should confirm the explanation before any launch."

    better = [v for v in prim if v["verdict"] in ("better", "below_bar")]
    if lead["verdict"] == "undetermined" and not better:
        if lead.get("threshold") is None:
            return "escalate", lead, f"{lead['metric']} reads {describe(lead)}; no bar is registered, so 'no effect' can't be shown."
        if lead.get("rules_out_bar"):
            return "no_effect", lead, (f"{lead['metric']} reads {describe(lead)}, which rules out the "
                                       f"{threshold_text(lead['threshold'], lead['unit'])} change the test was built to find.")
        factor = (lead["achieved_mde"] / lead["threshold"]) ** 2 if lead["threshold"] else float("inf")
        if factor <= std["max_extension_factor"]:
            return "keep_running", lead, (f"{lead['metric']} reads {describe(lead)}; ruling out the "
                                          f"{threshold_text(lead['threshold'], lead['unit'])} bar needs about "
                                          f"{factor:.1f} times the users so far.")
        return "escalate", lead, (f"{lead['metric']} reads {describe(lead)}; this test is too small to rule out the "
                                  f"{threshold_text(lead['threshold'], lead['unit'])} bar (it would need about {factor:.0f} times the users).")
    if rule == "all" and len(better) < len(prim):
        other = next(v for v in prim if v not in better)
        return "escalate", other, f"{better[0]['metric']} improved but {other['metric']} is undetermined, {describe(other)}; the test needs every primary to improve."

    missing = [v for v in guards if v["verdict"] in ("missing", "no_interval")]
    undetermined = [v for v in guards if v["verdict"] == "undetermined"]
    within_harm = [v for v in guards if v["verdict"] == "harm_within_margin"]
    head = f"{lead['metric']} improved {describe(lead)}"
    if missing:
        v = missing[0]
        return "escalate", v, f"{head}, but guardrail {v['metric']} is {'not in the scorecard' if v['verdict'] == 'missing' else 'missing an interval'}."
    if undetermined:
        v = undetermined[0]
        return "escalate", v, (f"{head}, but {v['metric']} ({describe(v)}) isn't shown within its "
                               f"{threshold_text(v['threshold'], v['unit'], v.get('display_unit', ''))} margin.")
    if within_harm and std["harm_within_margin"] != "allow":
        v = within_harm[0]
        call = "dont_ship" if std["harm_within_margin"] == "block" else "escalate"
        return call, v, (f"{head}, but {v['metric']} got worse, {describe(v)}, inside its "
                         f"{threshold_text(v['threshold'], v['unit'], v.get('display_unit', ''))} margin.")
    below = [v for v in prim if v["verdict"] == "below_bar"]
    if below and std["below_bar"] != "ship":
        v = below[0]
        call = "dont_ship" if std["below_bar"] == "dont_ship" else "escalate"
        return call, v, f"{v['metric']} improved {describe(v)}, real but short of the {threshold_text(v['threshold'], v['unit'])} bar."
    if harmful and std["secondary_harm"] == "escalate":
        return "escalate", {"metric": harmful[0]["metric"], "role": "secondary"}, \
            f"{head}, but secondary metric {harmful[0]['metric']} got worse after correction for many metrics."
    bar = f", which clears the {threshold_text(lead['threshold'], lead['unit'])} bar" if lead.get("threshold") is not None else ""
    guard_note = " and every guardrail held" if guards else "; no guardrails were registered"
    return "ship", lead, f"{head}{bar}{guard_note}."


def collect_open_items(verdicts, checks, fallbacks, status, harmful, call):
    items = []
    for v in verdicts:
        if v["verdict"] == "harm_within_margin" and v.get("point") is not None:
            items.append(f"{v['metric']} got worse inside its margin ({describe(v)})")
        if v["verdict"] == "undetermined" and v["role"] == "guardrail":
            items.append(f"{v['metric']} isn't shown within its margin ({describe(v)})")
    for c in checks:
        if c["status"] == chk.COULD_NOT_RUN:
            items.append(f"{c['check'].replace('_', ' ')} could not be checked: {c['summary']}")
        elif c["status"] == chk.FLAG:
            items.append(c["summary"])
    items.extend(fallbacks)
    if status.get("whole_weeks") is False:
        items.append(f"{status['days_run']} days is not whole weeks, so day-of-week mix differs from a full week")
    for m in harmful:
        items.append(f"secondary metric {m['metric']} got worse after correction")
    return items


def _sentence(text):
    text = text.strip()
    return (text[0].upper() + text[1:]).rstrip(".") + "."


def log_decision(decision):
    path = os.environ.get("DS_CHECKS_LOG") or os.path.join(os.getcwd(), ".ds-checks.log")
    entry = {"ts": round(time.time(), 3), "check": "ds_experiment_decide", "status": decision["call"],
             "summary": decision["reason"], "details": {"decider": decision["decider"].get("metric") or decision["decider"].get("check")}}
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, sort_keys=True) + "\n")


def load(path):
    if not path:
        return None
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--scorecard", required=True)
    parser.add_argument("--prereg", required=True)
    parser.add_argument("--config")
    parser.add_argument("--standards")
    parser.add_argument("--daily", help="JSON list of {day, rel_delta, rel_ci, basis} for the primary")
    parser.add_argument("--out")
    args = parser.parse_args(argv)
    try:
        decision = decide(load(args.scorecard), load(args.prereg), load(args.config), load(args.standards), load(args.daily))
    except (OSError, ValueError, KeyError) as err:
        print(f"decide: {err}", file=sys.stderr)
        return 2
    out = args.out or os.path.join(os.path.dirname(os.path.abspath(args.scorecard)), "decision.json")
    with open(out, "w", encoding="utf-8") as handle:
        json.dump(decision, handle, indent=2)
    log_decision(decision)
    for c in decision["checks"]:
        print(f"check {c['check']}: {c['status']} - {c['summary']}")
    for v in decision["verdicts"]:
        shown = describe(v) if v.get("point") is not None else ""
        print(f"{v['role']} {v['metric']}: {v['verdict']} {shown}")
    print(f"decide: {decision['call_text']} - {decision['reason']}")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
