#!/usr/bin/env python3
"""Explain the movements triage will ask about, propose where to dig next, and say
whether the experiment is ready for triage.

    python3 explain.py --decision decision.json --scorecard scorecard.json --prereg prereg.json \
        [--overlay DIR] [--segments segments.json] [--out explain.json]

Reads references/search_patterns.json, plus patterns.json and metric_families.json
from the overlay when present (overlay entries override by id or family name).

segments.json holds aggregates from deep-dive queries:
    {"<metric>": {"by": "query class", "parts": [{"segment", "rel_delta", "rel_ci", "weight"}]}}
weight is the segment's share of the control metric total. Segment cuts already in
the scorecard ("<metric> - <segment>") are used too, grouped by the pattern
library's segment dimensions.

Patterns are hypotheses, labelled inferred; decompositions computed from data are
measured. Writes explain.json next to the decision. Exit 0, or 2 on bad input.
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import decompose  # noqa: E402
import expstats  # noqa: E402
from decide import describe, moved  # noqa: E402

PATTERNS = os.path.join(os.path.dirname(HERE), "references", "search_patterns.json")
DEFAULT_DIMENSIONS = {"device": ["mobile", "desktop", "tablet", "app"],
                      "query class": ["head queries", "torso queries", "tail queries", "head", "torso", "tail"],
                      "intent": ["navigational", "informational", "transactional"]}
STATE_OK = {"up": {"up"}, "down": {"down"}, "flat": {"flat"}, "flat_or_down": {"flat", "down"},
            "up_or_flat": {"up", "flat"}, "moved": {"up", "down"}, "any": {"up", "down", "flat"}}


def load_library(overlay):
    with open(PATTERNS, encoding="utf-8") as handle:
        library = json.load(handle)
    if overlay:
        extra = os.path.join(overlay, "patterns.json")
        if os.path.exists(extra):
            with open(extra, encoding="utf-8") as handle:
                more = json.load(handle)
            ids = {p["id"]: i for i, p in enumerate(library["patterns"])}
            for p in more.get("patterns", []):
                if p["id"] in ids:
                    library["patterns"][ids[p["id"]]] = p
                else:
                    library["patterns"].append(p)
            library["families"].update(more.get("families", {}))
            library["ratios"].update(more.get("ratios", {}))
        names = os.path.join(overlay, "metric_families.json")
        if os.path.exists(names):
            with open(names, encoding="utf-8") as handle:
                library["exact_families"] = json.load(handle)
    return library


def state(m):
    ci = m.get("rel_ci") or m.get("abs_ci")
    if not ci:
        return None
    return "up" if ci[0] > 0 else "down" if ci[1] < 0 else "flat"


def base_metrics(comparison):
    return [m for m in comparison["metrics"] if " - " not in m["metric"]]


def map_families(library, metrics, registered):
    """family -> metric record. Exact overlay names first, then the library's patterns on base metrics."""
    out = {}
    exact = library.get("exact_families", {})
    by_name = {m["metric"].lower(): m for m in metrics}
    for family, names in exact.items():
        for name in names if isinstance(names, list) else [names]:
            if name.lower() in by_name:
                out[family] = by_name[name.lower()]
                break
    ordered = sorted(metrics, key=lambda m: m["metric"].lower() not in registered)
    for family, patterns in library["families"].items():
        if family in out:
            continue
        for m in ordered:
            if any(re.search(p, m["metric"].lower()) for p in patterns):
                out[family] = m
                break
    return out


def change_text(m):
    entry = {"point": m.get("rel_delta"), "low": (m.get("rel_ci") or [None, None])[0],
             "high": (m.get("rel_ci") or [None, None])[1], "unit": "relative"}
    if entry["point"] is None or entry["low"] is None:
        return "no interval"
    return moved(entry) if state(m) != "flat" else f"didn't move clearly ({describe(entry)})"


