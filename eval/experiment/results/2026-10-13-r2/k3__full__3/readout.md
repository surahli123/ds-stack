# Ranker v7: Keep running

Decision: Keep running. Successful Search Rate reads +0.12% (-0.36% to +0.60%); ruling out the 0.50% bar needs about 1.9 times the users so far.

Ask: Approve running the test longer.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: the remaining data; the call is made at the planned sample.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.12% (-0.36% to +0.60%) | at least 0.50% higher | unclear |
| 4 other guardrails | guardrail | | | all within margin |

Checks: passed: scorecard, sample split, config params, config edits; not run: pre period, novelty.

## What would change the call

- More users, with Successful Search Rate still near +0.12%, would show the 0.50% bar is out of reach and end the test with no win.
- If the extended data puts the whole range of Successful Search Rate above 0.50%, with every guardrail still inside its margin, the bar is met.
- A pre-exposure comparison and a daily series by days since first exposure would settle the two checks that could not run.

## Why it moved

- [guess] The scorecard has no segment cuts, so the mechanism behind the small lift in Successful Search Rate is not known.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
