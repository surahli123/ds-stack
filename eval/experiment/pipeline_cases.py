"""Run the deterministic pipeline (adapters -> decide) on every case and compare with gold.

    python3 eval/experiment/pipeline_cases.py        # prints one line per case, exit 1 on any miss
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "skills", "ds-experiment", "tools"))

import adapters  # noqa: E402
import decide  # noqa: E402


def load(directory, name):
    path = os.path.join(directory, name)
    return adapters.load_json(path) if os.path.exists(path) else None


def run_case(cid):
    directory = os.path.join(HERE, "cases", cid)
    request = load(directory, "request.json")
    scorecard = adapters.statsig_pulse([load(directory, "pulse.json")], request)
    config = adapters.statsig_config(load(directory, "experiment.json"), load(directory, "audit_logs.json"))
    if "exposures" in config.get("experiment_extra", {}):
        config["exposures"] = config["experiment_extra"]["exposures"]
    raw = load(directory, "experiment.json")["data"]
    if raw.get("exposures"):
        config["exposures"] = raw["exposures"]
    return decide.decide(scorecard, load(directory, "prereg.json"), config, None, load(directory, "daily_by_exposure_day.json"))


def compare(cid):
    with open(os.path.join(HERE, "gold", f"{cid}.json")) as handle:
        gold = json.load(handle)
    decision = run_case(cid)
    decider = decision["decider"].get("metric") if decision["decider"].get("check") in (None, "novelty") else decision["decider"]["check"]
    if decision["decider"].get("check") == "novelty":
        decider = decision["decider"]["metric"]
    ok = decision["call"] == gold["call"] and decider == gold["decider"]
    return ok, gold, decision, decider


def main():
    misses = 0
    for cid in sorted(os.listdir(os.path.join(HERE, "cases"))):
        ok, gold, decision, decider = compare(cid)
        misses += not ok
        print(f"{'ok  ' if ok else 'MISS'} {cid:3} gold {gold['call']:12} {gold['decider']:24} got {decision['call']:12} "
              f"{str(decider):24} | {decision['reason'][:110]}")
    print(f"{misses} misses")
    return 1 if misses else 0


if __name__ == "__main__":
    sys.exit(main())
