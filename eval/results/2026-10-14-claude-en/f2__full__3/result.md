```
## Answer
Headline: 55.0 % (54.6 to 55.4) [q5]
Navigational queries had a click-through rate of about 55.0% in 2026-W40, using each query's current intent label. [q5]
- Observed: 55.0 % (54.6 to 55.4) [q5]
- Adjusted: not computed (single week, no comparison, so no mix_shift)
- Causal effect: not identified (this is a level, not an effect)

## What it means for the planning doc
Use about 55%. Using the stale v1 labels gives 43.0% instead, so the label choice matters by about 12 pp. [q8, q5]

## Why we believe it
- Alternatives considered:
  - Stale labels: 300 queries have a non-current v1 label, and 100 of the 300 navigational v1 labels are non-current; filtering is_current=1 gives one label per query (0 duplicates) [q2, q4] [measured]
  - Label version mix: v1 and v2 navigational CTR agree (55.0% vs 55.0%), so version doesn't change the answer [q6] [measured]
  - Definition: CTR is clicks/searches pooled, not an average of per-query rates [q5] [measured]
  - Data quality: no zero-search rows and no clicks above searches [q7] [measured]
- Checks run:
  - fanout: pass row counts consistent with a many_to_one inner join [check:fanout#1]
  - completeness: could not run, only one week in the table [check:completeness#1]
  - mix_shift: skipped, no second period to compare

## Caveats, and what would change the answer
- Interval is a binomial interval on pooled searches (59800) and ignores clustering by query, so it is somewhat too narrow. [q5]
- Only W40 is in the table, so completeness of the week can't be confirmed.
- CTR definition (clicks / searches, current labels) is my choice, not from a metrics file.

## Provenance
- Metric: sum(clicks)/sum(searches) over navigational queries (is_current=1 label), week 2026-W40, from stated here [guess]
- Data: query_stats, query_labels, through 2026-W40
- Reconciled: not done (no dashboard or metrics.json available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (17 numbers on 6 lines; 6 queries, 2 checks, 0 given)
```