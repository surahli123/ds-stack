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

- A pre-exposure comparison showing the arms already differed on Successful Search Rate would void this result; the platform did not run one.
- A guardrail moving past its margin on a longer read would reverse it.

## Why it moved

- [measured] The lift held steady across the run: +0.81% in the first days and +0.80% in the last days, so it is not a novelty bump.
- [guess] The mechanism is unknown: the scorecard has no segment cuts, so we can't say which queries gained.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

Lint: 0 fail, 0 warn, 179 body words (readout)
Cold read: skim 2/2, full 3/3 - pass

(The cold-read reader noted that "Could reverse it" reads like a reason to reverse rather than a caveat, and that the guardrail margins aren't given as numbers.)