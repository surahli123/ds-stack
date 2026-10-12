# Ranker v7: Not an A/B test

Decision: Not an A/B test. This is a holdout test; the A/B launch rule doesn't apply.

Ask: Use the readout for this test design instead.

Status: day 14 of 90, 1,000,000 users per arm, above the planned 50,000, whole weeks.

Could reverse it: nothing here; this design needs its own readout.

Checks: sample split fail; passed: scorecard, config params, config edits; not run: pre period, novelty.

## What would change the call

- A comparison of Ranker v7 against a randomized control, registered as an A/B test with its own bar, would make the A/B rules apply.
- An explanation of why the arms are split evenly when the holdout design planned a small control group would need to be settled first.

## Why it moved

- [guess] The mechanism is unknown; the scorecard has no segment cuts, so no cause for the Successful Search Rate gain can be named.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
