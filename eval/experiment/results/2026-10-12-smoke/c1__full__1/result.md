# Ranker v7: Can't tell

Decision: Can't tell. The arms got 50.5% / 49.5% of exposures against a planned 50.0% / 50.0%, a gap chance almost never produces at this size. No launch decision from this data until it's fixed.

Ask: Agree to fix the test and rerun; no launch decision from this data.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: fixing the sample split problem and rerunning.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.81% (+0.41% to +1.21%) | at least 0.50% | better |
| Other guardrails | guardrail | Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User | | within margin |

Checks: sample split fail; pre period could not run; novelty could not run; scorecard pass; config params pass; config edits pass.

## What would change the call

- A logged cause for the uneven split, for example a bot filter or a logging bug in one arm, confirmed by the owner.
- A rerun or corrected exposure data with an even split, where the primary still clears its bar.

## Why it moved

- [guess] No segment cuts are in the scorecard, so why successful searches rose is not known.
- [inferred] The uneven split may mean one arm lost or gained users unevenly, which could bias the lift in either direction.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

0 fail, 0 warn, 208 body words (readout)
cold-read: skim 2/2, full 3/3 - pass