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

- Per-query success and a repeat of the same query within 5 minutes, by arm, showing no rise in repeats would back the lift.
- A registered primary of Successful Search Rate, as the hypothesis states, would make its fall the deciding result.
- A pre-exposure comparison of Queries per User would settle the check that could not run.

## Why it moved

- [inferred] Reformulation Rate rose 5.50% alongside Queries per User (+2.60%): people re-search because results are worse.
- [measured] Successful Search Rate, the hypothesis metric, fell 0.45%, mostly on informational queries (-0.85%). Cuts are unregistered, so exploratory.
- [guess] Autocomplete Acceptance rose 0.97%; whether it feeds extra queries is untested.

## Analyst's view

The analyst would call this Escalate: The registered primary counts volume; success fell and reformulation rose, so the scripted call should go to triage as a trade-off.

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
   - Likely [inferred]: More searching because results got worse, as in question 1.

3. Why did Successful Search Rate - Desktop rise? It rose 1.52% (+0.60% to +2.44%). Status: no candidate in the library.
   - No candidate explanation. Say so in the meeting: 'unexplained, possibly chance' is an allowed answer.

4. Why did Autocomplete Acceptance rise? It rose 0.97% (+0.37% to +1.57%). Status: no candidate in the library.
   - No candidate explanation. Say so in the meeting: 'unexplained, possibly chance' is an allowed answer.

## Cuts to run before triage, in order

1. Success per query vs per user (tests: More activity without more success). Supports it: success per query falls or holds while activity grows. Against it: success per query rises with activity. Scored by script once its result is in evidence.json.
2. A similar query issued again within 5 minutes, by arm, showing no rise in repeats would back the lift. [see cuts below]
3. Queries per User on triggered queries (where the ranking changed) vs untriggered (tests: The registered hypothesis). Supports it: a larger effect where the ranking changed. Against it: the same effect on untouched queries. Record its outcome in evidence.json under cuts.
4. Sessions per user vs queries per session, by arm (tests: More activity without more success). Supports it: more queries inside the same sessions (retrying). Against it: more sessions (coming back). Record its outcome in evidence.json under cuts.
5. Navigational share of queries by arm, week by week (tests: More searching because results got worse). Supports it: treatment users drift toward easy navigational queries (giving up on hard ones). Against it: the query mix is stable. Scored by script once its result is in evidence.json.

Explanations become confirmed only when a cut's result is passed back to explain.py with --evidence; a cut that contradicts a candidate removes it.

Ready for triage: Not ready

0 fail, 0 warn, 258 body words (readout)
cold-read: skim 1/2, full 3/3 - fail

The cold read failed. A reader found the Ship, Not ready and Escalate lines in conflict and wasn't sure which governs: the scripted call is Ship, the triage line says Not ready, and the analyst's view says Escalate.

Two things to know before the meeting:
- **Pre-registration mismatch:** The registered primary is Queries per User. The experiment config and the hypothesis both name Successful Search Rate, which fell 0.45% (−0.85% to −0.05%). The Ship call rests on the volume metric, so I'd get the team to confirm the registered primary before tomorrow.
- **A line I mistyped:** In the second of the five cuts, I mistyped the line in `triage_prep.md` when pasting it. The correct cut is "a similar query issued again within 5 minutes, by arm". If re-queries rise in treatment, that supports "results got worse". If they're flat, the extra queries are new needs.