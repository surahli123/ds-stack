#!/usr/bin/env python3
"""Regression cases from the adversarial pressure test of ds-experiment (2026-10-12).

Same shape as eval/experiment/cases/<id>/, plus expected.json ({"call", "decider", "why"},
or {"exit": 2, "message": ...} for inputs the tools must refuse) and, where a case needs a
non-default invocation, run.json ({"pulse": ["FILE:GROUP", ...], "daily": name}).

    python3 eval/experiment/make_regressions.py
"""
import copy
import json
import os
import random
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "eval", "experiment"))
import make_cases as mc  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "regressions")
DEFS = []


def case(cid, title, expected, overrides=None, exp=None, pre=None, request=None, days=None, audit=None,
         units=(mc.UNITS, mc.UNITS), primaries=("Successful Search Rate",), pulse_hook=None, extra=None, run=None):
    DEFS.append(dict(cid=cid, title=title, expected=expected, overrides=overrides if overrides is not None else mc.WIN,
                     exp=exp, pre=pre, request=request, days=days, audit=audit, units=units, primaries=primaries,
                     pulse_hook=pulse_hook, extra=extra or {}, run=run))


def exp_(call, decider, why):
    return {"call": call, "decider": decider, "why": why}


def all_records(p):
    return p["data"]["primaryMetrics"] + p["data"]["secondaryMetrics"]


# f01: margin in absolute units, breached. Latency +3.1% of 412ms = +12.8ms past a 10ms margin.
case("f01_abs_margin_breach", "absolute 10ms latency margin, breached",
     exp_("dont_ship", "Latency p95 (ms)", "latency +12.8ms (+10.3 to +15.2) past its 10ms margin"),
     overrides={**mc.WIN, "Latency p95 (ms)": {"rel": 0.031, "half": 0.006}},
     pre=mc.prereg(guardrails=[{"metric": "Latency p95 (ms)", "direction": "decrease", "margin": 10,
                                "margin_unit": "absolute", "display_unit": "ms"},
                               {"metric": "Abandonment Rate", "direction": "decrease", "margin": 0.01}]))

# f02: same numbers, but the analyst wrote margin 10 meaning ms and forgot margin_unit.
case("f02_abs_margin_no_unit", "margin 10 (meant ms) without margin_unit",
     exp_("dont_ship", "Latency p95 (ms)", "same breach; a relative margin of 1000% is a unit error, not a margin"),
     overrides={**mc.WIN, "Latency p95 (ms)": {"rel": 0.031, "half": 0.006}},
     pre=mc.prereg(guardrails=[{"metric": "Latency p95 (ms)", "direction": "decrease", "margin": 10},
                               {"metric": "Abandonment Rate", "direction": "decrease", "margin": 0.01}]))

# f03: bar written in percent (0.5 meaning 0.5%) on a clean win.
case("f03_bar_percent_as_fraction", "bar 0.5 meant 0.5% on the s1 win",
     exp_("ship", "Successful Search Rate", "+0.81% clears a 0.5% bar; a 50% relative bar is a unit error"),
     pre=mc.prereg(primaries={"rule": "all", "ship_requires": "point_at_bar",
                              "metrics": [{"metric": "Successful Search Rate", "direction": "increase", "bar": 0.5}]}))

# f04: decrease-is-good primary whose improvement fades by exposure day.
case("f04_decrease_good_fading", "time to first click (decrease is good) fading by exposure day",
     exp_("keep_running", "Time to First Click (s)", "effect fades from about -3.5% to -0.8% by exposure day"),
     overrides={**mc.GUARDS, "Time to First Click (s)": {"rel": -0.020, "half": 0.006}},
     primaries=("Time to First Click (s)",),
     pre=mc.prereg(primaries={"rule": "all", "ship_requires": "point_at_bar",
                              "metrics": [{"metric": "Time to First Click (s)", "direction": "decrease", "bar": 0.01}]}),
     days={"daily_by_exposure_day.json": mc.daily([-0.035, -0.032, -0.029, -0.026, -0.023, -0.020, -0.017, -0.015,
                                                   -0.013, -0.011, -0.009, -0.008])})

