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

- A latency owner accepting the 1.20% rise, or a fix that brings it back near zero, would clear the guardrail concern.
- A rerun with latency past the 2.00% margin would make the harm a breach.
- A pre-exposure comparison and a daily series by days since first exposure would let the two checks that could not run be run.

## Why it moved

- [measured] Successful Search Rate rose 0.81% and Latency p95 rose 1.20% in the same test arm.
- [inferred] A heavier ranking model plausibly costs extra serving time, which would explain the latency rise.
- [guess] No segment cuts were in the scorecard, so why the success rate rose is not known.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

0 fail, 0 warn, 229 body words (readout)
cold-read: skim 1/2, full 1/3 - fail

The cold read failed: the reader couldn't tell whether the 0.50% bar is judged on the point estimate or the interval's lower bound (+0.41%). They also found the "Could reverse it" line unclear.