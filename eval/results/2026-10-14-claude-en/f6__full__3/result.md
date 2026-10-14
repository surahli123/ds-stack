## Answer
Headline: +50.05 percent CTR (49.93 to 50.18) [q6]
Search CTR for 2026-10-05 to 2026-10-11 was 50.05%: 321,780 searches with a click out of 642,880 external searches with results [q6]
- Observed: +50.05 percent (49.93 to 50.18), a level, not a change; binomial interval [q6]
- Adjusted: not computed (no prior week in the warehouse, so no change to decompose; the data covers 2026-10-05 to 2026-10-11 only) [q5]
- Causal effect: not identified (this is a level, not an effect of anything)

## What it means for the weekly business review
Report 50.05%, to the nearest 0.1 pp; the interval is about ±0.12 pp [q6]. No decision threshold was given, and no week-over-week comparison is possible from this table [q5].

## Why we believe it
- Alternatives considered:
  - Counting clicks instead of searches with a click: ruled out; clicks/searches_with_results would give 70.07%, which breaks the metric definition [q6] [measured]
  - Bot and internal traffic inflating the count: ruled out; filtered to external, which excludes 105,117 bot and 35,062 internal searches [q4] [measured]
  - Day of week or one odd day: ruled out as a driver of the level; daily CTR stays between 49.87% and 50.17% [q2] [measured]
  - Platform mix: not applicable to a single-week level; desktop and mobile each sit near 50% [q3] [measured]
  - Incomplete data: ruled out; all 7 days are present with similar volume [q5, check:completeness#1] [measured]
- Checks run:
  - completeness: pass; 2026-10-11 has 102% of the trailing-day median [check:completeness#1]
  - fanout: skipped, no joins were used
  - mix_shift: skipped, the rate did not move between two periods because only one week exists
  - srm: skipped, not an experiment

## Caveats, and what would change the answer
- Metric reconciliation against the dashboard was not done; metrics.json says it matched the dashboard on 2026-10-01 only. Compare 50.05% with the dashboard tile before publishing.
- The interval treats searches as independent; repeat users would widen it slightly.
- There is no prior week, so I can't say whether CTR moved. A previous week's data is needed for that.

## Provenance
- Metric: searches_with_click / searches_with_results, traffic_type = 'external', from metrics.json (ctr)
- Data: search_daily_v, through 2026-10-11
- Reconciled: not done (the dashboard figure is not available here)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (20 numbers on 10 lines; 5 queries, 1 checks, 0 given)