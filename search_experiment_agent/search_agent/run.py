#!/usr/bin/env python3
"""One run of the search experiment agent, end to end.

    python3 -m search_agent.run --experiment <name | config id | console URL> --overlay DIR \
        --warehouse sqlite:PATH --configs DIR --out RUN_DIR [--knowledge DIR] [--cards DIR]

Steps: resolve the experiment; read T1's latest snapshot and daily series; run M0 on that
data and grade each (control, test) pair; run M1 per pair (launch call, explanations, and
the cuts the plan can script, fed back as evidence); render the readout and a triage prep per
pair; write the live trace, a card draft, a review form and the frozen case inputs.

Writes into RUN_DIR: readout.md, triage_prep_<arm>.md, trace.json, review.json,
card_draft.json and case/ (the aggregate inputs the learning loop replays). Prints counts only.
"""

import argparse
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

import explain  # noqa: E402
import render as core_render  # noqa: E402

from learning import cards as cardlib  # noqa: E402
from learning import knowledge  # noqa: E402
from search_agent import LIBRARY  # noqa: E402
from search_agent.m0.checks import run_m0  # noqa: E402
from search_agent.m0.grade import approval_status, readout_sha  # noqa: E402
from search_agent.m1 import cuts as cutlib  # noqa: E402
from search_agent.m1 import method  # noqa: E402
from search_agent.render import readout as rd  # noqa: E402
from search_agent.sources import config as cfgsrc  # noqa: E402
from search_agent.sources import resolver  # noqa: E402
from search_agent.sources import t1 as t1src  # noqa: E402
from search_agent.sources.warehouse import RecordingWarehouse, SqliteWarehouse  # noqa: E402
from search_agent.trace import Trace  # noqa: E402


def load_json(path, default=None):
    if path and os.path.exists(path):
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    return default


def write_json(path, value):
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(value, handle, indent=1, default=str)


