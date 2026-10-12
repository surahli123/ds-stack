Decision: Don't ship

The abandonment guardrail is breached. Abandonment Rate rose +2.20% (+1.50% to +2.90%), and the pre-registered margin is no worse than 1.00%.

Ask: Agree not to launch. The owner decides whether to iterate.

Status: day 14 of 14, 1,000,000 users per arm (planned 900,000), whole weeks.

Could reverse it: only a version that keeps Abandonment Rate no worse than 1.00%.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Abandonment Rate | guardrail | +2.20% (+1.50% to +2.90%) | no worse than 1.00% | past its margin |
| Successful Search Rate | primary | +1.24% (+0.84% to +1.64%) | at least 0.50% | better |
| Other guardrails | guardrail | Latency p95 (ms), Zero Result Rate, Revenue per User | | within margin |

Checks: pre-period could not run; novelty could not run; scorecard, sample split, config params and config edits all passed.

## What would change the call

- A team-confirmed definition showing Abandonment Rate is not a harm for this ranker, for example because it counts searches answered on the results page.
- A follow-up on head queries that brings the Abandonment Rate increase inside its 1.00% margin.
- A pre-exposure comparison and a daily series by days since first exposure. Both checks could not run here.

## Why it moved

- [measured] Successful Search Rate rose 1.24%, and clicks per user rose 2.1%, so more searches end in a click.
- [measured] Abandonment Rate rose 2.20% at the same time. The segment cuts are too noisy to say where it comes from, though head queries are the only cut clearly up (+1.55%).
- [guess] Both can be true if the new ranker draws more clicks but leaves a separate set of searches with no click at all. The mechanism is not known.

## Appendix

- Secondary metrics: 52 tested. After a false-discovery correction, CTR (+1.90%) and Clicks per User (+2.10%) moved. They are exploratory and don't change the call.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

Lint: 0 fail, 0 warn, 265 body words (readout)
Cold-read: skim 1/2, full 3/3 - fail

The cold read failed on the skim. A fresh reader didn't recover the reason for the call, only that the launch should not go ahead. The reader also said the readout doesn't state whether changes are relative or absolute. I changed one thing from the rendered file: I replaced its `# title` heading with your required first line, so the cold read ran on the unedited rendering. The full set of metrics is in `all_metrics.md`.