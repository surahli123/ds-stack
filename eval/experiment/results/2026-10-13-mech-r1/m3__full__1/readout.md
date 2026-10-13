# Ranker v7: No effect found

Decision: No effect found. Successful Search Rate reads +0.00% (-0.30% to +0.30%), which rules out the 0.50% change the test was built to find.

Ask: Agree to stop the test without launching.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: Latency p95 (ms) rose 6.00% (+5.20% to +6.80%), the wrong way, inside its margin.

Triage: Ready: every movement triage will ask about has a candidate explanation and none conflict; the explanations are inferred from co-movements, so the cuts below would confirm them.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.00% (-0.30% to +0.30%) | estimate at least 0.50% higher | unclear |
| Latency p95 (ms) | guardrail | +6.00% (+5.20% to +6.80%) | at most 10.00% higher | worse, within margin |
| Abandonment Rate | guardrail | +1.60% (+1.20% to +2.00%) | at most 3.00% higher | worse, within margin |

Checks: passed: scorecard, sample split, config params, config edits, novelty; not run: pre period.

## What would change the call

- Latency and abandonment by latency bucket showing the loss only in slow buckets, with relevance up where latency is unchanged, would turn this into a speed fix and rerun.
- A pre-period check on Successful Search Rate, which could not run, showing a baseline gap between arms.
- Tighter guardrail margins than the registered 10% latency and 3% abandonment, as in the team standards of 2% and 1%, would put both guardrails past their margin.

## Why it moved

- [inferred] Latency p95 rose 6.00% and Abandonment Rate rose 1.60%: slower results costing clicks is the leading candidate, and CTR dropping is the same story; no cut has been run yet.
- [guess] Successful Search Rate is flat (+0.00%), consistent with a relevance gain offset by the slowdown, or with no relevance gain; the data cannot separate these.
- [guess] Abandonment could also be users giving up on worse results rather than on slow pages; the answer-and-snippet split tells these apart.

## Appendix

- Secondary metrics: 54 tested; after a false-discovery correction these moved: CTR (-1.50%). They are exploratory and don't change the call.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
