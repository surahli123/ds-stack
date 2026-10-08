## Answer
Headline: 0.0 percentage points attributable to v2 on a like-for-like basis. The overall change was −2.1 pp (30.43% → 28.32%).

The whole drop comes from traffic shifting toward mobile, which has a much lower CTR. Within each platform and country segment, CTR didn't change at all between the two weeks.

## What it means for the rollback decision
The data gives no evidence that v2 hurt CTR, so the drop alone is not a reason to roll back. The open question is why mobile share jumped, because that is what moved the overall number.

## Why we believe it
- Alternatives considered:
  - v2 lowered CTR: ruled out as the main driver. Every segment's CTR is identical to two decimals across the weeks: desktop US 37.08 → 37.08, desktop other 34.74 → 34.74, mobile US 22.66 → 22.66, mobile other 21.23 → 21.23. [measured]
  - Traffic mix shift (Simpson's paradox): ruled in. Mobile's share of searches went from 40% (280k of 700k) to 55% (385k of 700k). Desktop CTR is about 36% and mobile about 22%. Applying the new mix to the old segment rates gives about 28.3%, which matches the observed figure. [measured]
  - Day-to-day noise or a pre-existing trend: ruled out. Daily CTR was flat at 30.1–30.7% for all 7 days before the rollout and flat at 28.0–28.6% for all 7 days after, with a step change on 09-28. [measured]
  - v2 caused the mobile share shift: not ruled out. The timing coincides with the rollout, but nothing in the data shows why mobile grew. [guess]
- Checks run:
  - Weekly CTR by ranker version: pass. 30.43% (v1) vs 28.32% (v2). [measured]
  - Segment-level CTR comparison: pass. Zero within-segment change in every segment.
  - Mix decomposition: pass. Essentially 100% of the −2.1 pp is mix.
  - Daily series: pass. Stable before and after.
  - Concurrent A/B holdout: could not run. v2 went to 100% of traffic with no v1 control group, and the data has no other releases or campaigns.

## Caveats, and what would change the answer
- This is a before/after comparison with no control group. Only the segments we can see are held constant.
- Identical CTRs to two decimals across all four segments is unusually tidy. It's worth checking that the pipeline isn't carrying CTR forward by segment.
- If the mobile surge was caused by v2 (for example, it changed which queries or entry points drive traffic), then v2 would be indirectly responsible. Check what drove the mobile traffic increase, such as a campaign, an app release or a logging change.
- A rollback or a holdout slice of v1 would settle the question directly.