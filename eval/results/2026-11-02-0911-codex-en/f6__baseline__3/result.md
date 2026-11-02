## Answer
Headline: +46.05% (95% interval: 45.93%–46.17%) [measured; provisional definition]
For October 5–11, 321,780 of 698,782 external searches had at least one click. [measured]
- Observed: +46.05% (95% interval: 45.93%–46.17%) [measured]
- Adjusted: not computed (reporting the weekly level; no comparison specified) [inferred]
- Causal effect: not identified (requires a defined intervention and randomized or credible comparison design) [inferred]

## What it means for the weekly business review
The interval extends approximately 0.12 percentage points either side of the estimate; no smallest decision-changing difference was supplied, so decision significance cannot be assessed. [measured/inferred] Confirm the metric definition before publishing, because alternative definitions materially change the result. [inferred]

## Why we believe it
- Alternatives considered:
  - All traffic: ruled in as an unresolved definition; yields 41.41%. [measured]
  - External searches with results as denominator: ruled in as an unresolved definition; yields 50.05%. [measured]
- Checks run:
  - Coverage: pass—all 42 expected date/platform/traffic combinations present. [measured]
  - Duplicate groups and invalid counts: pass—none found. [measured]
  - SQLite integrity: pass. [measured]
  - Ingestion completeness: could not run—no completeness metadata supplied. [measured]

## Caveats, and what would change the answer
- External-only traffic and all-search denominator are provisional choices. [guess]
- Wilson intervals assume independent searches; repeated-user clustering cannot be assessed from these aggregates. [inferred]
- This is a weekly level, not a change; no prior-week data are available. [measured]

## Provenance
- Metric: external searches with ≥1 click ÷ external searches × 100, from stated here [guess]; no metrics.json supplied. [measured]
- Data: `search_daily_v`, through 2026-10-11; all requested dates present, ingestion completeness unverified. [measured]
- Reconciled: not done (no dashboard or independent source supplied). [measured]
- Queries and checks: [analysis script](/private/tmp/ds-runs/427cb18807/analysis/ctr_analysis.py), [check log and results](/private/tmp/ds-runs/427cb18807/analysis/ctr_checks.json). [measured]
