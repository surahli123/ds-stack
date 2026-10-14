## Answer
Headline: 55.0 % (54.6 to 55.4 %, binomial interval that ignores query-level clustering)
Navigational queries had a click-through rate of about 55.0% in 2026-W40: 32,878 clicks on 59,800 searches across 400 queries.
- Observed: 55.0 % (54.6 to 55.4 %)
- Adjusted: not computed (this is a single level, not a comparison)
- Causal effect: not identified (this is a descriptive rate, so there is no intervention to estimate)

## What it means for the planning doc
Use about 55% for navigational CTR. The roughly ±0.4 pp interval is small next to any planning difference of a few points. A mistake in the label join could change the number by about 10 points, which is much larger than that.

## Why we believe it
- Alternatives considered:
  - Joining all label rows instead of only current ones: ruled out. It gives 45.0% because 200 superseded v1 labels add duplicate or stale rows. The join adds 300 rows (1,300 rows against 1,000 queries), which double-counts those queries. [measured]
  - Label version mix: ruled out as a driver. v1 gives 54.98% and v2 gives 54.99%. [measured]
  - Averaging per-query CTRs instead of dividing total clicks by total searches: not computed. I used total clicks over total searches, which is the usual definition. [guess]
- Checks run:
  - fanout: pass. Joining to `is_current=1` labels keeps 1,000 rows, with one current label per query (1,000 distinct) and no unmatched queries. [check:fanout#1]
  - completeness: could not run. It needs at least 3 earlier periods and the table only holds W40. I can't confirm W40 is fully loaded. It has 1,000 queries and no zero-search rows or rows with clicks above searches.
  - mix_shift and srm: skipped. There is no before/after comparison and no experiment.

## Caveats, and what would change the answer
- Only W40 is in the data, so I can't tell whether it is a typical or a partial week.
- The interval treats searches as independent. Clustering by query would make it wider.
- The headline relies on `is_current=1` being the correct label. Under the old v1 labels, navigational CTR would be different.
- The all-labels figure (45.0%) is wrong because of duplicate labels. Don't use it.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches), for queries whose current label is navigational. This is stated here [guess]; no metrics.json exists.
- Data: `query_stats` joined to `query_labels` on `is_current=1`, week 2026-W40 (the only week present).
- Reconciled: not done (no dashboard or other source provided).
- Queries and checks: ad hoc SQL run inline, not saved to a file. Check outputs are in `.ds-checks.log` (fanout#1, completeness#1).