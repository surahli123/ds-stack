Decision: Don't ship

Latency p95 (ms) moved the wrong way, +3.10% (+2.50% to +3.70%), past its 2.00% margin.

Ask: Agree not to launch; the owner decides whether to iterate.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: only a version that keeps Latency p95 (ms) at no worse than 2.00%.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Latency p95 (ms) | guardrail | +3.10% (+2.50% to +3.70%) | no worse than 2.00% | past its margin |
| Successful Search Rate | primary | +0.81% (+0.41% to +1.21%) | at least 0.50% | better |
| Other guardrails | guardrail | Abandonment Rate, Zero Result Rate, Revenue per User | | within margin |

Checks: pre period could not run; novelty could not run; scorecard pass; sample split pass; config params pass; config edits pass.

## What would change the call

- A serving fix or caching change that brings Latency p95 (ms) back inside its 2.00% margin, retested on the same plan.
- The owners formally widening the latency margin, which would turn this into a trade-off for triage.

## Why it moved

- [measured] Successful Search Rate rose +0.81% while Latency p95 (ms) rose +3.10%, so the new ranker helps result quality but is slower to respond.
- [guess] The slowdown plausibly comes from the heavier lambdamart_v7 model scoring each query; no segment cuts were read to confirm.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
