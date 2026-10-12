# Ranker v7: No effect found

Decision: No effect found. Successful Search Rate reads +0.06% (-0.24% to +0.36%), which rules out the 0.50% change the test was built to find.

Ask: Agree to stop the test without launching.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: pre period could not be checked: no pre-period interval or platform check.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.06% (-0.24% to +0.36%) | at least 0.50% higher | unclear |
| 4 other guardrails | guardrail | | | all within margin |

Checks: passed: scorecard, sample split, config params, config edits; not run: pre period, novelty.

## What would change the call

- A pre-exposure comparison of Successful Search Rate showing the arms were not matched before exposure began would make this result unreliable.
- A daily series by days since first exposure would let the novelty check run; it could not run here.

## Why it moved

- [measured] Successful Search Rate - Tail Queries rose 3.1% and survived the false-discovery correction, while the overall rate barely moved.
- [inferred] The new ranker may help rare queries only, which are too small a share of traffic to lift the overall rate.

## Appendix

- Secondary metrics: 52 tested; after a false-discovery correction these moved: Successful Search Rate - Tail Queries (+3.10%). They are exploratory and don't change the call.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

0 fail, 0 warn, 187 body words (readout)
cold-read: skim 2/2, full 3/3 - pass