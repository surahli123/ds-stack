## Answer
Headline: can't tell. The data gives no sign that v2 lowered CTR, but a rollout to 100% of traffic can't prove that.

Overall CTR fell 2.1 points, almost entirely because traffic shifted from desktop to mobile. Within each platform and country, CTR didn't move.
- Observed: −2.10 pp (−2.25 to −1.95), from 30.42% to 28.32% [measured]
- Adjusted: −0.01 pp (−0.16 to +0.15), holding platform × country mix fixed at the week-1 mix [measured]
- Causal effect: not identified. Everyone moved to v2 on the same day, so there was no concurrent v1 control group. Identifying it would take a holdout or an A/B split, or a staggered rollout. The within-segment comparison, an adjusted effect near zero, is the best available proxy.

## What it means for the rollback decision
The 2.1 pp drop is not evidence against v2. The adjusted interval rules out a v2 effect worse than about −0.16 pp within segments, and the roughly −2 pp headline comes from mix. I'd hold off on a rollback based on this drop. The one caveat is below: if v2 itself caused the mix shift, the drop could still be v2's.

## Why we believe it
- Alternatives considered:
  - Mix shift to mobile (mobile CTR is about 22% against about 36% for desktop): ruled in. Mobile's share of searches rose from 40% to 55% while each segment's CTR stayed flat [measured].
  - A v2 effect on CTR within segments: ruled out as large. All four segments moved by 0.1 pp or less, and the pooled interval is ±0.16 pp [measured].
  - v2 caused the shift to mobile: not ruled out. A ranker is unlikely to change which device people search from, but nothing here tests it, and total search volume was flat [inferred].
  - Seasonality or other concurrent changes: not ruled out. There are only two weeks of data, and release_log lists only the v2 rollout [guess].
- Checks run:
  - Segment-level CTR before and after: pass. The four platform × country cells are flat.
  - Daily series for the two weeks: pass. Searches per day are stable and the CTR step lines up with 09-28.
  - Control group or holdout: could not run. v2 went to 100% of traffic on day one.
  - Longer pre-period baseline for week-to-week noise: skipped. The table only covers these two weeks.

## Caveats, and what would change the answer
- Evidence of a mix shift caused by v2, such as a mobile-specific change shipped with it, would make part of the 2 pp attributable to v2.
- Only these two weeks are available, so I can't tell whether a 2 pp week-over-week move is unusual.
- The intervals treat searches as independent, so they are probably a little too narrow, because clicks cluster by user and day.
- Platform × country is the only adjustment available. Query type or user mix could also have shifted.

## Provenance
- Metric: CTR = clicks / searches, from stated here [guess]. No metrics.json was present.
- Data: search_daily and release_log, through 2026-10-04.
- Reconciled: not done (no dashboard or other source available).
- Queries and checks: ad hoc inline Python against warehouse.db, with no saved scripts. Adjusted = direct standardization to the week-1 mix, with binomial standard errors.