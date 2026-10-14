## Answer
Headline: 55.0 % (95% CI 54.6 to 55.4)

In 2026-W40, navigational queries (current labels) got 32,878 clicks on 59,800 searches, a click-through rate of 55.0%.
- Observed: 55.0 % (54.6 to 55.4) [measured]. The interval is a binomial approximation that treats searches as independent, so it is probably a bit too narrow because clicks cluster within queries.
- Adjusted: not computed (this is a single descriptive rate with nothing to adjust for)
- Causal effect: not identified (this is a descriptive rate, so there is no intervention to estimate)

## What it means for the planning doc
Use about 55% for navigational queries under the current labels. If marketing wants the old definition, the figure is about 43%, so the labeling version matters far more than the sampling noise of ±0.4 pp.

## Why we believe it
- Alternatives considered:
  - Joining every label row would double-count queries: ruled out by filtering to `is_current=1`. That gives exactly one label per query and covers all 1,000 queries [measured].
  - Using the older v1 labels instead of the current ones: ruled in as a sensitivity result, not the headline. v1 labels give 43.0% navigational, because 200 queries were relabeled from navigational to informational and 100 from informational to navigational in v2 [measured].
  - Averaging per-query rates instead of pooling clicks over searches: ruled out as a material difference, since it gives 55.0% as well [measured].
- Checks run:
  - Duplicate current labels: pass. There are none.
  - Stats rows with no current label: pass. There are none.
  - Null values or clicks above searches: pass. There are none.
  - Coverage: pass. `query_stats` contains only W40, with 1,000 distinct queries.

## Caveats, and what would change the answer
- The number depends on which label version defines "navigational". Current labels give 55.0%, v1 gives 43.0%. I used the current labels because `is_current=1` marks them as the live definition [inferred].
- CTR is defined as clicks divided by searches, pooled across queries. No `metrics.json` exists, so this definition is my assumption.
- The interval ignores clustering by query.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches) for queries with current intent 'navigational', stated here [guess]
- Data: `query_stats` joined to `query_labels` on `is_current=1`, covering 2026-W40 only
- Reconciled: not done (no dashboard or reference figure available)
- Queries and checks: run inline in Python/sqlite3. No log file was saved.