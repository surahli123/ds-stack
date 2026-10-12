# Ranker v7: Ship

Decision: Ship. Successful Search Rate rose 0.81% (+0.41% to +1.21%), which clears the 0.50% bar and every guardrail held.

Ask: Approve the launch to all traffic.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: pre period could not be checked: no pre-period interval or platform check.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.81% (+0.41% to +1.21%) | at least 0.50% higher | better |
| 4 other guardrails | guardrail | | | all within margin |

Checks: passed: scorecard, sample split, config params, config edits, novelty; not run: pre period.

## What would change the call

- A pre-exposure comparison showing the two groups already differed on Successful Search Rate would make the test unreliable, because that check could not run.
- A guardrail moving past its margin in a longer read or a post-release holdout would reverse the call.

## Why it moved

- [measured] The effect held steady from the first days after exposure (+0.81%) to the last days (+0.80%), so it is not a novelty bump.
- [guess] Mechanism is unknown: the scorecard has no segment cuts, so we cannot say which queries the new ranker helps.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

0 fail, 0 warn, 186 body words (readout)
cold-read: skim 2/2, full 2/3 - fail

The cold read failed. The reader noticed that only the point estimate clears the 0.50% bar. The lower end of the interval (+0.41%) is below it, which the team's registered rule (`point_at_bar`) allows. The reader also saw the missing pre-period check mentioned twice.