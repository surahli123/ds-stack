## Answer
Headline: 54.98 % (54.95 to 55.01) [q5, q6]
Navigational queries had a click-through rate of 54.98% in 2026-W40: 32,878 clicks on 59,800 searches across 400 queries [q5]. This is measured.
- Observed: 54.98 % (54.95 to 55.01) [q5, q6]
- Adjusted: not computed (single week, no comparison, so nothing moved)
- Causal effect: not identified (no intervention in question; this is a level, not a change)

## What it means for the marketing planning doc
Use about 55% for navigational CTR; the interval is under 0.1 pp wide [q6], so sampling noise would not change a planning figure. No decision threshold was given, so the real risk is the label definition below, not noise.

## Why we believe it
- Alternatives considered:
  - Stale labels (all label versions joined): ruled out by using only is_current=1 rows, one per query (1000 rows, 1000 distinct) [q4] [measured]
  - Relabeling changes the answer: version-1 labels no longer current show navigational CTR of 25.0% [q7], close to informational [q5]. Including them would give a wrong number [measured]
  - Mix-shift, seasonality, day of week: not applicable, since this is a single-week level, not a change [inferred]
  - Data completeness: only W40 exists in the table, so I could not compare it with earlier weeks [q2] [measured]
- Checks run:
  - fanout: pass, join of stats to current labels is many_to_one with 1000 rows in and out [check:fanout#1]
  - completeness: could not run, no earlier weeks to compare with [check:completeness#1]
  - mix_shift: skipped, no before/after comparison
  - srm: skipped, not an experiment

## Caveats, and what would change the answer
- No metrics.json was available, so the CTR definition is my own. If marketing defines CTR per search session or per unique user, the number would differ.
- The interval treats queries as the sampling unit (ratio estimator, computed from q6 sums). It does not cover week-to-week variation. Only one week was loaded, so W40 completeness is unconfirmed; the row count of 1000 queries looks complete [q2].
- Navigational is defined by current labels (label_version 1 and 2 with is_current=1). A different labeling convention would change the query set.

## Provenance
- Metric: CTR = sum(clicks)/sum(searches) over queries whose current label (is_current=1) is navigational, week 2026-W40, from query_stats joined to query_labels; stated here [guess]
- Data: query_stats, query_labels, through 2026-W40
- Reconciled: not done (no dashboard or other source available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (18 numbers on 7 lines; 5 queries, 2 checks, 0 given)