# Ranker v7: Keep running

Decision: Keep running. It's day 4 of 14; Successful Search Rate reads +1.42% (+0.32% to +2.52%) so far, too early to call.

Ask: Approve running the test longer.

Status: day 4 of 14, 260,000 users per arm, short of the planned 900,000, not whole weeks.

Could reverse it: the remaining data; the call is made at the planned sample.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +1.42% (+0.32% to +2.52%) | at least 0.50% higher | better |
| 4 other guardrails | guardrail | | | all within margin |

Checks: passed: scorecard, sample split, config params, config edits; not run: pre period, novelty.

## What would change the call

- The remaining data: the call is made at the planned sample of 900,000 users per arm, with Successful Search Rate still at or above the 0.50% bar.
- A daily series by days since first exposure would show whether the lift is fading.
- A pre-period comparison would settle the one check that could not run.

## Why it moved

- [guess] Successful Search Rate reads +1.42% on 4 days of data; no segment cuts are in the scorecard, so the mechanism is unknown.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

0 fail, 0 warn, 180 body words (readout)
cold-read: skim 2/2, full 3/3 - pass