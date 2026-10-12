# Ranker v7: Can't tell

Decision: Can't tell. Before exposure, Successful Search Rate already differed by +0.71% (+0.31% to +1.11%). No launch decision from this data until it's fixed.

Ask: Agree to fix the test and rerun; no launch decision from this data.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: fixing the pre period problem and rerunning.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.81% (+0.41% to +1.21%) | at least 0.50% higher | better |
| 4 other guardrails | guardrail | | | all within margin |

Checks: pre period fail; passed: scorecard, sample split, config params, config edits; not run: novelty.

## What would change the call

- A pre-exposure comparison that shows the groups were level, or a re-split that fixes the imbalance, would let the lift be read.
- A registered explanation for the pre-exposure gap, with evidence, would soften the failed check.
- A daily series by days since first exposure would let the novelty check run.

## Why it moved

- [measured] Before exposure, the Test group already ran ahead on Successful Search Rate, by about the same size as the lift seen during the test.
- [inferred] Most of the lift may come from how users were split between the groups, not from the new ranker.
- [guess] No segment cuts were read, so the mechanism is not known.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
