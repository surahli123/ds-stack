Decision: Escalate

Why: Successful Search Rate improved but Long Click Rate is undetermined, +0.12% (-0.48% to +0.72%); the test needs every primary to improve.

Ask: Decide the trade-off at triage.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: pre period could not be checked: no pre-period interval or platform check.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Long Click Rate | primary | +0.12% (-0.48% to +0.72%) | at least 0.50% | unclear |
| Successful Search Rate | primary | +0.81% (+0.41% to +1.21%) | at least 0.50% | better |
| Other guardrails | guardrail | Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User | | within margin |

Checks: pre period could not run; novelty could not run; scorecard pass; sample split pass; config params pass; config edits pass.

## What would change the call

- If the owners agree Long Click Rate is not required to move, only Successful Search Rate counts and the call becomes Ship.
- A longer run that shows Long Click Rate at or above +0.5% would also make it Ship; one extension would settle that.
- A Long Click Rate interval that sits wholly below +0.5% would make it No effect found.

## Why it moved

- [measured] Successful Search Rate rose +0.81% (+0.41% to +1.21%), above the 0.5% bar. Long Click Rate moved only +0.12% (-0.48% to +0.72%).
- [measured] Segment cuts are too wide to say where the gain sits; no segment shows a clear gain or loss in Long Click Rate.
- [guess] The mechanism is unknown. More searches may end in a click that is not a long one, so the gain may be shallower than hoped.

## Appendix

- Secondary metrics: 51 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

0 fail, 0 warn, 263 body words (readout)
cold-read: skim 2/2, full 3/3 - pass

The readout is saved as `out/readout.md`. I edited it by hand after rendering, to start with the exact `Decision:` line you asked for. The renderer's title line and its "Decision: Escalate. …" line are gone; the reason now sits under "Why:". The lint and cold-read results above are from the edited file.

I used the example team standards from `/home/user/ds-stack-exp/overlay.example/standards.json`, since no overlay was in this directory. The prereg's own bars and margins take precedence, but the example file supplies the sample-split threshold, the minimum run length, and the rule that harm inside a margin escalates. The triage meeting should confirm those.