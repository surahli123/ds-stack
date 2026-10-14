## Answer
Headline: 55.0% (95% CI 54.6% to 55.4%)
Navigational queries had a click-through rate of 55.0% in 2026-W40: 32,878 clicks on 59,800 searches. [measured]
- Observed: 55.0% (54.6% to 55.4%) [measured]. The interval is a binomial approximation that treats searches as independent. It is probably a little too narrow, because queries vary.
- Adjusted: not computed (this is a single-week level, not a comparison, so there is nothing to adjust for)
- Causal effect: not identified (this is a descriptive rate, and no causal question was asked)

## What it means for the planning doc
Use about 55%. The interval is roughly ±0.4 points, so sampling noise alone won't change a planning figure unless the decision turns on a difference of about half a point or less. No threshold was given, so I couldn't test that.

## Why we believe it
- Alternatives considered:
  - Stale or duplicate labels inflating the count: ruled out by using only `is_current=1` labels, which give exactly one label per query (1,000 queries, none unlabeled). [measured]
  - Label version changing the result: ruled out. Version-2 labels give 54.99% and version-1 labels give 54.98%. [measured]
  - Clicks exceeding searches: ruled out. No navigational query has more clicks than searches. [measured]
  - Averaging per-query rates instead of pooling: I used the pooled rate, clicks divided by searches, summed over all navigational queries. [inferred]
- Checks run:
  - fanout: pass. The join of 1,000 stats rows to the labels was many-to-one with no row gain or loss. [check:fanout#1]
  - completeness: could not run. It needs at least 3 earlier periods, and the table only contains W40. I can't confirm W40 is fully loaded. It has 1,000 rows, one per query.
  - mix_shift: skipped, because nothing is being compared over time.
  - srm: skipped, because there is no experiment.

## Caveats, and what would change the answer
- W40 is the only week in the table, so I couldn't check completeness or compare against other weeks.
- "Navigational" depends on the current label set. Using `is_current=1`, 400 queries are navigational. The label versions agree on the rate, so a relabel is unlikely to move it.
- I don't know whether Marketing's CTR counts all clicks or only the first click. The table only has total clicks.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches) over navigational queries. This definition is stated here [guess]. No metrics.json exists.
- Data: `query_stats` joined to `query_labels` on `query_id` with `is_current=1`, week 2026-W40 (the only week present).
- Reconciled: not done (no dashboard or source figure available)
- Queries and checks: the queries were run inline and not saved to a file. The check results are appended to `.ds-checks.log`.