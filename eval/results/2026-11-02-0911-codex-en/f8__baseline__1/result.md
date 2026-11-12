## Answer
Headline: +36.97% (95% interval: 36.68%–37.26%) [measured rate; inferred interval]
Shopping queries recorded 39,857 clicks across 107,810 searches in 2026-W41, a CTR of 36.97%. [measured]
- Observed: +36.97% (95% interval: 36.68%–37.26%) [measured rate; inferred interval]
- Adjusted: not computed (requested a descriptive rate; no adjustment target specified). [inferred]
- Causal effect: not identified (would require a defined intervention and credible comparison design). [inferred]

## What it means for merchandising’s citation
Cite 36.97% for the recorded week. [measured] No smallest decision-changing difference was supplied, so the interval cannot be compared with a decision threshold. [inferred]

## Why we believe it
- Alternatives considered:
  - Direct join yielding 40.90%: ruled out by 250 repeated category records that inflate CTR by 3.93 percentage points. [measured]
- Checks run:
  - Query-week uniqueness: pass; no duplicate fact keys. [measured]
  - Category consistency and coverage: pass; no conflicting categories or missing mappings. [measured]
  - Count validity: pass; no null, negative, or above-search click counts. [measured]
  - Independent aggregation: pass; `EXISTS` and distinct-query joins produce identical totals. [measured]

## Caveats, and what would change the answer
- The interval uses a Wilson binomial model assuming independent searches and one binary click outcome per search; aggregate data cannot verify those assumptions. The recorded rate itself is exact. [inferred]
- Week completeness is unverified; additional records or revised mappings could change the rate. [inferred]

## Provenance
- Metric: 100 × total clicks / total searches for shopping queries, counting each query-week once; stated here [guess], because no `metrics.json` was found.
- Data: `query_week`, `query_category`, `category_vertical`; latest available period 2026-W41 [measured]; last complete period unverified [inferred].
- Reconciled: not done (no dashboard or independent source supplied). [inferred]
- Queries and checks: [script](/private/tmp/ds-runs/9054901cdb/analysis/ctr_analysis.py) and [results](/private/tmp/ds-runs/9054901cdb/analysis/ctr_analysis_results.json). [measured]
