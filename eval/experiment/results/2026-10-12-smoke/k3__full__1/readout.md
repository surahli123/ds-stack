# Ranker v7: Keep running

Decision: Keep running. Successful Search Rate reads +0.12% (-0.36% to +0.60%); ruling out the 0.50% bar needs about 1.9 times the users so far.

Ask: Approve running the test longer.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: the remaining data; the call is made at the planned sample.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.12% (-0.36% to +0.60%) | at least 0.50% | unclear |
| Other guardrails | guardrail | Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User | | within margin |

Checks: pre period could not run; novelty could not run; scorecard pass; sample split pass; config params pass; config edits pass.

## What would change the call

- Nearly double the users so far, with the estimate still near +0.12%, would rule out the 0.50% bar and turn this into No effect found.
- An estimate near or above the 0.50% bar at that sample, with every guardrail still within its margin, would turn this into Ship.
- A daily series by days since first exposure would show whether the effect is fading; none was supplied.

## Why it moved

- [guess] The scorecard has no segment cuts, so the mechanism behind the small move in Successful Search Rate is unknown.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
