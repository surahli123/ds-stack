# Ranker v7: triage prep

Ready for triage: Ready: every movement triage will ask about has a candidate explanation and none conflict; the explanations are inferred from co-movements, so the cuts below would confirm them.

Scripted call: No effect found. Successful Search Rate reads +0.00% (-0.30% to +0.30%), which rules out the 0.50% change the test was built to find.

## Before any single metric

- What did you change? ranker_model: lambdamart_v6 -> lambdamart_v7; nothing else differs between arms.
- Is the data trustworthy? Yes, as far as the checks reach; not checked: pre period.
- Is the effect real, or chance? Successful Search Rate +0.00% (-0.30% to +0.30%); its interval includes zero. Across the scorecard 6 of 57 metrics moved clearly; about 2.9 would by chance alone.
- Will it last? Probably: effect by days since exposure: first days -0.01%, last days +0.01% (trend +0.002% per day).
- Did the change do what it was built to do? Not shown. If the scorecard or a cut has a coverage metric (the share of queries whose top results changed), register it as feature_metrics.

Metric families used: abandonment = Abandonment Rate, ad_ctr = Ad Click Rate, autocomplete = Autocomplete Acceptance, clicks_per_user = Clicks per User, ctr = CTR, latency = Latency p95 (ms), long_click = Long Click Rate, pagination = Pagination Rate, queries_per_user = Queries per User, reformulation = Reformulation Rate, revenue = Revenue per User, sessions_per_user = Sessions per User, success = Successful Search Rate, time_to_click = Time to First Click (s), zero_result = Zero Result Rate. A wrong pairing here changes every explanation below; fix it in the overlay's metric_families.json.

## Questions triage will ask

1. Successful Search Rate was expected to rise but didn't move. Why? It didn't move clearly (+0.00% (-0.30% to +0.30%)). Status: untested.
   - Likely [inferred]: More clicks, not more satisfaction. Results look more clickable (titles, snippets or positions) but satisfy no more often, so CTR rises without long clicks.
     Evidence: CTR rose 2.40% (+1.90% to +2.90%); Long Click Rate didn't move clearly (-0.10% (-0.60% to +0.40%)); Successful Search Rate didn't move clearly (+0.00% (-0.30% to +0.30%)); Clicks per User rose 2.20% (+1.50% to +2.90%).
     To check: cut 1, 3 below.
   - Possible [inferred]: More activity without more success. Users click or search more while success doesn't rise. Published cases read this as attractive results, confusion or users struggling, not engagement, until a cut shows otherwise.
     Evidence: Successful Search Rate didn't move clearly (+0.00% (-0.30% to +0.30%)); Clicks per User rose 2.20% (+1.50% to +2.90%).
     To check: cut 2, 3 below.

2. Why did CTR rise? It rose 2.40% (+1.90% to +2.90%). Status: untested.
   - Likely: More clicks, not more satisfaction, as in question 1.

3. Why did Clicks per User rise? It rose 2.20% (+1.50% to +2.90%). Status: untested.
   - Likely: More clicks, not more satisfaction, as in question 1.
   - Possible: More activity without more success, as in question 1.

## Cuts already run

- Config diff of presentation parameters (titles, snippets, thumbnails): inconclusive 'More clicks, not more satisfaction'. config differs in ranker_model (lambdamart_v6 -> lambdamart_v7).

## Cuts to run before triage, in order

1. SAT clicks (dwell of 30 seconds or more) vs all clicks, by arm (tests: More clicks, not more satisfaction). Supports it: clicks rise but SAT clicks don't. Against it: SAT clicks rise with clicks. Scored by script once its result is in evidence.json.
2. Success per query vs per user (tests: More activity without more success). Supports it: success per query falls or holds while activity grows. Against it: success per query rises with activity. Scored by script once its result is in evidence.json.
3. A similar query issued again within 5 minutes, by arm (tests: More clicks, not more satisfaction). Supports it: quick re-queries rise after clicks. Against it: re-queries are flat. Scored by script once its result is in evidence.json.
4. Sessions per user vs queries per session, by arm (tests: More activity without more success). Supports it: more queries inside the same sessions (retrying). Against it: more sessions (coming back). Record its outcome in evidence.json under cuts.
5. CTR and long-click rate by result position (tests: More clicks, not more satisfaction). Supports it: the CTR gain sits in top positions and comes with short clicks. Against it: long clicks rise wherever CTR rises. Record its outcome in evidence.json under cuts.

Explanations become confirmed only when a cut's result is passed back to explain.py with --evidence; a cut that contradicts a candidate removes it.

## Sources

- More clicks, not more satisfaction: Hassan et al., CIKM 2013 (attractive snippets, SAT clicks at 30 s dwell); Dmitriev et al., A Dirty Dozen: Twelve Common Metric Interpretation Pitfalls, KDD 2017 (clicks shift between page elements).
- More activity without more success: Kohavi et al., KDD 2012; Song, Shi, Fu, WWW 2013; Dmitriev et al., A Dirty Dozen, KDD 2017 (5.12, clicks up from confusion).
