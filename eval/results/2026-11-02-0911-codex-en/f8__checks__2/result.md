## Answer
Headline: +36.97% (95% interval: 36.68%–37.26%) [measured rate; inferred interval]
Shopping queries recorded 39,857 clicks across 107,810 searches in 2026-W41. [measured]
- Observed: +36.97% (95% interval: 36.68%–37.26%) [measured rate; inferred interval]
- Adjusted: not computed (a descriptive weekly rate was requested).
- Causal effect: not identified (would require a defined intervention and credible comparison design). [inferred]

## What it means for merchandising’s citation
Cite this as the rate in the available records; full-week completeness remains unverified. [inferred] No smallest decision-changing difference was supplied, so the interval cannot establish whether a merchandising threshold was met.

## Why we believe it
- Alternatives considered:
  - Direct category join: ruled out because repeated mappings duplicate query contributions. [measured]
  - Conflicting categories: ruled out by checking that each query maps to a single distinct category. [measured]
- Checks run:
  - Completeness: could not run—no earlier periods for comparison.
  - Raw join fanout: fail—added 250 rows. [measured]
  - Deduplicated category join: pass—preserved all rows and matched every query. [measured]
  - Vertical join: pass—preserved all rows and matched every category. [measured]
  - Metric validity and query-week uniqueness: pass. [measured]
  - Mix shift and experiment allocation: skipped—no comparison or experiment requested.

## Caveats, and what would change the answer
- The Wilson interval assumes independent searches with binary click outcomes; aggregated data cannot verify these assumptions. [inferred]
- A load-completion record would establish whether this represents the complete week. [inferred]

## Provenance
- Metric: total clicks divided by total searches for shopping queries, stated here [guess]; no metrics.json supplied.
- Data: query_week, query_category, category_vertical; available through 2026-W41, last complete period unverified.
- Reconciled: not done (no dashboard or independent source supplied).
- Queries and checks: [queries](analysis_output/queries.json), [calculation](analysis_output/calculate.py), [check results](.ds-checks.log).
