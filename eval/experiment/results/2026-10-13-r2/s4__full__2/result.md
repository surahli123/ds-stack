Decision: Ship

# Ranker v7: Ship

Decision: Ship. Successful Search Rate rose 0.81% (+0.41% to +1.21%), which clears the 0.50% bar and every guardrail held.

Ask: Approve the launch to all traffic.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: pre period could not be checked: no pre-period interval or platform check.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.81% (+0.41% to +1.21%) | at least 0.50% higher | better |
| 4 other guardrails | guardrail | | | all within margin |

Checks: passed: scorecard, sample split, config params, config edits; not run: pre period, novelty.

## What would change the call

- A pre-exposure comparison showing the arms already differed on Successful Search Rate would make the test unreadable.
- A daily effect series by days since first exposure that fades toward zero would mean the test needs more time.
- A Head Queries drop that holds up in a follow-up cut would make this a trade-off for triage.

## Why it moved

- [measured] Successful Search Rate rose 0.81% while CTR (-0.02%) and Long Click Rate (-0.23%) stayed flat, so the gain is not coming from more clicks.
- [measured] Successful Search Rate - Head Queries fell 0.95% and Successful Search Rate - Mobile rose 0.74%; neither survived correction, so the mechanism is unknown.
- [guess] The new ranker may resolve searches that used to end without a successful click, without changing click volume.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction on (changes are adjusted for pre-test behaviour); harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

0 fail, 0 warn, 222 body words (readout)
cold-read: skim 2/2, full 3/3 - pass

The cold-read reader flagged that the 0.50% bar is cleared by the point estimate, not the whole interval (the lower bound is +0.41%). That matches the pre-registration, which sets `ship_requires: point_at_bar`.