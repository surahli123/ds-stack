Decision: Keep running. It's day 4 of 14; Successful Search Rate reads +1.42% (+0.32% to +2.52%) so far, too early to call.

Ask: Approve running the test longer.

Status: day 4 of 14, 260,000 users per arm, short of the planned 900,000, not whole weeks.

Could reverse it: the remaining data; the call is made at the planned sample.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +1.42% (+0.32% to +2.52%) | at least 0.50% higher | better |
| 4 other guardrails | guardrail | | | all within margin |

Checks: passed: scorecard, sample split, config params, config edits; not run: pre period, novelty.

## What would change the call

- A pull covering all 14 days (this one is dated 2026-09-15, day 4) with Successful Search Rate at or above +0.5% and every guardrail within its margin.
- A full-length pull with Successful Search Rate below +0.5%.
- Any guardrail moving past its margin in the full-length pull.

## Why it moved

- [measured] Successful Search Rate is +1.42% overall, but Mobile is +0.12% and Desktop is -0.60%. Neither device reaches the overall lift, so devices do not explain it.
- [measured] Head Queries are +0.59% and Navigational is -0.60%. No query type shows a clear lift by itself.
- [guess] The mechanism is unknown. This is a 4-day read, and an early lift can fade.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

0 fail, 0 warn, 209 body words (readout)
cold-read: skim 2/2, full 3/3 - pass