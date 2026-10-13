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

# Ranker v7: triage prep

Ready for triage: Ready: every movement triage will ask about has a candidate explanation and none conflict; the explanations are inferred from co-movements, so the cuts below would confirm them.

Scripted call: No effect found. Successful Search Rate reads +0.02% (-0.28% to +0.32%), which rules out the 0.50% change the test was built to find.

## Before any single metric

- What did you change? ranker_model: lambdamart_v6 -> lambdamart_v7; nothing else differs between arms.
- Is the data trustworthy? Yes, as far as the checks reach; not checked: pre period.
- Is the effect real, or chance? Successful Search Rate +0.02% (-0.28% to +0.32%); its interval includes zero. Across the scorecard 1 of 57 metrics moved clearly; about 2.9 would by chance alone.
- Will it last? Probably: effect by days since exposure: first days +0.01%, last days +0.03% (trend +0.002% per day).
- Did the change do what it was built to do? Not shown. If the scorecard or a cut has a coverage metric (the share of queries whose top results changed), register it as feature_metrics.

Metric families used: abandonment = Abandonment Rate, ad_ctr = Ad Click Rate, autocomplete = Autocomplete Acceptance, clicks_per_user = Clicks per User, ctr = CTR, latency = Latency p95 (ms), long_click = Long Click Rate, pagination = Pagination Rate, queries_per_user = Queries per User, reformulation = Reformulation Rate, revenue = Revenue per User, sessions_per_user = Sessions per User, success = Successful Search Rate, time_to_click = Time to First Click (s), zero_result = Zero Result Rate. A wrong pairing here changes every explanation below; fix it in the overlay's metric_families.json.

## Questions triage will ask

1. Successful Search Rate was expected to rise but didn't move. Why? It didn't move clearly (+0.02% (-0.28% to +0.32%)). Status: answered by the call: the interval rules out the bar.

## Cuts to run before triage, in order

- Nothing to run.

Explanations become confirmed only when a cut's result is passed back to explain.py with --evidence; a cut that contradicts a candidate removes it.

doc_lint: 0 fail, 0 warn, 265 body words (readout)
cold-read: skim 2/2, full 3/3 - pass

Analyst line, separate from the scripted call: the tool's cut plan is empty, but two cuts are still worth running before the meeting.
- **Pre-exposure comparison of Successful Search Rate.** It is the only check that didn't run. A flat pre-period would support the flat result. A gap would void it.
- **Tail queries, by Successful Search Rate and Abandonment Rate.** Time to First Click on tail queries is the only metric that moved clearly (slower). If success and abandonment are also worse on tail queries, the slowdown is real harm. If they are flat, it is probably luck.

Ready for triage: Ready, with open questions