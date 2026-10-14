## Answer
Headline: can't tell [inferred]  
Overall CTR fell from 30.421% to 28.324%, a decline of 2.097 percentage points, almost entirely explained arithmetically by traffic mix [measured].

- Observed: −2.097 percentage points (95% interval: −2.248 to −1.946) [measured]
- Adjusted: −0.002 percentage points (95% interval: −0.153 to +0.148), holding platform × country shares fixed at their two-week midpoint [measured]
- Causal effect: not identified (a concurrent randomized v1/v2 comparison would identify it; version and week are confounded here) [inferred]

## What it means for the rollback decision
The smallest loss warranting rollback was not supplied; the adjusted interval includes losses up to 0.153 percentage points, but does not bound causal harm [inferred]. This comparison alone supports neither blaming v2 nor declaring it safe [inferred].

## Why we believe it
- Alternatives considered:
  - Traffic composition: ruled in by mobile share rising from 40.108% to 55.072%; the platform × country mix contribution is −2.095 percentage points [measured].
  - Other changes over time: ruled in as unresolved explanations because there is no concurrent control group [inferred].
- Checks run:
  - Completeness: pass — both week endpoints pass row-count and search-volume checks using trailing-day baselines [measured].
  - Integrity: pass — all requested dates and segment cells present; unique keys and valid counts [measured].
  - Mix shift: flag — composition accounts arithmetically for almost all the decline [measured].
  - Fanout: skipped — no joins used [measured].
  - SRM: skipped — no randomized assignment or planned allocation available [measured].

## Caveats, and what would change the answer
- Intervals assume independent searches and clicks representing searches with a click; daily aggregates cannot verify these assumptions [guess].
- If v2 changed search composition, adjustment could remove part of its effect [inferred].
- A randomized comparison, verified metric semantics, and an explicit rollback threshold would make the decision actionable [inferred].

## Provenance
- Metric: SUM(clicks) / SUM(searches), from stated here [guess]; no metrics.json supplied [measured].
- Data: search_daily and release_log, through 2026-10-04; apparently complete by checks, without an ingestion watermark [inferred].
- Reconciled: not done (no dashboard or independent source supplied) [measured].
- Queries and checks: [SQL and results](analysis_outputs/queries.json), [check results](analysis_outputs/check-results.json), [reproducible analysis](analysis_outputs/analyze.py), and [.ds-checks.log](.ds-checks.log) [measured].
