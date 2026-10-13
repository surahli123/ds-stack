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

- Registering Successful Search Rate, as the hypothesis states, as the primary: the pre-registration lists Queries per User instead.
- Success per query flat or up with no rise in repeat queries would show the extra queries are healthy.

## Why it moved

- [inferred] Queries per User rose 2.60% and Reformulation Rate rose 5.50%. Searchers retry because first results miss. Successful Search Rate fell 0.45%.
- [guess] Successful Search Rate - Desktop rose 1.52%. Mobile and informational queries did not follow. No cut has been run on this yet.
- [measured] Latency p95 (ms) is flat at +0.20%, so speed does not explain the moves.

## Analyst's view

The analyst would call this Escalate: The hypothesis and config name Successful Search Rate as primary, and it fell 0.45% while Reformulation Rate rose 5.50%. More searching with less success can mean worse results.

## Appendix

- Secondary metrics: 55 tested; after a false-discovery correction these moved: Reformulation Rate (+5.50%), Successful Search Rate - Desktop (+1.52%), Autocomplete Acceptance (+0.97%). They are exploratory and don't change the call.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms).
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
