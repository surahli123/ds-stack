#!/usr/bin/env python3
"""Synthetic search experiments with a planted mechanism, for the deep-dive layer.

    python3 eval/experiment/make_mechanisms.py

Same shape as eval/experiment/cases/<id>/. Gold (gold_mechanisms/<id>.json) names the
question triage will ask, the mechanism a good analyst would put first, the cut
that tests it, and the readiness verdict. Gold is written from the plant, not
from explain.py's output.
"""

import json
import os
import random
import shutil

import make_cases as mc

HERE = os.path.dirname(os.path.abspath(__file__))
CASES, GOLD = os.path.join(HERE, "mechanisms"), os.path.join(HERE, "gold_mechanisms")
HYPOTHESIS = "The new ranker raises the share of searches that end in a successful click."
DEFS = []


def case(cid, title, gold, overrides, pre=None):
    DEFS.append((cid, title, gold, overrides, pre))


def gold(metric, mechanism, keywords, cut_keywords, readiness, why):
    return {"question_metric": metric, "mechanism": mechanism, "mechanism_keywords": keywords,
            "cut_keywords": cut_keywords, "readiness": readiness, "why": why}


case("m1", "clicks rise, satisfaction doesn't",
     gold("CTR", "attractive_not_relevant", ["clickab", "attractive", "snippet", "title", "short click", "short-click", "not satisf"],
          ["position", "short click", "short-click", "back to result"], "ready",
          "CTR +2.4% with long clicks and success flat: more clickable, not more relevant"),
     {"Successful Search Rate": {"rel": 0.0, "half": 0.003}, "CTR": {"rel": 0.024, "half": 0.005},
      "Long Click Rate": {"rel": -0.001, "half": 0.005}, "Clicks per User": {"rel": 0.022, "half": 0.007}})
case("m2", "users retry because results got worse",
     gold("Successful Search Rate", "struggling_users", ["retry", "retri", "reformulat", "struggl", "searching more", "search again"],
          ["per query", "query class", "per session"], "ready",
          "success -0.7%, queries per user +2.3%, reformulation +4.8%: users retry"),
     {"Successful Search Rate": {"rel": -0.0072}, "Queries per User": {"rel": 0.023}, "Reformulation Rate": {"rel": 0.048, "half": 0.008}})
case("m3", "latency costs engagement",
     gold("Abandonment Rate", "speed_cost", ["latency", "slow", "speed", "load time"],
          ["latency bucket", "by latency", "device", "network"], "ready",
          "latency +1.4% inside its margin, abandonment +0.8% inside its margin, CTR down: speed cost"),
     {"Successful Search Rate": {"rel": 0.0, "half": 0.003}, "Latency p95 (ms)": {"rel": 0.014, "half": 0.004},
      "Abandonment Rate": {"rel": 0.008, "half": 0.003}, "CTR": {"rel": -0.009, "half": 0.004}},
     pre=mc.prereg(guardrails=[{"metric": "Latency p95 (ms)", "direction": "decrease", "margin": 0.03},
                               {"metric": "Abandonment Rate", "direction": "decrease", "margin": 0.02}]))
case("m4", "more results for hard queries, lower precision",
     gold("CTR", "recall_over_precision", ["zero result", "zero-result", "recall", "precision", "no result"],
          ["zero result", "zero-result", "had zero", "no result"], "ready",
          "zero results -12%, CTR -0.9%: weak results for queries that used to get none"),
     {"Successful Search Rate": {"rel": -0.001, "half": 0.003}, "Zero Result Rate": {"rel": -0.12, "half": 0.02},
      "CTR": {"rel": -0.009, "half": 0.004}},
     pre=mc.prereg(guardrails=[{"metric": "Latency p95 (ms)", "direction": "decrease", "margin": 0.02},
                               {"metric": "Revenue per User", "direction": "increase", "margin": 0.01}]))
case("m5", "answers on the page reduce clicks",
     gold("Abandonment Rate", "good_abandonment", ["answer", "on the page", "rich snippet", "good abandonment", "without click"],
          ["answer", "rich snippet", "retry", "return"], "ready",
          "abandonment +2.1% with success up and reformulation flat: answers on the page"),
     {"Successful Search Rate": {"rel": 0.0068}, "Abandonment Rate": {"rel": 0.021, "half": 0.006},
      "CTR": {"rel": -0.011, "half": 0.004}, "Clicks per User": {"rel": -0.012, "half": 0.007},
      "Reformulation Rate": {"rel": -0.001, "half": 0.008}},
     pre=mc.prereg(guardrails=[{"metric": "Latency p95 (ms)", "direction": "decrease", "margin": 0.02},
                               {"metric": "Abandonment Rate", "direction": "decrease", "margin": 0.04}]))
