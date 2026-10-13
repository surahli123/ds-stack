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
