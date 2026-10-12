# Ranker v7: Keep running

Decision: Keep running. Successful Search Rate rose 0.81% (+0.41% to +1.21%) overall, but the effect is fading with each day users have had it.

Ask: Approve running the test longer.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: the remaining data; the call is made at the planned sample.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.81% (+0.41% to +1.21%) | at least 0.50% higher | better |
| 4 other guardrails | guardrail | | | all within margin |

Checks: novelty flag; passed: scorecard, sample split, config params, config edits; not run: pre period.

## What would change the call

- The effect by days since exposure levels off near or above the 0.5% bar: the gain is durable and the test has settled.
- The effect keeps falling below the 0.5% bar: the gain is not durable.
- A pre-exposure comparison for the primary, which has not been run, would close the open check.

## Why it moved

- [measured] Successful Search Rate gain shrinks the longer users have had the new ranker: 1.50% on the first day, 0.40% by the last day measured.
- [inferred] Users may be responding to the change being new, so the early gain overstates the steady state.
- [guess] No segment cuts are in the scorecard, so the mechanism is unknown.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
