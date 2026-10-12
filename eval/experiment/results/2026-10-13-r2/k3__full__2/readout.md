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

- More users until the primary either clearly reaches the 0.50% bar or clearly falls short of it.
- A daily series by days since first exposure would show whether the effect is fading or new.
- A pre-exposure comparison would let the pre-period check run.

## Why it moved

- [measured] The primary reads +0.12% (-0.36% to +0.60%), so it neither clears nor rules out the 0.50% bar.
- [guess] No segment cuts or daily series were in the scorecard, so the mechanism is unknown.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
