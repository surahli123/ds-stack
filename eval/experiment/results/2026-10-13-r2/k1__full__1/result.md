Decision: Keep running

It's day 4 of 14; Successful Search Rate reads +1.42% (+0.32% to +2.52%) so far, too early to call.

Ask: Approve running the test longer.

Status: day 4 of 14, 260,000 users per arm, short of the planned 900,000, not whole weeks.

Could reverse it: the remaining data; the call is made at the planned sample.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +1.42% (+0.32% to +2.52%) | at least 0.50% higher | better |
| 4 other guardrails | guardrail | | | all within margin |

Checks: passed: scorecard, sample split, config params, config edits; not run: pre period, novelty.

## What would change the call

- Reaching the full 14 days with the lift still at or above the 0.5% bar, and the low end of the range clearing it too, would settle the primary.
- A daily series by days since first exposure would show whether the early lift is fading.
- A pre-exposure comparison on Successful Search Rate would let the pre-period check run.

## Why it moved

- [measured] Successful Search Rate reads +1.42% (+0.32% to +2.52%) after 4 of 14 days, and no guardrail has moved outside its margin.
- [guess] The mechanism is unknown: the scorecard has no segment cuts, so we cannot say which queries gained.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

doc_lint: 0 fail, 0 warn, 200 body words (readout)
cold-read: skim 2/2, full 3/3 - pass