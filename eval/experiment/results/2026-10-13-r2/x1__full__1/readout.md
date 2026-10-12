# Ranker v7: Not an A/B test

Decision: Not an A/B test. This is a interleaving test; the A/B launch rule doesn't apply.

Ask: Use the readout for this test design instead.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: nothing here; this design needs its own readout.

Checks: passed: scorecard, sample split, config params, config edits; not run: pre period, novelty.

## What would change the call

- A fresh two-arm A/B run of Ranker v7 against v6 with the same registered bar and margins would get a decision under the standard rule.
- Pre-registered interleaving rules, such as a preference win rate and its bar, would let this test be read on its own terms.

## Why it moved

- [guess] The scorecard shows Successful Search Rate up +0.81% with no guardrail outside its margin, but no segment cuts were read, so the mechanism is not known.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
