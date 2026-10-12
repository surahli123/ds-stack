Decision: Escalate

Ranker v7 raised Successful Search Rate by 0.31% (+0.13% to +0.49%). That is a real gain, but it falls short of the 0.50% bar the team pre-registered.

Ask: Decide the trade-off at triage.

Status: day 14 of 14, 1,000,000 users per arm (900,000 planned), whole weeks.

Could reverse it: the pre-period check could not run, because the export has no pre-period interval or platform check.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.31% (+0.13% to +0.49%) | at least 0.50% higher | better, below the bar |
| 4 other guardrails | guardrail | | | all within margin |

Checks: passed: scorecard, sample split, config params, config edits; not run: pre period, novelty.

## What would change the call

- A pre-exposure comparison showing the arms were balanced would clear the one check that could not run.
- The team accepting a bar of 0.31% or lower would clear the primary, since no guardrail is past its margin.
- A longer run that moves the estimate to 0.50% or more would clear the bar.

## Why it moved

- [measured] The only config change between arms is the ranker model, so the lift in Successful Search Rate of 0.31% comes from the new ranker.
- [guess] No segment cuts are in the scorecard, so which queries gain is not known.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

Lint: 0 fail, 0 warn, 198 body words (readout)
Cold read: skim 2/2, full 3/3 - pass

I moved the Decision line to the top because you asked for it as the first line. The rendered file opens with a title line, so this reply differs from it there.