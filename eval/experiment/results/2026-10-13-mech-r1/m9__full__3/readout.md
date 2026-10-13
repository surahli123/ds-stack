# Ranker v7: No effect found

Decision: No effect found. Successful Search Rate reads +0.02% (-0.28% to +0.32%), which rules out the 0.50% change the test was built to find.

Ask: Agree to stop the test without launching.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: no pre-period comparison, so a difference between the arms before the test isn't ruled out.

Triage: Ready: every movement triage will ask about has a candidate explanation and none conflict; the explanations are inferred from co-movements, so the cuts below would confirm them.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.02% (-0.28% to +0.32%) | estimate at least 0.50% higher | unclear |
| 4 other guardrails | guardrail | | | all within margin |

Checks: passed: scorecard, sample split, config params, config edits, novelty; not run: pre period.

## What would change the call

- A pre-exposure comparison of Successful Search Rate showing the arms already differed before the test started would make this test unreadable.
- A rerun on a larger sample that reads at or above 0.50% would reopen the case for v7.

## Why it moved

- [measured] Successful Search Rate did not move: +0.02% against the 0.50% the test was built to find, and the daily series stays flat from the first days to the last.
- [measured] Every guardrail stayed within its margin, so v7 changed rankings without hurting latency, abandonment, zero results or revenue.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
