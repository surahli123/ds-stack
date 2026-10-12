Decision: Ship. Successful Search Rate improved +0.81% (+0.41% to +1.21%), which clears the 0.50% bar and every guardrail held.

Ask: Approve the launch to all traffic.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: pre period could not be checked: no pre-period interval or platform check.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.81% (+0.41% to +1.21%) | at least 0.50% | better |
| Other guardrails | guardrail | Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User | | within margin |

Checks: pre period could not run; scorecard pass; sample split pass; config params pass; config edits pass; novelty pass.

## What would change the call

- The pre period could not be checked. A pre-exposure comparison showing the arms already differed on Successful Search Rate would make the test unreliable.
- A rollout holdout where the lift lands below 0.50% would argue for stopping, since the low end of the interval is under the bar.

## Why it moved

- [measured] The effect is stable by days since exposure: +0.81% early, +0.80% late, so it is not a novelty bump.
- [guess] No segment cuts were in the scorecard, so which queries gain is not known.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

0 fail, 0 warn, 196 body words (readout)
cold-read: skim 2/2, full 3/3 - pass