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

- A team decision that a 1.20% latency rise is acceptable for the 0.81% success lift would clear it to go out.
- A pre-exposure comparison and a day-by-day effect series would settle the two checks that could not run; a fading effect would mean more data is needed.
- Latency p95 rising past its 2.00% margin on more data would block it.

## Why it moved

- [inferred] Users may need fewer clicks to succeed, since CTR fell (-0.71%).
- [inferred] Latency p95 rose 1.20%, which fits a heavier ranking model scoring more candidates per query.
- [guess] No segment cut of Successful Search Rate (mobile, desktop, head, tail) stands apart, so which queries drive the lift is unknown.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
