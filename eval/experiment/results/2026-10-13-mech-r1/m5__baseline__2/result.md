**Ranker v7 is not shippable on the pre-registered rule, and the primary lift conflicts with its own segment cuts.** Triage can hear the "doesn't ship" story, but the engineer needs to resolve one data question first.

## Scorecard against the pre-registration

| Metric | Control → Test | Change (95% CI) | Reading |
|---|---|---|---|
| **Successful Search Rate** (primary) | 0.4120 → 0.4148 | +0.0028 abs (CI +0.0012 to +0.0044), +0.68% rel, p=0.0009 | Real-looking lift, but **below the 0.005 bar** |
| Abandonment Rate (guardrail) | 0.187 → 0.191 | +2.1% rel (CI about +1.5% to +2.7%), p<0.001 | Worse. Inside the 4% margin, but significantly worse. |
| Latency p95 (guardrail) | 412 → 412.8 ms | +0.2% (±0.5%) | Passes against the 2% margin |
| CTR | 0.305 → 0.3016 | −1.1% | Significant drop |
| Clicks per User | 3.60 → 3.56 | −1.2% | Significant drop |
| Autocomplete Acceptance | 0.338 → 0.3357 | −0.23 pp, p=0.025 | Marginal, see the multiplicity note below |
| Long Click Rate, Time to First Click, Reformulation, Queries and Sessions per User, Zero Result, Pagination, Ad Click Rate, Revenue per User | | all flat, p>0.2 | No evidence of movement |

- **Ship decision:** the pre-registration says `ship_requires: point_at_bar`. The point estimate is 0.0028 and even the CI's upper end (0.0044) is under 0.005. At face value this is a miss.
- **Design is sound:** about 1M units per arm against 900k planned, and the exposure-balance health check passed. The run covered the full 14 days from Sat 2026-09-12 to 09-25, so it includes two weekends. Sequential testing is off, so a fixed-horizon read is valid. There are no audit-log changes, and only `ranker_model` differs between arms (`snippet_length` is the same in both).

## Why the metrics moved

The data can't tell us why, so these are hypotheses for the engineer to label as such.

- **Fewer clicks but more "successful" searches.** SSR is up, while CTR and clicks per user are down. Long Click Rate and Time to First Click are flat, and Queries and Reformulation are flat. One reading is that better top results mean fewer clicks per search.
- **Abandonment is the awkward part.** Abandonment rises 2.1% while SSR also rises. "Good abandonment" (the answer is visible without a click) would explain both, but it would also predict lower reformulation, and reformulation is flat. So the benign story is not supported.
- **Revenue and ads are flat,** so there is no monetization cost visible yet.
- **Don't build stories on the marginal p-values.** The scorecard has roughly 16 secondaries plus about 36 segment cuts, with no multiplicity correction (`bonferroniCorrection: false`). That many comparisons should throw up 2–3 nominal hits by chance. CTR Desktop (p=0.011), Reformulation Mobile (p=0.043) and Autocomplete (p=0.025) fit that pattern. The CTR, Clicks, Abandonment and SSR movements are strong enough to stand.

## The issue to resolve before triage

The segment SSR cuts don't add up to the headline.
- **Mobile and Desktop:** SSR is −0.00095 and −0.0011, both negative, yet overall SSR is **+0.0028**.
- **Navigational and Informational:** −0.0011 and +0.00008, so none are positive.
- **Why it matters:** the platform split roughly partitions overall SSR (0.370 mobile and 0.438 desktop average to about 0.412). Navigational (0.52) and Informational (0.40) bracket it too, so Navigational and Informational may partition it as well. A lift that appears in no segment needs a mix shift of about 5 pp between the arms, or different denominators for the segment metrics. If it comes from a mix shift, the "lift" is a composition artifact and the primary result is unreliable.
- **Not a partition:** Head and Tail (0.353 and 0.305) both sit below the overall 0.412, so they can't be a full partition. There is probably a missing torso bucket, so don't read them as one.

## Deep-dive cuts to run, in priority order

1. **Segment share per arm (platform, query type).** Compare the share of exposed users and searches in each arm. If the test arm has a heavier desktop mix, the lift is composition. If the shares match, check how SSR is defined for the segment metrics versus the headline (per search or per user).
2. **Re-weighted SSR.** Stratify by platform × query type, or reweight the test arm to control's mix, and recompute the delta. I expect roughly zero or slightly negative if composition is the cause.
3. **Abandonment by query type and results-page features.** Check whether it rises where answers are shown without a click. If it is good abandonment, reformulation and re-query within the session should fall, and the flat reformulation result argues against that.
4. **Tail Queries.** Its SSR (−0.0018) and abandonment (+0.0019) are the worst of the segment cuts. Expect the damage to concentrate there if the new ranker does worse on sparse queries. These are not significant individually, so describe them as directional.
5. **Days since exposure.** The daily series is flat at about +0.64% to +0.72% relative, so there is no novelty decay. But it only covers 12 of 14 days, and the per-day CIs are about as wide on every day, which is odd for per-day samples. Confirm the series' definition (cumulative or per-day) before using it to claim stability.

## Verdict

The recommendation is clear: **don't ship**. SSR misses the bar, and abandonment is significantly worse. The open question is whether the +0.0028 lift is even real, and the engineer can't answer "why did SSR move?" until the mix-shift check is done.

Ready for triage: Ready, with open questions