## Answer
Headline: can't tell [inferred]
Overall CTR fell from 30.421% to 28.324%, a 2.097 percentage-point drop, but the amount caused by v2 is not identified. [measured; inferred]
- Observed: −2.097 percentage points (95% interval: −2.164 to −2.030) [measured]
- Adjusted: −0.008 percentage points (95% interval: −0.064 to +0.048), holding platform × country search shares fixed at the first week’s mix [measured]
- Causal effect: not identified; a concurrent randomized v1/v2 holdout would identify it [inferred]

## What it means for rollback
The smallest harmful change that would trigger rollback was not supplied; the adjusted interval spans a 0.064-point decline to a 0.048-point improvement, but does not bound causal harm. [measured; inferred] These data alone do not justify attributing the drop to v2 or declaring v2 harmless. [inferred]

## Why we believe it
- Alternatives considered:
  - Traffic composition: ruled in as an accounting explanation; mobile search share rose from 40.108% to 55.072%, and platform × country mix accounts for −2.089 points of the observed change. [measured]
  - Concurrent time effects: ruled in as an unresolved explanation because ranker version perfectly coincides with week. [measured; inferred]
- Checks run:
  - Coverage: pass — all 14 dates have all four platform × country cells. [measured]
  - Data validity: pass — no duplicate keys, null fields, nonpositive searches, or clicks outside zero-to-searches bounds; SQLite integrity check passed. [measured]
  - Treatment overlap: fail — first week contains only v1; second contains only v2. [measured]
  - Weight sensitivity: pass — using second-week weights gives an adjusted change of +0.003 points, also near zero. [measured]
  - Source completeness: could not run — no ingestion audit or external totals supplied. [measured]

## Caveats, and what would change the answer
- Intervals use a paired-weekday jackknife with a t(6) critical value; they assume independent weekday pairs and representative daily variation. Seven pairs provide limited uncertainty estimation and do not capture systematic bias. [inferred]
- Mix adjustment is descriptive; v2 could itself affect search frequency and therefore traffic shares. Query mix and other concurrent changes are unobserved. [inferred]
- A randomized holdout, a confirmed metric definition, and a rollback threshold would make the decision more defensible. [inferred]

## Provenance
- Metric: CTR = SUM(clicks) / SUM(searches), search-weighted; stated here [guess]. Whether clicks represent clicked searches is unverified.
- Data: `search_daily`, `release_log`; requested windows 2026-09-21–2026-09-27 and 2026-09-28–2026-10-04, with daily coverage through October 4; ingestion completeness unverified. [measured]
- Reconciled: not done (no dashboard or independent source supplied). [measured]
- Queries and checks: [query log](queries_and_checks.json), [reproducible analysis](analysis.py), [results and interval method](results.json). [measured]
