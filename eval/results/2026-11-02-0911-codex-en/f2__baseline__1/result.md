## Answer
Headline: +54.98% (95% interval: 54.58%–55.38%) [measured rate; inferred interval]  
Navigational queries generated 32,878 clicks from 59,800 searches in 2026-W40 using current intent labels. [measured]

- Observed: +54.98% (95% interval: 54.58%–55.38%) [measured rate; inferred interval]
- Adjusted: not computed (requested a descriptive rate). [inferred]
- Causal effect: not identified (would require a defined intervention and credible comparison design). [inferred]

## What it means for the planning doc
Use 54.98% as the observed baseline. [measured] The interval spans approximately ±0.40 percentage points; no smallest decision-changing difference was supplied, so decision sensitivity cannot be assessed. [inferred]

## Why we believe it
- Alternatives considered:
  - Including historical labels: ruled out for the current-label definition; it produces 44.99% by including obsolete navigational labels. [measured]
- Checks run:
  - Label coverage: pass — every query has exactly one current label matching its latest version. [measured]
  - Duplicate query/week records: pass — none found. [measured]
  - Counts: pass — no missing, negative, or inconsistent counts found. [measured]
  - Week completeness: could not run — no completeness metadata supplied. [measured]

## Caveats, and what would change the answer
- Wilson interval assumes independent searches with binary click outcomes; aggregate data cannot verify those assumptions. [inferred]
- Current labels may differ from labels applicable during W40; dated label history could change the answer. [inferred]

## Provenance
- Metric: 100 × total clicks / total searches for current navigational labels in W40; stated here [guess], because no metrics.json was supplied.
- Data: query_stats and query_labels; latest available period is 2026-W40, completeness unverified. [measured]
- Reconciled: not done (no dashboard or independent source supplied). [measured]
- Queries and checks: [analysis.py](/private/tmp/ds-runs/4eb0906b30/analysis/analysis.py), [results](/private/tmp/ds-runs/4eb0906b30/analysis/analysis_results.json). [measured]
