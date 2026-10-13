**Ranker v7 hasn't shown a win, and its scorecard has one unexplained movement the engineer should expect questions on.**

## Headline
The primary metric didn't move enough to count as a win, and the data rule out the pre-registered bar.

- **Successful Search Rate:** 0.4120 → 0.4116, a change of −0.04pp (95% CI −0.17pp to +0.08pp, p=0.51).
- **Pre-registered bar:** +0.5pp, and ship required the point estimate to reach it. Even the CI's upper end (+0.08pp) is far below it.
- **Verdict:** a well-powered null, not an inconclusive result. With 1M users per arm against a planned 900k, the test was big enough to rule out an effect near the bar.
- **Daily trend:** the effect by days since exposure stays flat at about −0.1% in every cohort, so there is no novelty or learning effect to wait out.
- **Guardrails** both pass:
  - Latency p95 is +0.8ms (+0.2%), and the CI's upper end is +0.7% against a 2% margin.
  - Revenue per User is −0.1%, and the CI's lower end is about −0.8% against a 1% margin.

## Why the metrics moved

- **Zero Result Rate fell 12%** (3.10% → 2.73%, p<0.001). This is the one clear, real effect, and it is plausible for a ranker change. It did not turn into more successful searches, abandonment, reformulation, or clicks.
- **CTR fell 1.8%** (−0.55pp, p<0.001). The engineer should not tell a confident story about this one, because the data don't support the obvious ones:
  - **Dilution doesn't work.** Zero-result queries have no clicks. Newly served queries would have to have negative clicks to explain a 0.55pp drop, because only 0.37pp of searches changed.
  - **The numerator and denominator disagree.** Clicks per user is −0.28% and queries per user is −0.29%, so CTR should be roughly flat (about 0%), not −1.8%.
  - **No cut shows it.** Every device, head/tail, and intent CTR cut moves between −0.14pp and +0.39pp, and none shows the −0.55pp drop. Navigational CTR is +0.39pp (p=0.009) and informational is +0.36pp (p=0.09). An overall drop outside the range of every sub-cut means either the mix shifted or the metric is defined differently from the cuts.
  - **Honest answer for triage:** "CTR is down, SSR, long clicks, abandonment, and clicks per user are flat, and we're checking the CTR definition."
- **Everything else is noise.** There are about 55 secondary metrics and cuts, with no multiple-comparison correction (`bonferroniCorrection` is false), so you'd expect 2–3 false positives at the 5% level. The three that appear are:
  - informational clicks per user, −1.7% (p=0.02)
  - head-query abandonment, +0.26pp (p=0.04)
  - navigational CTR, +0.39pp (p=0.009)

  None is worth a narrative, and none should be presented as a finding.

## Deep-dive cuts to run, in priority order

1. **CTR decomposition.** Split CTR into clicks, impressions or searches, and check the denominator definition. I expect clicks and searches to move together (about −0.3% each), so the −1.8% comes from a definition or denominator difference, such as counting only searches with results or per-impression counting. If the −1.8% reproduces in clicks per result-served search, it's a real behavior change.
2. **Searches that returned results in both arms.** Compare SSR and CTR on queries that were never zero-result. I expect both flat, which would show the CTR change comes from the set of queries counted rather than from ranking quality.
3. **The newly served queries.** Look at the queries that went from zero results to some results (the 0.37pp). I expect they skew to tail, informational, and mobile, with low success and click rates. That would show the zero-result win is real but too small (0.37pp of searches) to move SSR.
4. **Reconcile the cuts.** The device SSR cuts don't add up to the overall rate: mobile is 0.328 and desktop is 0.359, but overall is 0.412, and a partition's overall rate can't sit above both parts. The head/tail CTR cuts have the same problem. Confirm the cut definitions, any missing "other" bucket, and whether the cuts use the same population.
5. **Zero-result drop by segment.** The pulse has no zero-result cuts, so pull them by device, head/tail, and intent. I expect the drop to be concentrated in tail and informational queries.
6. **Refresh with CUPED.** This pulse was run without CUPED, which would tighten the CIs and might sharpen the CTR and cut questions.

## Data and process caveats
- **Stale pulse:** the pulse is dated 2026-09-25, 18 days ago, and the experiment still shows `status: active` past its 14-day duration. Re-pull it before presenting, and confirm the final numbers match.
- **Audit log:** `audit_logs.json` is empty, so there were no mid-flight config changes.
- **Parameters:** the only parameter that differs is the intended `ranker_model`. `snippet_length` is 160 in both arms.
- **Exposure:** the exposure check passed, and unit counts are equal at 1M per arm. The only health check configured is balanced exposures.

Ready for triage: Ready, with open questions

The null result and both guardrails are clear enough to present. The open questions are the CTR contradiction and the cuts that don't reconcile, so the engineer should resolve or flag those before the meeting, not explain them away.