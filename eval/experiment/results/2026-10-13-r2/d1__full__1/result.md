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

- A test run with the latency cost brought under 2.00% (model distillation or caching) while Successful Search Rate keeps its gain.
- A written, owner-signed waiver of the 2.00% latency margin, with the trade-off accepted, would move this to the triage meeting.
- A pre-period comparison and a daily series by days since first exposure would let the two checks that could not run be completed.

## Why it moved

- [measured] Successful Search Rate rose 0.81%, past the 0.50% bar, so the new ranker does help searches end in a good click.
- [inferred] Latency p95 rose 3.10%, against a 2.00% margin; a heavier lambdamart_v7 model scoring each query is the likely cause.
- [guess] The scorecard has no segment cuts, so which queries got slower is unknown.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

doc_lint: 0 fail, 0 warn, 241 body words (readout)
cold-read: skim 2/2, full 3/3 - pass