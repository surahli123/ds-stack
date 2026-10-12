Decision: Keep running. Successful Search Rate rose 0.81% (+0.41% to +1.21%) overall, but the effect is fading with each day users have had it.

Ask: Approve running the test longer.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: the remaining data; the call is made at the planned sample.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.81% (+0.41% to +1.21%) | at least 0.50% higher | better |
| 4 other guardrails | guardrail | | | all within margin |

Checks: novelty flag; passed: scorecard, sample split, config params, config edits; not run: pre period.

## What would change the call

- If the gain by days since exposure levels off above the 0.5% bar once the planned 14 days are in, the call becomes a win.
- If the gain keeps falling below the 0.5% bar through the planned 14 days, the call becomes a trade-off for triage.
- A before-start comparison of the two groups would let the pre-period check run.

## Why it moved

- [measured] The Successful Search Rate gain shrinks the longer users have had the new ranker, by about 0.1 points per day since exposure.
- [guess] Early users may react to a changed result order, and the gain settles lower as that wears off.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

0 fail, 0 warn, 205 body words (readout)
cold-read: skim 2/2, full 1/3 - fail

The cold read failed. A fresh reader missed two takeaways: that the effect is fading, and that the call is made at the planned sample. The readout's Status line (day 14 of 14, above the planned sample) also sits oddly with "Keep running", so a reviewer may ask why more days are needed. I didn't edit the rendered readout. I dropped its `# Ranker v7: Keep running` title so the file starts with the required Decision line.