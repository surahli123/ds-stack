# Ranker v7: No effect found

Decision: No effect found. Successful Search Rate reads +0.02% (-0.28% to +0.32%), which rules out the 0.50% change the test was built to find.

Ask: Agree to stop the test without launching.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: no pre-period comparison, so a difference between the arms before the test isn't ruled out.

Triage: Ready: every movement triage will ask about has a candidate explanation and none conflict; the explanations are inferred from co-movements, so the cuts below would confirm them.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.02% (-0.28% to +0.32%) | estimate at least 0.50% higher | unclear |
| 4 other guardrails | guardrail | | | all within margin |

Checks: passed: scorecard, sample split, config params, config edits, novelty; not run: pre period.

## What would change the call

- A pre-exposure comparison of Successful Search Rate showing a gap between arms before exposure would void this result.
- A tail-query cut showing Successful Search Rate or Abandonment Rate worse there would make the tail slowdown a real harm for triage.

## Why it moved

- [measured] Successful Search Rate is flat at +0.02% and the daily series is flat too, so v7 ranks differently but does not change how often searches succeed.
- [inferred] Time to First Click on tail queries is the one clear mover, and it got slower; one mover among this many metrics is what luck alone gives, so treat it as a lead.
- [guess] No coverage metric (share of queries whose top results changed) is on the scorecard, so we can't say whether v7 changed enough results to matter.

## Appendix

- Secondary metrics: 52 tested; none moved after a false-discovery correction.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.
