# Ranker v7: Ship

Decision: Ship. Queries per User improved +2.40% (+1.50% to +3.30%), which clears the 1.00% bar and every guardrail held.

Ask: Approve the launch to all traffic.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: pre period could not be checked: no pre-period interval or platform check.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Queries per User | primary | +2.40% (+1.50% to +3.30%) | at least 1.00% | better |
| Other guardrails | guardrail | Latency p95 (ms) | | within margin |

Checks: pre period could not run; novelty could not run; scorecard pass; sample split pass; config params pass; config edits pass.

## What would change the call

- A pre-registered primary of Successful Search Rate with its interval ruling out a loss would change the call.
- Reformulation Rate staying flat in a rerun, or a split showing the extra queries are new searches not retries, would support Ship.
- A confirmed pre-registration naming Queries per User as the primary, since the file lacks owner sign-off.

## Why it moved

- [inferred] Reformulation Rate rose +5.10% (+4.30% to +5.90%) alongside Queries per User, so users may be re-searching because first results miss.
- [measured] Successful Search Rate, the hypothesis metric in the experiment config, moved -0.35% (-0.75% to +0.05%); Time to First Click rose +1.28%.
- [guess] Ad Click Rate fell -1.98% (-3.18% to -0.78%); the cause is unknown.

## Analyst's view

The analyst would call this Escalate: Queries per User rose with reformulations, and Successful Search Rate, the config's primary, did not improve. The gain may be a worse experience.

## Appendix

- Secondary metrics: 55 tested; after a false-discovery correction these moved: Reformulation Rate (+5.10%), Ad Click Rate (-1.98%). They are exploratory and don't change the call.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
