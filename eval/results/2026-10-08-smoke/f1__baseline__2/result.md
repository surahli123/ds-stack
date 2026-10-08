## Answer
Headline: about 0.0 pp attributable to v2 (within-segment change: 0.00 pp in all four platform×country segments). The overall change was −2.1 pp, from 30.42% to 28.32%.

Overall CTR fell 2.10 pp (30.42% → 28.32%), and all of that fell out of a shift in traffic mix toward mobile. CTR within each platform×country segment is unchanged. (measured)

## What it means for the rollback decision
The data gives no sign that v2 hurts CTR, so the drop alone is not a reason to roll back. Because v2 went to 100% of traffic at once, we can't rule out that v2 itself caused the mobile shift. (inferred)

## Why we believe it
- Alternatives considered:
  - v2 lowered CTR within segments: ruled out. Segment CTRs match to four decimals: desktop-US 37.08%, desktop-other 34.74%, mobile-US 22.66%, mobile-other 21.23%. (measured)
  - Traffic mix shift (Simpson's paradox): ruled in. Mobile share of searches jumped from 40% to 55% on exactly 2026-09-28, and held at 55% every day after. Mobile CTR is about 13 pp lower than desktop. (measured)
  - Mobile share rose because of v2: could not be separated. Rollout and mix shift coincide on the same day. It could be an unrelated cause such as a mobile campaign or a logging change, or v2 could be driving more mobile searches. (guess)
  - Daily noise or a trend that was already under way: ruled out. Daily CTR is flat within each week, and the step happens on the rollout date. (measured)
- Checks run:
  - Segment-level before/after CTR comparison: pass. Identical CTR in every segment.
  - Mix-versus-rate breakdown: pass. The mix effect accounts for essentially all of the −2.1 pp.
  - Concurrent control group (v1 traffic after 09-28): could not run. There is no v1 traffic after the rollout.
  - Release log check for other changes: pass. Only the v2 rollout is logged, so a mobile-side change would not appear there.

## Caveats, and what would change the answer
- The data is only two weeks, with no holdout, so it can't separate v2 from anything else that changed on 09-28.
- Find out why mobile share jumped, for example a mobile app release or a marketing push. If v2 caused it, the question becomes whether it's good or bad that v2 draws more mobile searches.
- A v1 holdout or a staged rollout would give a clean causal estimate.
- Only the aggregate CTR is analyzed here. There are no per-user or per-query data, so this doesn't measure downstream quality such as satisfaction or conversions.