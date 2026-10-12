#!/usr/bin/env python3
"""Generate synthetic search-ranking experiments, each with one planted pitfall.

    python3 eval/experiment/make_cases.py

Each case directory holds what an analyst would have: a Statsig-shaped Pulse
response (pulse.json) with about 60 metrics, the experiment config
(experiment.json), its audit log, the request settings, the pre-registration,
sometimes a daily effect series, and the task. Gold goes to gold/<case>.json and
is never copied into a run. Deterministic: the same seed gives the same files.
"""

import json
import math
import os
import random
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
CASES, GOLD = os.path.join(HERE, "cases"), os.path.join(HERE, "gold")
START_MS = 1789171200000  # 2026-09-12 00:00 UTC
Z95 = 1.959964

# name, type, control mean, good direction, typical relative half-width of a 95% interval
BASE = [
    ("Successful Search Rate", "ratio", 0.412, "increase", 0.0040),
    ("CTR", "ratio", 0.305, "increase", 0.0050),
    ("Long Click Rate", "ratio", 0.221, "increase", 0.0060),
    ("Abandonment Rate", "ratio", 0.187, "decrease", 0.0070),
    ("Reformulation Rate", "ratio", 0.143, "decrease", 0.0080),
    ("Queries per User", "mean", 11.8, "increase", 0.0090),
    ("Sessions per User", "mean", 4.21, "increase", 0.0050),
    ("Time to First Click (s)", "mean", 6.4, "decrease", 0.0100),
    ("Zero Result Rate", "ratio", 0.031, "decrease", 0.0150),
    ("Latency p95 (ms)", "mean", 412.0, "decrease", 0.0060),
    ("Ad Click Rate", "ratio", 0.052, "increase", 0.0120),
    ("Revenue per User", "mean", 0.87, "increase", 0.0110),
    ("Clicks per User", "mean", 3.6, "increase", 0.0080),
    ("Pagination Rate", "ratio", 0.064, "decrease", 0.0130),
    ("Autocomplete Acceptance", "ratio", 0.338, "increase", 0.0060),
]
SEGMENTS = ["Mobile", "Desktop", "Head Queries", "Tail Queries", "Navigational", "Informational"]
SEGMENTED = ["Successful Search Rate", "CTR", "Abandonment Rate", "Reformulation Rate",
             "Long Click Rate", "Time to First Click (s)", "Clicks per User"]
UNITS = 1_000_000


def record(name, kind, control, direction, rel, half, units=(UNITS, UNITS), listed="secondary"):
    """One Pulse metric record in the spec's camelCase shape."""
    test = control * (1 + rel)
    abs_half = control * half
    se = abs_half / Z95
    z = (control * rel) / se if se else 0.0
    p = 2 * (1 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2))))
    return {"metricID": f"{name}::{kind}", "directionality": direction,
            "absoluteChange": round(test - control, 8), "absoluteConfidenceIntervalDelta": round(abs_half, 8),
            "percentChange": round(100 * rel, 6), "percentConfidenceIntervalDelta": round(100 * half, 6),
            "testMean": round(test, 8), "controlMean": round(control, 8),
            "testStd": round(se / math.sqrt(2), 10), "controlStd": round(se / math.sqrt(2), 10),
            "testUnits": units[1], "controlUnits": units[0], "pValue": round(p, 6), "_listed": listed}


def scorecard(rng, overrides, units=(UNITS, UNITS), primaries=("Successful Search Rate",)):
    """About 60 metrics: the base set plus segment cuts, null effects unless overridden."""
    rows = []
    for name, kind, control, direction, half in BASE:
        rows.append((name, kind, control, direction, half))
    for base_name in SEGMENTED:
        name, kind, control, direction, half = next(b for b in BASE if b[0] == base_name)
        for seg in SEGMENTS:
            rows.append((f"{name} - {seg}", kind, control * rng.uniform(0.7, 1.3), direction, half * rng.uniform(1.8, 2.6)))
    records = []
    for name, kind, control, direction, half in rows:
        spec = overrides.get(name, {})
        rel = spec.get("rel", rng.gauss(0, half / Z95))
        records.append(record(name, kind, spec.get("control", control), spec.get("direction", direction),
                              rel, spec.get("half", half), units,
                              "primary" if name in primaries else "secondary"))
    primary = [r for r in records if r.pop("_listed") == "primary"]
    for r in records:
        r.pop("_listed", None)
    secondary = [r for r in records if r not in primary]
    return {"message": "Pulse results retrieved", "data": {"ds": "2026-09-25", "primaryMetrics": primary,
                                                          "secondaryMetrics": secondary}}


