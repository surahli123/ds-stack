Decision: Escalate. Successful Search Rate improved but Long Click Rate is undetermined, +0.12% (-0.48% to +0.72%); the test needs every primary to improve.

# Ranker v7: Escalate

Decision: Escalate. Successful Search Rate improved but Long Click Rate is undetermined, +0.12% (-0.48% to +0.72%); the test needs every primary to improve.

Ask: Decide the trade-off at triage.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: pre period could not be checked: no pre-period interval or platform check.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Long Click Rate | primary | +0.12% (-0.48% to +0.72%) | at least 0.50% higher | unclear |
| Successful Search Rate | primary | +0.81% (+0.41% to +1.21%) | at least 0.50% higher | better |
| 4 other guardrails | guardrail | | | all within margin |

Checks: passed: scorecard, sample split, config params, config edits; not run: pre period, novelty.

## What would change the call

- More data showing Long Click Rate up by at least +0.5% would make the second primary clear its bar.
- A pre-period comparison that shows the two arms were alike before exposure would close the one check that could not run.

## Why it moved

- [measured] Successful Search Rate rose +0.81% while Long Click Rate moved only +0.12%, so more searches ended in a click but the scorecard does not show those clicks lasting.
- [guess] The ranker may surface results that get clicked but are abandoned quickly; no segment cuts were read, so the mechanism is not known.

## Appendix

- Secondary metrics: 51 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

0 fail, 0 warn, 209 body words (readout)
cold-read: skim 2/2, full 2/3 - fail

The cold read failed. The reader missed that the pre-period check could not run, and found it unclear how Successful Search Rate can read "better" when the low end of its range (+0.41%) is under the +0.50% bar.