"""Run decide.py and explain.py on the mechanism cases and compare with gold.

    python3 eval/experiment/mechanism_check.py
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "skills", "ds-experiment", "tools"))

import adapters  # noqa: E402
import decide  # noqa: E402
import explain  # noqa: E402


def run_case(cid):
    d = os.path.join(HERE, "mechanisms", cid)
    sc = adapters.statsig_pulse([adapters.load_json(os.path.join(d, "pulse.json"))], adapters.load_json(os.path.join(d, "request.json")))
    cfg = adapters.statsig_config(adapters.load_json(os.path.join(d, "experiment.json")), adapters.load_json(os.path.join(d, "audit_logs.json")))
    pre = adapters.load_json(os.path.join(d, "prereg.json"))
    daily_path = os.path.join(d, "daily_by_exposure_day.json")
    dec = decide.decide(sc, pre, cfg, None, adapters.load_json(daily_path) if os.path.exists(daily_path) else None)
    evidence_path = os.path.join(d, "evidence.json")
    evidence = adapters.load_json(evidence_path) if os.path.exists(evidence_path) else None
    return dec, explain.explain(dec, sc, pre, explain.load_library(None), evidence, cfg)


def compare(cid):
    with open(os.path.join(HERE, "gold_mechanisms", f"{cid}.json")) as handle:
        gold = json.load(handle)
    dec, result = run_case(cid)
    q = next((q for q in result["questions"] if q["metric"] == gold["question_metric"]), None)
    top = q["candidates"][0] if q and q["candidates"] else None
    wanted = gold["mechanism"] if isinstance(gold["mechanism"], list) else [gold["mechanism"]]
    if wanted == ["none"]:
        named = [q for q in result["questions"] if q["candidates"]] + result["patterns"]
        return not named and result["readiness"]["verdict"] == gold["readiness"], gold, None, result
    return top in wanted and result["readiness"]["verdict"] == gold["readiness"], gold, top, result


def main():
    os.environ.setdefault("DS_CHECKS_LOG", os.devnull)
    misses = 0
    for cid in sorted(os.listdir(os.path.join(HERE, "mechanisms"))):
        ok, gold, top, result = compare(cid)
        misses += not ok
        print(f"{'ok  ' if ok else 'MISS'} {cid} gold {gold['mechanism']}/{gold['readiness']} got {top}/{result['readiness']['verdict']}")
    print(f"{misses} misses")
    return 1 if misses else 0


if __name__ == "__main__":
    sys.exit(main())
