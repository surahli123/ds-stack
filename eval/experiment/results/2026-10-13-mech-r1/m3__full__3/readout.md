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

- A pre-test comparison of Successful Search Rate showing the arms already differed before exposure would make the flat read unreliable.
- Abandonment and CTR by latency bucket showing the harm sits only in slow queries would point to a fixable speed cost, worth a rerun with a faster v7.
- A rerun with many more users that finds a lift of 0.50% or more would reopen the call.

## Why it moved

- [measured] Successful Search Rate is flat at +0.00% and stayed flat across all 14 days, so there is no early lift that faded.
- [inferred] Latency p95 rose +6.00% and Abandonment Rate climbed +1.60%. Engagement suffered too, with CTR at -1.50%. A speed cost fits all three together.
- [guess] Worse results making users give up could also explain the abandonment and CTR moves. No cut has separated the two stories yet.

## Appendix

- Secondary metrics: 54 tested; after a false-discovery correction these moved: CTR (-1.50%). They are exploratory and don't change the call.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
