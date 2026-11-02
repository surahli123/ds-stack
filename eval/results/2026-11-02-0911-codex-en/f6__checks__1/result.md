## Answer
Headline: +46.05% (95% interval: 45.93%–46.17%) [measured, conditional on definition]
During October 5–11, 321,780 of 698,782 external searches received at least one click under the assumed definition. [measured]
- Observed: +46.05% (95% interval: 45.93%–46.17%) [measured]
- Adjusted: not computed (requested a weekly level, with no comparison period). [inferred]
- Causal effect: not identified (would require a defined intervention and a randomized or credible quasi-experimental comparison). [inferred]

## What it means for the weekly business review
Use this provisionally, pending confirmation of the CTR definition. [inferred] No decision threshold or comparison baseline was supplied, so the interval cannot establish a decision-relevant change. [inferred]

## Why we believe it
- Alternatives considered:
  - All traffic: ruled in as an unresolved definition alternative; including internal and bot traffic gives 41.41%. [measured]
  - Only searches with results: ruled in as an unresolved denominator alternative; external CTR becomes 50.05%. [measured]
  - Total clicks as numerator: ruled out for the assumed metric because repeated clicks would count multiple times per search. [inferred]
- Checks run:
  - Completeness: pass for October 8–11 using daily row counts and search volumes; could not run for October 5–7 because earlier history is insufficient. [measured]
  - Date/segment coverage, grain uniqueness, count consistency: pass; all requested dates are represented, with no duplicate keys or detected count violations. [measured]
  - Fanout: skipped (no joins). [measured]
  - Mix shift: skipped (no rate-change comparison). [inferred]
  - SRM: skipped (no experiment). [inferred]

## Caveats, and what would change the answer
- External traffic and inclusion of searches without results are assumed business definitions. [guess]
- The Wilson interval assumes independent searches; user clustering and ingestion errors are not covered. [inferred]
- Full loading is unverified; a load watermark or source reconciliation could change the result. [inferred]

## Provenance
- Metric: `100 × SUM(searches_with_click) / SUM(searches)`, external traffic, both platforms, dates inclusive; stated here [guess], because no `metrics.json` was available.
- Data: `warehouse.db`, `search_daily_v`, available through 2026-10-11; last complete period unverified. [measured]
- Reconciled: not done (no dashboard or independent source supplied). [inferred]
- Queries and checks: `queries.json`, `.ds-checks.log`, `artifacts/additional-checks.json`; calculation in `artifacts/calculate.py`, outputs in `artifacts/results.json`. [measured]
