# Ranker v7: Can't tell

Decision: Can't tell. The arms got 50.5% / 49.5% of exposures against a planned 50.0% / 50.0%, a gap chance almost never produces at this size. No launch decision from this data until it's fixed.

Ask: Agree to fix the test and rerun; no launch decision from this data.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: fixing the sample split problem and rerunning.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.81% (+0.41% to +1.21%) | at least 0.50% higher | better |
| 4 other guardrails | guardrail | | | all within margin |

Checks: sample split fail; passed: scorecard, config params, config edits; not run: pre period, novelty.

## What would change the call

- Find why the arms got an uneven exposure split, fix it, and rerun; the platform's own balance check shows passed, so the cause is not visible in the export.
- If the owner documents a cause for the uneven split in the pre-registration, the call moves to a trade-off for triage instead of a broken test.
- Supply a pre-exposure comparison and a daily series by days since first exposure so the two checks that could not run can run.

## Why it moved

- [guess] No segment cuts were in the scorecard, so the mechanism behind the +0.81% move in Successful Search Rate is not known.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

0 fail, 0 warn, 217 body words (readout)
cold-read: skim 2/2, full 3/3 - pass