def experiment(name, test_params=None, allocation=20, sizes=(50, 50), health=None, duration=14, extra=None):
    exp = {"id": name.lower().replace(" ", "_"), "name": name,
           "hypothesis": "The new ranker raises the share of searches that end in a successful click.",
           "idType": "userID", "layerID": "search_ranking", "allocation": allocation, "controlGroupID": "g_control",
           "groups": [{"id": "g_control", "name": "Control", "size": sizes[0], "parameterValues": {"ranker_model": "lambdamart_v6", "snippet_length": "160"}},
                      {"id": "g_test", "name": "Test", "size": sizes[1],
                       "parameterValues": {"ranker_model": "lambdamart_v7", "snippet_length": "160", **(test_params or {})}}],
           "startTime": START_MS, "duration": duration, "status": "active", "defaultConfidenceInterval": "95",
           "sequentialTesting": False, "bonferroniCorrection": False,
           "primaryMetrics": [{"name": "Successful Search Rate", "type": "ratio", "direction": "increase"}],
           "healthChecks": health or [{"type": "has_balanced_exposures", "name": "Exposures balanced", "status": "PASSED"}]}
    exp.update(extra or {})
    return {"message": "ok", "data": exp}


def prereg(**changes):
    base = {"experiment_id": "ranker_v7", "name": "Ranker v7", "design": "ab", "unit": "userID", "confirmed": True,
            "ci_level": 0.95, "planned": {"days": 14, "units_per_arm": 900000},
            "primaries": {"rule": "all", "ship_requires": "point_at_bar",
                          "metrics": [{"metric": "Successful Search Rate", "direction": "increase", "bar": 0.005}]},
            "guardrails": [{"metric": "Latency p95 (ms)", "direction": "decrease", "margin": 0.02},
                           {"metric": "Abandonment Rate", "direction": "decrease", "margin": 0.01},
                           {"metric": "Zero Result Rate", "direction": "decrease", "margin": 0.03},
                           {"metric": "Revenue per User", "direction": "increase", "margin": 0.01}],
            "intended_params": ["ranker_model"]}
    base.update(changes)
    return base


def daily(effects, basis="days_since_exposure", half=0.006):
    return [{"day": i + 1, "rel_delta": e, "rel_ci": [e - half, e + half], "basis": basis} for i, e in enumerate(effects)]


WIN = {"Successful Search Rate": {"rel": 0.0081}}
# Guardrails in a well-planned test are powered for their margins: near-zero effects, tight intervals.
GUARDS = {"Latency p95 (ms)": {"rel": 0.002, "half": 0.005}, "Abandonment Rate": {"rel": 0.001, "half": 0.006},
          "Zero Result Rate": {"rel": 0.0, "half": 0.014}, "Revenue per User": {"rel": -0.001, "half": 0.007}}
CASE_DEFS = []


def case(cid, title, gold, overrides=None, exp=None, pre=None, request=None, days=None, audit=None,
         units=(UNITS, UNITS), extra_files=None, primaries=("Successful Search Rate",), pulse_hook=None):
    CASE_DEFS.append(dict(cid=cid, title=title, gold=gold, overrides=overrides if overrides is not None else WIN,
                          exp=exp, pre=pre, request=request, days=days, audit=audit, units=units,
                          extra_files=extra_files or {}, primaries=primaries, pulse_hook=pulse_hook))


def gold(call, decider, value=None, accept=None, why=""):
    return {"call": call, "decider": decider, "primary_rel_pct": value, "accept_calls": accept or [call], "why": why}


# --- ship ---
case("s1", "clean win", gold("ship", "Successful Search Rate", 0.81, why="primary clears the bar; guardrails within"))
case("s2", "one secondary loses, uncorrected", gold("ship", "Successful Search Rate", 0.81,
     why="Ad Click Rate p~0.02 among ~57 secondaries does not survive correction and cannot block"),
     overrides={**WIN, "Ad Click Rate": {"rel": -0.028, "half": 0.024}})
