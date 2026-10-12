# Ranker v7: Can't tell

Decision: Can't tell. Parameters changed that the test didn't intend: {'Test': ['snippet_length']}. No launch decision from this data until it's fixed.

Ask: Agree to fix the test and rerun; no launch decision from this data.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: fixing the config params problem and rerunning.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.81% (+0.41% to +1.21%) | at least 0.50% higher | better |
| 4 other guardrails | guardrail | | | all within margin |

Checks: config params fail; passed: scorecard, sample split, config edits; not run: pre period, novelty.

## What would change the call

- Rerun with snippet_length equal in both arms, or confirm in the audit trail that the snippet change was intended and register it, and the existing numbers can be read.
- A pre-exposure comparison and a daily series by days since first exposure would clear the two checks that could not run.

## Why it moved

- [measured] The test arm ran a longer snippet as well as the new ranker, so the lift cannot be credited to the ranker alone.
- [guess] Longer snippets could change clicks on their own, which would feed straight into Successful Search Rate.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