# f05: rule any, three primaries, the first flat and the second clearly up.
ANY3 = {"rule": "any", "ship_requires": "point_at_bar", "metrics": [
    {"metric": "Successful Search Rate", "direction": "increase", "bar": 0.005},
    {"metric": "CTR", "direction": "increase", "bar": 0.005},
    {"metric": "Long Click Rate", "direction": "increase", "bar": 0.005}]}
case("f05_any_rule_lead_flat", "any-rule, 3 primaries, lead flat, CTR clears",
     exp_("ship", "CTR", "under 'any', CTR +1.5% clears the bar; the decider and reason must name CTR"),
     overrides={**mc.GUARDS, "Successful Search Rate": {"rel": 0.0005, "half": 0.003},
                "CTR": {"rel": 0.015, "half": 0.005}, "Long Click Rate": {"rel": 0.0, "half": 0.006}},
     primaries=("Successful Search Rate", "CTR", "Long Click Rate"), pre=mc.prereg(primaries=ANY3))

# f06: rule any, lead real but below the bar, CTR clears.
case("f06_any_rule_lead_below_bar", "any-rule, lead +0.31% below bar, CTR clears",
     exp_("ship", "CTR", "under 'any' one primary clearing the bar is enough"),
     overrides={**mc.GUARDS, "Successful Search Rate": {"rel": 0.0031, "half": 0.0018},
                "CTR": {"rel": 0.015, "half": 0.005}, "Long Click Rate": {"rel": 0.0, "half": 0.006}},
     primaries=("Successful Search Rate", "CTR", "Long Click Rate"), pre=mc.prereg(primaries=ANY3))

# f07: two test arms through two pulse files; arm B breaches latency.
case("f07_multi_arm", "two arms, B breaches latency; prereg picks g_test_b",
     exp_("dont_ship", "Latency p95 (ms)", "arm B latency +3.1% past its 2% margin"),
     pre=mc.prereg(test_group="g_test_b"),
     exp=mc.experiment("Ranker v7", sizes=(34, 33), extra={"groups": [
         {"id": "g_control", "name": "Control", "size": 34, "parameterValues": {"ranker_model": "lambdamart_v6", "snippet_length": "160"}},
         {"id": "g_test", "name": "Test A", "size": 33, "parameterValues": {"ranker_model": "lambdamart_v7", "snippet_length": "160"}},
         {"id": "g_test_b", "name": "Test B", "size": 33, "parameterValues": {"ranker_model": "lambdamart_v7b", "snippet_length": "160"}}]}),
     run={"pulse": ["pulse.json", "pulse_b.json"]},
     extra={"pulse_b": {**mc.WIN, "Latency p95 (ms)": {"rel": 0.031, "half": 0.006}}})

# f08: guardrail name off by punctuation while the metric itself is breached.
case("f08_guardrail_near_miss_breached", "prereg says 'Latency P95 ms', scorecard has 'Latency p95 (ms)' at +3.1%",
     exp_("dont_ship", "Latency p95 (ms)", "the breach is in the scorecard under a near-identical name"),
     overrides={**mc.WIN, "Latency p95 (ms)": {"rel": 0.031, "half": 0.006}},
     pre=mc.prereg(guardrails=[{"metric": "Latency P95 ms", "direction": "decrease", "margin": 0.02},
                               {"metric": "Abandonment Rate", "direction": "decrease", "margin": 0.01}]))

# f09: CUPED on and percent given as a fraction (should be caught).
case("f09_cuped_fraction_mixup", "CUPED on, percentChange as a fraction",
     exp_("cant_tell", "scorecard", "relative x control disagrees with the absolute change"),
     request={"cuped": "true", "confidence": "95"},
     pulse_hook=lambda p: [m.update(percentChange=round(m["percentChange"] / 100, 8),
                                    percentConfidenceIntervalDelta=round(m["percentConfidenceIntervalDelta"] / 100, 8))
                           for m in all_records(p)] + [m.update(testMean=round(m["controlMean"] * 1.0035, 8)) for m in p["data"]["primaryMetrics"]])


def strip_means_and_abs(p):
    for m in all_records(p):
        for k in ("controlMean", "testMean", "absoluteChange", "absoluteConfidenceIntervalDelta"):
            m.pop(k, None)
        m["percentChange"] = round(m["percentChange"] / 100, 8)
        m["percentConfidenceIntervalDelta"] = round(m["percentConfidenceIntervalDelta"] / 100, 8)


