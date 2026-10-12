# Ranker v7: Don't ship

Decision: Don't ship. Abandonment Rate rose 2.20% (+1.50% to +2.90%), the wrong way and past its 1.00% margin.

Ask: Agree not to launch; the owner decides whether to iterate.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: only a version that keeps Abandonment Rate at at most 1.00% higher.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Abandonment Rate | guardrail | +2.20% (+1.50% to +2.90%) | at most 1.00% higher | past its margin |
| Successful Search Rate | primary | +1.24% (+0.84% to +1.64%) | at least 0.50% higher | better |
| 3 other guardrails | guardrail | | | all within margin |

Checks: passed: scorecard, sample split, config params, config edits; not run: pre period, novelty.

## What would change the call

- A rerun or a pre-registered explanation showing the abandonment rise comes from a logging change rather than users leaving, which would bring Abandonment Rate back inside its 1.00% margin.
- A ranker tweak that cuts Abandonment Rate to within 1.00% of control while keeping Successful Search Rate above its 0.50% bar.
- A pre-period comparison and a by-exposure-day series, which the export lacks, would show whether the result holds up, though they cannot undo the breach.

## Why it moved

- [measured] Successful Search Rate rose 1.24% and Abandonment Rate rose 2.20%: more searches end in a good click, but more also end with no click at all.
- [measured] Only the head-query cut shows abandonment clearly up (+1.55%); mobile, desktop and tail cuts show no clear change either way.
- [guess] The new ranker may favor results that get clicked when people click, while pushing some head queries toward answers they skip. The scorecard cannot confirm this.

## Appendix

- Secondary metrics: 52 tested; after a false-discovery correction these moved: CTR (+1.90%), Clicks per User (+2.10%). They are exploratory and don't change the call.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

0 fail, 0 warn, 266 body words (readout)
cold-read: skim 2/2, full 3/3 - pass