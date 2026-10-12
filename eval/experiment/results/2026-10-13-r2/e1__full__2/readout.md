# Ranker v7: Escalate

Decision: Escalate. Successful Search Rate rose 0.81% (+0.41% to +1.21%), but Abandonment Rate (+0.60% (-0.40% to +1.60%)) isn't shown within its 1.00% margin.

Ask: Decide the trade-off at triage.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: pre period could not be checked: no pre-period interval or platform check.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Abandonment Rate | guardrail | +0.60% (-0.40% to +1.60%) | at most 1.00% higher | unclear |
| Successful Search Rate | primary | +0.81% (+0.41% to +1.21%) | at least 0.50% higher | better |
| 3 other guardrails | guardrail | | | all within margin |

Checks: passed: scorecard, sample split, config params, config edits; not run: pre period, novelty.

## What would change the call

- More data showing Abandonment Rate is within its 1.00% margin would clear the one open guardrail.
- Data showing Abandonment Rate is past its 1.00% margin would end the trade-off.
- A pre-exposure comparison and a daily series by days since first exposure would let the pre-period and novelty checks run.

## Why it moved

- [guess] The mechanism is unknown: the scorecard has no segment cuts, so we can't say why Successful Search Rate rose.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
