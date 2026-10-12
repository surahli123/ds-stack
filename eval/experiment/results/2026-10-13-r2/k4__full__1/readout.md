# Ranker v7: Keep running

Decision: Keep running. It's day 7 of 14; Successful Search Rate reads +0.55% (-0.21% to +1.31%) so far, too early to call.

Ask: Approve running the test longer.

Status: day 7 of 14, 480,000 users per arm, short of the planned 900,000, whole weeks.

Could reverse it: the remaining data; the call is made at the planned sample.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.55% (-0.21% to +1.31%) | at least 0.50% higher | unclear |
| Abandonment Rate | guardrail | +0.10% (-1.04% to +1.24%) | at most 1.00% higher | unclear |
| Revenue per User | guardrail | -0.10% (-1.43% to +1.23%) | at most 1.00% lower | unclear |
| 2 other guardrails | guardrail | | | all within margin |

Checks: passed: scorecard, sample split, config params, config edits; not run: pre period, novelty.

## What would change the call

- Day 14 data: if Successful Search Rate holds at or above +0.50% and no guardrail shows harm past its margin, the call moves to a positive one.
- A daily series by days since first exposure, to run the novelty check, and a pre-period comparison.

## Why it moved

- [guess] No segment cuts or daily series were available, so the mechanism is not known.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals, sequential (they stay valid when the test is checked early); variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Zero Result Rate.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
