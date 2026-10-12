Decision: Escalate

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

- The owner confirming the 0.50% bar is meant overall, not on triggered searches, would make the 1.9% triggered lift clear it.
- A pre-exposure comparison and a daily series by days since first exposure would let the two unrun checks run.

## Why it moved

- [measured] Successful Search Rate rose 1.9% on triggered searches, which are 20.5% of control successes, so overall it rose 0.39%.
- [guess] The scorecard has no segment cuts, so the mechanism behind the gain is unknown.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Successful Search Rate is measured on triggered traffic (+1.90%); the call uses the overall change, scaled by its 20.5% share of the control total.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Fallback: the primary is measured on triggered traffic, so its users aren't compared with the planned total.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

0 fail, 0 warn, 181 body words (readout)
cold-read: skim 1/2, full 3/3 - fail

The cold read failed on the skim: a fresh reader recovered the ask but not the headline answer.