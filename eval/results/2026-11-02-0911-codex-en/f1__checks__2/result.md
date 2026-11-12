## Answer
Headline: can't tell [inferred]

Overall CTR fell from 30.421% to 28.324%, largely reflecting a change in traffic mix. [measured]
- Observed: −2.097 percentage points (95% interval: −2.248 to −1.946). [measured]
- Adjusted: −0.002 percentage points (95% interval: −0.153 to +0.148), holding platform × country shares fixed at their average across the two weeks. [measured]
- Causal effect: not identified; a concurrent randomized v1/v2 holdout would separate ranker effects from changes over time. [inferred]

## What it means for rollback
The smallest decrease that would trigger rollback was not supplied; the adjusted interval includes decreases up to 0.153 percentage points, but does not bound causal harm. [inferred] These data alone establish neither grounds to blame v2 nor assurance that keeping it is safe. [inferred]

## Why we believe it
- Alternatives considered:
  - Traffic composition: ruled in by a −2.095 percentage-point mix component, almost entirely accounting for the observed decline. [measured]
  - Other changes over time: ruled in as unresolved confounding because ranker version coincides perfectly with week. [inferred]
  - Missing dates or duplicate records: ruled out by date coverage and key checks; partial ingestion remains possible. [measured]
- Checks run:
  - mix_shift: flag — decline is dominated by platform × country mix. [measured]
  - completeness: pass — daily row counts from September 24 onward and search-volume checks at both week endpoints. [measured]
  - completeness: could not run — September 21–23 lack sufficient earlier history. [measured]
  - Integrity: pass — requested dates and segment cells present; no duplicate keys or invalid counts found. [measured]
  - fanout: skipped — no joins. [measured]
  - srm: skipped — no experiment assignment or planned split supplied. [measured]

## Caveats, and what would change the answer
- Intervals assume independent searches and binary click outcomes; aggregate data cannot verify these assumptions or account for user clustering. [inferred]
- Traffic mix could itself respond to v2; adjustment could remove part of its effect. [inferred]
- A randomized holdout, verified metric semantics, ingestion confirmation, and a rollback threshold would strengthen the decision. [inferred]

## Provenance
- Metric: SUM(clicks) / SUM(searches), from stated here [guess]; no metrics.json supplied.
- Data: search_daily and release_log, through 2026-10-04; coverage checks pass at period endpoints, but last fully loaded period is unverified. [measured]
- Reconciled: not done (no dashboard or independent source supplied). [measured]
- Queries and checks: [queries and results](analysis_output/queries.json), [check log](.ds-checks.log), [methods and reproduction](analysis_output/methods.md). [measured]
