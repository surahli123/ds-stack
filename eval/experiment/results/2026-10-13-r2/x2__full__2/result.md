Decision: Not an A/B test

Ranker v7 is registered as a holdout, so the A/B launch rule doesn't apply.

Ask: Use the readout for this test design instead.

Status: day 14 of 90, 1,000,000 users per arm, above the planned 50,000, whole weeks.

Could reverse it: nothing here; this design needs its own readout.

Checks: sample split fail; passed: scorecard, config params, config edits; not run: pre period, novelty.

## What would change the call

- A randomized A/B test of the ranker alone, with the registered bar, would get a call on this ranker.
- An export whose arm sizes match the planned split would settle the sample check.

## Why it moved

- [guess] The mechanism is unknown; the scorecard has no segment cuts.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

doc_lint: 0 fail, 0 warn, 116 body words (readout)
cold-read: skim 2/2, full 3/3 - pass

I dropped the rendered title line so the readout starts with the `Decision:` line you asked for.