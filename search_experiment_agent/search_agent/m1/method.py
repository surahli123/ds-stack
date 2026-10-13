"""M1: why the metrics moved, which cut to run next, and whether the flight is ready for
triage. One (control, test) pair at a time.

The method is ds-experiment's: decide.py makes the launch call (unchanged), and explain.py
maps metric families, matches the enterprise patterns, and scores cut results against each
pattern's confirms_when and refutes_when. This module adds what an agent needs on top:

- it runs the planned cuts that have a SQL template, through the fixed runner, and feeds
  each result back to explain.py, so a candidate becomes confirmed or refuted by data;
- before the first full-page cut it checks that the full-page share of queries didn't move,
  since a filter on a surface the treatment shifts compares different query sets;
- on a not_permitted pair it runs only cuts that diagnose the blocking checks;
- it records every cut as an action (falsifier, predicted outcomes, statement or access gap)
  and recomputes the grade after each one;
- it turns explain.py's questions into structured claims, each with a support level and the
  statements behind it.
"""

import decide
import explain

from search_agent.m0.grade import grade
from search_agent.m1 import cuts as cutlib


def prereg_for(contract, test_group):
    return {**contract, "test_group": test_group}


def action_record(dive, test, run_id):
    return {"kind": "cut", "owner": "agent", "run_id": run_id, "pair": test, "target_pattern": dive.get("pattern"),
            "tests": dive.get("tests"), "exact_next_task": dive["cut"], "template": dive.get("sql"),
            "falsifier": dive.get("refutes"), "predicted_outcomes": {"confirms": dive.get("confirms"), "refutes": dive.get("refutes")},
            "diagnoses": dive.get("diagnoses", []), "status": "planned", "source_or_access_gap": None, "statement": None,
            "outcome": None}


def investigate(ctx, test, pair_checks, mid_flight, trace):
    """Run M1 for one pair. ctx carries the scorecard, configs, contract, standards, library,
    templates, warehouse and its overlay settings."""
    sc, contract = ctx["scorecard"], ctx["contract"]
    prereg = prereg_for(contract, test)
    actions = []
    blocked = grade(pair_checks, mid_flight)["grade"] == "not_permitted"
    daily = None if blocked else durability_series(ctx, test, trace, actions)
    try:
        decision = decide.decide(sc, prereg, ctx["config_for_decide"], ctx["standards"], daily)
    except decide.InputError as err:
        trace.step("decide", pair=test, status="refused", reason=str(err))
        raise
    graded = grade(pair_checks, mid_flight)
    trace.grade(test, graded, after="M0")
    evidence = {"metrics": []}
    explained = explain.explain(decision, sc, prereg, ctx["library"], evidence, ctx["config_for_decide"])
    tried = set()
    surface = {"checked": False, "moved": None}
    for _ in range(ctx["max_cuts"]):
        planned = [d for d in explained["deep_dives"] if d.get("sql") and d["sql"] not in tried and d["sql"] in ctx["templates"]]
        if graded["grade"] == "not_permitted":
            planned = [d for d in planned if set(d.get("diagnoses", [])) & set(graded["blocks"])]
        if not planned:
            break
        dive = planned[0]
        tried.add(dive["sql"])
        tpl = ctx["templates"][dive["sql"]]
        if tpl.get("full_page") and not surface["checked"] and "full_page_share" in ctx["templates"]:
            surface["checked"] = True
            guard = _run(ctx, "full_page_share", test, trace)
            record = {**action_record({"cut": "full-page share of all queries, by arm (a guard for full-page cuts)",
                                       "sql": "full_page_share", "refutes": "the share reaching the full page moved"},
                                      test, trace.run_id), "kind": "guard"}
            record.update(status="ran" if guard.get("metric") else "access gap" if guard.get("gap") else "no result",
                          statement=guard.get("statement"), source_or_access_gap=guard.get("gap") or guard.get("problem"),
                          produces=(guard.get("metric") or {}).get("metric"), outcome="inconclusive")
            trace.action(record, grade_after=graded["grade"])
            actions.append(record)
            if guard.get("metric"):
                evidence["metrics"].append(guard["metric"])
                state = explain.state(guard["metric"], ctx["library"]["families"]["full_page_share"]["practical"])
                surface["moved"] = state in ("up", "down")
                surface["text"] = f"the full-page share of queries {explain.change_text(guard['metric'])}"
        action = action_record(dive, test, trace.run_id)
        out = _run(ctx, dive["sql"], test, trace)
        if out.get("gap"):
            action.update(status="access gap", source_or_access_gap=out["gap"])
        elif out.get("problem"):
            action.update(status="no result", source_or_access_gap=out["problem"], statement=out.get("statement"))
        else:
            evidence["metrics"].append(out["metric"])
            explained = explain.explain(decision, sc, prereg, ctx["library"], evidence, ctx["config_for_decide"])
            hit = next((r for r in explained["cut_results"] if r["cut"] == dive["cut"]), None)
            action.update(status="ran", statement=out["statement"], produces=out["metric"]["metric"],
                          outcome=hit["outcome"] if hit else "inconclusive",
                          detail=hit["detail"] if hit else None,
                          caveat=surface.get("text") if surface.get("moved") and tpl.get("full_page")
                          and not tpl.get("surface_shift_is_the_question") else None)
        graded = grade(pair_checks, mid_flight)
        trace.action(action, grade_after=graded["grade"])
        actions.append(action)
    claims = build_claims(explained, actions, ctx["t1_statement"])
    return {"test": test, "decision": decision, "explained": explained, "grade": graded, "actions": actions,
            "claims": claims, "evidence": evidence, "surface": surface}


