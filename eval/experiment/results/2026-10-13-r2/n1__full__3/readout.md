# Ranker v7: No effect found

Decision: No effect found. Successful Search Rate reads +0.04% (-0.26% to +0.34%), which rules out the 0.50% change the test was built to find.

Ask: Agree to stop the test without launching.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: pre period could not be checked: no pre-period interval or platform check.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.04% (-0.26% to +0.34%) | at least 0.50% higher | unclear |
| 4 other guardrails | guardrail | | | all within margin |

Checks: passed: scorecard, sample split, config params, config edits; not run: pre period, novelty.

## What would change the call

- A rerun with a different ranker change that targets a larger gain than 0.50% in Successful Search Rate.
- A pre-exposure comparison or a daily series by days since first exposure; both could not run here and would only matter if they showed a problem with the data.
- A registered revenue target for this test, since Revenue per User is only a guardrail now.

## Why it moved

- [measured] Successful Search Rate is flat at +0.04%, and no guardrail is past its margin.
- [measured] Revenue per User rose +3.1% with no matching gain in search success, so the revenue lift is not explained by better results.
- [guess] The mechanism behind the revenue rise is unknown; no segment cuts were read.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
