## Answer
Headline: +54.98% (95% interval: 54.58%–55.38%) [measured; interval inferred]
Navigational queries recorded 32,878 clicks across 59,800 searches in 2026-W40 using current intent labels. [measured]
- Observed: +54.98% (95% interval: 54.58%–55.38%) [measured; interval inferred]
- Adjusted: not computed (a descriptive weekly rate was requested). [inferred]
- Causal effect: not identified (would require a defined intervention and credible comparison design). [inferred]

## What it means for the planning doc
Use 54.98% as the recorded rate, with completeness unverified. [inferred] No smallest decision-changing difference was supplied, so the interval cannot be compared with a planning threshold. [inferred]

## Why we believe it
- Alternatives considered:
  - Joining historical labels: ruled out because it duplicates query records; current labels preserve the original rows. [measured]
- Checks run:
  - Historical-label fanout: fail; the unrestricted join added 300 rows. [measured]
  - Current-label fanout: pass; all 1,000 source rows preserved. [measured]
  - Coverage and validity: pass; no missing current labels, duplicate query keys, or invalid counts. [measured]
  - Completeness: could not run; no earlier periods available. [measured]
  - Mix shift and experiment assignment: skipped; no change comparison or experiment requested. [inferred]

## Caveats, and what would change the answer
- The Wilson interval assumes independent searches and binary click outcomes; it excludes loading and labeling uncertainty. [inferred]
- Current labels may differ from labels used during the week; historical label timing or additional loaded records could change the answer. [inferred]

## Provenance
- Metric: total clicks / total searches × 100 for current navigational labels; stated here [guess], because no metrics.json was supplied.
- Data: query_stats and query_labels, available through 2026-W40; last complete period unverified. [measured]
- Reconciled: not done (no dashboard or independent source supplied). [inferred]
- Queries and checks: [queries](analysis_output/queries.json), [calculation](analysis_output/calculate.py), [check results](.ds-checks.log). [measured]
