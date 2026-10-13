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

- Success per query flat or down while Queries per User rises would confirm activity without success.
- A similar query repeated within 5 minutes rising in Test would confirm worse results; flat would point to real extra demand.

## Why it moved

- [inferred] Users ran more queries (+2.60%) and reformulated more (+5.50%), yet Successful Search Rate is down (-0.45%). That fits repeat searching after weak first results.
- [guess] Successful Search Rate is the registered hypothesis metric, and its drop is concentrated in Informational queries (down 0.85%) while Desktop rose 1.52%. No cut has been run to explain this yet.

## Analyst's view

The analyst would call this Escalate: The pre-registered primary is Queries per User, but the hypothesis is Successful Search Rate, which is down 0.45% and clearly below zero. Reformulation Rate is up 5.50%. More searching with less success can mean worse results, so settle the success cuts first.

## Appendix

- Secondary metrics: 55 tested; after a false-discovery correction these moved: Reformulation Rate (+5.50%), Successful Search Rate - Desktop (+1.52%), Autocomplete Acceptance (+0.97%). They are exploratory and don't change the call.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms).
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

# Ranker v7: triage prep

Ready for triage: Not ready

The scripted call is Ship. The best explanation of Queries per User is bad news: more activity without more success. Run the first cut before anything else.

Ready for triage: Not ready

## Before any single metric

- What did you change? ranker_model: lambdamart_v6 -> lambdamart_v7; nothing else differs between arms.
- Is the data trustworthy? Yes, as far as the checks reach; not checked: pre period.
- Is the effect real, or chance? Queries per User +2.60% (+1.70% to +3.50%); its interval excludes zero. Across the scorecard 8 of 57 metrics moved clearly; about 2.9 would by chance alone.
- Will it last? Probably: effect by days since exposure: first days -0.46%, last days -0.44% (trend +0.002% per day).
- Did the change do what it was built to do? Not shown. Register a coverage metric (the share of queries whose top results changed) if you have one.

## Questions triage will ask

1. Why did Queries per User rise? It rose 2.60% (+1.70% to +3.50%). Status: untested.
   - Likely [inferred]: More activity without more success. Users search more while success doesn't rise.
     Evidence: Successful Search Rate fell 0.45% (-0.85% to -0.05%); Queries per User rose 2.60% (+1.70% to +3.50%); Reformulation Rate rose 5.50% (+4.70% to +6.30%).
   - Likely [inferred]: More searching because results got worse. Users retry, so higher query volume is a cost, not engagement.
2. Why did Reformulation Rate rise? Same two candidates as question 1. Untested.
3. Why did Successful Search Rate - Desktop rise? It rose 1.52% (+0.60% to +2.44%). No candidate in the library. "Unexplained, possibly chance" is an allowed answer.
4. Why did Autocomplete Acceptance rise? It rose 0.97% (+0.37% to +1.57%). No candidate in the library. Same allowed answer.

## Cuts to run before triage, in order

1. Success per query vs per user. Supports "more activity without more success" if success per query falls or holds while activity grows. Against it if success per query rises with activity.
2. A similar query issued again within 5 minutes, by arm. Supports "results got worse" if quick re-queries rise in Test. Against it if flat, which would mean the extra queries are new needs.
3. Queries per User on triggered vs untriggered queries (where the ranking changed). Supports the registered hypothesis if the effect is larger where ranking changed. Against it if untouched queries show the same effect.
4. Sessions per user vs queries per session, by arm. Supports "retrying" if there are more queries inside the same sessions. Against it if there are more sessions (users coming back).
5. Navigational share of queries by arm, week by week. Supports "results got worse" if Test users drift toward easy navigational queries. Against it if the query mix is stable.

Cuts 1, 2 and 5 can be scored by script once their results are in evidence.json. Cuts 3 and 4 are recorded under cuts.

Lint: 0 fail, 0 warn, 270 body words (readout)
Cold read: skim 1/2, full 3/3 - fail. The reader had to reread the header against the triage and analyst view, since they disagree (Ship, Not ready, Escalate).