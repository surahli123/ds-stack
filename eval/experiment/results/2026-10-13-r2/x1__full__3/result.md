Decision: Not an A/B test

This is an interleaving test, so the A/B launch rule doesn't apply. I did not make a ship call. Ranker v7 is the product you'd ship, but a launch rule built for A/B tests can't read this design.

Ask: Use the readout for this test design instead.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: nothing here; this design needs its own readout.

Checks: passed: scorecard, sample split, config params, config edits; not run: pre period, novelty.

## What would change the call

- A separate A/B test of Ranker v7 against v6, with users split between arms, would get an ordinary call under the registered bar.
- A registered rule for reading interleaving preference would let this result count.

## Why it moved

- [guess] The mechanism is unknown, since the scorecard has no segment cuts.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

Lint: 0 fail, 0 warn, 118 body words (readout)
Cold read: skim 2/2, full 2/3 - fail. The reader missed the third takeaway, "Could reverse it: nothing here; this design needs its own readout."

I moved the call to its own first line, as you asked, and dropped the rendered title.