def durability_series(ctx, test, trace, actions):
    """The lead primary by days since first exposure, for the novelty check, once per run."""
    if "primary_by_exposure_day" not in ctx["templates"]:
        return None
    cache = ctx.setdefault("_series", {})
    if "result" not in cache:
        record = {**action_record({"cut": "lead primary by days since first exposure", "sql": "primary_by_exposure_day",
                                   "refutes": "the effect is steady across exposure days"}, "all", trace.run_id),
                  "kind": "series", "diagnoses": ["durability"]}
        try:
            res = cutlib.run_cut(ctx["warehouse"], "primary_by_exposure_day", ctx["templates"], ctx["wh_cfg"], ctx["experiment"],
                                 ctx["scorecard"]["analysis"]["as_of"], ctx["scorecard"]["control_group"],
                                 [c["test_group"] for c in ctx["scorecard"]["comparisons"]],
                                 ctx["wh_cfg"].get("min_units_per_cell", 100))
            trace.receipt(res["statement"], origin="cut primary_by_exposure_day", source_role="durability")
            record.update(status="ran", statement=res["statement"], outcome="series")
            cache["result"] = res["series"]
        except cutlib.AccessGap as gap:
            trace.gap("cut primary_by_exposure_day", str(gap))
            record.update(status="access gap", source_or_access_gap=str(gap))
            cache["result"] = {}
        trace.action(record, grade_after="before M1")
        actions.append(record)
    points = cache["result"].get(test)
    return points if points and len(points) >= 4 else None


def _run(ctx, template_id, test, trace):
    try:
        res = cutlib.run_cut(ctx["warehouse"], template_id, ctx["templates"], ctx["wh_cfg"], ctx["experiment"],
                             ctx["scorecard"]["analysis"]["as_of"], ctx["scorecard"]["control_group"], [test],
                             ctx["wh_cfg"].get("min_units_per_cell", 100))
    except cutlib.AccessGap as gap:
        trace.gap(f"cut {template_id}", str(gap))
        return {"gap": str(gap)}
    trace.receipt(res["statement"], origin=f"cut {template_id}", source_role="deep dive")
    if not res["metrics"]:
        return {"problem": "; ".join(res["problems"]), "statement": res["statement"]}
    return {"metric": res["metrics"][0], "statement": res["statement"]}


SUPPORT = {"confirmed by a cut": "confirmed", "confirmed by the scorecard": "confirmed", "confirmed by the checks": "confirmed"}


def build_claims(explained, actions, t1_statement):
    """One claim per question triage will ask. support_level: confirmed (a cut or the scorecard
    confirmed the candidate, with the statements that did), inferred (a candidate from
    co-movement only), exploratory, or none."""
    live = {}
    for inst in explained["patterns"]:
        live.setdefault(inst["id"], inst)
    scouted = {i["id"]: i for i in explained.get("exploratory", [])}
    claims = []
    for n, q in enumerate(explained["questions"], 1):
        candidates = [live[c] for c in q["candidates"] if c in live]
        top = candidates[0] if candidates else next((scouted[c] for c in q["candidates"] if c in scouted), None)
        if top is None:
            level, statements = "none", []
        elif top["status"] in SUPPORT:
            level = "confirmed"
            if top["status"] == "confirmed by a cut":
                text = " ".join(top["evidence"]).lower()
                statements = [a["statement"]["statement_id"] for a in actions
                              if a["status"] == "ran" and a.get("produces") and a["produces"].lower() in text]
            else:
                statements = [t1_statement]
        elif top["id"] in scouted and top["id"] not in live:
            level, statements = "exploratory", []
        else:
            level, statements = "inferred", []
        claims.append({"claim_id": f"c{n}", "metric": q["metric"], "question": q["question"], "change": q["change"],
                       "candidate_id": top["id"] if top else None, "candidate": top["name"] if top else None,
                       "mechanism": top["mechanism"] if top else None, "support_level": level, "statement_ids": statements,
                       "status": q["status"]})
    return claims


def unsupported(claims):
    """Claims stated as findings without the data behind them (the plan's second measure)."""
    return [c for c in claims if c["support_level"] == "confirmed" and not c["statement_ids"]]
