Decision: No effect found

Successful Search Rate reads -0.05% (-0.34% to +0.24%), which rules out the 0.50% change the test was built to find.

Ask: Agree to stop the test without launching.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: pre period could not be checked: no pre-period interval or platform check.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | -0.05% (-0.34% to +0.24%) | at least 0.50% | unclear |
| Other guardrails | guardrail | Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User | | within margin |

Checks: pre period could not run; novelty could not run; scorecard pass; sample split pass; config params pass; config edits pass.

## What would change the call

- A different bar from the owner: the interval reaches +0.24%, so only a bar below that is not ruled out.
- A pre-exposure comparison or daily series by days since exposure showing a problem with the test itself.

## Why it moved

- [guess] Successful Search Rate did not move: -0.05% on 1,000,000 users per arm. No segment cuts are in the scorecard, so the mechanism is unknown.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

Lint: `0 fail, 0 warn, 185 body words (readout)`
Cold read: `cold-read: skim 2/2, full 3/3 - pass`

I changed `readout.md` after rendering. I removed the title heading and split the Decision line from the reason so the file starts with exactly `Decision: No effect found`. I re-ran the lint after that edit (result above). I did not re-run the cold read.

The team standards (`standards.json`) came from the example overlay at `/home/user/ds-stack-exp/overlay.example/`, because no team overlay was in this directory. The prereg gave all four guardrail margins, so only the sample-split threshold and the days-and-escalation rules came from the example.