# f10: the same mix-up on an export that carries only relative values (no means, no absolute).
case("f10_fraction_mixup_no_means", "percentChange as a fraction, export has no means or absolutes",
     exp_("cant_tell", "scorecard", "nothing to cross-check; a +0.81% win reads as +0.008%"),
     pulse_hook=strip_means_and_abs)

# f11: sequential intervals narrower than the fixed ones (bad export), day 7 of 14.
case("f11_seq_narrower_than_fixed", "sequential half-width is half the fixed one, day 7 of 14",
     exp_("cant_tell", "scorecard", "a sequential interval can't be narrower than the fixed one; at best keep running"),
     overrides={**mc.GUARDS, "Successful Search Rate": {"rel": 0.0055, "half": 0.0040}}, units=(480000, 481000),
     request={"confidence": "95", "cuped": "false", "sequential": True}, pre=mc.prereg(sequential=True),
     pulse_hook=lambda p: [p["data"].update(ds="2026-09-18")] + [
         m.update(sequentialTestingConfidenceIntervalDelta=round(m["absoluteConfidenceIntervalDelta"] * 0.5, 8),
                  percentSequentialTestingConfidenceIntervalDelta=round(m["percentConfidenceIntervalDelta"] * 0.5, 6))
         for m in all_records(p)])

# f12: results requested at 90%, pre-registration at 95%. Abandonment +0.5% with a 90% half-width of 0.477%
# (95% would be 0.568%): within the 1% margin at 90%, not at 95%.
case("f12_ci90_read_as_95", "request confidence 90, prereg ci_level 0.95, abandonment just inside at 90%",
     exp_("escalate", "Abandonment Rate", "at the registered 95% the upper end is +1.07%, past the 1% margin"),
     overrides={**mc.WIN, "Abandonment Rate": {"rel": 0.005, "half": 0.00477}},
     request={"cuped": "false", "confidence": "90"})

# f13: an explained SRM.
case("f13_explained_srm", "c1's split with a listed explanation",
     exp_("escalate", "sample_split", "explanation listed in the prereg softens the fail to a flag; triage confirms"),
     exp=mc.experiment("Ranker v7", extra={"exposures": {"Control": 1010000, "Test": 990000}}),
     pre=mc.prereg(explanations=[{"check": "sample_split", "cause": "bot filter v3 applied to control only until day 2",
                                  "evidence": "infra ticket SRCH-4412; exposures balanced from 2026-09-14"}]))

# f14: allocation edit and a restart on the same day; 14 days of results after the restart.
case("f14_restart_same_day_edit", "edit then restart on 09-16, results through 09-29",
     exp_("ship", "Successful Search Rate", "the restart resets the window; the edit is before it"),
     audit={"data": [{"actionType": "experiment_edit", "date": "2026-09-16", "changeLog": "Allocation changed from 20% to 10%",
                      "changes": {"allocation": {"old": 20, "new": 10}}},
                     {"actionType": "experiment_restart", "date": "2026-09-16", "changeLog": "Pulse results restarted"}]},
     pulse_hook=lambda p: p["data"].update(ds="2026-09-29"))

# f15: the audit log holds the start event only.
case("f15_benign_start_event", "audit log has the experiment_start entry on the start date",
     exp_("ship", "Successful Search Rate", "a start event is not an edit and not a restart"),
     audit={"data": [{"actionType": "experiment_start", "date": "2026-09-12", "changeLog": "Experiment started"}]})

# f16: only a calendar-day series exists (s3's), passed as --daily.
case("f16_calendar_only", "s3 win, only the calendar-day series is available",
     exp_("ship", "Successful Search Rate", "a calendar-day fade is day-of-week and late joiners; ship with the exposure-day cut as an open item"),
     days={"daily_by_calendar_day.json": mc.daily([0.0125, 0.0118, 0.0102, 0.0095, 0.0088, 0.0071, 0.0066, 0.0084, 0.0079, 0.0070, 0.0061, 0.0058, 0.0054, 0.0050], basis="calendar_day"),
           "daily_no_basis.json": mc.daily([0.0125, 0.0118, 0.0102, 0.0095, 0.0088, 0.0071, 0.0066, 0.0084, 0.0079, 0.0070, 0.0061, 0.0058, 0.0054, 0.0050])},
     run={"daily": "daily_by_calendar_day.json"})
