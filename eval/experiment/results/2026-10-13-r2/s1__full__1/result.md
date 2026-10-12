Decision: Ship

# Ranker v7

Successful Search Rate rose 0.81% (+0.41% to +1.21%), which clears the 0.50% bar, and every guardrail held.

Ask: Approve the launch to all traffic.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: pre period could not be checked: no pre-period interval or platform check.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.81% (+0.41% to +1.21%) | at least 0.50% higher | better |
| 4 other guardrails | guardrail | | | all within margin |

Checks: passed: scorecard, sample split, config params, config edits; not run: pre period, novelty.

## What would change the call

- The pre period could not be checked; a pre-exposure comparison showing the arms already differed on Successful Search Rate would void the lift.
- A daily series by days since first exposure showing the effect fading would mean the lift is a novelty effect, since the novelty check could not run.
- Reformulation Rate still rising on informational queries in a longer run would show that some of the gain is users searching again.

## Why it moved

- [measured] Successful Search Rate rose 0.81% overall, but no single segment (device or query type) shows a clear gain on its own; the lift is spread thinly.
- [inferred] Reformulation Rate rose 0.96%, mostly on informational queries (+1.70%), so some users may be re-searching after the new ranker's first page.
- [guess] The mechanism behind the lift is unknown; the new ranker model is the only config difference.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

doc_lint: 0 fail, 0 warn, 238 body words (readout)
cold-read: skim 2/2, full 2/3 - fail

The cold read failed on takeaway 3: a fresh reader did not recover that the pre-period check could not run. I reworded the notes once and it still missed. I did not edit the spine.

I replaced the rendered title and first line with your exact `Decision: Ship` line. The full `readout.md` is in the working directory.