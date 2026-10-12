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

- A pre-exposure comparison or daily series by days since first exposure would let the pre-period and novelty checks run.
- A fixed ranker with the primary at or above the 0.5% bar and guardrails inside their margins would reopen the question.

## Why it moved

- [guess] Successful Search Rate fell 0.62% (-1.02% to -0.22%) and the scorecard has no segment cuts, so the mechanism is unknown.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
