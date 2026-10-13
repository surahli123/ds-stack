# Ranker v7: No effect found

Decision: No effect found. Successful Search Rate reads -0.10% (-0.40% to +0.20%), which rules out the 0.50% change the test was built to find.

Ask: Agree to stop the test without launching.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: secondary metric CTR got worse after correction.

Triage: Ready: every movement triage will ask about has a candidate explanation and none conflict; the explanations are inferred from co-movements, so the cuts below would confirm them.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | -0.10% (-0.40% to +0.20%) | estimate at least 0.50% higher | unclear |
| 2 other guardrails | guardrail | | | all within margin |

Checks: passed: scorecard, sample split, config params, config edits, novelty; not run: pre period.

## What would change the call

- A cut on queries that had zero results in control showing a clear success gain would mean the ranker helps hard queries and the flat total hides it.
- A pre-exposure comparison of Successful Search Rate showing no gap between arms would close the one check that could not run.

## Why it moved

- [measured] Successful Search Rate did not move (-0.10%, -0.40% to +0.20%), and it was just as flat in the last days as in the first, so this is not a novelty effect.
- [inferred] Zero Result Rate fell 12.00% and CTR fell 1.80%. The likely link is that queries that used to return nothing now return weak results, which pulls the CTR average down without helping success.
- [guess] Nothing else on the scorecard moved beyond what chance would produce, so no other story is needed.

## Appendix

- Secondary metrics: 54 tested; after a false-discovery correction these moved: CTR (-1.80%), Zero Result Rate (-12.00%). They are exploratory and don't change the call.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