for d in DEFS[-1:]:
    d["days"]["daily_no_basis.json"] = [{k: v for k, v in p.items() if k != "basis"} for p in d["days"]["daily_no_basis.json"]]

# f17: triggered primary with an undetermined interval and mass_share.
case("f17_mass_share_undetermined", "triggered +0.5% (-0.3 to +1.3), mass share 0.2",
     exp_("no_effect", "Successful Search Rate", "overall +0.10% (-0.06 to +0.26) rules out the 0.5% overall bar, but the readout must say it was scaled"),
     overrides={**mc.GUARDS, "Successful Search Rate": {"rel": 0.005, "half": 0.008}},
     pre=mc.prereg(primaries={"rule": "all", "ship_requires": "point_at_bar", "metrics": [
         {"metric": "Successful Search Rate", "direction": "increase", "bar": 0.005, "population": "triggered", "mass_share": 0.2}]}))

# f18: e4's triggered lift, but the triggered population is 100k users per arm.
case("f18_triggered_units_short", "e4 with 100k triggered users per arm, planned 900k overall",
     exp_("escalate", "Successful Search Rate", "+0.39% overall after scaling, below the bar; units planned refer to overall"),
     overrides={**mc.GUARDS, "Successful Search Rate": {"rel": 0.019, "half": 0.006}}, units=(100000, 100000),
     pre=mc.prereg(primaries={"rule": "all", "ship_requires": "point_at_bar", "metrics": [
         {"metric": "Successful Search Rate", "direction": "increase", "bar": 0.005, "population": "triggered", "mass_share": 0.205}]}))


def add_zero_control_secondary(p):
    r = mc.record("Sponsored Module Clicks per User", "mean", 0.0, "increase", 0.0, 0.0)
    r.update(controlMean=0.0, testMean=0.05, absoluteChange=0.05, absoluteConfidenceIntervalDelta=0.01,
             percentChange=None, percentConfidenceIntervalDelta=None, pValue=0.00001)
    p["data"]["secondaryMetrics"].append(r)


# f19: a zero-control-mean secondary that survives correction.
case("f19_zero_control_mean_secondary", "s1 plus a new-module metric with control mean 0",
     exp_("ship", "Successful Search Rate", "ship; the appendix must list the survivor sensibly"),
     pulse_hook=add_zero_control_secondary)

# f20: no p-values anywhere.
case("f20_no_pvalues", "s1 with pValue removed from every record",
     exp_("ship", "Successful Search Rate", "ship; the appendix must not claim 0 secondaries were tested"),
     pulse_hook=lambda p: [m.pop("pValue", None) for m in all_records(p)])


def add_invariants(p):
    rng = random.Random(7)
    for name, rel_mult in (("Exposures per User", 0.0), ("Logged-in Share", 0.3), ("App Version Share", -0.4),
                           ("Pre-period CTR", 1.1)):
        half = 0.004
        p["data"]["secondaryMetrics"].append(mc.record(name, "mean", 1.0 if "Share" not in name else 0.6, "increase",
                                                       rel_mult * half, half))


# f21: four invariants, one at p ~ 0.03.
case("f21_invariants_multiplicity", "four invariants, one crosses zero at p~0.03",
     exp_("ship", "Successful Search Rate", "one of four invariants at p=0.03 is chance; invariants need a tighter alpha"),
     pulse_hook=add_invariants,
     pre=mc.prereg(invariants=[{"metric": "Exposures per User"}, {"metric": "Logged-in Share"},
                               {"metric": "App Version Share"}, {"metric": "Pre-period CTR"}]))

# f22: a registered invariant that isn't in the scorecard.
case("f22_missing_invariant", "s1 plus an invariant the scorecard doesn't carry",
     exp_("escalate", "Exposures per User", "a registered check that can't run should not vanish"),
     pre=mc.prereg(invariants=[{"metric": "Exposures per User"}]))

# f23: unit spelled user_id in the prereg, userID in the config.
case("f23_unit_spelling", "prereg unit 'user_id' vs config idType 'userID'",
     exp_("ship", "Successful Search Rate", "same unit, different spelling"),
     pre=mc.prereg(unit="user_id"))

