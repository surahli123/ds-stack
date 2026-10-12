# Ranker v7: Don't ship

Decision: Don't ship. Latency p95 (ms) rose 3.10% (+2.50% to +3.70%), the wrong way and past its 2.00% margin.

Ask: Agree not to launch; the owner decides whether to iterate.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: only a version that keeps Latency p95 (ms) at at most 2.00% higher.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Latency p95 (ms) | guardrail | +3.10% (+2.50% to +3.70%) | at most 2.00% higher | past its margin |
| Successful Search Rate | primary | +0.81% (+0.41% to +1.21%) | at least 0.50% higher | better |
| 3 other guardrails | guardrail | | | all within margin |

Checks: passed: scorecard, sample split, config params, config edits; not run: pre period, novelty.

## What would change the call

- A v7 build whose Latency p95 rise stays within 2.00% while Successful Search Rate keeps clearing 0.50% would flip the call.
- A review that formally accepts a latency rise beyond the registered 2.00% margin in exchange for the search gain would reopen it.

## Why it moved

- [measured] Successful Search Rate rose 0.81%, above the 0.50% bar, so the new ranker finds more successful searches.
- [inferred] Latency p95 rose 3.10%, past the 2.00% margin; a heavier lambdamart_v7 model scoring each query is the likely cause, but no cut by query type was read.
- [guess] No segment cuts were read, so which queries pay the latency cost is not known.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
