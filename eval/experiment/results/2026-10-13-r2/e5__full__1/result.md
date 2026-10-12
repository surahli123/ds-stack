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

- More data showing Long Click Rate up by at least +0.5% would mean both primaries clear their bars.
- The owner confirming that Long Click Rate was meant as a primary, since the Statsig config lists only Successful Search Rate, would change the bar the call is made against.
- A pre-period comparison and a daily series by days since first exposure would let the pre-period and novelty checks run; both could not run.

## Why it moved

- [measured] Successful Search Rate rose +0.81% while Long Click Rate stayed flat at +0.12%, so the extra successes were not longer clicks.
- [guess] The new ranker may be getting more searches to a click that counts as a success without lifting satisfied, longer clicks. No segment cuts were provided, so the mechanism is unknown.

## Appendix

- Secondary metrics: 51 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

0 fail, 0 warn, 242 body words (readout)
cold-read: skim 2/2, full 2/3 - fail

The cold read failed: a fresh reader missed the third takeaway, that the pre-period check could not be run.