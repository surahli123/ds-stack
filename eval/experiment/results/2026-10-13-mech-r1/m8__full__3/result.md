# Ranker v7: Ship

Decision: Ship. Queries per User rose 2.60% (+1.70% to +3.50%), which clears the 1.00% bar and every guardrail held.

Ask: Approve the launch to all traffic.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: secondary metric Reformulation Rate got worse after correction.

Triage: Not ready: the scripted call is Ship, but the best explanation of Queries per User is bad news: 'More activity without more success'. Run first: success per query vs per user.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Queries per User | primary | +2.60% (+1.70% to +3.50%) | estimate at least 1.00% higher | better |
| 1 other guardrail | guardrail | | | within margin |

Checks: passed: scorecard, sample split, config params, config edits, novelty; not run: pre period.

## What would change the call

- Registering Successful Search Rate, as the hypothesis states, as the primary: the pre-registration lists Queries per User instead.
- Success per query flat or up with no rise in repeat queries would show the extra queries are healthy.

## Why it moved

- [inferred] Queries per User rose 2.60% and Reformulation Rate rose 5.50%. Searchers retry because first results miss. Successful Search Rate fell 0.45%.
- [guess] Successful Search Rate - Desktop rose 1.52%. Mobile and informational queries did not follow. No cut has been run on this yet.
- [measured] Latency p95 (ms) is flat at +0.20%, so speed does not explain the moves.

## Analyst's view

The analyst would call this Escalate: The hypothesis and config name Successful Search Rate as primary, and it fell 0.45% while Reformulation Rate rose 5.50%. More searching with less success can mean worse results.

## Appendix

- Secondary metrics: 55 tested; after a false-discovery correction these moved: Reformulation Rate (+5.50%), Successful Search Rate - Desktop (+1.52%), Autocomplete Acceptance (+0.97%). They are exploratory and don't change the call.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms).
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

# Ranker v7: triage prep

Ready for triage: Not ready: the scripted call is Ship, but the best explanation of Queries per User is bad news: 'More activity without more success'. Run first: success per query vs per user.

Scripted call: Ship. Queries per User rose 2.60% (+1.70% to +3.50%), which clears the 1.00% bar and every guardrail held.

## Before any single metric

- What did you change? ranker_model: lambdamart_v6 -> lambdamart_v7; nothing else differs between arms.
- Is the data trustworthy? Yes, as far as the checks reach; not checked: pre period.
- Is the effect real, or chance? Queries per User +2.60% (+1.70% to +3.50%); its interval excludes zero. Across the scorecard 8 of 57 metrics moved clearly; about 2.9 would by chance alone.
- Will it last? Probably: effect by days since exposure: first days -0.46%, last days -0.44% (trend +0.002% per day).
- Did the change do what it was built to do? Not shown. If the scorecard or a cut has a coverage metric (the share of queries whose top results changed), register it as feature_metrics.

Metric families used: abandonment = Abandonment Rate, ad_ctr = Ad Click Rate, autocomplete = Autocomplete Acceptance, clicks_per_user = Clicks per User, ctr = CTR, latency = Latency p95 (ms), long_click = Long Click Rate, pagination = Pagination Rate, queries_per_user = Queries per User, reformulation = Reformulation Rate, revenue = Revenue per User, sessions_per_user = Sessions per User, success = Successful Search Rate, time_to_click = Time to First Click (s), zero_result = Zero Result Rate. A wrong pairing here changes every explanation below; fix it in the overlay's metric_families.json.

## Questions triage will ask

1. Why did Queries per User rise? It rose 2.60% (+1.70% to +3.50%). Status: untested.
   - Likely [inferred]: More activity without more success. Users click or search more while success doesn't rise. Published cases read this as attractive results, confusion or users struggling, not engagement, until a cut shows otherwise.
     Evidence: Successful Search Rate fell 0.45% (-0.85% to -0.05%); Queries per User rose 2.60% (+1.70% to +3.50%); Reformulation Rate rose 5.50% (+4.70% to +6.30%).
     To check: cut 1, 2 below.
   - Likely [inferred]: More searching because results got worse. Users search more because they retry: reformulations rise and success doesn't, so higher query volume is a cost, not engagement. A worse ranker can raise queries and even sessions per user for days before engagement falls.
     Evidence: Queries per User rose 2.60% (+1.70% to +3.50%); Reformulation Rate rose 5.50% (+4.70% to +6.30%); Successful Search Rate fell 0.45% (-0.85% to -0.05%).
     To check: cut 1, 2 below.

2. Why did Reformulation Rate rise? It rose 5.50% (+4.70% to +6.30%). Status: untested.
   - Likely: More activity without more success, as in question 1.
   - Likely: More searching because results got worse, as in question 1.

3. Why did Successful Search Rate - Desktop rise? It rose 1.52% (+0.60% to +2.44%). Status: no candidate in the library.
   - No candidate explanation. Say so in the meeting: 'unexplained, possibly chance' is an allowed answer.

4. Why did Autocomplete Acceptance rise? It rose 0.97% (+0.37% to +1.57%). Status: no candidate in the library.
   - No candidate explanation. Say so in the meeting: 'unexplained, possibly chance' is an allowed answer.

## Cuts to run before triage, in order

1. Success per query vs per user (tests: More activity without more success). Supports it: success per query falls or holds while activity grows. Against it: success per query rises with activity. Scored by script once its result is in evidence.json.
2. A similar query issued again within 5 minutes, by arm (tests: More searching because results got worse). Supports it: quick similar re-queries rise in treatment. Against it: re-queries are flat, so the extra queries are new needs. Scored by script once its result is in evidence.json.
3. Queries per User on triggered queries (where the ranking changed) vs untriggered (tests: The registered hypothesis). Supports it: a larger effect where the ranking changed. Against it: the same effect on untouched queries. Record its outcome in evidence.json under cuts.
4. Sessions per user vs queries per session, by arm (tests: More activity without more success). Supports it: more queries inside the same sessions (retrying). Against it: more sessions (coming back). Record its outcome in evidence.json under cuts.
5. Navigational share of queries by arm, week by week (tests: More searching because results got worse). Supports it: treatment users drift toward easy navigational queries (giving up on hard ones). Against it: the query mix is stable. Scored by script once its result is in evidence.json.

Explanations become confirmed only when a cut's result is passed back to explain.py with --evidence; a cut that contradicts a candidate removes it.

## Sources

- More activity without more success: Kohavi et al., KDD 2012; Song, Shi, Fu, WWW 2013; Dmitriev et al., A Dirty Dozen, KDD 2017 (5.12, clicks up from confusion).
- More searching because results got worse: Kohavi et al., Five Puzzling Outcomes, KDD 2012 (a ranking bug raised queries per user 10% and revenue 30%); Song, Shi, Fu, WWW 2013 (a worse ranker raised sessions per user for days); Hassan et al., CIKM 2013 (re-query within 5 minutes).

0 fail, 0 warn, 258 body words (readout)
cold-read: skim 1/2, full 3/3 - fail

The cold read failed: a skim of the readout recovered the launch ask but not the full "Ship: Queries per User rose 2.60%…" answer.

Ready for triage: Not ready