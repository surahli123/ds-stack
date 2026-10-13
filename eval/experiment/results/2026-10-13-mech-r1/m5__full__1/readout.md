# Ranker v7: Escalate

Decision: Escalate. Successful Search Rate rose 0.68% (+0.28% to +1.08%), but Abandonment Rate rose 2.10% (+1.50% to +2.70%), the wrong way, though inside its 4.00% margin.

Ask: Decide the trade-off at triage.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: secondary metric CTR got worse after correction.

Triage: Ready: every movement triage will ask about has a candidate explanation and none conflict; the explanations are inferred from co-movements, so the cuts below would confirm them.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Abandonment Rate | guardrail | +2.10% (+1.50% to +2.70%) | at most 4.00% higher | worse, within margin |
| Successful Search Rate | primary | +0.68% (+0.28% to +1.08%) | estimate at least 0.50% higher | better |
| 1 other guardrail | guardrail | | | within margin |

Checks: passed: scorecard, sample split, config params, config edits, novelty; not run: pre period.

## What would change the call

- Abandonment concentrated on queries with an answer or rich snippet would make the rise benign, and the trade-off would favor the lift.
- More same-query repeats within 5 minutes after an abandoned query would make the rise failed searches, and the trade-off would favor holding back.
- A pre-exposure comparison of Successful Search Rate, not yet run, would clear the one check that could not run.

## Why it moved

- [inferred] Abandonment Rate rose 2.10%. Answers shown on the page may satisfy people without a click, which would also explain lower CTR and Clicks per User. Untested.
- [inferred] Successful Search Rate rose 0.68% at the same size from the first days to the last, with Long Click Rate and Reformulation Rate flat. That fits a relevance gain.
- [guess] Device and query-class rows are all flat or lower, which the overall rise cannot be built from. The segment rows need a check.

## Appendix

- Secondary metrics: 54 tested; after a false-discovery correction these moved: CTR (-1.10%), Clicks per User (-1.20%). They are exploratory and don't change the call.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms).
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
