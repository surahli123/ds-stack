## Answer
Headline: can't tell

Overall CTR fell from 30.441% to 28.615%, but the amount attributable to v3 cannot be determined. [measured; inferred attribution limit]

- Observed: −1.827 percentage points (95% interval: −1.978 to −1.675). [measured]
- Adjusted: −1.818 percentage points (95% interval: −1.967 to −1.668), holding platform × country shares fixed at the first week’s distribution. [measured]
- Causal effect: not identified; a concurrent randomized v2 holdout or randomized rollback would identify it. Ranker version and week are perfectly confounded here. [inferred]

## What it means for rollback
The adjusted interval excludes zero, but it measures a before/after change, not v3’s effect. [inferred] No smallest rollback-triggering loss was supplied, and no causal interval is identified to compare against that threshold; these data alone cannot establish that rollback would restore CTR. [inferred]

## Why we believe it
- Alternatives considered:
  - Platform/country traffic mix as the main explanation: ruled out by a mix contribution of only −0.009 percentage points under baseline-share standardization. [measured]
  - Desktop-specific effects, including v3 or another contemporaneous change: ruled in as compatible; desktop CTR fell 3.107 points in US and 2.872 elsewhere, while mobile changes were −0.031 and −0.043 points. [measured; inferred compatibility]
  - Mobile as an untreated control: ruled out because mobile also received v3. [measured]
- Checks run:
  - Coverage: pass—56 rows cover all four platform/country cells across all 14 dates. [measured]
  - Integrity: pass—no duplicate keys, nulls, nonpositive searches, negative clicks, or clicks exceeding searches. [measured]
  - Treatment overlap: fail—only v2 before September 7 and only v3 afterward. [measured]
  - Day-level sensitivity: pass—paired-weekday jackknife intervals also exclude zero for both descriptive changes. [measured]

## Caveats, and what would change the answer
- Reported intervals use independent binary-search binomial approximations; repeated users and whether clicks represent unique clicked searches cannot be checked from these aggregates. [inferred]
- Adjustment covers only recorded platform/country mix; query mix, instrumentation changes, and other time effects remain unresolved. [inferred]
- Randomized concurrent comparison, validated click semantics, and a rollback threshold would make the decision support stronger. [inferred]

## Provenance
- Metric: `SUM(clicks) / SUM(searches)`, from stated here [guess]; no `metrics.json` supplied.
- Data: `search_daily`, `release_log`, through September 13, 2026; all dates present, ingestion completeness unverified. [measured]
- Reconciled: not done (no dashboard or independent source supplied). [measured]
- Queries and checks: [SQL and check outputs](queries_and_checks.json), [analysis script](analysis.py), [computed results](results.json). [measured]
