Decision: Can't tell

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

- Fixing the sample split problem and rerunning: the owner finds the cause (bucketing, bot filtering or a logging gap) and the scorecard is re-pulled.
- A pre-exposure comparison is added, since the pre-period check could not run.
- A daily series by days since first exposure is supplied, since the novelty check could not run.

## Why it moved

- [guess] The mechanism is unknown: the scorecard has no segment cuts, and the uneven arm sizes mean the lift may not come from the ranker.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

0 fail, 0 warn, 195 body words (readout)
cold-read: skim 2/2, full 2/3 - fail

The cold read failed: the reader did not recover the third takeaway (the "Could reverse it" line), and found the primary row's "better" confusing next to the Can't tell call.