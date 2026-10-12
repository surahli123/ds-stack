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

- A pre-exposure comparison and a daily series by days since first exposure were not available; a pre-period gap or a fading effect would put the test in question.
- A registered bar below 0.50% would leave the result undecided, since the range reaches +0.36%.

## Why it moved

- [guess] The scorecard has no segment cuts, so the mechanism is unknown.

## Appendix

- Secondary metrics: 52 tested; after a false-discovery correction these moved: Successful Search Rate - Tail Queries (+3.10%). They are exploratory and don't change the call.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
