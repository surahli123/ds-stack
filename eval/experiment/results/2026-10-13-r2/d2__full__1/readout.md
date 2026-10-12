# Ranker v7: Don't ship

Decision: Don't ship. Successful Search Rate fell 0.62% (-1.02% to -0.22%), the wrong way.

Ask: Agree not to launch; the owner decides whether to iterate.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: only a version where Successful Search Rate improves.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | -0.62% (-1.02% to -0.22%) | at least 0.50% higher | worse |
| 4 other guardrails | guardrail | | | all within margin |

Checks: passed: scorecard, sample split, config params, config edits; not run: pre period, novelty.

## What would change the call

- A rerun of the same test where Successful Search Rate is no longer worse, which would mean this result was a fluke.
- A finding that the success metric is logged differently for lambdamart_v7 results, which would mean the drop is a measurement artifact.

## Why it moved

- [measured] No cut explains the drop: Successful Search Rate - Mobile moved +0.44% and Desktop -0.37%, and neither cut is clearly different from no change.
- [guess] Reformulation Rate moved +0.11%, which is no visible change, so users are not re-searching more. The mechanism is unknown.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
