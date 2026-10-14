## Answer
Headline: +46.05 % search CTR (95% CI 45.93 to 46.17) [q6]
Search CTR for 2026-10-05 to 2026-10-11 was 46.05% on external (non-bot, non-internal) traffic: 321,780 searches with a click out of 698,782 searches [q5, q6].
- Observed: +46.05 % (45.93 to 46.17) external-only; all traffic including bots and internal is 41.41 % (41.31 to 41.52) [q5, q6]
- Adjusted: not computed (single week, no comparison period, so no change to decompose)
- Causal effect: not identified (no intervention or comparison; this is a level, not a change)

## What it means for the weekly business review
Report the level at 46.05% (interval about ±0.1 pp) [q6]; no decision threshold was given, so nothing to compare the interval with. If the review's standard counts bot and internal traffic, the figure is 41.41% instead, a 4.6 pp gap that is much larger than the interval [q5].

## Why we believe it
- Alternatives considered:
  - Bot traffic deflating CTR: ruled in as a reason to exclude it; bot CTR is 1.97% on 105,117 searches (12.5% of volume) [q4] [measured]
  - Internal traffic inflating CTR: ruled in as a reason to exclude it; internal CTR is 67.2% [q4] [measured]
  - Platform mix: ruled out for the level; desktop 46.06% and mobile 46.04% external CTR are nearly identical [q4] [measured]
  - Clicks/searches as the definition: ruled out as CTR here since it counts multiple clicks per search; it is 64.5% external [q5] [guess]
  - Incomplete week: ruled out, all 7 days have all 6 segment rows [q2] [measured]
- Checks run:
  - completeness: pass 2026-10-11 has 6 rows, 100% of trailing median [check:completeness#1]
  - mix_shift: skipped, no comparison period exists (table starts 2026-10-05)
  - fanout: skipped, no joins
  - srm: skipped, not an experiment

## Caveats, and what would change the answer
- No metrics.json: the definition is my guess. Excluding bot/internal and using searches_with_click/searches changes the number from 41.41% to 46.05%. Confirm which the WBR uses.
- No earlier weeks in the table, so I can't say whether the level is up or down, or run a seasonality check.
- Interval is sampling-only (normal approximation), and assumes searches are independent.

## Provenance
- Metric: searches_with_click / searches, traffic_type = external, 2026-10-05..2026-10-11, from stated here [guess]
- Data: search_daily_v, through 2026-10-11
- Reconciled: not done (no dashboard or metrics.json available)
- Queries and checks: .ds-queries.log, .ds-checks.log
- Verified: verify_readout: pass (27 numbers on 10 lines; 4 queries, 1 checks, 0 given)