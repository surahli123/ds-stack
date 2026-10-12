Decision: Ship

# Ranker v7: Ship

Decision: Ship. Successful Search Rate improved +0.81% (+0.41% to +1.21%), which clears the 0.50% bar and every guardrail held.

Ask: Approve the launch to all traffic.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: pre period could not be checked: no pre-period interval or platform check.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.81% (+0.41% to +1.21%) | at least 0.50% | better |
| Other guardrails | guardrail | Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User | | within margin |

Checks: pre period could not run; novelty could not run; scorecard pass; sample split pass; config params pass; config edits pass.

## What would change the call

- A pre-exposure comparison showing the arms already differed on Successful Search Rate would void the lift.
- A daily series by days since first exposure showing the lift fading would move this to Keep running.
- A desktop drop that holds up in a rerun on more traffic would make this an Escalate.

## Why it moved

- [measured] Informational queries gained most on Successful Search Rate (+0.47%); mobile and head queries moved little.
- [measured] Desktop fell -1.29% and navigational -0.77% on the same metric; these are secondary cuts and cannot block.
- [guess] The new model likely reorders results for open-ended queries, where there is more to gain than for lookups.

## Appendix

- Secondary metrics: 52 tested; after a false-discovery correction these moved: Clicks per User (-1.20%), Successful Search Rate - Desktop (-1.29%). They are exploratory and don't change the call.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

0 fail, 0 warn, 219 body words (readout)
cold-read: skim 2/2, full 2/3 - fail

The cold read failed: a fresh reader got stuck on the 0.50% bar, because the lower end of the interval (+0.41%) sits below it. The pre-registration says the point estimate must clear the bar, and I left that as scripted.

One thing the readout doesn't say: the first run returned "Can't tell" because the scorecard check failed. The Pulse `percentChange` fields are fractions, not percents, in all 57 metrics, and the adapter assumed percents. I ran the call on a unit-converted copy, `fixed/pulse.json`. I left the original pulse and the tools unchanged. All outputs are in `fixed/`.