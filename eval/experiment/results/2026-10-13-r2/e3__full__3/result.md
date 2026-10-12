Decision: Escalate. Successful Search Rate rose 0.31% (+0.13% to +0.49%), a real change in the good direction but short of the 0.50% bar.

Ask: Decide the trade-off at triage.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: pre period could not be checked: no pre-period interval or platform check.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.31% (+0.13% to +0.49%) | at least 0.50% higher | better, below the bar |
| 4 other guardrails | guardrail | | | all within margin |

Checks: passed: scorecard, sample split, config params, config edits; not run: pre period, novelty.

## What would change the call

- The team accepting a bar below 0.31% for this ranker would make the primary clear it, with every guardrail still within its margin.
- A pre-exposure comparison and a daily series by days since first exposure would let the two unrun checks run; a fading effect or a pre-period gap would weaken the case.

## Why it moved

- [measured] Successful Search Rate rose 0.31% (+0.13% to +0.49%) with the new ranker model as the only change between arms.
- [guess] No segment cuts were in the scorecard, so which queries gained is not known.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

0 fail, 0 warn, 194 body words (readout)
cold-read: skim 2/2, full 2/3 - fail

The cold read failed. The reader missed the third takeaway, the pre-period check that couldn't run, and found "Could reverse it" confusing.