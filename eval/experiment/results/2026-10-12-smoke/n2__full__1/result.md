Decision: No effect found

# Ranker v7: No effect found

Decision: No effect found. Successful Search Rate reads +0.06% (-0.24% to +0.36%), which rules out the 0.50% change the test was built to find.

Ask: Agree to stop the test without launching.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: pre period could not be checked: no pre-period interval or platform check.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.06% (-0.24% to +0.36%) | at least 0.50% | unclear |
| Other guardrails | guardrail | Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User | | within margin |

Checks: pre period could not run; novelty could not run; scorecard pass; sample split pass; config params pass; config edits pass.

## What would change the call

- A planned extension large enough to rule out a true lift between 0.24% and 0.50% would change the call to Keep running, but the team's bar says that lift is too small to launch.
- A pre-exposure comparison showing the arms differed before launch would change the call to Can't tell.

## Why it moved

- [guess] No segment cuts are in the scorecard, so the mechanism is unknown. The search success rate barely moved: +0.06%.

## Appendix

- Secondary metrics: 52 tested; after a false-discovery correction these moved: Successful Search Rate - Tail Queries (+3.10%). They are exploratory and don't change the call.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

doc_lint: 0 fail, 0 warn, 191 body words (readout)
cold-read: skim 2/2, full 3/3 - pass