# Ranker v7: Escalate

Decision: Escalate. Successful Search Rate improved but Long Click Rate is undetermined, +0.12% (-0.48% to +0.72%); the test needs every primary to improve.

Ask: Decide the trade-off at triage.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: pre period could not be checked: no pre-period interval or platform check.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Long Click Rate | primary | +0.12% (-0.48% to +0.72%) | at least 0.50% higher | unclear |
| Successful Search Rate | primary | +0.81% (+0.41% to +1.21%) | at least 0.50% higher | better |
| 4 other guardrails | guardrail | | | all within margin |

Checks: passed: scorecard, sample split, config params, config edits; not run: pre period, novelty.

## What would change the call

- Long Click Rate rising to at least its +0.50% bar with more data would clear the second primary, if the checks that could not run also pass.
- A pre-exposure comparison and a daily series by days since first exposure would let the two checks that could not run be run.

## Why it moved

- [guess] No segment cuts were in the scorecard, so the mechanism is not known.

## Appendix

- Secondary metrics: 51 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
