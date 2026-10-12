Decision: Ship

# Ranker v7: Ship

Decision: Ship. Successful Search Rate rose 0.81% (+0.41% to +1.21%), which clears the 0.50% bar and every guardrail held.

Ask: Approve the launch to all traffic.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: pre period could not be checked: no pre-period interval or platform check.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.81% (+0.41% to +1.21%) | at least 0.50% higher | better |
| 4 other guardrails | guardrail | | | all within margin |

Checks: passed: scorecard, sample split, config params, config edits; not run: pre period, novelty.

## What would change the call

- A pre-exposure comparison on Successful Search Rate showing the arms already differed before exposure would make the test unreadable.
- A daily series by days since first exposure showing the lift fading toward zero would mean the result needs more time.

## Why it moved

- [measured] Successful Search Rate rose 0.81% overall, but CTR (-0.02%) and Long Click Rate (-0.23%) did not move, so the extra successes are not showing up as more clicks.
- [measured] Reformulation Rate rose 2.42% on navigational queries; this is a secondary cut among many that did not survive correction, so it is a lead, not a finding.
- [guess] The new ranker may help some query types and hurt others, but no segment cut was designed to test this.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction on (changes are adjusted for pre-test behaviour); harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

0 fail, 0 warn, 218 body words (readout)
cold-read: skim 2/2, full 3/3 - pass

The cold-read reader said it got lost on the bar logic. The pre-registration says the point estimate must clear the bar, and the lower end of the interval (+0.41%) sits below it.