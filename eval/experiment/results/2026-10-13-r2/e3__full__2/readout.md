# Ranker v7: Escalate

Decision: Escalate. Successful Search Rate rose 0.31% (+0.13% to +0.49%), a real change in the good direction but short of the 0.50% bar.

Ask: Decide the trade-off at triage.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: pre period could not be checked: no pre-period interval or platform check.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.31% (+0.13% to +0.49%) | at least 0.50% higher | better, below the bar |
| 4 other guardrails | guardrail | | | all within margin |

Checks: passed: scorecard, sample split, config params, config edits; not run: pre period, novelty.

## What would change the call

- A pre-exposure comparison showing the arms were balanced would clear the one check that could not run.
- The team accepting a bar of 0.31% or lower would clear the primary, since no guardrail is past its margin.
- A longer run that moves the estimate to 0.50% or more would clear the bar.

## Why it moved

- [measured] The only config change between arms is the ranker model, so the lift in Successful Search Rate of 0.31% comes from the new ranker.
- [guess] No segment cuts are in the scorecard, so which queries gain is not known.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