def run(experiment, overlay, warehouse, configs, out_dir, knowledge_dir=None, cards_dir=None):
    os.makedirs(os.path.join(out_dir, "case"), exist_ok=True)
    warehouse = RecordingWarehouse(warehouse)
    wh_cfg = load_json(os.path.join(overlay, "warehouse.json"))
    if not wh_cfg:
        raise FileNotFoundError(f"{overlay}/warehouse.json is missing")
    std = {**load_json(os.path.join(overlay, "standards.json"), {}), "srm_unit_fallback": False}
    kdir = knowledge_dir or overlay
    library = explain.load_library(kdir, base=LIBRARY)
    templates = cutlib.load_templates(kdir)
    version = knowledge.version_hash(kdir)
    cols, table = t1src.columns(wh_cfg), wh_cfg["tables"]["t1"]

    who = resolver.resolve(experiment, configs, warehouse, table, cols)
    name, cfg = who["experiment_name"], who["config"]
    run_id = f"{name}-{time.strftime('%Y%m%dT%H%M%S', time.gmtime())}"
    trace = Trace(run_id, name, version)
    trace.step("resolve", how=who["how"], config_id=who["config_id"], notes=who["notes"])
    trace.receipt(who["statement"], origin="resolve", source_role="identity")

    latest = warehouse.query(t1src.latest_sql(table, cols), {"experiment": name}, label="T1 latest snapshot")
    trace.receipt({k: latest[k] for k in ("statement_id", "label", "row_count", "sql_sha")}, "T1 latest snapshot", "scorecard")
    sc = t1src.scorecard_from_rows(latest["rows"], cols, wh_cfg.get("prefer_cuped", True), wh_cfg.get("ci_level", 0.95))
    contract = load_json(os.path.join(overlay, "contracts", f"{name}.json"))
    if not contract:
        raise FileNotFoundError(f"no contract for {name} in {overlay}/contracts")
    split_metric = wh_cfg.get("split_count_metric")
    watched = [m for m in [split_metric] + [s["metric"] for s in (contract.get("primaries") or {}).get("metrics", [])] if m]
    series = warehouse.query(t1src.series_sql(table, cols), {"experiment": name, "metrics": watched}, label="T1 daily series")
    trace.receipt({k: series[k] for k in ("statement_id", "label", "row_count", "sql_sha")}, "T1 daily series", "data quality")
    trace.action({"kind": "query", "owner": "agent", "run_id": run_id, "pair": "all", "target_pattern": None,
                  "exact_next_task": "exposed units and primaries by day and arm (T1 series)", "diagnoses": ["M0-2", "M0-6"],
                  "falsifier": "units fall or jump between snapshots", "status": "ran",
                  "statement": {k: series[k] for k in ("statement_id", "row_count")}}, grade_after="before M0")

    m0, mid = run_m0(sc, series["rows"], cfg, contract, std, wh_cfg, configs.command)
    split = {}
    for c in sc["comparisons"]:
        m = next((x for x in c["metrics"] if split_metric and x["metric"].lower() == split_metric.lower()), None)
        if m:
            split[sc["control_group"]] = int(m["control_units"] or 0)
            split[c["test_group"]] = int(m["test_units"] or 0)
    ctx = {"scorecard": sc, "contract": contract, "standards": std, "library": library, "templates": templates,
           "warehouse": warehouse, "wh_cfg": wh_cfg, "experiment": name, "config_for_decide": cfgsrc.for_decide(cfg, split),
           "t1_statement": latest["statement_id"], "max_cuts": wh_cfg.get("max_cuts", 4)}
    pairs = []
    for comparison in sc["comparisons"]:
        test = comparison["test_group"]
        out = method.investigate(ctx, test, m0[test], mid[test], trace)
        out["m0"] = m0[test]
        out["feature_metrics"] = contract.get("feature_metrics") or []
        out["metrics"] = comparison["metrics"]
        out["m0_details"] = next(c["details"] for c in m0[test] if c["id"] == "M0-1")
        trace.claims(test, out["claims"])
        pairs.append(out)

    families = pairs[0]["explained"]["families"] if pairs else {}
    card = cardlib.draft(run_id, cfg, name, pairs, families)
    confirmed, drafts = cardlib.similar(cardlib.load(cards_dir), name, (cfg or {}).get("layer"), (cfg or {}).get("tags"),
                                        card["families_moved"])
    display = (cfg or {}).get("name") or name
    provenance = (f"T1 snapshot {sc['analysis']['as_of']} ({latest['statement_id']}); config "
                  f"{(cfg or {}).get('id') or 'not fetched'}; knowledge version {version[:12]}; run {run_id}.")
    text = rd.render(display, sc["control_group"], pairs, confirmed, drafts, provenance, {}, cfg is not None)
    sha = readout_sha(text)
    approvals = {p["test"]: approval_status(out_dir, p["grade"], text) for p in pairs}
    if any(approvals.values()):
        text = rd.render(display, sc["control_group"], pairs, confirmed, drafts, provenance, approvals, cfg is not None)
    with open(os.path.join(out_dir, "readout.md"), "w", encoding="utf-8") as handle:
        handle.write(text)
    for p in pairs:
        with open(os.path.join(out_dir, f"triage_prep_{p['test']}.md"), "w", encoding="utf-8") as handle:
            handle.write(core_render.triage_prep(p["decision"], p["explained"]))

    claims = [c for p in pairs for c in p["claims"]]
    counts = {"pairs": len(pairs), "claims": len(claims), "unsupported": len(method.unsupported(claims)),
              "confirmed": sum(c["support_level"] == "confirmed" for c in claims),
              "cuts_ran": sum(a["status"] == "ran" for p in pairs for a in p["actions"]),
              "access_gaps": sum(a["status"] == "access gap" for p in pairs for a in p["actions"]),
              "grades": {p["test"]: p["grade"]["grade"] for p in pairs},
              "next_check": next_check_proxies(pairs, templates, wh_cfg)}
    trace.finish(sha, counts)
    trace.write(os.path.join(out_dir, "trace.json"))
    write_json(os.path.join(out_dir, "card_draft.json"), card)
    if cards_dir:
        cardlib.save(cards_dir, card)
    write_json(os.path.join(out_dir, "review.json"), {
        "run_id": run_id, "reviewer": None, "date": None,
        "claims": [{"claim_id": c["claim_id"], "pair": p["test"], "metric": c["metric"], "candidate": c["candidate"],
                    "support_level": c["support_level"], "verdict": None, "note": ""} for p in pairs for c in p["claims"]],
        "checks": [{"pair": p["test"], "cut": a["exact_next_task"], "status": a["status"], "useful": None}
                   for p in pairs for a in p["actions"]],
        "missing": []})
    case = os.path.join(out_dir, "case")
    write_json(os.path.join(case, "scorecard.json"), sc)
    write_json(os.path.join(case, "series.json"), series["rows"])
    write_json(os.path.join(case, "config.json"), cfg)
    write_json(os.path.join(case, "contract.json"), contract)
    write_json(os.path.join(case, "evidence.json"), {p["test"]: p["evidence"] for p in pairs})
    warehouse.save(os.path.join(case, "queries.json"))
    write_json(os.path.join(case, "meta.json"), {"experiment": name, "run_id": run_id, "knowledge_version": version,
                                                 "input": experiment, "config_id": (cfg or {}).get("id"),
                                                 "wh_cfg": {k: wh_cfg.get(k) for k in ("split_count_metric", "ci_level")}})
    return {"run_id": run_id, "readout": text, "pairs": pairs, "counts": counts, "trace": trace.data, "card": card}


