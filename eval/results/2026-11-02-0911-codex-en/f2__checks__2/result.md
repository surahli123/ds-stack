## Answer
Headline: +54.98% (95% interval: 54.58%–55.38%) [measured; interval inferred]
Navigational queries in 2026-W40 recorded 32,878 clicks across 59,800 searches, a 54.98% click-through rate using current labels. [measured]
- Observed: +54.98% (95% interval: 54.58%–55.38%) [measured; interval inferred]
- Adjusted: not computed (a descriptive weekly rate was requested).
- Causal effect: not identified (would require a defined intervention and a credible comparison design). [inferred]

## What it means for the planning doc
Use 54.98% as the observed rate, with completeness unverified. [inferred] No smallest decision-changing difference was supplied, so the interval cannot establish whether uncertainty would alter the plan. [inferred]

## Why we believe it
- Alternatives considered:
  - Joining all label versions: ruled out by duplicate matches; current labels preserve each query once. [measured]
- Checks run:
  - completeness#1: could not run — no earlier periods available.
  - fanout#1: fail — unfiltered labels expanded 1,000 rows to 1,300. [measured]
  - fanout#2: pass — current-label join retained all 1,000 rows without duplication. [measured]
  - Metric validation: pass — no invalid counts or duplicate query rows in the requested week. [measured]
  - Mix shift and SRM: skipped — no rate comparison or experiment requested.

## Caveats, and what would change the answer
- The Wilson interval assumes independent searches and binary click outcomes; these assumptions are unverified. [inferred]
- Historical intent assignments or late-arriving data could change the rate. [inferred]

## Provenance
- Metric: total clicks ÷ total searches × 100 for `intent='navigational'`, `is_current=1`; stated here [guess], because no metrics.json was available.
- Data: `query_stats`, `query_labels`; available period 2026-W40, last complete period unverified. [measured]
- Reconciled: not done (no dashboard or independent source available).
- Queries and checks: [queries](analysis_output/queries.json), [calculation](analysis_output/calculate.py), [results](analysis_output/result.json), [check log](.ds-checks.log).
