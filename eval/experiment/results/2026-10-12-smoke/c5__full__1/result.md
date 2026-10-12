Decision: Can't tell

# Ranker v7: Can't tell

Decision: Can't tell. The test was edited mid-flight on 2026-09-16 (Allocation changed from 20% to 10%) and the results include days before and after. No launch decision from this data until it's fixed.

Ask: Agree to fix the test and rerun; no launch decision from this data.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: fixing the config edits problem and rerunning.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.81% (+0.41% to +1.21%) | at least 0.50% | better |
| Other guardrails | guardrail | Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User | | within margin |

Checks: config edits fail; pre period could not run; novelty could not run; scorecard pass; sample split pass; config params pass.

## What would change the call

- A re-run, or an analysis limited to days after the 2026-09-16 edit, that shows the lift holds on a stable allocation.
- A daily series by days since first exposure, to check the lift is not fading and the early cohort is not driving it.
- Even then the lower end of the primary interval sits under the 0.5% bar, so a clean result may still only escalate.

## Why it moved

- [guess] No segment cuts or daily series were available, so the mechanism behind the successful-search lift is not known.
- [measured] Allocation was cut in half on 2026-09-16, so results mix users exposed before and after that edit.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

0 fail, 0 warn, 234 body words (readout)
cold-read: skim 2/2, full 3/3 - pass