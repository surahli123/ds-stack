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

- A pre-exposure comparison of Successful Search Rate showing the arms already differed would make the test unreadable.
- A segment where the new ranker lifts Successful Search Rate by 0.50% or more would justify a narrower follow-up test.
- A rerun with a larger sample that finds a lift of 0.50% or more would reopen the question.

## Why it moved

- [measured] Successful Search Rate is flat at -0.05%, and the related click metrics barely moved: CTR +0.31%, Long Click Rate -0.08%, Reformulation Rate -0.09%.
- [inferred] Queries per User rose 1.9% but it is a secondary, and success did not rise with it, so it shows no gain in result quality.
- [guess] No segment cuts are in the scorecard, so which queries the new ranker changes is not known.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
