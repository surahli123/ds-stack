# Ranker v7: Ship

Decision: Ship. Successful Search Rate rose 0.81% (+0.41% to +1.21%), which clears the 0.50% bar and every guardrail held.

Ask: Approve the launch to all traffic.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: secondary metric Queries per User got worse after correction.

Triage: Ready: every movement triage will ask about has a candidate explanation and none conflict; the explanations are inferred from co-movements, so the cuts below would confirm them.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.81% (+0.41% to +1.21%) | estimate at least 0.50% higher | better |
| 4 other guardrails | guardrail | | | all within margin |

Checks: passed: scorecard, sample split, config params, config edits, novelty; not run: pre period.

## What would change the call

- Success on triggered queries (ranking changed) flat or negative, with the Queries per User drop traced to logging or dropped searches, would remove the win.
- The same lift on triggered queries with unchanged search logging would confirm the relevance gain.
- A pre-exposure comparison that shows the arms already differed would make the test unreliable.

## Why it moved

- [inferred] Successful Search Rate rose 0.81% while Queries per User fell 1.9% and Clicks per User stayed flat, so part of the rise may come from fewer searches in the denominator, not better results.
- [inferred] Every device, head/tail and query-type cut of Successful Search Rate is flat or negative, yet the total is up, which points to a mix shift in which searches get counted.
- [inferred] CTR rose 2.1%, in line with the same smaller query count rather than more clicks.

## Analyst's view

The analyst would call this Escalate: The rule sees a primary above its bar, but Queries per User fell 1.9% with flat clicks and no cut of Successful Search Rate is positive, so the lift may be a denominator effect. Run the triggered-queries and search-volume cuts before approving.

## Appendix

- Secondary metrics: 52 tested; after a false-discovery correction these moved: CTR (+2.10%), Queries per User (-1.90%). They are exploratory and don't change the call.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

# Ranker v7: triage prep

Ready for triage: Ready: every movement triage will ask about has a candidate explanation and none conflict; the explanations are inferred from co-movements, so the cuts below would confirm them.

Scripted call: Ship. Successful Search Rate rose 0.81% (+0.41% to +1.21%), which clears the 0.50% bar and every guardrail held.

## Before any single metric

- What did you change? ranker_model: lambdamart_v6 -> lambdamart_v7; nothing else differs between arms.
- Is the data trustworthy? Yes, as far as the checks reach; not checked: pre period.
- Is the effect real, or chance? Successful Search Rate +0.81% (+0.41% to +1.21%); its interval excludes zero. Across the scorecard 6 of 57 metrics moved clearly; about 2.9 would by chance alone.
- Will it last? Probably: effect by days since exposure: first days +0.80%, last days +0.82% (trend +0.002% per day).
- Did the change do what it was built to do? Not shown. If the scorecard or a cut has a coverage metric (the share of queries whose top results changed), register it as feature_metrics.

Metric families used: abandonment = Abandonment Rate, ad_ctr = Ad Click Rate, autocomplete = Autocomplete Acceptance, clicks_per_user = Clicks per User, ctr = CTR, latency = Latency p95 (ms), long_click = Long Click Rate, pagination = Pagination Rate, queries_per_user = Queries per User, reformulation = Reformulation Rate, revenue = Revenue per User, sessions_per_user = Sessions per User, success = Successful Search Rate, time_to_click = Time to First Click (s), zero_result = Zero Result Rate. A wrong pairing here changes every explanation below; fix it in the overlay's metric_families.json.

## Questions triage will ask

1. Why did Successful Search Rate rise? It rose 0.81% (+0.41% to +1.21%). Status: untested.
   - Likely [inferred]: Better results, more satisfied clicks. The ranking puts better results where users look, so more searches end in a satisfying click.
     Evidence: Successful Search Rate rose 0.81% (+0.41% to +1.21%); CTR rose 2.10% (+1.60% to +2.60%); Reformulation Rate didn't move clearly (+0.17% (-0.63% to +0.97%)); Abandonment Rate didn't move clearly (+0.10% (-0.50% to +0.70%)).
     To check: cut 1, 4 below.
   - Likely [inferred]: The registered hypothesis. The new ranker raises the share of searches that end in a successful click.
     Evidence: Successful Search Rate rose 0.81% (+0.41% to +1.21%).
     To check: cut 2 below.

