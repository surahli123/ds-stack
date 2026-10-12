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

- A pre-exposure comparison that is clean, or a documented cause of the head start, would let the +0.81% be read as the ranker's effect.
- A rerun with fresh assignment, or an analysis that adjusts for each user's pre-test behaviour, would give a fair comparison.
- A daily series by days since first exposure would show whether the lift holds up.

## Why it moved

- [measured] Successful Search Rate was already higher in the test arm before exposure by nearly as much as the +0.81% seen after, so the lift may be a head start rather than the ranker.
- [guess] The head start suggests the arms were not comparable at assignment, for example a skewed user mix.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
