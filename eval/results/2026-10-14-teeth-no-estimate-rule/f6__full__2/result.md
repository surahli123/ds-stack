## Answer
Headline: 50.05 % CTR (95% CI 49.93 to 50.17 %, binomial on the q5 counts) [q5]
External search CTR for 2026-10-05 to 2026-10-11 was 50.05%: 321,780 searches with a click out of 642,880 searches with results. [q5]

## What it means for the weekly business review
This is a level for one week, not a change, so there is no decision threshold to compare the interval against; report 50.05% (about ±0.12 pp). [q5]

## Why we believe it
- Alternatives considered:
  - Counting clicks instead of searches with a click: ruled out; that gives 70.07%, which overcounts multi-click searches and is the pitfall named in metrics.json [q5] [measured]
  - Using all searches as the denominator: ruled out; that gives 46.05%, but metrics.json uses searches with results [q5] [measured]
  - Bot and internal traffic included: ruled out by the external-only filter; bot and internal rows are separate in the data [q4] [measured]
  - Incomplete week or missing days: ruled out; all 7 days have 6 rows each [q3] [measured]
  - Mix-shift, seasonality, logging change: not assessed; the table holds only this one week, so there is no comparison period [q3] [inferred]
- Checks run:
  - completeness: pass 2026-10-11 has 6 rows, 100% of the trailing-day median [check:completeness#1]
  - mix_shift: skipped, no prior period in the data and the question asks for a level, not a change
  - fanout: skipped, no joins
  - srm: skipped, not an experiment

## Caveats, and what would change the answer
- The interval treats searches as independent and ignores day-to-day variation; it is approximate.
- Completeness is judged only against days within this week, as there is no earlier history.
- Not reconciled with the dashboard, which I can't access; if the dashboard differs by more than 0.1 pp, the filters should be re-checked.

## Provenance
- Metric: searches_with_click / searches_with_results, traffic_type = 'external', grain search, from metrics.json
- Data: search_daily_v, through 2026-10-11
- Reconciled: not done (no dashboard access; metrics.json notes a 0.1 pp match on 2026-10-01)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (14 numbers on 7 lines; 3 queries, 1 checks, 0 given)