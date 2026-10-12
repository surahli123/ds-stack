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

- Rerun on a window that starts after the 2026-09-16 allocation change, or with the allocation held fixed for the whole test, and the result can be called.
- Export the daily effect by days since first exposure, so the fade check can run.
- Add a pre-exposure comparison so the pre-period check can run.

## Why it moved

- [guess] The mechanism is unknown: the scorecard has no segment cuts, so we can't say which queries or users drive the +0.81% in Successful Search Rate.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
