**Ready for triage: Ready, with open questions**

The results are clean and the call is clear: the primary is flat and the ranker is not shippable. The open questions are about why CTR, abandonment and latency moved, which the data can't answer yet.

## What the scorecard says

The pulse is 1M users per arm with the exposure check passing. It was pulled without CUPED at 95% confidence, and the config shows no mid-test changes (the audit log is empty).

**Primary: Successful Search Rate is flat.**
- It is 0.4120 in both arms. The change is 0.0000, p = 1.0, and the 95% CI is ±0.0012 absolute (±0.3% relative).
- The prereg bar is +0.005, which the interval rules out. That holds whether the bar is read as absolute or as relative (about +0.0021 absolute). The prereg also requires the point estimate to reach the bar, and it is at 0.
- This is a well-powered null. Don't present it as "inconclusive" or "needs more time".
- The daily series by days since exposure is flat, with deltas between -0.04% and +0.04%. That argues against a novelty or learning effect hiding an early difference.

**Real movements, all in the wrong direction:**

| Metric | Control | Test | Change | Note |
|---|---|---|---|---|
| CTR | 0.305 | 0.3004 | -0.0046 (-1.5%) | CI ±0.4%, significant |
| Abandonment Rate | 0.187 | 0.190 | +0.0030 (+1.6%) | CI ±0.4%, significant, worse |
| Latency p95 | 412 ms | 436.7 ms | +24.7 ms (+6.0%) | CI ±0.8%, significant, worse |

**Guardrails:** Both are inside their prereg margins, so there is no formal breach. The margin units aren't stated in the prereg, and I checked both readings.
- Latency: the worst-case upper bound is +6.8% relative, or +28 ms. That is under the 0.1 margin read either way.
- Abandonment: the worst case is +2.0% relative, or +0.0037 absolute. That is under the 0.03 margin read either way.
- Still, both moved significantly the wrong way, and the primary shows no gain to offset them.

**Everything else is null.** That covers:
- Long click rate
- Reformulation rate
- Queries, sessions and clicks per user
- Time to first click
- Zero-result rate
- Ad click rate
- Revenue per user
- Pagination
- Autocomplete

## Why did the metrics move?

Don't claim causes you haven't tested. Here is what the data supports and what is still a hypothesis.

1. **Successful Search Rate didn't move.** The v7 ranker did not change whether searches end in a successful click, at a precision of about ±0.3%. The hypothesis in the prereg is not supported.
2. **Latency is up 6%.** This is the one effect with an obvious mechanism: a heavier model (`lambdamart_v7` vs `v6`) costs more at serving time. It is the only parameter that differs, because `snippet_length` is 160 in both arms. This is probable but not measured. Ask whether v7 inference time was benchmarked offline.
3. **CTR is down and abandonment is up, with no change in successful searches.** A hypothesis is that slower results lead some users to skip or abandon a search that would otherwise have produced a low-value click. That fits with SSR and long-click rate (a stand-in for satisfied clicks) staying flat. It is not established. A different ranking order could also reduce clicks without changing success. Present it as a hypothesis, not a finding.
4. **Be careful with the nominally significant segment results.** The pulse has 42 segment metrics, and no multiplicity correction was applied. About two would show p<0.05 by chance, and exactly two do:
   - Desktop long click rate, p = 0.033, -0.0029.
   - Mobile SSR, p = 0.053, -0.0035, which is borderline.

   Neither is a finding. If triage asks "is mobile hurt?", the answer is that the interval is wide (±0.0036) and it doesn't survive correction.

## Deep-dive cuts to run next

1. **Latency distribution by segment (mobile vs desktop, head vs tail).**
   - Expected: the +24.7 ms is broad, and larger for tail and informational queries that need more reranking.
   - Why it matters: if it is concentrated, it may be fixable.
2. **CTR and abandonment, split by latency bucket within each arm.**
   - Expected: if latency drives the CTR drop and abandonment rise, then within a latency bucket test and control look similar. The arm gap should shrink or vanish after conditioning on latency.
   - Caveat: latency after assignment is a post-treatment variable. Read this as diagnostic, not causal.
3. **CTR vs clicks per user vs queries per user.**
   - CTR is a ratio, and clicks per user (+0.012) and queries per user (-0.044) are both null.
   - Expected: the CTR drop comes from the denominator and numerator moving a little in opposite directions. Check whether it is fewer clicks or more searches without clicks.
4. **Position-of-click and result-rank distribution.**
   - Expected: if v7 reorders results, clicks shift in position without changing success rate.
   - This tells triage whether v7 changes behavior at all or is just a more expensive v6.
5. **Mobile SSR and desktop long-click, as pre-specified follow-ups only.**
   - Expected: no effect. Treat them as hypotheses to check on a rerun, not results.
6. **Power and equivalence statement.** Report the SSR CI as "we can rule out any lift ≥ +0.12 points" for the writeup.

## Housekeeping to tidy before the meeting

- **Dates:**
  - The pulse snapshot is dated 2026-09-25, and the run was 09-12 to 09-26. Today is 10-13, so the snapshot is about 18 days old.
  - The daily series covers only 12 of the planned 14 days.
  - Re-pull the final pulse so the scorecard covers the full run. Nothing suggests the conclusion will change, given the null's precision.
- **Sample size:** 1.0M users per arm were exposed, against 900K planned. Be ready to say why.
- **Status:** The experiment still shows `active` in the config. Confirm it is stopped.
- **Prereg margins:** State the units (relative or absolute) so the guardrail read is unambiguous.

## Recommendation

Don't ship v7 as it stands. The primary shows no lift, and there are modest, statistically significant regressions in CTR, abandonment and latency. If the team wants to keep going, the lever is latency and model cost, then rerunning the test.