2. Why did CTR rise? It rose 2.10% (+1.60% to +2.60%). Status: confirmed by the scorecard.
   - Confirmed [measured]: A ratio moved because its denominator moved. CTR moved because Queries per User moved (fell 1.90% (-2.60% to -1.20%)), not because Clicks per User changed; the ratio's story is about volume, not quality.
     Evidence: CTR rose 2.10% (+1.60% to +2.60%); Clicks per User didn't move clearly (+0.10% (-0.70% to +0.90%)); Queries per User fell 1.90% (-2.60% to -1.20%); 95% of the split comes from Queries per User.
   - Likely: Better results, more satisfied clicks, as in question 1.

3. Why did Queries per User fall? It fell 1.90% (-2.60% to -1.20%). Status: confirmed by the scorecard.
   - Confirmed: A ratio moved because its denominator moved, as in question 2.

## Ruled out

- More clicks, not more satisfaction: Successful Search Rate rose 0.81% (+0.41% to +1.21%).

## Cuts to run before triage, in order

1. Success on triggered queries only (where the ranking actually changed) vs untriggered (tests: Better results, more satisfied clicks). Supports it: a larger effect on triggered queries, diluted overall. Against it: the same effect on untouched queries, pointing to something other than ranking. Scored by script once its result is in evidence.json.
2. Successful Search Rate on triggered queries (where the ranking changed) vs untriggered (tests: The registered hypothesis). Supports it: a larger effect where the ranking changed. Against it: the same effect on untouched queries. Record its outcome in evidence.json under cuts.
3. Clicks per User and Queries per User per user, side by side (tests: A ratio moved because its denominator moved). Supports it: the denominator carries the change. Against it: the numerator moves too. Record its outcome in evidence.json under cuts.
4. Success by query class and device (tests: Better results, more satisfied clicks). Supports it: the gain is largest where the change acts (for example tail queries for a recall change). Against it: the gain is uniform, which a ranking change rarely produces. Record its outcome in evidence.json under cuts.
5. What changed the Queries per User (query volume, sessions, logging of searches) (tests: A ratio moved because its denominator moved). Supports it: a volume or logging change explains it. Against it: volume is steady. Record its outcome in evidence.json under cuts.

Explanations become confirmed only when a cut's result is passed back to explain.py with --evidence; a cut that contradicts a candidate removes it.

## Sources

- Better results, more satisfied clicks: Kohavi, Tang, Xu 2020, ch. 20 (triggered analysis needs counterfactual logging, and the untriggered complement must look like an A/A).
- A ratio moved because its denominator moved: Dmitriev et al., A Dirty Dozen: Twelve Common Metric Interpretation Pitfalls, KDD 2017 (module CTR -40% while clicks +74% and impressions +200%).

0 fail, 0 warn, 310 body words (readout)
cold-read: skim 2/2, full 2/3 - fail

The cold read failed. A fresh reader missed the "Could reverse it" takeaway.

My view differs from the script's. The script says Ready, but I read it as not ready. The scorecard's own segment rows contradict the headline: Successful Search Rate is flat or negative on mobile, desktop, head, tail and informational queries, and only navigational is slightly positive (not clearly). Yet the total is up 0.81%, while Queries per User fell 1.9% and Clicks per User stayed flat. That looks like a denominator or mix effect, not a relevance gain. I haven't run any cuts, because I have no data access. The pre-period check also didn't run. Cuts 1, 2, 3 and 5 above should run first. Cut 5 matters most, because a logging change behind the Queries per User drop would undo the win.

Ready for triage: Not ready