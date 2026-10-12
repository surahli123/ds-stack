# Ranker v7: Escalate

Decision: Escalate. Successful Search Rate improved +0.31% (+0.13% to +0.49%), real but short of the 0.50% bar.

Ask: Decide the trade-off at triage.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: pre period could not be checked: no pre-period interval or platform check.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.31% (+0.13% to +0.49%) | at least 0.50% | better, below the bar |
| Other guardrails | guardrail | Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User | | within margin |

Checks: pre period could not run; novelty could not run; scorecard pass; sample split pass; config params pass; config edits pass.

## What would change the call

- The owner confirms a lower bar than 0.50% as acceptable, or the review decides +0.31% is worth shipping anyway; then the call becomes Ship.
- A rerun or follow-up that shows the true lift reaches 0.50%; this readout's range tops out at +0.49%.
- A pre-exposure comparison that fails would make the test unreliable and the call Can't tell.

## Why it moved

- [measured] Mobile (-0.35%), desktop (+0.59%), head queries (-0.70%) and tail queries (-0.14%) all have intervals that include zero, so no segment explains the +0.31% gain.
- [measured] Guardrails Latency p95, Abandonment Rate, Zero Result Rate and Revenue per User all stayed inside their margins, so the gain did not come from a visible cost.
- [guess] The mechanism is unknown; better ranking of results is the intended cause but no cut here confirms it.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

0 fail, 0 warn, 244 body words (readout)
cold-read: skim 2/2, full 3/3 - pass