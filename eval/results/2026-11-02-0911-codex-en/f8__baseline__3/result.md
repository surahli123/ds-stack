## Answer
Headline: +36.97% (95% interval: 36.21%–37.75%) [measured estimate; inferred interval]
Shopping queries recorded 39,857 clicks across 107,810 searches in 2026-W41, a CTR of 36.97%. [measured]
- Observed: +36.97% (95% interval: 36.21%–37.75%) [measured estimate; inferred interval]
- Adjusted: not computed (requested a descriptive rate; no comparison specified). [measured]
- Causal effect: not identified (would require a defined intervention and randomized or credible comparison design). [inferred]

## What it means for merchandising’s citation
Cite 36.97% as the observed shopping CTR. [measured] No decision threshold was supplied, so the 36.21%–37.75% interval cannot be compared with the smallest decision-changing difference. [inferred]

## Why we believe it
- Alternatives considered:
  - Direct-join CTR of 40.90%: ruled out by 250 repeated category records that duplicate query counts. [measured]
- Checks run:
  - Query-week uniqueness: pass; no duplicates. [measured]
  - Mapping consistency: pass; no conflicting categories, nonunique category-to-vertical mappings, or unmapped queries. [measured]
  - Count validity: pass; no missing, negative, or clicks-above-searches counts. [measured]
  - Independent aggregation: pass; deduplicated join matches membership filtering across 900 shopping queries. [measured]
  - Week completeness: could not run; weekly aggregates lack completeness evidence. [measured]

## Caveats, and what would change the answer
- Interval uses 10,000 query-level bootstrap samples, assuming independent, representative queries; the recorded aggregate itself is exact. [inferred]
- Missing records or a different official CTR definition could change the answer. [inferred]

## Provenance
- Metric: 100 × total clicks / total searches for shopping queries, from stated here [guess]; no metrics.json supplied. [measured]
- Data: query_week, query_category, category_vertical; available through 2026-W41, last complete period unverified. [measured]
- Reconciled: not done (no dashboard or independent source supplied). [measured]
- Queries and checks: [analysis_log.json](/private/tmp/ds-runs/f4e65826d0/analysis/analysis_log.json); reproducible [analysis.py](/private/tmp/ds-runs/f4e65826d0/analysis/analysis.py). [measured]
