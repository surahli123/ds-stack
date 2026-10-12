Decision: Don't ship. Successful Search Rate fell 0.62% (-1.02% to -0.22%), the wrong way.

Ask: Agree not to launch; the owner decides whether to iterate.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: only a version where Successful Search Rate improves.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | -0.62% (-1.02% to -0.22%) | at least 0.50% higher | worse |
| 4 other guardrails | guardrail | | | all within margin |

Checks: passed: scorecard, sample split, config params, config edits; not run: pre period, novelty.

## What would change the call

- A rerun showing the primary at or above the 0.5% bar, with the guardrails still within margin.
- A corrected export, if the primary's metric definition changed mid-test, would void this read.
- A pre-exposure comparison of the primary showing the arms already differed before exposure.

## Why it moved

- [measured] Successful Search Rate fell 0.62% overall, and the segment cuts do not isolate where: Desktop fell 0.37% while Mobile rose 0.44%.
- [inferred] CTR also fell 0.36%, which fits fewer searches ending in a successful click.
- [guess] The mechanism is unknown: the new ranker model is the only config change, and nothing here shows which results got worse.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

0 fail, 0 warn, 197 body words (readout)
cold-read: skim 2/2, full 3/3 - pass