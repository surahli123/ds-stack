Decision: Keep running

It's day 4 of 14; Successful Search Rate reads +1.42% (+0.32% to +2.52%) so far, too early to call.

Ask: Approve running the test longer.

Status: day 4 of 14, 260,000 users per arm, short of the planned 900,000, not whole weeks.

Could reverse it: the remaining data; the call is made at the planned sample.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +1.42% (+0.32% to +2.52%) | at least 0.50% | better |
| Other guardrails | guardrail | Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User | | within margin |

Checks: pre period could not run; novelty could not run; scorecard pass; sample split pass; config params pass; config edits pass.

## What would change the call

- Reaching the planned 14 days and 900,000 users per arm, with the lift still at or above the 0.5% bar, would allow a Ship.
- A guardrail moving past its margin, or the lift fading as exposure days pass, would turn this into Don't ship or Escalate.

## Why it moved

- [guess] No segment cuts are in the scorecard, so the mechanism is not known.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

Lint: `0 fail, 0 warn, 178 body words (readout)`
Cold read: `cold-read: skim 2/2, full 3/3 - pass`

I dropped the rendered title line so the readout starts with the required `Decision:` line, and moved the reason onto its own line. The full set of outputs is in `/tmp/o2`.