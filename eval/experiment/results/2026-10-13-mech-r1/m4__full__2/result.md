# Ranker v7: No effect found

Decision: No effect found. Successful Search Rate reads -0.10% (-0.40% to +0.20%), which rules out the 0.50% change the test was built to find.

Ask: Agree to stop the test without launching.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: secondary metric CTR got worse after correction.

Triage: Ready: every movement triage will ask about has a candidate explanation and none conflict; the explanations are inferred from co-movements, so the cuts below would confirm them.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | -0.10% (-0.40% to +0.20%) | estimate at least 0.50% higher | unclear |
| 2 other guardrails | guardrail | | | all within margin |

Checks: passed: scorecard, sample split, config params, config edits, novelty; not run: pre period.

## What would change the call

- A cut on queries that had zero results in control showing a clear success gain would mean the ranker helps hard queries and the flat total hides it.
- A pre-exposure comparison of Successful Search Rate showing no gap between arms would close the one check that could not run.

## Why it moved

- [measured] Successful Search Rate did not move (-0.10%, -0.40% to +0.20%), and it was just as flat in the last days as in the first, so this is not a novelty effect.
- [inferred] Zero Result Rate fell 12.00% and CTR fell 1.80%. The likely link is that queries that used to return nothing now return weak results, which pulls the CTR average down without helping success.
- [guess] Nothing else on the scorecard moved beyond what chance would produce, so no other story is needed.

## Appendix

- Secondary metrics: 54 tested; after a false-discovery correction these moved: CTR (-1.80%), Zero Result Rate (-12.00%). They are exploratory and don't change the call.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

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

doc_lint: 0 fail, 0 warn, 263 body words (readout)
cold-read: skim 2/2, full 3/3 - pass

My view, separate from the script's output: the script says "Ready", but both explanations for the secondary moves (CTR down, Zero Result Rate down) are inferred and no cut has been run. The pre-period check also could not run. I would tell the engineer to run the two cuts above before the meeting. If they can't, they should say the CTR and zero-result story is still a hypothesis.

Ready for triage: Ready, with open questions