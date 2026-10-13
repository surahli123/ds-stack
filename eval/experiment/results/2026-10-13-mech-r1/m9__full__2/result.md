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

- A pre-exposure comparison showing the arms differed before the start would mean the test cannot be read.
- A coverage metric showing most queries' top results changed would point to a weak ranker, not a small effect.
- A tail-query cut where slower first clicks come with lower success would make that cut a concern.

## Why it moved

- [measured] Successful Search Rate did not move; the data rules out a change as large as the 0.50% bar.
- [inferred] Only Time to First Click (s) - Tail Queries moved clearly, +2.38%; across the whole scorecard a few metrics would do that by luck, so treat it as exploratory.
- [guess] No reformulation, abandonment, latency or revenue movement offers a competing story; the model may change few top results.

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

Metric families used: abandonment = Abandonment Rate, ad_ctr = Ad Click Rate, autocomplete = Autocomplete Acceptance, clicks_per_user = Clicks per User, ctr = CTR, latency = Latency p95 (ms), long_click = Long Click Rate, pagination = Pagination Rate, queries_per_user = Queries per User, reformulation = Reformulation Rate, revenue = Revenue per User, sessions_per_user = Sessions per User, success = Successful Search Rate, time_to_click = Time to First Click (s), zero_result = Zero Result Rate, A wrong pairing here changes every explanation below; fix it in the overlay's metric_families.json.

## Questions triage will ask

1. Successful Search Rate was expected to rise but didn't move. Why? It didn't move clearly (+0.02% (-0.28% to +0.32%)). Status: answered by the call: the interval rules out the bar.

## Cuts to run before triage, in order

- Nothing to run.

Explanations become confirmed only when a cut's result is passed back to explain.py with --evidence; a cut that contradicts a candidate removes it.

doc_lint: 0 fail, 0 warn, 258 body words (readout)
cold-read: skim 2/2, full 3/3 - pass

Ready for triage: Ready, with open questions

The tool's own verdict is "Ready". I downgraded it to "Ready, with open questions" for three reasons:
- The pre-period check couldn't run.
- No coverage metric is registered, so nothing shows the ranker changed many results.
- The one clear mover, Time to First Click on tail queries (+2.38%), is a secondary that didn't survive correction.

The planned cuts list is empty, but I'd still run two cuts before the meeting. Neither is run yet. A tail-query cut on Successful Search Rate would show whether the slower first clicks come with a drop in success. A coverage cut would show how many queries' top results the new ranker changed.