def next_check_proxies(pairs, templates, wh_cfg):
    """The plan's first measure without a reviewer: is the top remaining check scriptable,
    runnable under current access, and aimed at the top open question?"""
    out = {}
    for p in pairs:
        plan = p["explained"]["deep_dives"]
        questions = [q for q in p["explained"]["questions"] if not q["status"].startswith("confirmed")]
        if not plan:
            out[p["test"]] = {"has_next_check": False}
            continue
        top = plan[0]
        approved = set(wh_cfg.get("approved") or [])
        out[p["test"]] = {"has_next_check": True, "scriptable": bool(top.get("needs")),
                          "runnable": bool(top.get("sql")) and all(t in approved for t in cutlib.needed_tables(wh_cfg)),
                          "targets_top_question": bool(questions) and top.get("pattern") in questions[0]["candidates"]}
    return out


def warehouse_from(spec):
    kind, _, target = spec.partition(":")
    if kind == "sqlite":
        return SqliteWarehouse(target)
    raise ValueError("only sqlite:PATH at home; at work, wire McpWarehouse in sources/warehouse.py")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--experiment", required=True)
    parser.add_argument("--overlay", required=True)
    parser.add_argument("--warehouse", required=True)
    parser.add_argument("--configs")
    parser.add_argument("--out", required=True)
    parser.add_argument("--knowledge")
    parser.add_argument("--cards")
    args = parser.parse_args(argv)
    try:
        result = run(args.experiment, args.overlay, warehouse_from(args.warehouse), cfgsrc.JsonDirConfig(args.configs),
                     args.out, args.knowledge, args.cards)
    except (resolver.Unresolved, FileNotFoundError, ValueError) as err:
        print(f"run: {err}", file=sys.stderr)
        return 2
    c = result["counts"]
    print(f"run: {result['run_id']}: {c['pairs']} pairs, grades {c['grades']}, {c['claims']} claims "
          f"({c['confirmed']} confirmed, {c['unsupported']} unsupported), {c['cuts_ran']} cuts ran, {c['access_gaps']} access gaps")
    return 0


if __name__ == "__main__":
    sys.exit(main())
