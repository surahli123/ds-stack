# Ranker v7: Not an A/B test

Decision: Not an A/B test. This is a interleaving test; the A/B launch rule doesn't apply.

Ask: Use the readout for this test design instead.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: nothing here; this design needs its own readout.

Checks: pre period could not run; novelty could not run; scorecard pass; sample split pass; config params pass; config edits pass.

## What would change the call

- The owner confirming users were randomized into two arms, not interleaved, would let the A/B rule apply.
- A pre-exposure comparison and a daily series by days since first exposure, both missing now, would be needed first.

## Why it moved

- [measured] Successful Search Rate rose 0.81% (0.41% to 1.21%) with the ranker_model change as the only config difference between arms.
- [guess] No segment cuts are in the scorecard, so which queries gained is unknown.

## Analyst's view

The analyst would call this Escalate: experiment.json shows user-level groups with different ranker_model values, which looks like an A/B test, not interleaving. Owner should confirm the design label before the review.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
