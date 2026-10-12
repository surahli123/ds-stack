Decision: Can't tell. The arms got 50.5% / 49.5% of exposures against a planned 50.0% / 50.0%, a gap chance almost never produces at this size. No launch decision from this data until it's fixed.

Ask: Agree to fix the test and rerun; no launch decision from this data.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: fixing the sample split problem and rerunning.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.81% (+0.41% to +1.21%) | at least 0.50% higher | better |
| 4 other guardrails | guardrail | | | all within margin |

Checks: sample split fail; passed: scorecard, config params, config edits; not run: pre period, novelty.

## What would change the call

- Find why the arms got an uneven share of exposures (assignment bug, bot filtering, or logging loss in one arm), fix it and re-export the scorecard.
- Once the split is even, the primary's +0.81% against the 0.5% bar would be read again and could clear.
- Add a pre-exposure comparison and a daily series by days since first exposure so the two checks that could not run can run.

## Why it moved

- [guess] The mechanism is unknown: no segment cuts were read, and the uneven split means the arms may not be comparable.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

0 fail, 0 warn, 206 body words (readout)
cold-read: skim 2/2, full 3/3 - pass

The cold reader flagged two spots: the table says "better" for the primary while the headline says "Can't tell", and the +0.81% is not labelled relative or absolute.