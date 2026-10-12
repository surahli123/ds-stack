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

- A pre-exposure comparison showing the arms already differed on Successful Search Rate would void this result, since the test would be broken.
- A daily series by days since first exposure showing the lift fading would mean the test needs more time.
- Revenue per User falling past its 1% margin on a longer window would block the release.

## Why it moved

- [measured] Successful Search Rate rose 0.81%; desktop moved +0.84% and mobile +0.07%, but neither cut is clear on its own, so the split is unproven.
- [measured] Ad Click Rate fell 2.8%, an unregistered secondary; Revenue per User held at -0.10%.
- [guess] The mechanism is unknown; the ranker may surface the answer sooner, so fewer ad clicks follow.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
