Decision: Can't tell

# Ranker v7: Can't tell

Decision: Can't tell. The scorecard's relative and absolute changes disagree by about 100 times, so a percent column was probably read as a fraction or the reverse. No launch decision from this data until it's fixed.

Ask: Agree to fix the test and rerun; no launch decision from this data.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: fixing the scorecard problem and rerunning.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.01% (+0.00% to +0.01%) | at least 0.50% higher | better, below the bar |
| 4 other guardrails | guardrail | | | all within margin |

Checks: scorecard fail; passed: sample split, config params, config edits; not run: pre period, novelty.

## What would change the call

- Re-export the Pulse results with percent and absolute columns on the same scale, then rerun; the call is made on the corrected scorecard.
- Supply a pre-exposure comparison and a daily series by days since first exposure, so the pre-period and novelty checks can run.

## Why it moved

- [guess] The mechanism is unknown; no segment cuts are in the scorecard and no daily series was supplied.

## Appendix

- Secondary metrics: 52 tested; after a false-discovery correction these moved: Successful Search Rate - Desktop (-0.01%), Clicks per User (-0.01%). They are exploratory and don't change the call.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

doc_lint: 0 fail, 0 warn, 184 body words (readout)
cold-read: skim 2/2, full 3/3 - pass