case("m6", "CTR up because searches fell",
     gold("CTR", "denominator_driven", ["fewer searches", "fewer queries", "queries per user fell", "denominator", "search volume", "fewer search"],
          ["per user", "volume", "queries per user", "denominator"], "ready",
          "CTR +2.1% while clicks per user are flat and queries per user -1.9%"),
     {**mc.WIN, "CTR": {"rel": 0.021, "half": 0.005}, "Clicks per User": {"rel": 0.001, "half": 0.008},
      "Queries per User": {"rel": -0.019, "half": 0.007}})
case("m7", "the win sits in tail queries",
     gold("Successful Search Rate", "concentrated_segment", ["tail"], ["tail", "triggered", "query class"], "ready",
          "overall flat, tail +3.4%: a tail-only effect diluted overall"),
     {"Successful Search Rate": {"rel": 0.0008, "half": 0.003},
      "Successful Search Rate - Tail Queries": {"rel": 0.034, "half": 0.009}})
case("m8", "volume primary up for the wrong reason",
     gold("Queries per User", "struggling_users", ["retry", "retri", "reformulat", "struggl", "worse results"],
          ["per query", "query class", "per session"], "not_ready",
          "queries per user is the primary and rose, but reformulation rose and success fell: two opposite readings"),
     {"Queries per User": {"rel": 0.026}, "Reformulation Rate": {"rel": 0.055, "half": 0.008},
      "Successful Search Rate": {"rel": -0.0045, "half": 0.004}},
     pre=mc.prereg(primaries={"rule": "any", "ship_requires": "point_at_bar", "metrics": [
         {"metric": "Queries per User", "direction": "increase", "bar": 0.01}]},
         guardrails=[{"metric": "Latency p95 (ms)", "direction": "decrease", "margin": 0.02}]))

TASK = """You are the data scientist on a search ranking experiment, "Ranker v7". The engineer who ran it presents it at the triage meeting tomorrow. Triage reads the scorecard and asks the engineer why each metric moved.

Files in this directory:
- pulse.json: the Statsig Pulse results (Console API response), requested with {request}
- experiment.json: the Statsig experiment config; audit_logs.json: its change history
- prereg.json: the pre-registration the team wrote before launch

Prepare the engineer for triage: say why the metrics moved, which deep-dive cuts to run next and what each would show, and whether the results are ready for triage. Your reply must contain one line, exactly:
Ready for triage: <Ready | Ready, with open questions | Not ready>
"""


def build():
    for path in (CASES, GOLD):
        shutil.rmtree(path, ignore_errors=True)
        os.makedirs(path)
    for i, (cid, title, g, overrides, pre) in enumerate(DEFS):
        directory = os.path.join(CASES, cid)
        os.makedirs(directory)
        pulse = mc.scorecard(random.Random(5000 + i), {**mc.GUARDS, **overrides})
        request = {"control": "g_control", "test": "g_test", "cuped": "false", "confidence": "95"}
        prereg = pre or mc.prereg()
        prereg["hypothesis"] = HYPOTHESIS
        primary = next(m for m in pulse["data"]["primaryMetrics"])
        effect = primary["percentChange"] / 100
        files = {"pulse.json": pulse, "experiment.json": mc.experiment("Ranker v7"), "audit_logs.json": {"data": []},
                 "request.json": request, "prereg.json": prereg,
                 "daily_by_exposure_day.json": mc.daily([effect + 0.0004 * ((d % 3) - 1) for d in range(12)])}
        for name, content in files.items():
            with open(os.path.join(directory, name), "w") as handle:
                json.dump(content, handle, indent=1)
        with open(os.path.join(directory, "task.md"), "w") as handle:
            handle.write(TASK.format(request=json.dumps({"cuped": "false", "confidence": "95"})))
        with open(os.path.join(GOLD, f"{cid}.json"), "w") as handle:
            json.dump({"title": title, **g}, handle, indent=1)
    print(f"wrote {len(DEFS)} mechanism cases to {CASES}")


if __name__ == "__main__":
    build()