def match_comovement(library, fam, states):
    found, ruled_out = [], []
    for p in library["patterns"]:
        if p.get("kind") or not p.get("when"):
            continue
        need = p["when"]
        if not all(f in states and states[f] in STATE_OK[s] for f, s in need.items()):
            continue
        contra = [f for f, s in (p.get("contradicted_by") or {}).items() if f in states and states[f] in STATE_OK[s]]
        support = [f for f, s in (p.get("strengthened_by") or {}).items()
                   if f in states and states[f] in STATE_OK[s] and s != "any"]
        evidence = [f"{fam[f]['metric']} {change_text(fam[f])}" for f in list(need) + support]
        instance = {"id": p["id"], "name": p["name"], "label": "inferred", "mechanism": p["mechanism"], "reading": p.get("reading", "neutral"),
                    "source": p.get("source"),
                    "families": list(need) + support, "metrics": [fam[f]["metric"] for f in list(need) + support],
                    "evidence": evidence, "score": len(support), "deep_dives": p.get("deep_dives", [])}
        if contra:
            instance["ruled_out_by"] = [f"{fam[f]['metric']} {change_text(fam[f])}" for f in contra]
            ruled_out.append(instance)
        else:
            found.append(instance)
    return found, ruled_out


def fill(template, values):
    return re.sub(r"\{(\w+)\}", lambda m: str(values.get(m.group(1), m.group(0))), template)


def ratio_patterns(library, fam, level):
    out = []
    spec = next((p for p in library["patterns"] if p.get("kind") == "ratio"), None)
    for ratio_family, parts in library.get("ratios", {}).items():
        r, n, d = fam.get(ratio_family), fam.get(parts["numerator"]), fam.get(parts["denominator"])
        if not (spec and r and n and d) or state(r) not in ("up", "down"):
            continue
        if None in (n.get("rel_delta"), d.get("rel_delta")):
            continue
        split = decompose.ratio({"metric": n["metric"], "rel_delta": n["rel_delta"], "rel_ci": n.get("rel_ci")},
                                {"metric": d["metric"], "rel_delta": d["rel_delta"], "rel_ci": d.get("rel_ci")}, level)
        if split["driver"] != "denominator":
            continue
        values = {"ratio": r["metric"], "numerator": n["metric"], "denominator": d["metric"],
                  "denominator_change": change_text(d)}
        out.append({"id": spec["id"], "name": spec["name"], "label": "measured", "mechanism": fill(spec["mechanism"], values),
                    "reading": spec.get("reading", "neutral"), "source": spec.get("source"),
                    "families": [ratio_family, parts["numerator"], parts["denominator"]],
                    "metrics": [r["metric"], n["metric"], d["metric"]],
                    "evidence": [f"{r['metric']} {change_text(r)}", f"{n['metric']} {change_text(n)}",
                                 f"{d['metric']} {change_text(d)}",
                                 f"{round(100 * split['denominator_share'])}% of the ratio's change comes from {d['metric']}"],
                    "score": 3, "deep_dives": [{k: fill(v, values) for k, v in dd.items()} for dd in spec["deep_dives"]]})
    return out


def segment_groups(comparison, library, extra):
    """{metric: [(dimension, parts)]} from scorecard cuts named '<metric> - <segment>' and from segments.json."""
    dims = library.get("segment_dimensions", DEFAULT_DIMENSIONS)
    groups = {}
    for m in comparison["metrics"]:
        if " - " not in m["metric"]:
            continue
        base, segment = m["metric"].rsplit(" - ", 1)
        dim = next((d for d, names in dims.items() if segment.lower() in names), None)
        if dim is None:
            continue
        groups.setdefault(base, {}).setdefault(dim, []).append({
            "segment": segment, "rel_delta": m.get("rel_delta"), "rel_ci": m.get("rel_ci"), "units": m.get("control_units")})
    for metric, cut in (extra or {}).items():
        groups.setdefault(metric, {})[cut.get("by", "segment")] = [dict(p, measured=True) for p in cut["parts"]]
    return groups


