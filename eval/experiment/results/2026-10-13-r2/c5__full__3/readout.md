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

- Rerun the test with allocation held fixed for the full 14 days, or export results for only the days after 2026-09-16, and the call can be made from the registered bar.
- A pre-exposure comparison and a daily series by days since first exposure would fill the two checks that could not run.

## Why it moved

- [guess] No segment cuts were read, so the mechanism behind the +0.81% in Successful Search Rate is not known.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
