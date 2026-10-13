# Ranker v7: No effect found

Decision: No effect found. Successful Search Rate reads +0.08% (-0.22% to +0.38%), which rules out the 0.50% change the test was built to find.

Ask: Agree to stop the test without launching.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: no pre-period comparison, so a difference between the arms before the test isn't ruled out.

Triage: Ready: every movement triage will ask about has a candidate explanation and none conflict; the explanations are inferred from co-movements, so the cuts below would confirm them.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.08% (-0.22% to +0.38%) | estimate at least 0.50% higher | unclear |
| 4 other guardrails | guardrail | | | all within margin |

Checks: passed: scorecard, sample split, config params, config edits, novelty; not run: pre period.

## What would change the call

- A Tail Queries cut on triggered queries showing the lift holds and the other classes do not fall would justify a rerun aimed at tail traffic.
- A sample split or logging imbalance within Tail Queries by arm would mean the tail lift is an artifact.
- A pre-exposure comparison of Successful Search Rate showing a gap between arms would undermine this read.

## Why it moved

- [measured] The overall rate is flat because gains and losses cancel by query class: Successful Search Rate is +3.40% on Tail Queries, -0.53% on Head Queries and -1.07% on Navigational.
- [inferred] The new ranker probably surfaces better results for rare, long-tail queries and slightly displaces the right top result on navigational ones; Reformulation Rate on Navigational rose 1.71%.
- [guess] CTR - Mobile fell 1.43% while Successful Search Rate - Mobile did not clearly move; no cut has been run on it.

## Appendix

- Secondary metrics: 52 tested; after a false-discovery correction these moved: Successful Search Rate - Tail Queries (+3.40%). They are exploratory and don't change the call.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Abandonment Rate, Zero Result Rate, Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

# Ranker v7: triage prep

Ready for triage: Ready: every movement triage will ask about has a candidate explanation and none conflict; the explanations are inferred from co-movements, so the cuts below would confirm them.

Scripted call: No effect found. Successful Search Rate reads +0.08% (-0.22% to +0.38%), which rules out the 0.50% change the test was built to find.

## Before any single metric

- What did you change? ranker_model: lambdamart_v6 -> lambdamart_v7; nothing else differs between arms.
- Is the data trustworthy? Yes, as far as the checks reach; not checked: pre period.
- Is the effect real, or chance? Successful Search Rate +0.08% (-0.22% to +0.38%); its interval includes zero. Across the scorecard 4 of 57 metrics moved clearly; about 2.9 would by chance alone.
- Will it last? Probably: effect by days since exposure: first days +0.07%, last days +0.09% (trend +0.002% per day).
- Did the change do what it was built to do? Not shown. If the scorecard or a cut has a coverage metric (the share of queries whose top results changed), register it as feature_metrics.

Metric families used: abandonment = Abandonment Rate, ad_ctr = Ad Click Rate, autocomplete = Autocomplete Acceptance, clicks_per_user = Clicks per User, ctr = CTR, latency = Latency p95 (ms), long_click = Long Click Rate, pagination = Pagination Rate, queries_per_user = Queries per User, reformulation = Reformulation Rate, revenue = Revenue per User, sessions_per_user = Sessions per User, success = Successful Search Rate, time_to_click = Time to First Click (s), zero_result = Zero Result Rate. A wrong pairing here changes every explanation below; fix it in the overlay's metric_families.json.

## Questions triage will ask

1. Successful Search Rate was expected to rise but didn't move. Why? It didn't move clearly (+0.08% (-0.22% to +0.38%)). Status: untested.
   - Likely [inferred]: The effect sits in one segment. Successful Search Rate's change comes mostly from Tail Queries (while the overall change is about zero of the overall change), and segments differ more than noise allows.
     Evidence: Successful Search Rate by query class: Head Queries -0.53%; Tail Queries +3.40%.
     To check: cut 1, 2 below.

2. Why is Successful Search Rate's change concentrated in Tail Queries? Status: untested.
   - Likely: The effect sits in one segment, as in question 1.

## Cuts to run before triage, in order

1. Successful Search Rate for Tail Queries vs the rest, with triggered queries only (tests: The effect sits in one segment). Supports it: the change is real and confined to Tail Queries. Against it: the other segments move too once diluted traffic is removed. Record its outcome in evidence.json under cuts.
2. What the treatment changes for Tail Queries (ranking features, coverage, rendering) (tests: The effect sits in one segment). Supports it: a mechanism specific to Tail Queries. Against it: nothing in the change targets Tail Queries. Record its outcome in evidence.json under cuts.
3. Sample split and event logging within Tail Queries, by arm (tests: The effect sits in one segment). Supports it: the segment is balanced and logs the same way. Against it: the segment itself is imbalanced or logs differently (an artifact). Record its outcome in evidence.json under cuts.

Explanations become confirmed only when a cut's result is passed back to explain.py with --evidence; a cut that contradicts a candidate removes it.

## Sources

- The effect sits in one segment: Dmitriev et al., A Dirty Dozen: Twelve Common Metric Interpretation Pitfalls, KDD 2017 (effects confined to a country, browser or version); tail-query lifts reported for semantic retrieval (snippet-level).

Lint: 0 fail, 0 warn, 278 body words (readout)
Cold read: skim 2/2, full 3/3 - pass

The scripted triage verdict says "Ready". I'd mark it lower, for these reasons:
- No cut has been run. Every mechanism is inferred from co-movement.
- The pre-period check couldn't run.
- Navigational Successful Search Rate fell 1.07%, and that segment's Reformulation Rate rose 1.71%. Triage will ask about it and the prep sheet has no cut for it. I'd add a Navigational cut, and a Mobile cut for the 1.43% CTR drop.
- Only the Tail lift survives the false-discovery correction, so the Tail, Head and Navigational splits are all exploratory. Query class is a registered segment, but the Tail lift can't change the call.

Ready for triage: Ready, with open questions