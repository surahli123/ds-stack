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

- If the effect by days since exposure levels off at or above 0.5% over a longer run, the primary clears its bar and the call moves to a win.
- If the effect keeps fading toward zero, it drops below the bar and the call moves against the change.
- A pre-exposure comparison of Successful Search Rate (the platform check could not run) would close the open validity check.

## Why it moved

- [guess] The mechanism is unknown; no segment cuts were provided. A lift that shrinks with days since exposure fits a novelty effect, but nothing here confirms it.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
