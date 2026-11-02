## Answer
Headline: +36.97% (95% interval: 36.68%–37.26%) [measured; interval inferred]
Shopping queries in 2026-W41 recorded 39,857 clicks across 107,810 searches, giving a 36.97% click-through rate [measured].
- Observed: +36.97% (95% interval: 36.68%–37.26%) [measured; interval inferred]
- Adjusted: not computed (descriptive rate; no comparison requested) [inferred]
- Causal effect: not identified (would require a defined intervention and credible comparison design) [inferred]

## What it means for merchandising’s citation
Cite 36.97% as the rate in the available records, with completeness unverified [measured]. No smallest decision-changing difference was supplied, so the interval cannot establish whether a merchandising threshold was met [inferred].

## Why we believe it
- Alternatives considered:
  - Direct category join: ruled out by repeated mappings that inflate counts [measured].
  - Conflicting categories: ruled out by the mapping audit [measured].
- Checks run:
  - Raw join fanout: fail — added 250 duplicate rows [measured].
  - Deduplicated category join: pass — preserved all 2,000 query rows with complete matching [measured].
  - Vertical mapping join: pass — preserved rows with complete matching [measured].
  - Count and key integrity: pass — no duplicate query-week records or invalid counts [measured].
  - Completeness: could not run — no earlier periods available [measured].
  - Mix shift and experiment assignment: skipped — no temporal comparison or experiment requested [inferred].

## Caveats, and what would change the answer
- The Wilson interval assumes independent searches and binary click outcomes; aggregate counts cannot verify these assumptions [inferred].
- A load-completion record could establish completeness; missing records or corrected mappings could change the rate [inferred].

## Provenance
- Metric: total shopping clicks divided by total shopping searches × 100, from stated here [guess]; no metrics.json supplied.
- Data: query_week, query_category, category_vertical; available through 2026-W41, last complete period unverified [measured].
- Reconciled: not done (no dashboard or independent source supplied) [inferred].
- Queries and checks: queries.json, analysis.py, results.json, and .ds-checks.log in the working directory [measured].