def segment_patterns(library, comparison, extra, registered_names, level):
    spec = next((p for p in library["patterns"] if p.get("kind") == "segment"), None)
    if not spec:
        return [], []
    base = {m["metric"]: m for m in base_metrics(comparison)}
    groups = segment_groups(comparison, library, extra)
    tests = sum(len(dims) for metric, dims in groups.items() if metric in base)
    found, notes = [], []
    for metric, dims in groups.items():
        overall = base.get(metric)
        if not overall or not overall.get("rel_ci"):
            continue
        for dim, parts in dims.items():
            for p in parts:
                if "weight" not in p:
                    units = [q.get("units") for q in parts]
                    p["weight"] = p.get("units") if len(set(units)) > 1 else None
            try:
                result = decompose.segments(overall, parts, level)
            except ValueError:
                continue
            threshold = 0.01 / max(tests, 1)
            standout = [s for s in result["segments"] if s["differs_from_pooled"] and s["clear_of_zero"]]
            if result["heterogeneity_p"] >= threshold or not standout:
                continue
            top = standout[0] if all(s["contribution"] is None for s in standout) else max(standout, key=lambda s: abs(s["contribution"] or 0))
            share = f"{round(100 * top['share_of_overall'])}%" if top.get("share_of_overall") is not None else "an unknown share (segment sizes not given)"
            values = {"metric": metric, "segment": top["segment"], "share": share}
            measured = any(p.get("measured") for p in parts)
            found.append({"id": spec["id"], "name": spec["name"], "label": "measured" if measured else "inferred",
                          "reading": spec.get("reading", "neutral"), "source": spec.get("source"),
                          "mechanism": fill(spec["mechanism"], values), "families": [], "metrics": [metric],
                          "segment": top["segment"], "dimension": dim,
                          "evidence": [f"{metric} by {dim}: " + "; ".join(
                              f"{s['segment']} {100 * s['rel_delta']:+.2f}%" for s in result["segments"])],
                          "score": 2 if metric.lower() in registered_names else 1,
                          "deep_dives": [{k: fill(v, values) for k, v in dd.items()} for dd in spec["deep_dives"]]})
    return found, notes


def check_patterns(library, decision):
    out = []
    for spec in (p for p in library["patterns"] if p.get("kind") == "check"):
        wanted = set(spec["check"].split("|"))
        hits = [c for c in decision["checks"] if c["check"] in wanted and c["status"] in ("fail", "flag")]
        if "invariant" in wanted:
            hits += [{"check": "invariant", "summary": f"{v['metric']} moved"} for v in decision["verdicts"]
                     if v["role"] == "invariant" and v["verdict"] == "moved"]
        if hits:
            out.append({"id": spec["id"], "name": spec["name"], "label": "measured", "mechanism": spec["mechanism"],
                        "reading": spec.get("reading", "bad"), "source": spec.get("source"),
                        "families": [], "metrics": [], "evidence": [h["summary"] for h in hits], "score": 5,
                        "deep_dives": spec["deep_dives"], "blocking": spec["id"] == "artifact"
                        and any(h.get("status") == "fail" or h["check"] == "invariant" for h in hits)})
    return out


def expectations(prereg, decision):
    out = []
    listed = prereg.get("expectations")
    if listed is None:
        listed = [{"metric": v["metric"], "direction": v.get("direction")} for v in decision["verdicts"] if v["role"] == "primary"]
        listed += [{"metric": v["metric"], "direction": "flat"} for v in decision["verdicts"] if v["role"] == "guardrail"]
    return listed


def build_questions(decision, comparison, expected, instances, segment_found):
    by_name = {m["metric"].lower(): m for m in comparison["metrics"]}
    questions, seen = [], set()

    def add(metric, text, kind):
        if metric.lower() in seen or metric.lower() not in by_name:
            return
        seen.add(metric.lower())
        related = sorted((i for i in instances if metric in i["metrics"]),
                         key=lambda i: (i["label"] != "measured", -i["score"]))
        questions.append({"metric": metric, "question": text, "kind": kind, "change": change_text(by_name[metric.lower()]),
                          "candidates": [i["id"] for i in related]})

    for e in expected:
        m = by_name.get(str(e["metric"]).lower())
        if not m or not state(m):
            continue
        observed = state(m)
        want = {"increase": "up", "decrease": "down", "flat": "flat"}.get(e.get("direction"), None)
        if want and observed != want:
            verb = {"up": "rose", "down": "fell", "flat": "didn't move"}[observed]
            goal = {"up": "rise", "down": "fall", "flat": "stay flat"}[want]
            add(m["metric"], f"{m['metric']} was expected to {goal} but {verb}. Why?", "not as expected")
    for v in decision["verdicts"]:
        m = by_name.get(v["metric"].lower())
        if m and state(m) in ("up", "down"):
            add(v["metric"], f"Why did {v['metric']} {'rise' if state(m) == 'up' else 'fall'}?", v["role"])
    segmented = {f["metrics"][0].lower() for f in segment_found}
    for s in decision["secondaries"]["survivors"]:
        m = by_name.get(s["metric"].lower())
        if m and not (" - " in s["metric"] and s["metric"].rsplit(" - ", 1)[0].lower() in segmented):
            add(s["metric"], f"Why did {s['metric']} {'rise' if state(m) == 'up' else 'fall'}?", "secondary")
    for f in segment_found:
        metric = f["metrics"][0]
        key = f"{metric} [{f['segment']}]"
        if key not in seen:
            seen.add(key)
            questions.append({"metric": metric, "question": f"Why is {metric}'s change concentrated in {f['segment']}?",
                              "kind": "segment", "change": f["evidence"][0], "candidates": [f["id"]]})
    return questions


