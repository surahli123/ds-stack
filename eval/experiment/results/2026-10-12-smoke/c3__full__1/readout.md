# Ranker v7: Can't tell

Decision: Can't tell. Before exposure, Successful Search Rate already differed by +0.71% (+0.31% to +1.11%). No launch decision from this data until it's fixed.

Ask: Agree to fix the test and rerun; no launch decision from this data.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: fixing the pre period problem and rerunning.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.81% (+0.41% to +1.21%) | at least 0.50% | better |
| Other guardrails | guardrail | Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User | | within margin |

Checks: pre period fail; novelty could not run; scorecard pass; sample split pass; config params pass; config edits pass.

## What would change the call

- A pre-exposure comparison that shows no gap, or a re-randomised rerun, would let the +0.81% lift be judged against the 0.5% bar.
- An adjusted readout that removes the pre-exposure gap and still clears the 0.5% bar would restore a Ship call.

## Why it moved

- [measured] Before exposure, Test users already had a higher Successful Search Rate, by +0.71%, against a measured lift of +0.81%.
- [guess] Most of the lift may come from who landed in Test, not from the ranker; the cause of the imbalance is not known.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
