Decision: No effect found

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

- A pre-exposure comparison for Successful Search Rate that shows the arms differed before exposure would make the test broken.
- A daily series by days since first exposure that shows the effect growing late would make a longer run worth it.

## Why it moved

- [measured] The primary barely moved: Successful Search Rate reads +0.04%, against the 0.50% bar.
- [measured] Revenue per User rose +3.10% while search success stayed flat, which the primary does not explain.
- [guess] The scorecard has no segment cuts, so the mechanism behind the flat result is unknown.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

0 fail, 0 warn, 193 body words (readout)
cold-read: skim 1/2, full 3/3 - fail

The cold read failed on the skim: a reader skimming the readout did not recover the key figures (+0.04% and its interval) as the answer.