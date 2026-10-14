## Answer
Headline: 55.0 % (95% CI 54.6 to 55.4)
Navigational queries had a click-through rate of 55.0% in 2026-W40 (32,878 clicks on 59,800 searches), using each query's current intent label.
- Observed: 55.0 % (54.6 to 55.4), measured as clicks divided by searches for the 400 queries labelled navigational (`is_current=1`).
- Adjusted: not computed (this is a level, not a comparison, so there is nothing to adjust)
- Causal effect: not identified (this is a descriptive rate, not an effect; no intervention is involved)

## What it means for the marketing planning doc
Use about 55%. The interval is ±0.4 points, so the sampling error is too small to change a planning figure. The choice of label version matters far more: the older v1 labels give 43.0%, a gap of about 12 points.

## Why we believe it
- Alternatives considered:
  - Using v1 labels (all rows): ruled out. Using v1 for every query gives 43.0%, but 300 queries have been relabelled in v2 and the current label is the intended one [inferred]. Both label versions agree on the current-label rate for navigational queries: 54.98% for v1-current queries and 54.99% for v2 [measured].
  - Duplicate labels inflating counts: ruled out. Each query has exactly one `is_current=1` label, and no query_id and week pair is duplicated [measured].
  - Unlabelled queries dropped: ruled out. All 1,000 queries have a current label [measured].
- Checks run:
  - fanout: pass. The join is many-to-one and 1,000 rows stay 1,000.
  - completeness: could not run. W40 is the only week in the table, so there is no baseline. Whether W40 is fully loaded is unverified.
  - mix_shift: skipped. There is only one period, so no rate movement to decompose.
  - srm: skipped. This is not an experiment.

## Caveats, and what would change the answer
- W40 is the only week loaded, and I couldn't confirm it is complete. A partial week would shift the figure.
- The interval treats searches as independent. Clicks cluster within queries, so the true interval is probably wider.
- "Click-through rate" is computed as total clicks over total searches (pooled). A simple average of per-query rates would differ.
- A different definition of "navigational" (for example, the v1 labels) would change the number to about 43%.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches), navigational by current label, stated here [guess]. There is no metrics.json.
- Data: `query_stats` joined to `query_labels` on `query_id` (`is_current=1`), through 2026-W40 (completeness unverified).
- Reconciled: not done (no dashboard or other source available).
- Queries and checks: the queries were run inline and not saved. The check results are logged in `.ds-checks.log`.