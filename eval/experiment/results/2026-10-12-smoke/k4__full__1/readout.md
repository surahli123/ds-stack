Decision: Keep running

It's day 7 of 14; Successful Search Rate reads +0.55% (-0.21% to +1.31%) so far, too early to call.

Ask: Approve running the test longer.

Status: day 7 of 14, 480,000 users per arm, short of the planned 900,000, whole weeks.

Could reverse it: the remaining data; the call is made at the planned sample.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.55% (-0.21% to +1.31%) | at least 0.50% | unclear |
| Abandonment Rate | guardrail | +0.10% (-1.04% to +1.24%) | no worse than 1.00% | unclear |
| Revenue per User | guardrail | -0.10% (-1.43% to +1.23%) | no worse than 1.00% | unclear |
| Other guardrails | guardrail | Latency p95 (ms), Zero Result Rate | | within margin |

Checks: pre period could not run; novelty could not run; scorecard pass; sample split pass; config params pass; config edits pass.

## What would change the call

- A refreshed scorecard at the full 14 days: the results we have stop at day 7, 2026-09-18.
- If Successful Search Rate stays at or above +0.5% with its range clear of zero at 900,000 users per arm, the call becomes Ship, given every guardrail stays within its margin.
- If the range at full sample sits wholly below +0.5%, the call becomes No effect found.

## Why it moved

- [guess] The mechanism is unknown: the scorecard has no segment cuts, so nothing says which searches gained.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
