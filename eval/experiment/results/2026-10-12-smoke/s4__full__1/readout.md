# Ranker v7: Ship

Decision: Ship. Successful Search Rate improved +0.81% (+0.41% to +1.21%), which clears the 0.50% bar and every guardrail held.

Ask: Approve the launch to all traffic.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: pre period could not be checked: no pre-period interval or platform check.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.81% (+0.41% to +1.21%) | at least 0.50% | better |
| Other guardrails | guardrail | Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User | | within margin |

Checks: pre period could not run; novelty could not run; scorecard pass; sample split pass; config params pass; config edits pass.

## What would change the call

- A pre-exposure comparison showing the arms already differed on Successful Search Rate would make the call Can't tell.
- A daily series by days since first exposure showing the lift fading would move the call to Keep running.

## Why it moved

- [guess] The scorecard has no segment cuts, so the mechanism is unknown; the hypothesis is that the new ranker lifts the share of searches ending in a successful click.
- [measured] Click-based secondaries (CTR, Long Click Rate) did not rise with the primary.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction on (changes are adjusted for pre-test behaviour); harm inside a margin goes to escalate.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
