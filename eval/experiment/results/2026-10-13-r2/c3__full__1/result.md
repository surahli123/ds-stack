Decision: Can't tell. Before exposure, Successful Search Rate already differed by +0.71% (+0.31% to +1.11%). No launch decision from this data until it's fixed.

# Ranker v7: Can't tell

Ask: Agree to fix the test and rerun; no launch decision from this data.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: fixing the pre period problem and rerunning.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.81% (+0.41% to +1.21%) | at least 0.50% higher | better |
| 4 other guardrails | guardrail | | | all within margin |

Checks: pre period fail; passed: scorecard, sample split, config params, config edits; not run: novelty.

## What would change the call

- A pre-exposure comparison showing no gap on Successful Search Rate, for example after a re-randomized rerun, would let the call be made from the lift.
- A documented cause for the pre-exposure gap, added to the pre-registration, would move this to triage.
- A daily effect series by days since first exposure would allow the novelty check to run.

## Why it moved

- [measured] Successful Search Rate already differed between the arms before exposure, by about as much as the lift seen after.
- [inferred] The arms were likely not comparable at the start, so the lift may mostly reflect who was assigned, not the new ranker.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

0 fail, 0 warn, 208 body words (readout)
cold-read: skim 2/2, full 3/3 - pass