# Ranker v7: No effect found

Decision: No effect found. Successful Search Rate reads +0.00% (-0.30% to +0.30%), which rules out the 0.50% change the test was built to find.

Ask: Agree to stop the test without launching.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: no pre-period comparison, so a difference between the arms before the test isn't ruled out.

Triage: Ready: every movement triage will ask about has a candidate explanation and none conflict; the explanations are inferred from co-movements, so the cuts below would confirm them.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.00% (-0.30% to +0.30%) | estimate at least 0.50% higher | unclear |
| 4 other guardrails | guardrail | | | all within margin |

Checks: passed: scorecard, sample split, config params, config edits, novelty; not run: pre period.

## What would change the call

- A dwell-time cut showing the extra clicks are short ones confirms no gain; mostly long clicks would reopen the result.
- A pre-exposure comparison showing the arms differed before the test would make the whole read unreliable.

## Why it moved

- [inferred] CTR rose 2.4% and Clicks per User 2.2%, but Successful Search Rate and Long Click Rate did not move: extra clicks, not extra satisfaction.
- [guess] Reformulation Rate fell 0.9%, a hint users re-search less, yet Queries per User and Abandonment Rate are flat.
- [guess] Every CTR segment row is negative while overall CTR is up; segment rows do not reconcile with the total.

## Appendix

- Secondary metrics: 52 tested; after a false-discovery correction these moved: CTR (+2.40%), Clicks per User (+2.20%). They are exploratory and don't change the call.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
