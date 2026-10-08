## Answer
Headline: -1.80 pp (no statistical interval: this is a single before/after comparison with no holdout)
Overall CTR fell from 30.42% to 28.62%. All of the drop is within desktop (US -3.1 pp, other -2.9 pp). Mobile is exactly flat, and mix did not shift. Practically all of the -1.8 pp coincides with v3, but that is a timing link, not a controlled test.

## What it means for the v3 rollback decision
v3 is the only logged change that lines up with a drop of this size, so the data points to v3 hurting desktop CTR (inferred). I'd treat it as a real regression on desktop and not as a traffic-mix artifact. Before you commit to a rollback, confirm with a desktop holdout or a rollout log check, because there is no control group here.

## Why we believe it
- Alternatives considered:
  - Mix shift (platform/country): ruled out. The segment weights are identical across the two weeks (33/27/22/18%), so the mix effect is 0.00 pp and the whole -1.80 pp is a within-segment change [measured].
  - Day of week / seasonality: ruled out for the most part. Both windows are full Monday–Sunday weeks. Daily search volumes are identical day by day across the weeks, and mobile CTR is unchanged. One week of history can't rule out a broader seasonal shift [measured for the volume and mobile evidence, inferred for the rest].
  - Data completeness or logging problem: partly ruled out. Both weeks have 28 rows (4 segments × 7 days) and no gaps [measured]. A desktop-only logging change at the same moment can't be excluded from this table [guess].
  - v3 effect on mobile: nothing found. Mobile clicks are identical to the click across the weeks, even though the ranker label reads v3. That is unusually exact, so mobile may not actually be running v3, or the mobile data may be carried over [measured, cause unknown].
  - PM's claim that v3 caused the drop: consistent with the data but not proven. The drop starts on the rollout day, 2026-09-07, and sits in desktop only. With no holdout, anything else that changed that day is confounded with v3 [inferred].
- Checks run:
  - mix_shift: pass. -1.80 pp = within-segment -1.80 pp + mix 0.00 pp. Desktop US contributes -1.02 pp and desktop other -0.78 pp.
  - completeness: could not run. The tool needs at least 3 periods and only 2 weeks exist. I checked the row counts by hand instead: 28 rows in each week.
  - fanout: skipped. No joins were used.
  - srm: skipped. This was a 100% rollout, so there are no assignment counts.

## Caveats, and what would change the answer
- There is no concurrent control. A holdout or staged-rollout data would give a real causal estimate. If some desktop traffic stayed on v2 and its CTR also fell, the cause is not v3.
- The mobile figures are suspiciously exact. Check whether mobile actually serves v3. If it doesn't, the real v3 effect is the desktop drop only (about -3 pp on desktop, which is 60% of searches).
- Check for other changes on 2026-09-07, such as a desktop UI change, a tracking change, or a marketing push. Any of them would shrink the share attributable to v3.
- Only one week of history is available, so week-to-week noise can't be estimated.