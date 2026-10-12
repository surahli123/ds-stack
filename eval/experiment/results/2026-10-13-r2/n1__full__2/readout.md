# Ranker v7: No effect found

Decision: No effect found. Successful Search Rate reads +0.04% (-0.26% to +0.34%), which rules out the 0.50% change the test was built to find.

Ask: Agree to stop the test without launching.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: pre period could not be checked: no pre-period interval or platform check.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.04% (-0.26% to +0.34%) | at least 0.50% higher | unclear |
| 4 other guardrails | guardrail | | | all within margin |

Checks: passed: scorecard, sample split, config params, config edits; not run: pre period, novelty.

## What would change the call

- A pre-exposure comparison of Successful Search Rate showing the arms already differed would make the test unreadable.
- A daily series by days since first exposure showing a lift that faded would reopen the question.

## Why it moved

- [measured] Successful Search Rate is flat at +0.04%; the new ranker did not change how often searches end in a successful click.
- [guess] The segment cuts in the scorecard were not used here, so the mechanism is unknown.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
