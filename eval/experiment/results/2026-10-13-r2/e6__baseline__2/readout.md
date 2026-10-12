Decision: Escalate

# Ranker v7 – launch readout

## Bottom line
Ranker v7 passes the pre-registered ship rule, but I don't think the primary win is a real user benefit. The same data shows more reformulations, no gain in successful searches, and fewer ad clicks. That is a product call, not a mechanical "ship". I recommend the review decide whether to ship, with the evidence below in front of them.

## Pre-registered test (95% CI, no CUPED, as requested)
| | Pre-reg requirement | Result | Verdict |
|---|---|---|---|
| Primary: Queries per User | point estimate ≥ +1% relative | 11.80 → 12.08, **+2.4% (CI +1.5% to +3.3%), p<0.001** | Met. The whole CI is above the bar. |
| Guardrail: Latency p95 | no worse than +2% | 412.0 → 412.8 ms, **+0.2% (CI −0.3% to +0.7%)** | Passed. The upper bound is under 2%. |

The design is a valid A/B test. Units are 1.0M per arm against 0.9M planned, the 50/50 split is balanced, the exposure health check passed, and the audit log is empty, so there were no mid-test config changes. Only the `ranker_model` parameter differs between arms, which matches the intended parameters.

## Why I don't trust the primary
1. **The queries increase looks like reformulation.** Reformulation Rate went up from 14.3% to 15.0%, **+5.1% (CI +4.3% to +5.9%), p<0.001**. Lower is better for this metric, so it moved the wrong way. Users issuing more queries because the first results failed is a plausible cause of the Queries per User lift. The pre-reg named no reformulation guardrail.
2. **The stated hypothesis is not supported.** The experiment's hypothesis is that v7 raises the share of searches ending in a successful click. Successful Search Rate is 41.2% → 41.06%, **−0.35% (CI −0.75% to +0.05%), p=0.09**. That is flat to slightly negative. CTR, Long Click Rate, Clicks per User and Abandonment are all null.
3. **The config and the pre-reg disagree on the primary.** experiment.json lists Successful Search Rate as the primary. prereg.json lists Queries per User. Someone should confirm which one the team meant. Under the config's primary, this is a null result.
4. **Other metrics are worse.**
   - Ad Click Rate: −2.0% (CI −3.2% to −0.8%), p=0.001.
   - Time to First Click: +1.3% (CI +0.3% to +2.3%), p=0.012. Lower is better.
   - Revenue per User is flat at −0.1% (CI ±0.7%), so the ad drop has not yet shown up in revenue.

## Caveats
- The Pulse snapshot is dated 2026-09-25. The test started 2026-09-12 and was planned for 14 days, so the snapshot may miss the last day. The experiment still shows "active" today, 2026-10-12. Refresh the data and close the test.
- Pulse lists 56 secondary metrics, including segment cuts, with no multiplicity correction. A few other p<0.05 segment results (for example Navigational Long Click Rate, Head-query Clicks per User) are what chance would give, so I'm ignoring them. The reformulation, ad click and time-to-first-click findings are overall metrics, and the first two are far below any plausible corrected threshold. Time to First Click is weaker evidence.
- I did not look at the unreported cuts of reformulation by query count, so I can't prove that reformulation caused the queries lift. That is a hypothesis.

## Recommendation and next steps
- Don't ship on Queries per User alone. Before the review, or as a condition of shipping, check whether the extra queries come from reformulation chains, for example queries per session split by whether the next query is a reformulation.
- Ship only if the review accepts more reformulation and fewer ad clicks in exchange for the queries lift, or if that analysis shows the lift is not reformulation-driven.
- If the review wants a clean answer, rerun or extend with Successful Search Rate and Reformulation Rate registered as primary and guardrail.
