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

- Abandonment Rate back inside its 1.00% margin on a rerun, for example after a fix to head-query ranking, would reopen the call.
- A registered explanation that the Abandonment Rate definition changed between arms would send this to triage.

## Why it moved

- [measured] Successful Search Rate rose 1.24% and CTR rose 1.90%, while Abandonment Rate rose 2.20%: more searches get a click, but more also end with none.
- [inferred] Abandonment Rate rose 1.55% on head queries and fell 0.38% on tail queries; the tail drop is too small to trust, so the harm may sit in head queries.
- [guess] Why the new ranker lifts clicks yet also lifts abandonment is unknown; no per-query data was provided.

## Appendix

- Secondary metrics: 52 tested; after a false-discovery correction these moved: CTR (+1.90%), Clicks per User (+2.10%). They are exploratory and don't change the call.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
