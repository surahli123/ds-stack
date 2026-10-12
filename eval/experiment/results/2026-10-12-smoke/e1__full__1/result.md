# Ranker v7: Escalate

Decision: Escalate. Successful Search Rate improved +0.81% (+0.41% to +1.21%), but Abandonment Rate (+0.60% (-0.40% to +1.60%)) isn't shown within its 1.00% margin.

Ask: Decide the trade-off at triage.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: pre period could not be checked: no pre-period interval or platform check.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Abandonment Rate | guardrail | +0.60% (-0.40% to +1.60%) | no worse than 1.00% | unclear |
| Successful Search Rate | primary | +0.81% (+0.41% to +1.21%) | at least 0.50% | better |
| Other guardrails | guardrail | Latency p95 (ms), Zero Result Rate, Revenue per User | | within margin |

Checks: pre period could not run; novelty could not run; scorecard pass; sample split pass; config params pass; config edits pass.

## What would change the call

- Abandonment Rate interval narrowing to sit inside its 1.00% margin with more data would turn this into a launch.
- A pre-exposure comparison confirming the arms were balanced would close the one check that could not run.
- Abandonment Rate rising past the 1.00% margin would turn this into a stop.

## Why it moved

- [guess] No segment cuts or daily series were read, so the mechanism behind the Successful Search Rate gain is not known.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

0 fail, 0 warn, 198 body words (readout)
cold-read: skim 2/2, full 2/3 - fail

The cold read failed. Full-read takeaway 3, the "Could reverse it" line, was missed. The generated spine fixes that line, so I didn't edit it.