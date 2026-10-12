Decision: Can't tell. The scorecard's relative and absolute changes disagree by about 100 times, so a percent column was probably read as a fraction or the reverse. No launch decision from this data until it's fixed.

# Ranker v7: Can't tell

Ask: Agree to fix the test and rerun; no launch decision from this data.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: fixing the scorecard problem and rerunning.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.01% (+0.00% to +0.01%) | at least 0.50% higher | better, below the bar |
| 4 other guardrails | guardrail | | | all within margin |

Checks: scorecard fail; passed: sample split, config params, config edits; not run: pre period, novelty.

## What would change the call

- Re-export the scorecard with the percent-change column in one consistent unit, matching the absolute change divided by the control mean, then rerun the decision.
- Add a pre-exposure comparison and a daily series by days since first exposure, so the pre-period and novelty checks can run.

## Why it moved

- [guess] The mechanism is unknown: the scorecard has no segment cuts, and its change columns disagree with each other, so no effect size can be trusted yet.

## Appendix

- Secondary metrics: 52 tested; after a false-discovery correction these moved: Successful Search Rate - Desktop (-0.01%), Clicks per User (-0.01%). They are exploratory and don't change the call.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

0 fail, 0 warn, 194 body words (readout)
cold-read: skim 2/2, full 2/3 - fail

The cold read failed: the reader missed full takeaway 3, "Could reverse it: fixing the scorecard problem and rerunning."