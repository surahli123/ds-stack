## Answer
Headline: +50.05 % CTR (95% CI 49.93 to 50.17) [q5]
Search CTR for 2026-10-05 to 2026-10-11 was 50.05%: 321,780 searches with a click out of 642,880 external searches with results [q5]. [measured]
- Observed: +50.05 % (95% CI 49.93 to 50.17), a level, not a change [q5]
- Adjusted: not computed (only this one week is in the table, so there is no comparison week to adjust against) [q4]
- Causal effect: not identified (no comparison and no experiment; a prior week and a known change would be needed)

## What it means for the weekly business review
This is a level for reporting, so no decision threshold applies; the interval is about ±0.12 pp [q5]. Using total clicks instead of searches with a click would give 70.07%, which is wrong for this metric [q5].

## Why we believe it
- Alternatives considered:
  - Clicks-based definition (the pitfall in metrics.json): ruled out because the numerator is searches_with_click, and the clicks-based figure is 70.07% [q5] [measured]
  - Bot and internal traffic in the mix: ruled out because the filter is traffic_type = 'external' [q5] [measured]
  - Incomplete week: ruled out because all 7 days are present with 6 rows each [q4, check:completeness#1] [measured]
  - Mix-shift, seasonality and logging changes: not assessable, since there is no prior week in the table [q4] [inferred]
- Checks run:
  - completeness: pass 2026-10-11 has 6 rows, 100% of the trailing median [check:completeness#1]
  - mix_shift: skipped, no comparison period exists, and this is a level rather than a move
  - fanout: skipped, no joins were used
  - srm: skipped, not an experiment

## Caveats, and what would change the answer
- Table holds only 2026-10-05 to 2026-10-11, so no week-over-week change or trend can be given. Prior weeks would settle this.
- The completeness baseline is only the trailing days of the same week, so a whole-week undercount would not be visible.
- The interval treats searches as independent; user-level clustering would widen it.
- Not re-reconciled to the dashboard this session; the metrics.json note says the 2026-10-01 version matched.

## Provenance
- Metric: searches_with_click / searches_with_results, traffic_type = 'external', grain search, from metrics.json
- Data: search_daily_v, through 2026-10-11
- Reconciled: not done (the dashboard figure for this week is not available here)
- Queries and checks: .ds-queries.log, .ds-checks.log
- Verified: verify_readout: pass (16 numbers on 7 lines; 2 queries, 1 checks, 0 given)