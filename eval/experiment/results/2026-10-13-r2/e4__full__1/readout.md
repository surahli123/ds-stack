# Ranker v7: Escalate

Decision: Escalate. Successful Search Rate rose 0.39% (+0.27% to +0.51%), a real change in the good direction but short of the 0.50% bar.

Ask: Decide the trade-off at triage.

Status: day 14 of 14, 1,000,000 users per arm, whole weeks.

Could reverse it: the primary is measured on triggered traffic, so its users aren't compared with the planned total.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.39% (+0.27% to +0.51%) overall | at least 0.50% higher | better, below the bar |
| 4 other guardrails | guardrail | | | all within margin |

Checks: passed: scorecard, sample split, config params, config edits; not run: pre period, novelty.

## What would change the call

- A team decision that an overall lift of 0.39% is worth taking would settle the trade-off at triage.
- A pre-exposure comparison and a daily series by days since first exposure would show whether the lift holds steady; a fading lift would lower the case.

## Why it moved

- [guess] The mechanism is unknown: the scorecard has no segment cuts, so we can't say which queries gained.
- [measured] On triggered searches the rate rose 1.9%; triggered searches carry 20.5% of control successes, so the overall lift is 0.39%.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Successful Search Rate is measured on triggered traffic (+1.90%); the call uses the overall change, scaled by its 20.5% share of the control total.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Fallback: the primary is measured on triggered traffic, so its users aren't compared with the planned total.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
