# Ranker v7: triage prep

Ready for triage: Ready: every movement triage will ask about has a candidate explanation and none conflict; the explanations are inferred from co-movements, so the cuts below would confirm them.

Scripted call: No effect found. Successful Search Rate reads -0.10% (-0.40% to +0.20%), which rules out the 0.50% change the test was built to find.

## Before any single metric

- What did you change? ranker_model: lambdamart_v6 -> lambdamart_v7; nothing else differs between arms.
- Is the data trustworthy? Yes, as far as the checks reach; not checked: pre period.
- Is the effect real, or chance? Successful Search Rate -0.10% (-0.40% to +0.20%); its interval includes zero. Across the scorecard 5 of 57 metrics moved clearly; about 2.9 would by chance alone.
- Will it last? Probably: effect by days since exposure: first days -0.11%, last days -0.09% (trend +0.002% per day).
- Did the change do what it was built to do? Not shown. If the scorecard or a cut has a coverage metric (the share of queries whose top results changed), register it as feature_metrics.

Metric families used: abandonment = Abandonment Rate, ad_ctr = Ad Click Rate, autocomplete = Autocomplete Acceptance, clicks_per_user = Clicks per User, ctr = CTR, latency = Latency p95 (ms), long_click = Long Click Rate, pagination = Pagination Rate, queries_per_user = Queries per User, reformulation = Reformulation Rate, revenue = Revenue per User, sessions_per_user = Sessions per User, success = Successful Search Rate, time_to_click = Time to First Click (s), zero_result = Zero Result Rate. A wrong pairing here changes every explanation below; fix it in the overlay's metric_families.json.

## Questions triage will ask

1. Successful Search Rate was expected to rise but didn't move. Why? It didn't move clearly (-0.10% (-0.40% to +0.20%)). Status: answered by the call: the interval rules out the bar.

2. Why did CTR fall? It fell 1.80% (-2.30% to -1.30%). Status: untested.
   - Likely [inferred]: More results for hard queries, lower precision. The change returns results for queries that used to get none, but those results are weak, so averages over all queries fall.
     Evidence: Zero Result Rate fell 12.00% (-14.00% to -10.00%); CTR fell 1.80% (-2.30% to -1.30%).
     To check: cut 1, 2 below.

3. Why did Zero Result Rate fall? It fell 12.00% (-14.00% to -10.00%). Status: untested.
   - Likely: More results for hard queries, lower precision, as in question 2.

## Cuts to run before triage, in order

1. Success and CTR on queries that had zero results in control (tests: More results for hard queries, lower precision). Supports it: these queries now get results but low success. Against it: they succeed at the normal rate. Record its outcome in evidence.json under cuts.
2. The same metrics excluding those queries (tests: More results for hard queries, lower precision). Supports it: the rest of the traffic is flat. Against it: the drop is broad. Record its outcome in evidence.json under cuts.

Explanations become confirmed only when a cut's result is passed back to explain.py with --evidence; a cut that contradicts a candidate removes it.

## Sources

- More results for hard queries, lower precision: Dmitriev et al., A Dirty Dozen: Twelve Common Metric Interpretation Pitfalls, KDD 2017 (ratio metrics move with their denominator); reasoned, no published case of this exact signature.
