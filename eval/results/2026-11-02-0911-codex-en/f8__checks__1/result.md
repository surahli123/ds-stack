## Answer
Headline: +36.97% (95% interval: 36.68%–37.26%) [measured; interval inferred]
Shopping queries recorded 39,857 clicks across 107,810 searches in 2026-W41, giving a CTR of 36.97%. [measured]
- Observed: +36.97% (95% interval: 36.68%–37.26%) [measured; interval inferred]
- Adjusted: not computed (requested an overall weekly rate). [inferred]
- Causal effect: not identified (would require a defined intervention and credible comparison design). [inferred]

## What it means for merchandising’s citation
The observed rate supports citing “36.97% of recorded shopping searches,” subject to confirming load completeness. [inferred] No smallest decision-changing difference was supplied, so the interval cannot be assessed against that threshold. [inferred]

## Why we believe it
- Alternatives considered:
  - Direct category join: ruled out because repeated mappings inflate counts; identical query-category mappings were deduplicated. [measured]
  - Conflicting categories: ruled out by checking category uniqueness per query. [measured]
- Checks run:
  - completeness#1: could not run — insufficient earlier periods to verify completeness. [measured]
  - fanout#1: fail — raw category join added 250 rows. [measured]
  - fanout#2 and fanout#3: pass — deduplicated category and vertical joins preserved all rows with complete matching. [measured]
  - Metric integrity: pass — no duplicate query-week records, missing counts, negative counts, or clicks exceeding searches. [measured]
  - Mix shift and experiment allocation: skipped — no rate comparison or experiment requested. [inferred]

## Caveats, and what would change the answer
- The Wilson interval assumes independent search outcomes and clicks representing clicked searches; repeated users or multiple clicks per search could invalidate it. [inferred]
- A completed-load confirmation and an authoritative metric definition would strengthen the citation; additional records could change the rate. [inferred]

## Provenance
- Metric: total clicks divided by total searches, multiplied by 100; stated here [guess], because no metrics.json was supplied.
- Data: query_week, query_category, category_vertical; available for 2026-W41, last complete period unverified. [measured]
- Reconciled: not done (no dashboard or independent source supplied). [inferred]
- Queries and checks: [queries.json](queries.json), [analysis.py](analysis.py), [.ds-checks.log](.ds-checks.log), and [result.json](result.json). [measured]
