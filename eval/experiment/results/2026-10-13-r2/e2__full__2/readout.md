# Ranker v7: Escalate

Decision: Escalate. Successful Search Rate rose 0.81% (+0.41% to +1.21%), but Latency p95 (ms) rose 1.20% (+0.70% to +1.70%), the wrong way, though inside its 2.00% margin.

Ask: Decide the trade-off at triage.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: pre period could not be checked: no pre-period interval or platform check.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Latency p95 (ms) | guardrail | +1.20% (+0.70% to +1.70%) | at most 2.00% higher | worse, within margin |
| Successful Search Rate | primary | +0.81% (+0.41% to +1.21%) | at least 0.50% higher | better |
| 3 other guardrails | guardrail | | | all within margin |

Checks: passed: scorecard, sample split, config params, config edits; not run: pre period, novelty.

## What would change the call

- A latency owner accepting a 1.20% slower p95 as within the 2.00% margin would move this to a clear win.
- A latency rise that grows past 2.00% on more data would make it a loss.
- A pre-exposure comparison and a daily series by days since first exposure would let the two unrun checks pass.

## Why it moved

- [measured] Successful Search Rate rose 0.81% and Latency p95 (ms) rose 1.20% in the same arm; no segment cuts are in the scorecard.
- [guess] The slower responses may come from a heavier ranker model, which is the only parameter that differs between arms.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
