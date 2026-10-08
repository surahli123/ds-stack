```
## Answer
Headline: about 0.0 pp attributable to v2 (within-platform effect −0.0001 pp). Overall CTR fell 2.10 pp, from 30.42% to 28.32%, and that fall is almost entirely a shift in platform mix.
Mobile's share of searches rose from 40% to 55%. Mobile CTR is about 22% and desktop is about 36%, so the blend dropped. CTR within each platform and country did not move. [measured]

## What it means for the rollback decision
The data gives no reason to roll back v2 on CTR grounds. Rolling back would not bring back the 2.1 pp, because the drop comes from the traffic mix. The data also can't prove v2 is harmless, because v2 shipped to 100% of traffic with no holdout (see caveats).

## Why we believe it
- Alternatives considered:
  - v2 lowered CTR: ruled out as the main driver. Desktop CTR was 36.029% before and 36.029% after. Mobile CTR was 22.018% before and 22.018% after. Within-segment effect was −0.0001 pp. The US/other split inside each platform was also flat. [measured]
  - Mix shift (more mobile traffic): ruled in. It explains 99.99% of the −2.10 pp, and the desktop share fell from 60% to 45%. [measured]
  - Day of week or seasonality: ruled out as the main driver. Both weeks cover the same Monday-to-Sunday span, and daily volumes are nearly identical (~100k searches per day). Within-segment CTR is flat, so there is nothing seasonal to explain. [inferred]
  - Incomplete data or a logging change: ruled out. All 14 days have 4 rows each (2 platforms × 2 countries), and the last day is 100% of baseline. Total volume is flat, and a logging change would have shifted segment CTR. [measured]
  - Why mobile share rose: not determined. It could be a campaign, an app release or a traffic-source change. It happened on the same day as the v2 rollout, and the data can't tell the two apart. [guess]
- Checks run:
  - completeness: pass. 2026-10-04 has 4 rows, which is 100% of the trailing median.
  - mix_shift: fail. The check flags a mix-driven change: −2.10 pp total = −0.00 pp within-segment + −2.10 pp mix. This confirms the finding above.
  - fanout: skipped. No joins were used.
  - srm: skipped. This is a before/after comparison, not an experiment with assignment counts.

## Caveats, and what would change the answer
- There is no concurrent v1 control. v2 switched on for all traffic on the same day, so a before/after comparison can't fully separate v2 from anything else that changed that day. The flat within-segment CTR suggests v2 had no effect on CTR at this level of aggregation. [inferred]
- The data is daily aggregates by platform and country only. A v2 effect that differs by query type, or one that offsets itself across them, would not show up here.
- Tracing why mobile share jumped (a marketing push, an app release, or v2 changing the platform mix of searches) would show whether the mix shift is separate from v2. A holdout of v1 traffic would settle the question of a v2 effect.
```