Decision: No effect found. Successful Search Rate reads -0.05% (-0.34% to +0.24%), which rules out the 0.50% change the test was built to find.

# Ranker v7: No effect found

Decision: No effect found. Successful Search Rate reads -0.05% (-0.34% to +0.24%), which rules out the 0.50% change the test was built to find.

Ask: Agree to stop the test without launching.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: pre period could not be checked: no pre-period interval or platform check.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | -0.05% (-0.34% to +0.24%) | at least 0.50% higher | unclear |
| 4 other guardrails | guardrail | | | all within margin |

Checks: passed: scorecard, sample split, config params, config edits; not run: pre period, novelty.

## What would change the call

- A pre-exposure comparison for the primary would fill the check that could not run; it would not move the call unless it failed.
- A daily series by days since first exposure would fill the novelty check that could not run.
- A new test with a lower registered bar than 0.5% would be needed to look for a smaller gain.

## Why it moved

- [measured] Successful Search Rate is flat at -0.05%, and no segment (mobile, desktop, head, tail, navigational, informational) shows a clear move.
- [measured] Queries per User rose 1.9% and Ad Click Rate fell 1.5%, but neither is a registered metric and neither changes the call.
- [guess] The new ranker may reorder results without changing which result gets the click; the scorecard cannot show this.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

0 fail, 0 warn, 228 body words (readout)
cold-read: skim 2/2, full 3/3 - pass

The cold reader flagged that the table verdict "unclear" and the headline "No effect found" look inconsistent. The headline is the call: the interval's upper end (+0.24%) is below the 0.50% bar.