def hypothesis_candidate(decision, prereg, comparison, instances):
    """When a primary moved the registered way, the registered hypothesis is itself a candidate."""
    text = prereg.get("hypothesis")
    by_name = {m["metric"].lower(): m for m in comparison["metrics"]}
    out = []
    for v in decision["verdicts"]:
        m = by_name.get(v["metric"].lower())
        want = {"increase": "up", "decrease": "down"}.get(v.get("direction"))
        if v["role"] != "primary" or not m or state(m) != want:
            continue
        support = [i for i in instances if v["metric"] in i["metrics"] and i["id"] in ("relevance_gain", "real_engagement")]
        out.append({"id": "as_hypothesized", "name": "The registered hypothesis", "label": "inferred", "reading": "good",
                    "mechanism": text or "The change works the way the experiment was designed to; no hypothesis text was registered.",
                    "families": [], "metrics": [v["metric"]],
                    "evidence": [f"{v['metric']} {change_text(m)}"] + (support[0]["evidence"][1:3] if support else []),
                    "score": 1 + len(support),
                    "deep_dives": [{"cut": f"{v['metric']} where the change acts (triggered queries) vs where it doesn't",
                                    "confirms": "a larger effect where the ranking changed", "refutes": "the same effect on untouched queries"}]})
    return out


def chance_count(comparison, level):
    """How many metrics moved clearly, against how many would by chance alone."""
    tested = [m for m in comparison["metrics"] if m.get("rel_ci") or m.get("abs_ci")]
    moved = [m for m in tested if state(m) in ("up", "down")]
    return {"tested": len(tested), "moved": len(moved), "expected_by_chance": round(len(tested) * (1 - level), 1)}


def standard_questions(decision, prereg, comparison, chance):
    """The four questions triage asks of every experiment before any single metric."""
    checks = {c["check"]: c for c in decision["checks"]}
    problems = [c for c in decision["checks"] if c["status"] in ("fail", "flag") and c["check"] != "novelty"]
    unrun = [c["check"].replace("_", " ") for c in decision["checks"] if c["status"] == "could_not_run" and c["check"] != "novelty"]
    trust = ("No: " + "; ".join(c["summary"] for c in problems[:2])) if problems else (
        "Yes, as far as the checks reach" + (f"; not checked: {', '.join(unrun)}" if unrun else ""))
    lead = next((v for v in decision["verdicts"] if v["role"] == "primary" and v.get("se")), None)
    if lead:
        p = expstats.two_sided_p(lead["point"], lead["se"])
        real = (f"{lead['metric']} {describe(lead)}; " + ("its interval excludes zero" if lead["low"] > 0 or lead["high"] < 0
                                                        else "its interval includes zero")
                + (f", but p is about {p:.2f}, and wins that borderline often fail a rerun" if 0.01 < p < 0.05 else "")
                + f". Across the scorecard {chance['moved']} of {chance['tested']} metrics moved clearly; about "
                  f"{chance['expected_by_chance']:g} would by chance alone.")
    else:
        real = "No primary interval to judge."
    novelty = checks.get("novelty")
    if novelty and novelty["status"] == "pass":
        last = "Probably: " + novelty["summary"] + "."
    elif novelty and novelty["status"] == "flag":
        last = "Maybe not: " + novelty["summary"] + "."
    else:
        last = "Unknown: there is no effect series by days since first exposure. Cut the primary by exposure day before triage."
    features = prereg.get("feature_metrics") or []
    by_name = {m["metric"].lower(): m for m in comparison["metrics"]}
    shown = [(f, by_name.get(str(f).lower())) for f in features]
    if not features:
        did = ("Not shown. Add a coverage metric, such as the share of queries whose top results changed, so triage can "
               "see the change actually reached users.")
    else:
        did = "; ".join(f"{f} {change_text(m)}" if m else f"{f} is not in the scorecard" for f, m in shown) + "."
    return [{"question": "Is the data trustworthy?", "answer": trust, "ok": not problems},
            {"question": "Is the effect real, or chance?", "answer": real, "ok": bool(lead) and not (lead and 0.01 < expstats.two_sided_p(lead["point"], lead["se"]) < 0.05)},
            {"question": "Will it last?", "answer": last, "ok": bool(novelty and novelty["status"] == "pass")},
            {"question": "Did the change do what it was built to do?", "answer": did,
             "ok": bool(features) and all(m and state(m) in ("up", "down") for f, m in shown)}]


