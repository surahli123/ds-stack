Decision: No effect found

Successful Search Rate reads +0.04% (-0.26% to +0.34%), which rules out the 0.50% change the test was built to find.

Ask: Agree to stop the test without launching.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: pre period could not be checked: no pre-period interval or platform check.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.04% (-0.26% to +0.34%) | at least 0.50% | unclear |
| Other guardrails | guardrail | Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User | | within margin |

Checks: pre period could not run; novelty could not run; scorecard pass; sample split pass; config params pass; config edits pass.

## What would change the call

- A pre-exposure comparison for Successful Search Rate: the pre-period check could not run, so a pre-test imbalance is not ruled out.
- A repeat test that targets a smaller lift than 0.50% would need a new pre-registered bar and a larger sample.
- A segment cut or follow-up showing the Revenue per User gain is real and tied to the ranker would justify a separate revenue hypothesis.

## Why it moved

- [measured] Successful Search Rate is flat at +0.04%, and the click metrics in the appendix are flat too, so the new ranker did not change how often searches succeed.
- [guess] Revenue per User rose +3.1% while the primary stayed flat. No segment cuts were read, so the cause is unknown.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

0 fail, 0 warn, 236 body words (readout)
cold-read: skim 2/2, full 3/3 - pass