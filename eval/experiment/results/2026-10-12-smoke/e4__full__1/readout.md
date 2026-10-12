# Ranker v7: Escalate

Decision: Escalate. Successful Search Rate improved +0.39% (+0.27% to +0.51%), real but short of the 0.50% bar.

Ask: Decide the trade-off at triage.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: pre period could not be checked: no pre-period interval or platform check.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.39% (+0.27% to +0.51%) | at least 0.50% | better, below the bar |
| Other guardrails | guardrail | Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User | | within margin |

Checks: pre period could not run; novelty could not run; scorecard pass; sample split pass; config params pass; config edits pass.

## What would change the call

- A longer run or more traffic that tightens the overall interval so it sits wholly above or below the 0.50% bar.
- Owner agreeing the bar is a floor for a small win with all guardrails within margin; then it becomes a ship.

## Why it moved

- [guess] The mechanism is unknown: the scorecard has no segment or query-type cuts, so why the new ranker lifts successful searches is not measured.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