case("s3", "calendar trend fades, flat by days since exposure", gold("ship", "Successful Search Rate", 0.81,
     why="the calendar-day fade is day-of-week and late joiners; by exposure day the effect is flat"),
     days={"daily_by_exposure_day.json": daily([0.0082, 0.0079, 0.0084, 0.0080, 0.0081, 0.0078, 0.0083, 0.0080, 0.0082, 0.0079, 0.0081, 0.0080]),
           "daily_by_calendar_day.json": daily([0.0125, 0.0118, 0.0102, 0.0095, 0.0088, 0.0071, 0.0066, 0.0084, 0.0079, 0.0070, 0.0061, 0.0058, 0.0054, 0.0050], basis="calendar_day")})
case("s4", "CUPED on: deltas are adjusted, means are raw", gold("ship", "Successful Search Rate", 0.81,
     why="CUPED delta is the estimate; the absolute in brackets must be rel x control mean"),
     request={"cuped": "true", "confidence": "95"},
     pulse_hook=lambda pulse: [m.update(testMean=round(m["controlMean"] * 1.0035, 8)) for m in pulse["data"]["primaryMetrics"]])
# --- don't ship ---
case("d1", "latency guardrail breached", gold("dont_ship", "Latency p95 (ms)", 0.81, why="latency +3.1% past its 2% margin"),
     overrides={**WIN, "Latency p95 (ms)": {"rel": 0.031, "half": 0.006}})
case("d2", "primary got worse", gold("dont_ship", "Successful Search Rate", -0.62, why="primary fell, CI excludes zero"),
     overrides={"Successful Search Rate": {"rel": -0.0062}})
case("d3", "strong win hides an abandonment breach", gold("dont_ship", "Abandonment Rate", 1.24,
     why="abandonment +2.2% past its 1% margin; the primary win doesn't override a guardrail"),
     overrides={"Successful Search Rate": {"rel": 0.0124}, "Abandonment Rate": {"rel": 0.022, "half": 0.007},
                "CTR": {"rel": 0.019}, "Clicks per User": {"rel": 0.021}})
# --- escalate ---
case("e1", "abandonment interval crosses its margin", gold("escalate", "Abandonment Rate", 0.81,
     why="abandonment +0.6% (-0.4% to +1.6%) is not shown within its 1% margin"),
     overrides={**WIN, "Abandonment Rate": {"rel": 0.006, "half": 0.010}})
case("e2", "latency worse but inside its margin", gold("escalate", "Latency p95 (ms)", 0.81,
     why="latency +1.2% is significantly worse but inside the 2% margin; team standard sends it to triage"),
     overrides={**WIN, "Latency p95 (ms)": {"rel": 0.012, "half": 0.005}})
case("e3", "real win below the bar", gold("escalate", "Successful Search Rate", 0.31,
     why="+0.31% is real (CI excludes zero) but short of the 0.5% bar"),
     overrides={"Successful Search Rate": {"rel": 0.0031, "half": 0.0018}})
case("e4", "triggered lift reported as overall", gold("escalate", "Successful Search Rate", 0.39,
     why="+1.9% on triggered searches is +0.39% overall at a 20.5% metric-mass share, below the 0.5% overall bar"),
     overrides={"Successful Search Rate": {"rel": 0.019, "half": 0.006}},
     pre=prereg(primaries={"rule": "all", "ship_requires": "point_at_bar", "metrics": [
         {"metric": "Successful Search Rate", "direction": "increase", "bar": 0.005, "population": "triggered",
          "mass_share": 0.205, "note": "scorecard is on triggered searches (10% of searches, 20.5% of control successes); the bar is overall"}]}))
case("e5", "two primaries, one undetermined", gold("escalate", "Long Click Rate", 0.81,
     why="the pre-registration needs both primaries; long clicks are undetermined"),
     overrides={**WIN, "Long Click Rate": {"rel": 0.0012, "half": 0.006}},
     primaries=("Successful Search Rate", "Long Click Rate"),
     pre=prereg(primaries={"rule": "all", "ship_requires": "point_at_bar", "metrics": [
         {"metric": "Successful Search Rate", "direction": "increase", "bar": 0.005},
         {"metric": "Long Click Rate", "direction": "increase", "bar": 0.005}]}))
