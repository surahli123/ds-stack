## Answer
Headline: +0.00 pp (95% CI about −0.15 to +0.15 pp) from v2's within-segment effect on CTR. The overall drop is −2.10 pp.
Overall CTR fell from 30.42% to 28.32% (−2.10 pp). Essentially all of that is a shift in traffic mix toward mobile, which has a lower CTR. CTR within each platform and country segment didn't change.

## What it means for the rollback decision
Your PM's claim is that v2 caused the drop. This data shows no per-segment CTR harm from v2, with a bound of about ±0.15 pp. A harm smaller than that would be too small to see here. A change in how users reach search that happened at the same time as the rollout would explain the drop. Rolling back v2 would not be expected to restore the 2.1 pp. The one thing that could change this is if v2 itself caused the mobile shift. That is untested here (see Caveats).

## Why we believe it
- Alternatives considered:
  - v2 lowered CTR within segments: ruled out by the four platform×country segments, which differ by −0.0 to +0.1 pp (desktop US 37.07→37.07, desktop other 34.79→34.71, mobile US 22.66→22.71, mobile other 21.24→21.25). The standardized effect is +0.003 pp, CI ±0.15 pp [measured].
  - Traffic mix shift: ruled in. Mobile share rose from 40.1% to 55.1% of searches, and the mix term is −2.10 pp of the −2.10 pp total [measured].
  - v2 caused the mobile surge (so rollback would indirectly matter): not ruled out, because the rollout was at 100% and there is no concurrent control group [guess].
  - Normal week-to-week noise: ruled out for the overall drop. Daily CTR was 30.1–30.8% before and 28.1–28.6% after, with no overlap [measured].
- Checks run:
  - Rate vs. mix decomposition (week 1 weights vs. week 2 weights): pass. Rate term −0.008 pp, mix term −2.100 pp.
  - Binomial CI on the standardized rate effect: pass. It treats searches as independent, so the real interval is probably somewhat wider [inferred].
  - Daily trend: pass. The step is at 09-28 and then flat; no pre-trend within the week.
  - Mix-shift cause: could not run. The data has no traffic-source, app-release or marketing fields.

## Caveats, and what would change the answer
- Only one week before and one week after, with v1 and v2 never running side by side. Any simultaneous change is confounded with v2.
- I can't tell why mobile traffic rose. Find out whether a mobile release, a campaign or an outage on desktop coincided with 09-28. If v2 is shown to push users toward mobile, the picture changes.
- Segments are only platform×country. Unseen segments, such as query type, could hide a v2 effect that offsets the mix.
- Searches are treated as independent. Clustering by user would widen the interval.

## Provenance
- Metric: CTR = clicks / searches, from stated here [guess]. No metrics.json was present.
- Data: search_daily and release_log in warehouse.db, 2026-09-21 through 2026-10-04 (both weeks complete).
- Reconciled: not done (no dashboard or other source available).
- Queries and checks: ad hoc Python/SQLite run in this session, not saved to a file. The queries are the daily and segment aggregations and the decomposition shown above.