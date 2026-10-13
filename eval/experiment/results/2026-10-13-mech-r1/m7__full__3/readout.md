# Ranker v7: No effect found

Decision: No effect found. Successful Search Rate reads +0.08% (-0.22% to +0.38%), which rules out the 0.50% change the test was built to find.

Ask: Agree to stop the test without launching.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: no pre-period comparison, so a difference between the arms before the test isn't ruled out.

Triage: Ready: every movement triage will ask about has a candidate explanation and none conflict; the explanations are inferred from co-movements, so the cuts below would confirm them.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.08% (-0.22% to +0.38%) | estimate at least 0.50% higher | unclear |
| 4 other guardrails | guardrail | | | all within margin |

Checks: passed: scorecard, sample split, config params, config edits, novelty; not run: pre period.

## What would change the call

- A Tail Queries cut on triggered queries showing the lift holds and the other classes do not fall would justify a rerun aimed at tail traffic.
- A sample split or logging imbalance within Tail Queries by arm would mean the tail lift is an artifact.
- A pre-exposure comparison of Successful Search Rate showing a gap between arms would undermine this read.

## Why it moved

- [measured] The overall rate is flat because gains and losses cancel by query class: Successful Search Rate is +3.40% on Tail Queries, -0.53% on Head Queries and -1.07% on Navigational.
- [inferred] The new ranker probably surfaces better results for rare, long-tail queries and slightly displaces the right top result on navigational ones; Reformulation Rate on Navigational rose 1.71%.
- [guess] CTR - Mobile fell 1.43% while Successful Search Rate - Mobile did not clearly move; no cut has been run on it.

## Appendix

- Secondary metrics: 52 tested; after a false-discovery correction these moved: Successful Search Rate - Tail Queries (+3.40%). They are exploratory and don't change the call.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
