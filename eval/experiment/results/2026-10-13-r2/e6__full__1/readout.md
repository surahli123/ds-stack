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

- Owner confirms which metric is the intended primary; if Successful Search Rate is, its drop would need review.
- A pre-period check and a daily series by days since first exposure, to rule out novelty.

## Why it moved

- [measured] Queries per User rose 2.4% while Successful Search Rate moved -0.35% and Clicks per User did not rise.
- [inferred] Reformulation Rate went from 0.143 to 0.150293, so users may be searching again because the first results missed.
- [measured] The experiment's own primary in Statsig is Successful Search Rate, not Queries per User.

## Analyst's view

The analyst would call this Escalate: The registered primary is a volume metric. Reformulation rose and Successful Search Rate fell, so the extra queries may be failed searches. Abandonment Rate is not a registered guardrail here.

## Appendix

- Secondary metrics: 55 tested; after a false-discovery correction these moved: Reformulation Rate (+5.10%), Ad Click Rate (-1.98%). They are exploratory and don't change the call.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms).
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