def readiness(decision, instances, questions, standard=None):
    """Ready, ready with open questions, or not ready, with the reason and the first thing to do."""
    by_id = {}
    for inst in instances:
        by_id.setdefault(inst["id"], inst)
    reasons, first = [], None
    if decision["call"] in ("cant_tell", "not_ab"):
        reasons.append(f"the call is {decision['call_text']}: {decision['reason']}")
    if decision["call"] == "keep_running":
        reasons.append(f"the test needs more data: {decision['reason']}")
    blocking = [i for i in instances if i.get("blocking")]
    if blocking:
        reasons.append("a data problem is unresolved: " + "; ".join(blocking[0]["evidence"][:2]))
        first = blocking[0]["deep_dives"][0] if blocking[0]["deep_dives"] else None
    if any(i["id"] == "novelty" for i in instances) and decision["call"] != "keep_running":
        reasons.append("the effect is fading, so the scorecard average overstates the long-run effect")
    registered = [q for q in questions if q["kind"] in ("primary", "guardrail", "not as expected")]
    for q in registered:
        readings = {by_id[c]["reading"] for c in q["candidates"] if c in by_id}
        if "good" in readings and "bad" in readings:
            bad = next(by_id[c] for c in q["candidates"] if c in by_id and by_id[c]["reading"] == "bad")
            good = next(by_id[c] for c in q["candidates"] if c in by_id and by_id[c]["reading"] == "good")
            reasons.append(f"{q['metric']} has two opposite explanations, '{good['name']}' and '{bad['name']}', "
                           "and they lead to different decisions")
            first = first or (bad["deep_dives"][0] if bad["deep_dives"] else None)
            break
    features_failed = [q for q in (standard or []) if q["question"].startswith("Did the change") and q["answer"] and not q["ok"]
                       and not q["answer"].startswith("Not shown")]
    if features_failed:
        reasons.append("the change may not have reached users: " + features_failed[0]["answer"])
    if reasons:
        return {"verdict": "not_ready", "text": "Not ready", "reasons": reasons, "first": first}
    borderline = []
    for v in decision["verdicts"]:
        if v["role"] == "primary" and v["verdict"] in ("better", "below_bar") and v.get("se"):
            p = expstats.two_sided_p(v["point"], v["se"])
            if p > 0.01:
                borderline.append(f"{v['metric']}'s win is borderline (p about {p:.2f}); wins like this often fail a rerun, "
                                  "so expect triage to ask for one")
    open_q = [q for q in questions if not q["candidates"]]
    weak = [q for q in registered if q["candidates"] and all(by_id[c]["score"] == 0 for c in q["candidates"] if c in by_id)]
    durability = [q for q in (standard or []) if q["question"] == "Will it last?" and not q["ok"]]
    if open_q or weak or borderline or durability:
        parts = list(borderline) + (["durability is unknown: no effect series by days since first exposure"] if durability else [])
        if open_q:
            parts.append(f"{len(open_q)} of {len(questions)} movements have no candidate explanation yet")
        if weak:
            parts.append(f"{len(weak)} registered movements rest on a single co-movement")
        return {"verdict": "open_questions", "text": "Ready, with open questions", "reasons": parts, "first": None}
    measured = all(any(by_id[c]["label"] == "measured" for c in q["candidates"] if c in by_id) for q in registered)
    note = "" if measured else "; the explanations are inferred from co-movements, so the deep dives below would make them measured"
    return {"verdict": "ready", "text": "Ready", "first": None,
            "reasons": [f"every movement triage will ask about has a candidate explanation and none conflict{note}"]}


