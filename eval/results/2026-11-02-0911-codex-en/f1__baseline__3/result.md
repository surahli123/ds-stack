## Answer
Headline: can't tell [inferred]
Overall CTR fell from 30.421% to 28.324%, a drop of 2.097 percentage points, but these data cannot isolate v2’s contribution. [measured; inferred]
- Observed: −2.097 percentage points (95% interval: −2.248 to −1.946). [measured; interval inferred]
- Adjusted: −0.008 percentage points (95% interval: −0.163 to +0.148), holding platform × country search shares fixed at the first week’s mix. [measured; interval inferred]
- Causal effect: not identified (a concurrent randomized v1/v2 comparison would identify it). [inferred]

## What it means for rollback
The smallest harmful change that would trigger rollback was not supplied; the adjusted interval includes both a 0.163-point decline and a 0.148-point improvement, but does not bound v2’s causal effect. [measured; inferred] This comparison alone does not establish that rollback would recover the observed loss. [inferred]

## Why we believe it
- Alternatives considered:
  - Traffic composition: ruled in as an arithmetic explanation for −2.089 points of the decline; mobile’s search share increased from 40.108% to 55.072%, and mobile CTR was lower. [measured]
  - Concurrent time effects: ruled in as an unresolved explanation because version and week coincide exactly. [inferred]
- Checks run:
  - Data integrity: pass SQLite integrity check, no duplicate dimension keys, null fields, or invalid counts. [measured]
  - Coverage: pass all four platform/country groups appear on each of the 14 dates. [measured]
  - Rollout consistency: pass exclusively v1 before September 28 and v2 afterward, matching the release log. [measured]
  - Causal comparison: fail no concurrent untreated group or randomized assignment is available. [measured]
  - Within-group changes: pass descriptive calculation; changes range from −0.080 to +0.051 percentage points. [measured]

## Caveats, and what would change the answer
- Intervals assume independent searches and binary click outcomes; aggregate counts cannot verify these assumptions or account for user/session clustering. [inferred]
- Mix adjustment is descriptive: v2 could itself affect traffic composition, and unmeasured changes could offset its effect. [inferred]
- Randomized comparison data and an explicit rollback threshold would support the decision. [inferred]

## Provenance
- Metric: sum(clicks) / sum(searches), from stated here [guess]; no metrics.json supplied. [measured]
- Data: search_daily and release_log, through 2026-10-04; all expected daily groups present, ingestion completeness unverified. [measured]
- Reconciled: not done (no independent dashboard or source supplied). [measured]
- Queries and checks: [SQL and check outputs](queries_and_checks.json), [analysis script](analysis.py), [results](results.json). [measured]
