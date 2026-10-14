## Answer
Headline: 50.05 % (49.93 to 50.18 %) [q4]
Search CTR for 2026-10-05 to 2026-10-11 was 50.05%, i.e. 321,780 searches with a click out of 642,880 external searches with results. [q4]
- Observed: 50.05 % (49.93 to 50.18 %) [q4]
- Adjusted: not computed (single level question, no comparison period; the table holds only this week)
- Causal effect: not identified (no change or comparison was asked about)

## What it means for the weekly business review
This is a level for reporting, not a change; no threshold was given, so there is no decision cut-off to compare with. The interval is about ±0.12 pp wide. [q4]

## Why we believe it
- Alternatives considered:
  - Counting clicks instead of searches with a click: ruled out; per-click counting would give 70.07%, which overstates CTR, and metrics.json says to use searches_with_click [q4] [measured]
  - Bot and internal traffic inflating or deflating the rate: ruled out by filtering to traffic_type = 'external' as the metric requires [q3] [measured]
  - Incomplete week: ruled out, all 7 days have all 6 segment rows [q2] [measured]
  - Platform mix: desktop and mobile are about equal in size [q4] [inferred]
- Checks run:
  - completeness: pass 2026-10-11 has 6 rows, 100% of the median [check:completeness#1]
  - mix_shift: skipped, there is no prior period in the table to compare against
  - fanout: skipped, no joins used

## Caveats, and what would change the answer
- The table holds only 2026-10-05 to 2026-10-11, so no week-over-week comparison or same-weekday history is possible; pulling earlier weeks would allow one.
- The interval is a binomial interval treating searches as independent; repeat users would make it somewhat wider.
- No dashboard figure was available to reconcile against.

## Provenance
- Metric: searches_with_click / searches_with_results, traffic_type = 'external', from metrics.json
- Data: search_daily_v, through 2026-10-11
- Reconciled: not done (no dashboard value for this week supplied)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (15 numbers on 7 lines; 3 queries, 1 checks, 0 given)