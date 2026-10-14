## Answer
Headline: 46.0% (no interval; this is a full-population rate, not a sample estimate)
Search CTR for 2026-10-05 to 2026-10-11 was 46.0%, counting searches with at least one click over external (real-user) searches. Bots and internal traffic are excluded. [measured]
- Observed: 46.0% for external traffic. Unfiltered across all traffic it is 41.4%, which is diluted by bot traffic. [measured]
- Adjusted: not computed (there is no comparison period or contrast to adjust)
- Causal effect: not identified (this is a level, not a change, so there is nothing to attribute)

## What it means for the weekly business review
Report 46.0% as the external-traffic CTR. The definition choice moves the number by several points: 41.4% with bots included, 47.1% with internal traffic included, and 64.5% if CTR is clicks per search. Use the 46.0% only if the review's definition is searches with a click divided by searches, external only.

## Why we believe it
- Alternatives considered:
  - Include bots: ruled out. Bots are 12.5% of searches and click at only about 2%, which drags the rate down artificially [measured].
  - Include internal traffic: ruled out. It is employee traffic and clicks at about 67%. Including it gives 47.1% [measured, inferred that it should be excluded].
  - Clicks/searches instead of searches-with-click/searches: ruled out because the second is the standard per-search CTR. The first gives 64.5% [inferred].
- Checks run:
  - completeness: pass. 2026-10-11 has 6 rows, 100% of the trailing median, and all 7 days have 6 rows each [check:completeness#1].
  - fanout, srm, mix_shift: skipped. There are no joins, no experiment, and no period comparison.

## Caveats, and what would change the answer
- No metrics.json exists, so the CTR definition and the exclusion of bot and internal traffic are my assumptions. If your official definition differs, the number changes as listed above.
- I did not reconcile against a dashboard.
- I did not check whether the bot filter is complete.

## Provenance
- Metric: searches_with_click / searches, traffic_type = external, summed over desktop and mobile. This is stated here [guess], because no metrics.json exists.
- Data: search_daily_v, 2026-10-05 to 2026-10-11, all 7 days loaded.
- Reconciled: not done (no dashboard or source available).
- Queries and checks: ad-hoc Python/sqlite queries in this session; the check result is logged in .ds-checks.log (completeness#1).