# f24: request.json says "sequential": "false" as a string; the export carries sequential intervals anyway.
case("f24_sequential_string_false", "fixed-horizon test at day 14, request sequential 'false' (string), seq intervals present",
     exp_("ship", "Successful Search Rate", "+0.55% (+0.15 to +0.95) at the planned sample clears the bar"),
     overrides={**mc.GUARDS, "Successful Search Rate": {"rel": 0.0055, "half": 0.0040}},
     request={"confidence": "95", "cuped": "false", "sequential": "false"},
     pulse_hook=lambda p: [m.update(sequentialTestingConfidenceIntervalDelta=round(m["absoluteConfidenceIntervalDelta"] * 1.9, 8),
                                    percentSequentialTestingConfidenceIntervalDelta=round(m["percentConfidenceIntervalDelta"] * 1.9, 6))
                           for m in all_records(p)])

# f25: the pulse response has no ds field.
case("f25_missing_ds", "s1 without the ds field in the response",
     exp_("ship", "Successful Search Rate", "day count unknown is not 'before the planned sample' when units exceed the plan"),
     pulse_hook=lambda p: p["data"].pop("ds"))

# f26: an invariant guardrail: primary in absolute units (seconds).
case("f26_abs_bar_primary", "time to first click with an absolute bar of 0.1s",
     exp_("ship", "Time to First Click (s)", "-0.13s clears a 0.1s absolute bar"),
     overrides={**mc.GUARDS, "Time to First Click (s)": {"rel": -0.020, "half": 0.006}},
     primaries=("Time to First Click (s)",),
     pre=mc.prereg(primaries={"rule": "all", "ship_requires": "point_at_bar",
                              "metrics": [{"metric": "Time to First Click (s)", "direction": "decrease", "bar": 0.1, "bar_unit": "absolute"}]}))


def build():
    os.makedirs(OUT, exist_ok=True)
    for i, d in enumerate(DEFS):
        rng = random.Random(5000 + i)
        directory = os.path.join(OUT, d["cid"])
        os.makedirs(directory, exist_ok=True)
        pulse = mc.scorecard(rng, {**mc.GUARDS, **d["overrides"]}, d["units"], d["primaries"])
        if d["pulse_hook"]:
            d["pulse_hook"](pulse)
        request = d["request"] or {"control": "g_control", "test": "g_test", "cuped": "false", "confidence": "95"}
        request = {"control": "g_control", "test": "g_test", **request}
        files = {"pulse.json": pulse, "experiment.json": d["exp"] or mc.experiment("Ranker v7"),
                 "audit_logs.json": d["audit"] or {"data": []}, "request.json": request,
                 "prereg.json": d["pre"] or mc.prereg(), "expected.json": {"title": d["title"], **d["expected"]}}
        if d["run"]:
            files["run.json"] = d["run"]
        if "pulse_b" in d["extra"]:
            files["pulse_b.json"] = mc.scorecard(random.Random(9000 + i), {**mc.GUARDS, **d["extra"]["pulse_b"]}, d["units"], d["primaries"])
        files.update(d["days"] or {})
        for name, content in files.items():
            with open(os.path.join(directory, name), "w") as handle:
                json.dump(content, handle, indent=1)
    # Where the tools deliberately differ from the tester's first expectation.
    decided = {
        "f02_abs_margin_no_unit": {"exit": 2, "message": "margin_unit",
                                   "why": "a relative margin of 10 (1000%) is refused with a hint, never guessed"},
        "f03_bar_percent_as_fraction": {"exit": 2, "message": "bar_unit",
                                        "why": "a relative bar of 0.5 (50%) is refused with a hint, never guessed"},
        "f10_fraction_mixup_no_means": {"call": "escalate", "decider": "scorecard",
                                        "why": "units can't be verified without control means: escalate, don't call it broken"},
    }
    for cid, expected in decided.items():
        path = os.path.join(OUT, cid, "expected.json")
        with open(path) as handle:
            old = json.load(handle)
        with open(path, "w") as handle:
            json.dump({"title": old.get("title"), **expected}, handle, indent=1)
    run_path = os.path.join(OUT, "f07_multi_arm", "run.json")
    with open(run_path, "w") as handle:
        json.dump({"pulse": ["pulse.json:g_test", "pulse_b.json:g_test_b"]}, handle, indent=1)
    print(f"wrote {len(DEFS)} cases to {OUT}")


if __name__ == "__main__":
    build()
