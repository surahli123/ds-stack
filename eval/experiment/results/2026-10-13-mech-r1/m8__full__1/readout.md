# Ranker v7: Ship

Decision: Ship. Queries per User rose 2.60% (+1.70% to +3.50%), which clears the 1.00% bar and every guardrail held.

Ask: Approve the launch to all traffic.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: secondary metric Reformulation Rate got worse after correction.

Triage: Not ready: the scripted call is Ship, but the best explanation of Queries per User is bad news: 'More activity without more success'. Run first: success per query vs per user.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Queries per User | primary | +2.60% (+1.70% to +3.50%) | estimate at least 1.00% higher | better |
| 1 other guardrail | guardrail | | | within margin |

Checks: passed: scorecard, sample split, config params, config edits, novelty; not run: pre period.

## What would change the call

- Success per query flat or down while Queries per User rises would confirm activity without success.
- A similar query repeated within 5 minutes rising in Test would confirm worse results; flat would point to real extra demand.

## Why it moved

- [inferred] Users ran more queries (+2.60%) and reformulated more (+5.50%), yet Successful Search Rate is down (-0.45%). That fits repeat searching after weak first results.
- [guess] Successful Search Rate is the registered hypothesis metric, and its drop is concentrated in Informational queries (down 0.85%) while Desktop rose 1.52%. No cut has been run to explain this yet.

## Analyst's view

The analyst would call this Escalate: The pre-registered primary is Queries per User, but the hypothesis is Successful Search Rate, which is down 0.45% and clearly below zero. Reformulation Rate is up 5.50%. More searching with less success can mean worse results, so settle the success cuts first.

## Appendix

- Secondary metrics: 55 tested; after a false-discovery correction these moved: Reformulation Rate (+5.50%), Successful Search Rate - Desktop (+1.52%), Autocomplete Acceptance (+0.97%). They are exploratory and don't change the call.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms).
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
