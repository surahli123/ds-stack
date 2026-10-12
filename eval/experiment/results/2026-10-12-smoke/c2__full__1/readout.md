# Ranker v7: Can't tell

Decision: Can't tell. Parameters changed that the test didn't intend: {'Test': ['snippet_length']}. No launch decision from this data until it's fixed.

Ask: Agree to fix the test and rerun; no launch decision from this data.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: fixing the config params problem and rerunning.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.81% (+0.41% to +1.21%) | at least 0.50% | better |
| Other guardrails | guardrail | Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User | | within margin |

Checks: config params fail; pre period could not run; novelty could not run; scorecard pass; sample split pass; config edits pass.

## What would change the call

- A rerun, or a split of the data, where snippet length is the same in both arms would settle whether the ranker alone clears the bar.
- A pre-registration note that the snippet change was intended, with evidence, would turn this into an escalation.
- A daily series by days since first exposure would let us check the lift is not fading.

## Why it moved

- [measured] The test arm differs from control in two settings: the ranker model, and snippet length. Only the ranker was meant to change.
- [guess] Longer snippets could raise successful searches by themselves, so the lift may not come from the ranker.
- [guess] No segment cuts or daily series are in the scorecard, so the mechanism is unknown.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
