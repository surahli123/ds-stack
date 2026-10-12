Decision: Don't ship. Latency p95 (ms) rose 3.10% (+2.50% to +3.70%), the wrong way and past its 2.00% margin.

# Ranker v7: Don't ship

Ask: Agree not to launch; the owner decides whether to iterate.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: only a version that keeps Latency p95 (ms) at at most 2.00% higher.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Latency p95 (ms) | guardrail | +3.10% (+2.50% to +3.70%) | at most 2.00% higher | past its margin |
| Successful Search Rate | primary | +0.81% (+0.41% to +1.21%) | at least 0.50% higher | better |
| 3 other guardrails | guardrail | | | all within margin |

Checks: passed: scorecard, sample split, config params, config edits; not run: pre period, novelty.

## What would change the call

- Only a new version that keeps Latency p95 (ms) at most 2.00% higher while Successful Search Rate stays at least 0.50% higher.
- The team confirming a slower p95 is acceptable for this lift, which changes the registered margin and needs the owner's sign-off.
- A pre-exposure comparison and a daily series by days since first exposure, so the two checks that could not run can run.

## Why it moved

- [measured] Successful Search Rate rose 0.81% and Latency p95 (ms) rose 3.10% in the same arm.
- [guess] The v7 model is likely heavier to score, which would explain the slower responses alongside better results.
- [guess] No segment cuts were in the scorecard, so which queries or regions drive the latency rise is not known.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

Lint: 0 fail, 0 warn, 239 body words (readout)
Cold read: skim 2/2, full 3/3 - pass (on the third run). The first run missed one full-read takeaway. The second missed the skim answer. Both runs were of the same readout apart from one reworded "what would change" bullet.