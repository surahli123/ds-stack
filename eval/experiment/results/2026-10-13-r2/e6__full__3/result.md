Decision: Ship. Queries per User rose 2.40% (+1.50% to +3.30%), which clears the 1.00% bar and every guardrail held.

Ask: Approve the launch to all traffic.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: secondary metric Reformulation Rate got worse after correction.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Queries per User | primary | +2.40% (+1.50% to +3.30%) | at least 1.00% higher | better |
| 1 other guardrail | guardrail | | | within margin |

Checks: passed: scorecard, sample split, config params, config edits; not run: pre period, novelty.

## What would change the call

- A pre-exposure comparison on Queries per User would fill the check that could not run.
- A daily series by days since first exposure would show whether the lift is fading.
- The owner confirming Queries per User, not Successful Search Rate, as the primary would settle which bar applies.

## Why it moved

- [measured] Queries per User rose 2.4% while Reformulation Rate rose 5.1% and Successful Search Rate moved -0.35%.
- [inferred] Users may be searching again because the first results miss, which would raise query volume without better results.
- [guess] No segment cuts were read, so which queries drive the rise is not known.

## Analyst's view

The analyst would call this Escalate: The config hypothesis is more successful searches, but the registered primary is query volume. Queries rose while reformulations rose and successful searches did not improve, which can mean worse results, not more engagement.

## Appendix

- Secondary metrics: 55 tested; after a false-discovery correction these moved: Reformulation Rate (+5.10%), Ad Click Rate (-1.98%). They are exploratory and don't change the call.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms).
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

0 fail, 0 warn, 233 body words (readout)
cold-read: skim 2/2, full 3/3 - pass