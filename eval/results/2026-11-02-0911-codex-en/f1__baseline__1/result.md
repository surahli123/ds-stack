## Answer
Headline: can't tell [inferred]

Overall CTR fell from 30.421% to 28.324%, a 2.097 percentage-point drop, but the amount attributable to v2 is not identified. [measured; inferred attribution limit]

- Observed: −2.097 percentage points (95% interval: −2.246 to −1.948). [measured]
- Adjusted: −0.008 percentage points (95% interval: −0.163 to +0.148), holding platform × country search shares fixed at the first week’s distribution. [measured]
- Causal effect: not identified; a concurrent randomized v1/v2 comparison would identify it. [inferred]

## What it means for rollback
The smallest decline that would trigger rollback was not supplied; the adjusted interval includes declines up to 0.163 percentage points, but it is not a causal bound. [measured; inferred] The overall decline alone does not justify attributing harm to v2 or rolling it back. [inferred]

## Why we believe it
- Alternatives considered:
  - Traffic composition: ruled in as an arithmetic explanation; mobile share increased from 40.108% to 55.072%, and platform × country mix accounts for −2.089 percentage points of the decline using post-week stratum CTRs. [measured]
  - Calendar effects or concurrent changes: ruled in as unresolved possibilities because ranker version perfectly coincides with week. [inferred]
- Checks run:
  - Coverage: pass — all 14 dates have all four platform × country cells. [measured]
  - Data integrity: pass — no duplicate keys, null fields, nonpositive search counts, or clicks outside search-count bounds. [measured]
  - Decomposition: pass — mix contribution plus adjusted change equals observed change. [measured]
  - Weekday sensitivity: pass — paired-weekday adjusted change is −0.007 percentage points (95% interval: −0.062 to +0.048). [measured]
  - Causal identification: fail — no concurrent v1 traffic or untreated comparison group. [measured]

## Caveats, and what would change the answer
- Reported primary intervals assume independent binary click outcomes within strata and fixed traffic shares; aggregate data cannot verify these assumptions or user clustering. [inferred]
- Adjustment is descriptive; if v2 changed search composition, it could remove part of v2’s effect. [inferred]
- A randomized comparison and an explicit rollback threshold would make the decision assessable. [inferred]

## Provenance
- Metric: total clicks / total searches, from stated here [guess]; no `metrics.json` supplied.
- Data: `search_daily`, `release_log`, through 2026-10-04; daily cell coverage is complete, ingestion completeness unverified. [measured]
- Reconciled: not done (no dashboard or independent source supplied). [measured]
- Queries and checks: [SQL and results](queries_and_checks.json), [analysis script](analysis.py), [estimates and interval assumptions](results.json). [measured]
