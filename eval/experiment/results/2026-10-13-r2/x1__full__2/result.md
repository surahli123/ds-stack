Decision: Not an A/B test

This is an interleaving test, so the A/B launch rule doesn't apply. The readout is not a ship or don't-ship call.

Ask: Use the readout for this test design instead.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: nothing here; this design needs its own readout.

Checks: passed: scorecard, sample split, config params, config edits; not run: pre period, novelty.

## What would change the call

- The interleaving analysis, with its own preference metric, would give the call for this design.
- A rerun as a plain A/B test, with v6 and v7 served to separate users, would let the A/B rule apply.

## Why it moved

- [guess] The mechanism is unknown: the scorecard has no segment cuts, and the test arm mixes v6 and v7 results in one list.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

```
0 fail, 0 warn, 131 body words (readout)
got    skim answer     key: Not an A/B test: This is a interleaving test; the A/B launch rule does
got    skim decision   key: Use the readout for this test design instead.
got    full takeaway 1 key: Interleaving
got    full takeaway 2 key: Use the readout for this test design instead.
MISSED full takeaway 3 key: Could reverse it: nothing here; this design needs its own readout.
reader got lost: I had to reread the "Decision" and "Could reverse it" lines. "Could reverse it: nothing here; this design needs its own readout" doesn't clearly say whether the change can be rolled back. I was also confused by "1,000,000 users per arm" alongside "interleaving." In interleaving, each user usually sees both rankers, so an arm split is unclear. The "test arm mixes v6 and v7 results" line adds to the confusion.
cold-read: skim 2/2, full 2/3 - fail
```

The cold read failed: the reader missed the "Could reverse it" takeaway. I didn't edit the rendered text, because the spine and rendered lines are fixed.

I moved the reason onto its own line so the first line is exactly the Decision line. I also left out the rendered title.