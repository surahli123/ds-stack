## Answer
Headline: +54.98% (95% interval: 54.58%–55.38%) [measured; interval inferred]
Navigational queries recorded 32,878 clicks across 59,800 searches in 2026-W40 using current intent labels. [measured]
- Observed: +54.98% (95% interval: 54.58%–55.38%) [measured; interval inferred]
- Adjusted: not computed (requested a descriptive weekly rate). [inferred]
- Causal effect: not identified (would require a defined intervention and credible comparison design). [inferred]

## What it means for the planning doc
Use 54.98% as the observed weekly CTR. [measured] The interval spans roughly ±0.40 percentage points; no smallest decision-changing difference was supplied, so decision sensitivity cannot be assessed. [inferred]

## Why we believe it
- Alternatives considered:
  - Including historical labels: ruled out for current classification because 200 obsolete navigational labels would enter the calculation. [measured]
- Checks run:
  - Label coverage and uniqueness: pass; every query has exactly one current label. [measured]
  - Duplicate query-week rows: pass; none found. [measured]
  - Count validity: pass; no missing, negative, or above-search click counts. [measured]
  - Week completeness: could not run; no completeness metadata available. [measured]

## Caveats, and what would change the answer
- The Wilson interval assumes independent searches with binary click outcomes; aggregate counts cannot verify those assumptions. [inferred]
- Current labels may differ from labels at the time of search; historical classification or missing records could change the answer. [inferred]

## Provenance
- Metric: `100 × SUM(clicks) / SUM(searches)` for `week='2026-W40'`, `intent='navigational'`, and `is_current=1`, from stated here [guess].
- Data: `warehouse.db`: `query_stats`, `query_labels`; latest available period 2026-W40, completeness unverified. [measured]
- Reconciled: not done (no dashboard or independent source supplied). [measured]
- Queries and checks: [analysis.py](/private/tmp/ds-runs/242bd7c621/analysis/analysis.py), [results](/private/tmp/ds-runs/242bd7c621/analysis/analysis_results.json). [measured]
