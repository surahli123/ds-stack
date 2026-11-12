## Answer
Headline: +50.05 % (49.93 to 50.18) [q4]
Search CTR for 2026-10-05 to 2026-10-11 was 50.05%, i.e. 321,780 clicked searches out of 642,880 searches with results (external traffic) [q4]. (The signed "+" is just the readout format; this is a level, not a change.)
- Observed: +50.05 % (49.93 to 50.18) [q4]
- Adjusted: not computed (no comparison period, so there is no change to adjust; the table only holds this one week [q5])
- Causal effect: not identified (a single level, not a change; no experiment or intervention is asked about)

## What it means for the weekly business review
This is a level, not a change; no decision threshold was given. Desktop (50.06%) and mobile (50.04%) agree, so the figure is not driven by one platform [q4].

## Why we believe it
- Alternatives considered:
  - Counting clicks instead of clicked searches: ruled out by using searches_with_click; clicks would give a higher number because multi-click searches count repeatedly [q4] [measured]
  - Bot/internal traffic inflating the rate: ruled out by filtering traffic_type='external' per the metric definition [q4] [measured]
  - Incomplete week: ruled out, all 7 days present with 6 rows each [check:completeness#1] [measured]
  - Mix-shift, seasonality, logging changes: not ruled out; the table holds only 2026-10-05 to 2026-10-11, so no earlier week exists to compare [q5] [inferred]
- Checks run:
  - completeness: pass 2026-10-11 has 6 rows = 100% of trailing median [check:completeness#1]
  - mix_shift: skipped, no comparison period to decompose
  - fanout: skipped, no joins
  - srm: skipped, not an experiment

## Caveats, and what would change the answer
- The interval is a normal-approximation binomial interval treating searches as independent (computed by hand from the q4 counts, not a logged query); clustering by user would widen it.
- Not reconciled to the dashboard; if it differs by more than 0.1 pp, the dashboard's definition should be checked.
- Only one week is in the warehouse, so week-over-week change cannot be given.

## Provenance
- Metric: searches_with_click / searches_with_results, traffic_type='external', from metrics.json
- Data: search_daily_v, through 2026-10-11
- Reconciled: not done (the weekly business review dashboard figure was not available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (15 numbers on 6 lines; 2 queries, 1 checks, 0 given); ds-verify: pass (0 fail, 0 could not verify, 0 warn, 16 pass)