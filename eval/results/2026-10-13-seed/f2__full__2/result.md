## Answer
Headline: 55.0 percent (54.6 to 55.4) [q6]
Navigational queries had a click-through rate of 55.0% in 2026-W40 (32,878 clicks on 59,800 searches across 400 queries), using each query's current label only [q6].

## What it means for the marketing planning doc
Use about 55%; the interval is under half a point wide [q6], so sampling noise is not the issue. The real risk is the label choice: joining all label versions would give 45.0% instead [q7], and no threshold for the decision was given.

## Why we believe it
- Alternatives considered:
  - Join to every label row (all versions): ruled out, it duplicates 300 queries and gives 45.0% [q7] [check:fanout#2] [measured]
  - Stale v1 labels instead of current ones: ruled out, 300 queries were relabeled in v2 and v1 rows are flagged not current [q2] [measured]
  - Mix-shift, seasonality and day of week: ruled out as not applicable, this is a single-week level, not a change between periods [q3] [inferred]
- Checks run:
  - fanout (current labels only): pass, 1000 rows to 1000 keys [check:fanout#1]
  - fanout (all label rows): fail, 300 duplicate-key rows added by the join, so that variant was discarded [check:fanout#2]
  - completeness: could not run, only one week exists in query_stats so there is no history to compare [check:completeness#1]
  - mix_shift: skipped, no comparison period

## Caveats, and what would change the answer
- Metric definition is my guess: clicks divided by searches, summed over navigational queries (a search-weighted rate). An average of per-query rates would differ. Confirm with the metric owner.
- Whether W40 is fully loaded is unverified, since there is no earlier week. Confirm with the data owner.
- The interval treats searches as independent, so it is probably somewhat too narrow, because clicks cluster within queries.
- The is_current flag is assumed to be the correct labeling. Confirm with whoever owns query_labels.

## Provenance
- Metric: click-through rate = sum(clicks) / sum(searches), for queries whose is_current=1 label is navigational, week 2026-W40 [guess]; no metrics.json was available, since $DS_OVERLAY_DIR is unset
- Data: query_stats joined to query_labels (is_current=1), through 2026-W40
- Reconciled: not done (no dashboard or other source provided)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (15 numbers on 7 lines; 4 queries, 3 checks, 0 given)