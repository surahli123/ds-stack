## Answer
Headline: +54.98% (95% interval: 54.58%–55.38%) [measured; interval inferred]
Navigational queries in 2026-W40 recorded 32,878 clicks across 59,800 searches using current labels. [measured]
- Observed: +54.98% (95% interval: 54.58%–55.38%) [measured; interval inferred]
- Adjusted: not computed (descriptive rate requested). [inferred]
- Causal effect: not identified (requires a defined intervention and credible comparison design). [inferred]

## What it means for the planning doc
Use 54.98% as the observed rate under current labels. [measured] The interval spans roughly ±0.40 percentage points; no smallest decision-changing difference was supplied, so its planning significance cannot be assessed. [inferred]

## Why we believe it
- Alternatives considered:
  - Including historical labels: ruled out for current-label reporting; it produces 44.99% by including obsolete classifications. [measured]
- Checks run:
  - Label coverage and uniqueness: pass; every query has exactly one current label. [measured]
  - Duplicate query-week rows: pass; none found. [measured]
  - Count validity: pass; no missing, negative, or clicks-above-searches counts. [measured]
  - Week completeness: could not run; no completeness metadata supplied. [measured]

## Caveats, and what would change the answer
- The Wilson interval assumes independent searches and at most one counted click per search; aggregates cannot verify those assumptions. [inferred]
- Current labels may differ from labels effective during W40; historical effective dates could change the answer. [inferred]

## Provenance
- Metric: 100 × total clicks / total searches for W40 queries labeled navigational with `is_current=1`, stated here [guess]; no metrics.json supplied.
- Data: `query_stats`, `query_labels`; latest available period 2026-W40, completeness unverified. [measured]
- Reconciled: not done (no dashboard or independent source supplied). [measured]
- Queries and checks: [ctr_analysis_log.json](/private/tmp/ds-runs/492acfc351/analysis/ctr_analysis_log.json), reproduced by [ctr_analysis.py](/private/tmp/ds-runs/492acfc351/analysis/ctr_analysis.py). [measured]
