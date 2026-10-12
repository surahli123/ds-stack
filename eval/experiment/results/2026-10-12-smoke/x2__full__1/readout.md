# Ranker v7: Not an A/B test

Decision: Not an A/B test. This is a holdout test; the A/B launch rule doesn't apply.

Ask: Use the readout for this test design instead.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: nothing here; this design needs its own readout.

Checks: pre period could not run; novelty could not run; scorecard pass; sample split pass; config params pass; config edits pass.

## What would change the call

- The owner confirming this was a standard two-arm A/B would turn this into a Ship on the same numbers.
- A pre-exposure comparison showing a gap between arms would turn the call into Can't tell.
- A daily series by days since first exposure showing the lift fading would turn it into Keep running.

## Why it moved

- [measured] Successful Search Rate rose 0.81%, with every guardrail inside its margin.
- [inferred] Gains show in head and tail queries; CTR and clicks per user did not rise, so the lift is not from more clicking.
- [guess] The mechanism is unknown; no pre-period or daily series was available.

## Analyst's view

The analyst would call this Ship: The config shows two equal-size arms differing only in ranker_model, with no holdout group, so the holdout label looks like a pre-registration error. If the owner confirms, the rule gives Ship.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
