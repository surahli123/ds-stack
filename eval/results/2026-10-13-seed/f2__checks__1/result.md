## Answer
Headline: 55.0 % (95% interval 54.9 to 55.0)
Navigational queries in 2026-W40 had a click-through rate of 55.0%: 32,878 clicks on 59,800 searches across 400 queries. [measured]

## What it means for the planning doc
You can use 55.0%. The interval is about ±0.03 points, so sampling noise doesn't matter. The label definition does. Using the older v1 labels gives 43.0%, a 12-point difference.

## Why we believe it
- Alternatives considered:
  - Using the old v1 labels: ruled out. 100 queries were relabeled from navigational to informational and 100 went the other way in v2. Only is_current=1 is the current labeling, and each query has exactly one current row. [measured]
  - Joining all label rows with no current filter: ruled out. It gives 44.99% and double-counts relabeled queries. [measured]
  - Averaging per-query CTRs instead of dividing total clicks by total searches: not run. I used total clicks over total searches. [guess]
- Checks run:
  - completeness: could not run. The table holds only W40, so there is no earlier history to compare with. Query coverage is 1,000 of 1,000 labeled queries. [check:completeness#1]
  - fanout: pass. The join of stats to current labels gave 1,000 rows from 1,000, with no duplicates. [check:fanout#1]
  - srm and mix_shift: skipped. This is not an experiment, and no rate comparison was made.

## Caveats, and what would change the answer
- "Navigational" depends on which label version marketing means. 55.0% is for current labels, which mix v1 and v2.
- The interval is a ratio-estimator interval that treats queries as independent. It only covers sampling noise, not label errors.
- Whether W40 is fully loaded is unconfirmed, because there is no history to compare. The row counts look complete.
- metrics.json does not exist, so the CTR definition (clicks / searches) is my assumption.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches), navigational per is_current=1 labels, stated here [guess]
- Data: query_stats joined to query_labels, W40 only (the only week present)
- Reconciled: not done (no dashboard or source available)
- Queries and checks: the queries were run inline and not saved. The checks are logged in .ds-checks.log.