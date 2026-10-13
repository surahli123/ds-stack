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

- Per-query success and a repeat of the same query within 5 minutes, by arm, showing no rise in repeats would back the lift.
- A registered primary of Successful Search Rate, as the hypothesis states, would make its fall the deciding result.
- A pre-exposure comparison of Queries per User would settle the check that could not run.

## Why it moved

- [inferred] Reformulation Rate rose 5.50% alongside Queries per User (+2.60%): people re-search because results are worse.
- [measured] Successful Search Rate, the hypothesis metric, fell 0.45%, mostly on informational queries (-0.85%). Cuts are unregistered, so exploratory.
- [guess] Autocomplete Acceptance rose 0.97%; whether it feeds extra queries is untested.

## Analyst's view

The analyst would call this Escalate: The registered primary counts volume; success fell and reformulation rose, so the scripted call should go to triage as a trade-off.

## Appendix

- Secondary metrics: 55 tested; after a false-discovery correction these moved: Reformulation Rate (+5.50%), Successful Search Rate - Desktop (+1.52%), Autocomplete Acceptance (+0.97%). They are exploratory and don't change the call.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms).
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
