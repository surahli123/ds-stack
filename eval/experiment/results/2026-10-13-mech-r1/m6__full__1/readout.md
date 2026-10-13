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

- Success per user (not per query) flat while queries fall: the lift is the denominator, so the bar is not met.
- Success on queries where ranking changed up clearly, with untriggered queries flat: a real relevance gain.
- A pre-exposure comparison showing the arms already differed before the test started.

## Why it moved

- [inferred] Queries per User fell 1.9% while Clicks per User (+0.1%) and Sessions per User (-0.1%) stayed flat, so per-query rates like CTR (+2.1%) can rise with no better results.
- [measured] Successful Search Rate rose 0.81%, but Long Click Rate, Abandonment Rate and Reformulation Rate did not move, and no query class or device shows a clear gain.
- [guess] Ranker v7 may have cut repeat or accidental queries, which would be a real gain, but nothing on the scorecard shows it yet.

## Analyst's view

The analyst would call this Escalate: The primary is a per-query rate and queries per user fell while clicks stayed flat; this may be the denominator, not better ranking.

## Appendix

- Secondary metrics: 52 tested; after a false-discovery correction these moved: CTR (+2.10%), Queries per User (-1.90%). They are exploratory and don't change the call.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
