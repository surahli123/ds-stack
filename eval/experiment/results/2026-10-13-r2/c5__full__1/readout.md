# Ranker v7: Can't tell

Decision: Can't tell. The test was edited mid-flight on 2026-09-16 (Allocation changed from 20% to 10%) and the results include days before and after. No launch decision from this data until it's fixed.

Ask: Agree to fix the test and rerun; no launch decision from this data.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: fixing the config edits problem and rerunning.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.81% (+0.41% to +1.21%) | at least 0.50% higher | better |
| 4 other guardrails | guardrail | | | all within margin |

Checks: config edits fail; passed: scorecard, sample split, config params; not run: pre period, novelty.

## What would change the call

- A rerun on only the days after the 2026-09-16 allocation change, or a fresh test at a fixed share, that reaches the planned 14 days.
- A daily effect series by days since first exposure, which would also show whether the lift is fading.
- A pre-exposure comparison of the two arms, which the platform did not run.

## Why it moved

- [measured] Successful Search Rate is up 0.81% against a 0.5% bar, and no registered guardrail moved past its margin.
- [guess] No segment cuts are in the scorecard, so the mechanism is not known. The edit to the traffic share part-way through may also have changed who was in each arm.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