case("e6", "engagement primary up for the wrong reason", gold("ship", "Queries per User", 2.4, accept=["escalate", "dont_ship"],
     why="the rule ships on queries per user, but reformulation and abandonment rose and success fell: the analyst should disagree"),
     overrides={"Queries per User": {"rel": 0.024}, "Reformulation Rate": {"rel": 0.051, "half": 0.008},
                "Successful Search Rate": {"rel": -0.0035, "half": 0.004}, "Abandonment Rate": {"rel": 0.004, "half": 0.007}},
     primaries=("Queries per User",),
     pre=prereg(primaries={"rule": "all", "ship_requires": "point_at_bar", "metrics": [
         {"metric": "Queries per User", "direction": "increase", "bar": 0.01}]},
         guardrails=[{"metric": "Latency p95 (ms)", "direction": "decrease", "margin": 0.02}]))
# --- keep running ---
case("k1", "early win on day 4 of 14", gold("keep_running", "Successful Search Rate", 1.42, why="fixed-horizon interval on day 4 of 14"),
     overrides={"Successful Search Rate": {"rel": 0.0142, "half": 0.0110}}, units=(260000, 261000),
     exp=experiment("Ranker v7"), pulse_hook=lambda p: p["data"].update(ds="2026-09-15"))
case("k2", "effect fading by days since exposure", gold("keep_running", "Successful Search Rate", 0.81,
     why="effect falls from about +1.4% to +0.4% by exposure day"),
     days={"daily_by_exposure_day.json": daily([0.0150, 0.0138, 0.0127, 0.0115, 0.0100, 0.0091, 0.0082, 0.0070, 0.0061, 0.0052, 0.0046, 0.0040])})
case("k3", "inconclusive but one more week settles it", gold("keep_running", "Successful Search Rate", 0.12,
     why="interval -0.36% to +0.60% can't rule out the 0.5% bar; about 1.2x the users would"),
     overrides={"Successful Search Rate": {"rel": 0.0012, "half": 0.0048}})
case("k4", "sequential testing on, mid-test", gold("keep_running", "Successful Search Rate", 0.55,
     why="sequential interval includes zero on day 7 of 14"),
     overrides={"Successful Search Rate": {"rel": 0.0055, "half": 0.0040}}, units=(480000, 481000),
     request={"confidence": "95", "cuped": "false", "sequential": True},
     pre=prereg(sequential=True),
     pulse_hook=lambda p: [p["data"].update(ds="2026-09-18")] + [m.update(sequentialTestingConfidenceIntervalDelta=round(m["absoluteConfidenceIntervalDelta"] * 1.9, 8),
                                                  percentSequentialTestingConfidenceIntervalDelta=round(m["percentConfidenceIntervalDelta"] * 1.9, 6))
                                                  for m in p["data"]["primaryMetrics"] + p["data"]["secondaryMetrics"]])
# --- no effect found ---
case("n1", "flat at full power, one secondary 'wins'", gold("no_effect", "Successful Search Rate", 0.04,
     why="interval rules out the 0.5% bar; Revenue per User +2.5% (p~0.004) does not survive correction"),
     overrides={"Successful Search Rate": {"rel": 0.0004, "half": 0.0030}, "Revenue per User": {"rel": 0.031, "half": 0.021}})
case("n2", "flat overall, tail queries win", gold("no_effect", "Successful Search Rate", 0.06, accept=["no_effect", "escalate"],
     why="the registered primary is overall; a tail-only win is an analyst's note, not a launch"),
     overrides={"Successful Search Rate": {"rel": 0.0006, "half": 0.0030}, "Successful Search Rate - Tail Queries": {"rel": 0.031, "half": 0.010}})
case("n3", "flat primary, heavy users move queries per user", gold("no_effect", "Successful Search Rate", -0.05,
     why="queries per user +1.9% is a secondary; the primary rules out the bar"),
     overrides={"Successful Search Rate": {"rel": -0.0005, "half": 0.0029}, "Queries per User": {"rel": 0.019, "half": 0.017}})