def plan(instances, questions, limit=5):
    order = sorted(instances, key=lambda i: (not i.get("blocking"), i["id"] != "artifact", -i["score"]))
    cuts, seen = [], set()
    for inst in order:
        for dd in inst["deep_dives"]:
            if dd["cut"].lower() in seen:
                continue
            seen.add(dd["cut"].lower())
            cuts.append({**dd, "tests": inst["name"], "pattern": inst["id"]})
            break
    for inst in order:
        for dd in inst["deep_dives"][1:]:
            if len(cuts) >= limit:
                break
            if dd["cut"].lower() not in seen:
                seen.add(dd["cut"].lower())
                cuts.append({**dd, "tests": inst["name"], "pattern": inst["id"]})
    return cuts[:limit]


def explain(decision, scorecard, prereg, library, extra_segments=None):
    group = decision["experiment"].get("test_group")
    comparison = next((c for c in scorecard["comparisons"] if c.get("test_group") == group), scorecard["comparisons"][0])
    level = decision["settings"].get("scorecard_ci_level") or decision["settings"]["ci_level"]
    registered = {v["metric"].lower() for v in decision["verdicts"]}
    fam = map_families(library, base_metrics(comparison), registered)
    states = {f: state(m) for f, m in fam.items() if state(m)}
    found, ruled_out = match_comovement(library, fam, states)
    found += ratio_patterns(library, fam, level)
    seg_found, _ = segment_patterns(library, comparison, extra_segments, registered, level)
    found += seg_found
    checks_found = check_patterns(library, decision)
    for inst in checks_found:
        if inst["id"] == "novelty":
            inst["metrics"] = [v["metric"] for v in decision["verdicts"] if v["role"] == "primary"][:1]
    found += checks_found
    found += hypothesis_candidate(decision, prereg, comparison, found)
    expected = expectations(prereg, decision)
    questions = build_questions(decision, comparison, expected, found, seg_found)
    by_id = {i["id"]: i for i in found}
    for q in questions:
        labels = [by_id[c]["label"] for c in q["candidates"] if c in by_id]
        q["status"] = "confirmed by a cut" if "measured" in labels else "untested" if labels else "unexplained (possibly chance)"
    chance = chance_count(comparison, level)
    standard = standard_questions(decision, prereg, comparison, chance)
    ready = readiness(decision, found, questions, standard)
    return {"readiness": ready, "standard": standard, "chance": chance, "questions": questions,
            "patterns": sorted(found, key=lambda i: -i["score"]),
            "ruled_out": ruled_out, "deep_dives": plan(found, questions), "families": {f: m["metric"] for f, m in fam.items()},
            "expectations": expected}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--decision", required=True)
    parser.add_argument("--scorecard", required=True)
    parser.add_argument("--prereg", required=True)
    parser.add_argument("--overlay", default=os.environ.get("DS_OVERLAY_DIR"))
    parser.add_argument("--segments")
    parser.add_argument("--out")
    args = parser.parse_args(argv)
    try:
        load = lambda p: json.load(open(p, encoding="utf-8")) if p else None  # noqa: E731
        result = explain(load(args.decision), load(args.scorecard), load(args.prereg), load_library(args.overlay),
                         load(args.segments))
    except (OSError, ValueError, KeyError, TypeError) as err:
        print(f"explain: {type(err).__name__}: {err}", file=sys.stderr)
        return 2
    out = args.out or os.path.join(os.path.dirname(os.path.abspath(args.decision)), "explain.json")
    with open(out, "w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2)
    r = result["readiness"]
    print(f"triage readiness: {r['text']} - {'; '.join(r['reasons'])}")
    for q in result["questions"]:
        print(f"question: {q['question']} [{', '.join(q['candidates']) or 'no candidate yet'}]")
    for d in result["deep_dives"]:
        print(f"deep dive: {d['cut']} (tests: {d['tests']})")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
