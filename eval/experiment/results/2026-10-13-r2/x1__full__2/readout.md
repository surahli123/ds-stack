# Ranker v7: Not an A/B test

Decision: Not an A/B test. This is a interleaving test; the A/B launch rule doesn't apply.

Ask: Use the readout for this test design instead.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: nothing here; this design needs its own readout.

Checks: passed: scorecard, sample split, config params, config edits; not run: pre period, novelty.

## What would change the call

- The interleaving analysis, with its own preference metric, would give the call for this design.
- A rerun as a plain A/B test, with v6 and v7 served to separate users, would let the A/B rule apply.

## Why it moved

- [guess] The mechanism is unknown: the scorecard has no segment cuts, and the test arm mixes v6 and v7 results in one list.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
