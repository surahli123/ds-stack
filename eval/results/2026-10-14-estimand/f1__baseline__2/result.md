## Answer
Headline: about 0.0 pp (−0.15 to +0.15 pp) attributable to v2, on a mix-adjusted basis, not a randomized effect.
Overall CTR fell 2.1 pp (30.4% to 28.3%) because traffic shifted toward mobile, which has a lower CTR. CTR within each platform and country segment didn't change.
- Observed: −2.10 pp (−2.25 to −1.95) [measured]
- Adjusted: −0.00 pp (−0.15 to +0.15), holding platform × country mix fixed [measured]
- Causal effect: not identified (v2 went to 100% of traffic the same day the mix shifted, so there is no concurrent control group. A holdout or an A/B split would identify it.)

## What it means for the rollback decision
The drop is almost entirely a mix change. Even the worst end of the interval is only −0.15 pp, a small fraction of the −2.1 pp drop the PM is worried about. So this data gives no reason to roll back v2 because of CTR. It also can't show that v2 is harmless, because mix and v2 changed together.

## Why we believe it
- Alternatives considered:
  - Traffic mix shift: ruled in. Mobile share of searches rose from about 40% to about 55% (e.g. mobile/US 22% to 30%), while per-segment CTR was flat to within about 0.1 pp. [measured]
  - v2 lowering CTR within segments: ruled out as a large effect. The standardized within-segment change is −0.002 pp, with a CI of ±0.15 pp. [measured]
  - Why mobile traffic rose (a promotion, a seasonal pattern, or v2 changing the traffic mix): not determined. [guess]
  - Other concurrent changes (tracking, UI, seasonality): the data has no log of them. The release_log table has only the v2 entry. [inferred]
- Checks run:
  - Volume: pass. Total searches are about 100k per day in both weeks.
  - Segment-level before/after CTR: pass. All four segments are within 0.1 pp.
  - Standardized decomposition: pass. Segments were weighted at the pooled two-week mix. The CI is binomial only.

## Caveats, and what would change the answer
- This is a pre/post comparison over one week each, with no holdout.
- v2 could affect the mix itself, for example by changing which users search on mobile. That would not show up in the within-segment CTR.
- The CI ignores day-to-day variance and uses only binomial sampling error. Segments are coarse (platform × country only).
- A 5–10% holdout on v1, or the cause of the mobile surge, would settle it.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches) [guess]. There is no metrics.json, so I used this definition.
- Data: search_daily (56 rows, 4 segments × 14 days) and release_log, through 2026-10-04.
- Reconciled: not done (no dashboard or source figure to compare against).
- Queries and checks: ad hoc Python/sqlite3 run inline in this session, not saved to a file.