# Ranker v7: Don't ship

Decision: Don't ship. Successful Search Rate fell 0.72% (-1.12% to -0.32%), the wrong way.

Ask: Agree not to launch; the owner decides whether to iterate.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: only a version where Successful Search Rate improves.

Triage: Ready: every movement triage will ask about has a candidate explanation and none conflict; the explanations are inferred from co-movements, so the cuts below would confirm them.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | -0.72% (-1.12% to -0.32%) | estimate at least 0.50% higher | worse |
| 4 other guardrails | guardrail | | | all within margin |

Checks: passed: scorecard, sample split, config params, config edits, novelty; not run: pre period.

## What would change the call

- A pre-exposure comparison showing the arms already differed on Successful Search Rate before exposure would make this a broken test.
- Cuts showing the drop sits in one fixable query class would justify a rerun of a revised ranker.

## Why it moved

- [inferred] Reformulation Rate rose 4.80%, and Queries per User rose 2.30%. Together with the 0.72% drop in the primary, that fits users searching again because first results were worse.
- [measured] The drop is steady from the first days after exposure to the last, so it is not a novelty effect.
- [guess] Part of the extra queries may come from a few struggling users or one query class such as tail queries; no cut has been run yet.

## Appendix

- Secondary metrics: 52 tested; after a false-discovery correction these moved: Reformulation Rate (+4.80%), Queries per User (+2.30%). They are exploratory and don't change the call.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
