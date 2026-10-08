## Answer
Headline: -1.80 pp (overall CTR 30.42% → 28.62%). I'm treating all of the drop as v3's, but that is inferred, with no interval.
Overall CTR fell 1.80 percentage points week over week. All of the fall is in desktop (US -3.1 pp, other -2.9 pp). Mobile is unchanged to four decimals. [measured]

## What it means for the rollback decision
Mix shift and incomplete data don't explain the drop, so it is a real within-segment decline on desktop that began the day v3 launched. This points toward rolling back, or at least a desktop-only rollback. I'd confirm first that nothing else changed on desktop on 2026-09-07, because v3 was at 100% and there is no holdout.

## Why we believe it
- Alternatives considered:
  - Traffic mix shift (platform or country): ruled out. Segment weights are identical across the two weeks (33/27/22/18%), so mix contributes +0.00 pp. [measured]
  - Seasonality or day of week: ruled out. Both weeks are full Monday-to-Sunday weeks, and the daily searches match across weeks. The same weekday pairs line up (e.g. 08-31 vs 09-07 have identical volume). Mobile CTR is identical week to week, so there is no general seasonal dip. [measured]
  - Data incompleteness or logging gaps: ruled out. All 14 days have 4 segment rows each, and the last day is at 100% of the trailing median. [measured]
  - Ranker v3 (the PM's cause): ruled in, with caution. The desktop drop starts exactly on 09-07 and persists every day through 09-13. [measured] Mobile also moved to v3 but shows zero change, so v3 would have to be harmless on mobile and harmful on desktop. Another desktop-specific change on that date would look the same. [inferred]
  - Mobile as a control: it can't serve as a clean control. It shares the v3 rollout, so it shows only that the effect is desktop-specific. [inferred]
- Checks run:
  - completeness: pass. 2026-09-13 has 4 rows, 100% of the trailing median.
  - mix_shift: pass. Overall change -1.80 pp = within-segment -1.80 pp + mix +0.00 pp (mix share 0%).
  - fanout: skipped. I ran no joins.
  - srm: skipped. This is a pre/post comparison, not a randomized experiment.

## Caveats, and what would change the answer
- This is a before/after comparison at 100% rollout with no concurrent control. Any other desktop change on 09-07 (UI, logging, or a desktop client release) would be counted as v3. A holdout or staged rollback on desktop would separate them.
- Mobile CTR equal to four decimals across weeks looks unusually clean. Check whether v3 actually serves mobile traffic, or whether the mobile rows are carried over from the prior week.
- Only 2 weeks of data and no sampling variance. The interval is omitted because the figures are aggregate counts, not a sample estimate.
- CTR is the only metric here. Whether v3 improves downstream outcomes such as conversions is not tested.