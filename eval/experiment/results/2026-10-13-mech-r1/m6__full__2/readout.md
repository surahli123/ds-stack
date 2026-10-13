# Ranker v7: Ship

Decision: Ship. Successful Search Rate rose 0.81% (+0.41% to +1.21%), which clears the 0.50% bar and every guardrail held.

Ask: Approve the launch to all traffic.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: secondary metric Queries per User got worse after correction.

Triage: Ready: every movement triage will ask about has a candidate explanation and none conflict; the explanations are inferred from co-movements, so the cuts below would confirm them.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.81% (+0.41% to +1.21%) | estimate at least 0.50% higher | better |
| 4 other guardrails | guardrail | | | all within margin |

Checks: passed: scorecard, sample split, config params, config edits, novelty; not run: pre period.

## What would change the call

- Success on triggered queries (ranking changed) flat or negative, with the Queries per User drop traced to logging or dropped searches, would remove the win.
- The same lift on triggered queries with unchanged search logging would confirm the relevance gain.
- A pre-exposure comparison that shows the arms already differed would make the test unreliable.

## Why it moved

- [inferred] Successful Search Rate rose 0.81% while Queries per User fell 1.9% and Clicks per User stayed flat, so part of the rise may come from fewer searches in the denominator, not better results.
- [inferred] Every device, head/tail and query-type cut of Successful Search Rate is flat or negative, yet the total is up, which points to a mix shift in which searches get counted.
- [inferred] CTR rose 2.1%, in line with the same smaller query count rather than more clicks.

## Analyst's view

The analyst would call this Escalate: The rule sees a primary above its bar, but Queries per User fell 1.9% with flat clicks and no cut of Successful Search Rate is positive, so the lift may be a denominator effect. Run the triggered-queries and search-volume cuts before approving.

## Appendix

- Secondary metrics: 52 tested; after a false-discovery correction these moved: CTR (+2.10%), Queries per User (-1.90%). They are exploratory and don't change the call.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
