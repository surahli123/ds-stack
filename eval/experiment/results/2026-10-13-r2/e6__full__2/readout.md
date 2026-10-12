# Ranker v7: Ship

Decision: Ship. Queries per User rose 2.40% (+1.50% to +3.30%), which clears the 1.00% bar and every guardrail held.

Ask: Approve the launch to all traffic.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: secondary metric Reformulation Rate got worse after correction.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Queries per User | primary | +2.40% (+1.50% to +3.30%) | at least 1.00% higher | better |
| 1 other guardrail | guardrail | | | within margin |

Checks: passed: scorecard, sample split, config params, config edits; not run: pre period, novelty.

## What would change the call

- A cut of Queries per User by whether the query followed a reformulation, showing the gain comes from new intent and not rephrasing, would remove the concern.
- A longer run in which Successful Search Rate is flat or up and Reformulation Rate stops rising would remove the concern.
- A Successful Search Rate loss that holds with more data would make this a clear block.

## Why it moved

- [measured] Queries per User rose 2.4% while Reformulation Rate rose 5.1%, so part of the extra searching is people rephrasing a query.
- [measured] Successful Search Rate, the hypothesis metric in the experiment config, moved -0.35%, and its range includes zero, so it neither confirms nor rules out a loss.
- [guess] The new ranker may return less relevant first results, which makes users search again.

## Analyst's view

The analyst would call this Escalate: Queries per User is a volume metric and the registered primary, but Reformulation Rate rose 5.1% after correction and Successful Search Rate moved -0.35%. More searching here may mean worse results, so the review should weigh the trade-off before approving.

## Appendix

- Secondary metrics: 55 tested; after a false-discovery correction these moved: Reformulation Rate (+5.10%), Ad Click Rate (-1.98%). They are exploratory and don't change the call.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms).
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
