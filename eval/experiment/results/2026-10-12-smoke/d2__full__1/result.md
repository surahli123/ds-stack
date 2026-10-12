Decision: Don't ship. Successful Search Rate moved the wrong way, -0.62% (-1.02% to -0.22%).

Ask: Agree not to launch; the owner decides whether to iterate.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: only a version where Successful Search Rate improves.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | -0.62% (-1.02% to -0.22%) | at least 0.50% | worse |
| Other guardrails | guardrail | Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User | | within margin |

Checks: pre period could not run; novelty could not run; scorecard pass; sample split pass; config params pass; config edits pass.

## What would change the call

- A pre-exposure comparison or daily series by days since first exposure showing the drop is a pre-existing imbalance or a fading novelty effect would reopen the call.
- A confirmed prereg from the owner with a different primary metric or direction would change the call.

## Why it moved

- [measured] Segment cuts of Successful Search Rate (mobile, desktop, head, tail, navigational, informational) are all unclear and mixed in sign, so the drop is not localized to one segment.
- [measured] Guardrails are all within margin, so the drop is not paired with a latency, abandonment, zero-result or revenue move.
- [guess] The mechanism is unknown; no data here shows why the new ranker lowered successful searches.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

0 fail, 0 warn, 219 body words (readout)
cold-read: skim 2/2, full 3/3 - pass