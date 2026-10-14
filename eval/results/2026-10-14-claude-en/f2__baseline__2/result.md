## Answer
Headline: 54.98 % (95% CI 54.95 to 55.01, query-level bootstrap)
Navigational queries in 2026-W40 had a click-through rate of about 55.0%: 32,878 clicks on 59,800 searches across 400 queries.
- Observed: 54.98 % (54.95 to 55.01) [measured]
- Adjusted: not computed (a single descriptive rate, nothing to adjust for)
- Causal effect: not identified (this is a level, not an effect, so no causal claim applies)

## What it means for the planning doc
Use about 55%. The interval is only ±0.03 points, so it would not change a plan unless the planning doc needs a different label definition. That choice matters far more: 45.0% under the older labels versus 55.0% under the current ones.

## Why we believe it
- Alternatives considered:
  - Old label versions counted too: ruled out. Joining all labels double-counts queries and gives 45.0%. Filtering to `is_current=1` gives exactly one label per query [measured].
  - Averaging per-query CTRs instead of pooling: ruled out. It gives 55.0%, the same as the pooled rate [measured].
- Checks run:
  - Label uniqueness: pass. No query has more than one current label, and every query in the stats has a current label.
  - Data sanity: pass. There are no null searches and no rows where clicks exceed searches. W40 is the only week in the table, with 1,000 distinct queries.
  - Interval: flag. It is very narrow because per-query CTRs are tightly clustered. I did not check whether this is typical of the real data.

## Caveats, and what would change the answer
- I defined CTR as total clicks divided by total searches (pooled). The answer is the same if you average per query.
- 100 queries moved from informational to navigational in label version 2, and 200 navigational labels were retired. The figure follows the current labels. If marketing used an older labelling, the number would differ.
- There is no `metrics.json`, so I did not reconcile against a dashboard.

## Provenance
- Metric: sum(clicks)/sum(searches) over queries whose current label (`is_current=1`) is navigational, in 2026-W40. This definition is stated here [guess].
- Data: `query_stats` and `query_labels` in warehouse.db, through 2026-W40 (the only week present).
- Reconciled: not done (no dashboard or metrics definition provided).
- Queries and checks: run inline in the shell session only; no log file was saved.