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

- A Tail Queries gain that holds in the triggered-only cut would make a segment-only test worth proposing.
- A pre-exposure comparison for the primary; the check could not run.

## Why it moved

- [inferred] Overall Successful Search Rate is flat (+0.08%) because a gain on Tail Queries (+3.40%) is cancelled by small losses elsewhere: Head Queries -0.53%, Navigational -1.07%.
- [guess] Navigational queries look worse: Successful Search Rate -1.07%, with Reformulation Rate up. The new ranker may be pushing the expected top result down for queries with one right answer.
- [measured] Guardrails sit inside their margins, and the effect is steady by days since exposure, so this is not a novelty fade.

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

Lint: 0 fail, 0 warn, 244 body words (readout)
Cold read: cold-read: skim 2/2, full 3/3 - pass

The cold-read reader flagged "triggered-only cut" as undefined and was unsure how much weight the Tail Queries result carries.

Ready for triage: Ready, with open questions

The scripted verdict above says "Ready", and I'm downgrading it on my own judgment. I had no data access, so I ran none of the cuts. Every explanation is inferred or a guess, and the pre-period check didn't run. Two things in the scorecard aren't in the scripted questions:
- **Navigational queries:** Successful Search Rate is -1.07% with an interval that excludes zero, and Mobile CTR is down. Expect triage to ask about this.
- **Tail Queries:** query class is a registered segment, so the +3.40% gain isn't purely exploratory, even though the readout's appendix labels it that way. The primary has no bar on that segment, so it can't change the call.