# --- can't tell ---
case("c1", "sample ratio mismatch", gold("cant_tell", "sample_split", 0.81, why="exposures 50.5/49.5 at a million per arm"),
     exp=experiment("Ranker v7", extra={"exposures": {"Control": 1010000, "Test": 990000}}))
case("c2", "test changed a second parameter", gold("cant_tell", "config_params", 0.81, why="snippet_length 160 -> 220 in test only"),
     exp=experiment("Ranker v7", test_params={"snippet_length": "220"}))
case("c3", "pre-period bias", gold("cant_tell", "pre_period", 0.81, why="arms differed by +0.7% before exposure"),
     pre=prereg(pre_period={"Successful Search Rate": {"rel_delta": 0.0071, "rel_ci": [0.0031, 0.0111]}}))
case("c4", "export has lift as a fraction where percent is expected", gold("cant_tell", "scorecard", None,
     why="percentChange 0.0081 read as percent gives 0.008%, which disagrees with the means"),
     pulse_hook=lambda p: [m.update(percentChange=round(m["percentChange"] / 100, 8),
                                    percentConfidenceIntervalDelta=round(m["percentConfidenceIntervalDelta"] / 100, 8))
                           for m in p["data"]["primaryMetrics"] + p["data"]["secondaryMetrics"]])
case("c5", "allocation cut mid-test", gold("cant_tell", "config_edits", 0.81, why="allocation 20 -> 10 on day 5, no restart"),
     audit={"data": [{"actionType": "experiment_edit", "date": "2026-09-16", "changeLog": "Allocation changed from 20% to 10%",
                      "changes": {"allocation": {"old": 20, "new": 10}}}]})
# --- not an A/B test ---
case("x1", "interleaving test", gold("not_ab", "design", None, why="team-draft interleaving: preference, not an A/B lift"),
     pre=prereg(design="interleaving"))
case("x2", "long-term holdout", gold("not_ab", "design", None, why="holdout measures a bundle of launches"),
     pre=prereg(design="holdout"))

TASK = """You are the data scientist on a search ranking experiment, "{name}". The launch review meets tomorrow.

Files in this directory:
- pulse.json: the Statsig Pulse results (Console API response), requested with {request}
- experiment.json: the Statsig experiment config; audit_logs.json: its change history
- prereg.json: the pre-registration the team wrote before launch
{daily}
Write the readout the launch review will read. It must start with one line, exactly:
Decision: <Ship | Don't ship | Escalate | Keep running | No effect found | Can't tell | Not an A/B test>
"""


def build():
    for path in (CASES, GOLD):
        shutil.rmtree(path, ignore_errors=True)
        os.makedirs(path)
    for i, d in enumerate(CASE_DEFS):
        rng = random.Random(1000 + i)
        directory = os.path.join(CASES, d["cid"])
        os.makedirs(directory)
        pulse = scorecard(rng, {**GUARDS, **d["overrides"]}, d["units"], d["primaries"])
        if d["pulse_hook"]:
            d["pulse_hook"](pulse)
        request = d["request"] or {"control": "g_control", "test": "g_test", "cuped": "false", "confidence": "95"}
        request = {"control": "g_control", "test": "g_test", **request}
        files = {"pulse.json": pulse, "experiment.json": d["exp"] or experiment("Ranker v7"),
                 "audit_logs.json": d["audit"] or {"data": []}, "request.json": request,
                 "prereg.json": d["pre"] or prereg()}
        files.update(d["days"] or {})
        for name, content in files.items():
            with open(os.path.join(directory, name), "w") as handle:
                json.dump(content, handle, indent=1)
        daily_note = "".join(f"- {n}: the primary metric's daily effect ({n.split('_by_')[1].replace('.json', '').replace('_', ' ')})\n"
                             for n in sorted(d["days"] or {}))
        with open(os.path.join(directory, "task.md"), "w") as handle:
            handle.write(TASK.format(name=files["prereg.json"].get("name", "Ranker v7"),
                                     request=json.dumps({k: v for k, v in request.items() if k not in ("control", "test")}),
                                     daily=daily_note))
        with open(os.path.join(GOLD, f"{d['cid']}.json"), "w") as handle:
            json.dump({"title": d["title"], **d["gold"]}, handle, indent=1)
    print(f"wrote {len(CASE_DEFS)} cases to {CASES}")


if __name__ == "__main__":
    build()
