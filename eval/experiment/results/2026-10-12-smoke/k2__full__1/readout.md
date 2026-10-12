# Ranker v7: Keep running

Decision: Keep running. Successful Search Rate reads +0.81% (+0.41% to +1.21%) overall, but the effect is fading over the days of the test.

Ask: Approve running the test longer.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: the remaining data; the call is made at the planned sample.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.81% (+0.41% to +1.21%) | at least 0.50% | better |
| Other guardrails | guardrail | Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User | | within margin |

Checks: novelty flag; pre period could not run; scorecard pass; sample split pass; config params pass; config edits pass.

## What would change the call

- An extension where the lift by days since exposure levels off at or above 0.5% would make this a Ship.
- An extension where the lift keeps falling below 0.5% would make this a Don't ship or No effect found.
- A pre-exposure comparison showing the arms were balanced would close the one check that could not run.

## Why it moved

- [measured] Successful Search Rate lift shrinks with days since first exposure: +1.33% in the first days, +0.50% in the last days.
- [inferred] A fading lift fits a novelty effect, where users react to changed rankings and then settle back.
- [guess] No segment cuts in the scorecard, so which users or queries drive the fade is unknown.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
