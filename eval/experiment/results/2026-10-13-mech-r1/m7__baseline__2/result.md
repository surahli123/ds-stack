**Bottom line:** Ranker v7 did not move the primary metric, and it does not meet the ship rule. The one striking result is a gain on tail queries. That is a lead to investigate, not a win to claim.

## Why the metrics moved

**Primary: Successful Search Rate (SSR) is flat.**
- The change is +0.033pp (0.41200 → 0.41233), which is +0.08% relative. The 95% CI is ±0.124pp and p = 0.60.
- The prereg ship rule needs the point estimate at or above the 0.005 bar. The point estimate is about 15× below the bar if it is absolute, and about 5× below if it is relative.
- The CI upper bound (+0.157pp, or +0.38% relative) is also under the bar either way. So this is a well-powered null, not an "inconclusive" result.
- With 1M users per arm, we can rule out any lift near the target.
- The engineer should say "no detectable effect; the hypothesis wasn't supported." They should not say "directionally positive."

**Secondary metrics: nothing is distinguishable from zero.**
- CTR (+0.05pp), Long Click Rate, Abandonment, Reformulation, Time to First Click, Clicks per User, Queries per User and Sessions per User all have p > 0.14.
- The signs are mixed, which is what noise looks like.
- If asked "why did Queries per User go down 0.7%?", the answer is that it is not significant (p = 0.15). It also isn't a signal of fewer searches, because the CI spans zero.

**Guardrails: all pass, and the evidence is meaningful.**

| Guardrail | Observed change | Margin | Result |
|---|---|---|---|
| Latency p95 | +0.2% ±0.5% | 2% | Within margin |
| Zero Result Rate | exactly 0 (p = 1.0) | 3% | Within margin |
| Revenue per User | −0.1% ±0.7% | 1% | Worst-case CI bound is about −0.8%, inside the −1% margin, but only just |
| Abandonment | +0.1% | 1% | Within margin |

- Revenue's lower bound is the tightest of the four. Expect questions on it.
- Zero Result Rate is exactly unchanged. That is plausible for a re-ranker, since it reorders results and doesn't change which ones are retrieved.

**Segments: one real-looking outlier, plus noise.**
- **Tail Queries SSR is +1.13pp (z ≈ 7.4, p ≈ 0).** It survives any multiple-comparison correction. About 40 segment metrics were scanned, and the Bonferroni cutoff is about 0.001.
- It is also a prereg'd segment ("query class"), so it isn't a post-hoc cut.
- The other query classes are flat or negative:
  - Head SSR is −0.25pp (p = 0.31).
  - Navigational SSR is −0.45pp (p = 0.02). That would not survive correction.
  - Informational SSR is flat.
- Mobile CTR is −0.44pp (p = 0.007). This is the only other nominal hit. It is one of about 40 tests and doesn't carry over to Mobile SSR (−0.24pp, p = 0.14). Treat it as probably chance, but check it.
- A plausible story is that the ranker helps rare or long-tail queries, where the old model had little signal, and is neutral to slightly worse on head and navigational queries. The tail gain then dilutes to nothing overall.
- That story is only consistent with the numbers. Nothing here tests it.
- It reconciles if tail queries are roughly 20–30% of traffic. Confirm the actual traffic shares.

## Deep-dive cuts to run, and what each would show

1. **Traffic share by query class.**
   - It tells us whether the +1.13pp tail gain and the small negative head and navigational effects add up to the +0.03pp overall.
   - If tail is about 20–30% of volume, they do. If tail is only a few percent, the tail number is hard to square with the rest.
2. **Tail Queries SSR by exposure day (days 1–14).**
   - A real ranking improvement should be stable. A decay would point to a novelty effect, or to a short-lived one from cache or index warm-up.
   - The overall daily SSR delta is flat at about +0.04% to +0.12% with no trend, so no novelty or learning effect is hiding at the aggregate level.
3. **Tail × device (mobile vs. desktop), and Mobile CTR vs. Mobile SSR.**
   - This shows whether the mobile CTR dip is real and linked to the tail effect, for example through snippet or position changes on small screens.
   - If Mobile CTR is down but SSR is not, results may be getting satisfied without a click.
4. **Tail definition and the metric's denominator.**
   - Check how "tail" is assigned (query frequency threshold, and whether it is fixed per query or per day).
   - Check whether SSR is per search or per user, and whether tail queries have a different search count per user.
   - A definitional quirk, such as the tail bucket being assigned from post-treatment data, would manufacture an effect of this size.
5. **Revenue and Ad Click Rate by query class.**
   - Revenue's CI nearly touches the margin. See whether the small ad and revenue softness (Ad Click Rate −0.36%, not significant) is concentrated in head or navigational queries.
   - If it is, a head-only guardrail risk would matter for any "ship to tail only" idea.
6. **Validate the tail result on fresh data.**
   - Treat it as a hypothesis for a follow-up test that targets tail queries, with its own prereg and bar.

## Readiness

**What checks out:**
- Numbers are internally consistent. p-values and CIs recompute from the reported means and standard errors for every metric.
- The audit log is empty, so there were no mid-test config changes.
- The exposure-balance health check passed, and arms are exactly 1.0M each. That is above the planned 900k per arm, which is fine.
- The window matches the plan: started Sep 12, results cut at Sep 25, which is 14 days. No sequential testing was configured, so there is no peeking problem.
- Pulse was pulled without CUPED, as specified.

**Open questions:**
- The prereg bar is 0.005 and doesn't say whether it is absolute or relative. The verdict is the same either way, but the engineer should be ready to say which one the team meant.
- Tail's +1.13pp has not been checked beyond the one Pulse readout. Items 1, 2 and 4 above should be run before the tail claim is stated confidently.
- The only health check listed is exposure balance. Say so if asked about other checks, such as SRM, and don't imply others passed.

The results are fine to present as a null on the primary with a lead on tail queries. They are not fine to present as a win.

Ready for triage: Ready, with open questions