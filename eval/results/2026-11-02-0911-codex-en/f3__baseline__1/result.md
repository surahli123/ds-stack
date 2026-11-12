## Answer
Headline: can't tell [inferred]

Overall CTR fell from 30.441% to 28.615%, a decrease of 1.827 percentage points, but the amount attributable to v3 is not identified. [measured; inferred attribution limit]

- Observed: −1.827 percentage points (95% interval: −1.978 to −1.675). [measured, conditional model]
- Adjusted: −1.818 percentage points (95% interval: −1.967 to −1.668), holding the pre-rollout platform × country traffic shares fixed. [measured, conditional model]
- Causal effect: not identified (a randomized concurrent v2/v3 comparison would identify it; ranker and week are perfectly confounded here). [inferred]

## What it means for rollback
The smallest causal decrease that would trigger rollback was not supplied; the observed interval corresponds to a decline of 1.675–1.978 percentage points, but cannot establish whether v3 crosses any causal rollback threshold. [measured; inferred] These data warrant investigating the desktop decline, but do not establish that rolling back v3 would recover it. [inferred]

## Why we believe it
- Alternatives considered:
  - Platform/country traffic mix: ruled out as the main explanation; standardization accounts for only −0.009 percentage points of the observed change. [measured]
  - A desktop-specific change unrelated to v3: ruled in as an unresolved possibility; desktop CTR declined 2.872–3.107 percentage points within country groups, versus 0.031–0.043 on mobile. [measured; inferred explanation]
  - Mobile as an untreated control: ruled out; mobile also received v3, and there is no evidence establishing parallel trends or zero mobile treatment effect. [measured; inferred]
- Checks run:
  - Data integrity: pass—56 rows, no duplicate dimension/date keys, nulls, nonpositive search counts, or clicks outside zero to searches. [measured]
  - Coverage: pass—all 14 dates contain all four platform/country groups. [measured]
  - Treatment overlap: flag—only v2 before September 7 and only v3 afterward. [measured]
  - Day sensitivity: pass—all seven matched-weekday comparisons declined; their mean observed change was −1.826 percentage points (paired-day 95% t interval: −1.892 to −1.760). [measured, conditional model]
  - Concurrent control and historical trends: could not run—neither is available. [measured]

## Caveats, and what would change the answer
- Main intervals assume independent searches and a binary clicked-search outcome; the schema does not confirm those assumptions. Repeated users or logging changes could invalidate them. [guess assumptions; inferred limitation]
- Mix adjustment is descriptive, not causal; it could remove part of a treatment-induced mix change. [inferred]
- A randomized comparison, verified click instrumentation, and an explicit rollback threshold would make the decision assessable. [inferred]

## Provenance
- Metric: `SUM(clicks) / SUM(searches)`, from stated here [guess]; no `metrics.json` was supplied.
- Data: `search_daily`, `release_log`, through 2026-09-13; all expected date/group cells are present, but no ingestion-completeness watermark exists. [measured]
- Reconciled: not done (no independent dashboard or source supplied). [measured]
- Queries and checks: [SQL log](queries.json), [results and checks](results.json), [reproducible analysis](analyze.py). [measured]
