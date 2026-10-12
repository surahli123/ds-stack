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

- Fixing the config params problem and rerunning with snippet_length equal in both arms, or adding an arm that isolates the snippet change.
- A pre-exposure comparison and a daily series by days since first exposure would let the remaining checks run.

## Why it moved

- [measured] Test arm also has a longer snippet_length than control, which the pre-registration did not intend, so the ranker and the snippet change are mixed together.
- [guess] Longer snippets could raise successful searches on their own by helping people judge results before clicking.
- [measured] No segment cuts in the scorecard, so how much of the +0.81% comes from the ranker is unknown.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
