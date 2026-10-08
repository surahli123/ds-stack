## Answer
Headline: about 0.0 pp attributable to v2 (within-segment effect −0.0001 pp; the overall drop of −2.10 pp is almost entirely mix shift)
Overall CTR fell from 30.42% to 28.32% (−2.10 pp), but CTR within every platform×country segment is unchanged. The drop comes from traffic moving to mobile, which has a lower CTR. [measured]

## What it means for the rollback decision
The CTR drop gives no reason to roll back v2: it does not show v2 hurting ranking. Don't roll back on this evidence. Find out why mobile share rose from 40% to 55%, for example a campaign, an app release, or a logging change. [inferred]

## Why we believe it
- Alternatives considered:
  - v2 lowered relevance (the PM's theory): ruled out as the main driver. Within-segment CTR is identical before and after in all four segments, for example desktop_US 37.08% to 37.08% and mobile_US 22.66% to 22.66%. [measured]
  - Mix shift toward mobile: ruled in, at 100% of the change (−2.10 pp). Mobile share went from 40% to 55% of searches. Desktop CTR is about 35–37% and mobile about 21–23%. [measured]
  - Seasonality and day of week: ruled out. Both periods are full Monday–Sunday weeks, and the segment rates are flat day to day. [inferred]
  - Incomplete data: ruled out. All 14 days have 4 rows each. [measured]
  - Why mobile share rose: not determined. It coincides with the v2 rollout date, and nothing in the data separates the two. [guess]
- Checks run:
  - mix_shift: fail. Mix effect is −2.10 pp and the within-segment effect is −0.00 pp (mix share 100%). The fail flags the mix shift, and it changes the answer: the v2 effect is about 0, not −2.1 pp.
  - completeness: pass. 2026-10-04 has 4 rows, 100% of the trailing median.
  - srm: skipped. This is not a randomized experiment, because v2 went to 100% of traffic at once.
  - fanout: skipped. No joins were used.

## Caveats, and what would change the answer
- There is no concurrent v1 control. Every row after 09-28 is v2 and every row before is v1, so "no within-segment change" is a before/after comparison. A change that moved all segments at once would not show up here.
- If the mobile surge was itself caused by v2, for example through a UI or traffic-routing change, v2 would be indirectly responsible for the drop. Checking this needs traffic-source data or a holdout.
- CTR is the only metric examined. v2 could still affect clicks, conversion, or satisfaction in ways CTR doesn't show.
- Only four coarse segments were available. Finer segments could hide a within-segment effect.