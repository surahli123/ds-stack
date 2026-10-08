## Answer
Headline: −1.80 pp overall CTR, week over week (30.42% → 28.62%). I can't separate v3's share of that from anything else that changed that week.

Overall search CTR fell 1.80 pp. All of the fall is on desktop (US −3.1 pp, other −2.9 pp). Mobile clicks and searches are identical to the prior week. [measured]

## What it means for the rollback decision
The drop lines up with the v3 rollout, and v3 is the only change in the release log. It is plausibly v3's effect, but there is no concurrent control, so this doesn't prove it. If v3 is the cause, the effect is concentrated on desktop, where it is roughly −3 pp. A short holdback or a desktop-only rollback test would settle it.

## Why we believe it
- Alternatives considered:
  - Mix shift (platform/country): ruled out. Searches per segment are identical across the two weeks, and the mix effect is +0.00 pp. [measured]
  - Day of week or seasonality: ruled out for the weekly comparison, since both weeks cover Monday to Sunday with near-identical daily volumes. The drop appears on every day from 09-07 on, and daily CTR never overlapped between the weeks. [measured] Whether this is normal early-September variation can't be checked with only 2 weeks. [guess]
  - Data completeness: ruled out. There are 4 rows every day in both weeks. [measured]
  - Logging or definition change: not ruled out. Mobile clicks and searches are exactly identical to the prior week, 34,899 and 26,751 clicks, which is implausible for real traffic. Either mobile was untouched by an effect that left it exactly flat, or mobile data is copied or frozen. [inferred]
  - v3 caused the drop (the PM's hypothesis): ruled in as plausible, not confirmed. The timing matches, and v3 is the only logged change. v3 went to 100% of traffic at once, so there's no same-period v2 control. [inferred]
- Checks run:
  - completeness: pass. The last day (09-13) has 4 rows, 100% of the trailing median.
  - mix_shift: pass. The −1.80 pp change is entirely within-segment, with mix share 0%.
  - fanout: skipped. No joins were used.
  - srm: skipped. This was not an experiment with assignment counts.

## Caveats, and what would change the answer
- With no concurrent control, any other change that week would be counted as v3's effect. Examples are a desktop UI change, click-tracking changes, or a seasonal change. Only the release log was available.
- The exactly flat mobile numbers need a data-owner check. If mobile is stale, the true overall change and the v3 attribution could differ.
- A v2 holdback, or a desktop-only comparison against a stable control, would turn the −1.80 pp into a clean causal estimate.
- Clicks per search is not the same as search quality. Check downstream metrics such as task completion or reformulations before deciding.