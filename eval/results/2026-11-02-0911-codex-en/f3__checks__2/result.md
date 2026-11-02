## Answer
Headline: can't tell [inferred]
CTR fell by 1.83 percentage points after rollout, but these data cannot identify how much v3 caused. [measured; inferred]
- Observed: −1.827 percentage points (95% interval: −1.978 to −1.675). [measured]
- Adjusted: −1.817 percentage points (95% interval: −1.966 to −1.667), holding platform × country shares fixed at their average across the two weeks. [measured]
- Causal effect: not identified (a randomized concurrent v2 holdout would identify it; ranker version and week are completely confounded here). [inferred]

## What it means for the rollback
The adjusted association’s interval indicates a decline, but it cannot bound the causal harm from v3. The smallest loss warranting rollback was not supplied, so a threshold comparison is unavailable; this evidence alone cannot establish that rollback would restore CTR. [inferred]

## Why we believe it
- Alternatives considered:
  - Platform/country mix as the main explanation: ruled out by a mix contribution of only −0.010 percentage points. [measured]
  - Desktop-specific change: ruled in by declines concentrated in desktop segments while mobile rates were nearly unchanged; the cause remains unresolved. [measured; inferred]
  - Mobile as an untreated control: ruled out because mobile also received v3. [measured]
  - Concurrent demand, logging, or product changes: ruled in as unresolved alternatives because there is no concurrent untreated comparison. [inferred]
- Checks run:
  - completeness: pass for both week endpoints using trailing-day row counts; upstream load completion is not certified. [measured]
  - mix_shift: pass; platform/country composition explains little of the decline. [measured]
  - Grid/count validation: pass; all expected daily segments are present, keys are unique, and counts satisfy clicks ≤ searches. [measured]
  - Rollout validation: pass; all pre-period rows use v2 and all post-period rows use v3. [measured]
  - fanout: skipped; no joins used.
  - srm: skipped; no randomized assignment or planned allocation supplied.

## Caveats, and what would change the answer
- Intervals assume independent searches with binary click outcomes; repeated users, daily shocks, or multiple clicks per search could invalidate them. [inferred]
- Adjustment removes measured composition changes, not time confounding or unmeasured query mix. [inferred]
- A randomized holdout, verified click semantics, ingestion records, and a rollback threshold would strengthen the decision. [inferred]

## Provenance
- Metric: total clicks / total searches; post-week minus pre-week, multiplied by 100 for percentage points, stated here [guess]; no metrics.json supplied.
- Data: warehouse.db’s search_daily and release_log, through 2026-09-13; daily coverage passes, upstream completeness unverified. [measured]
- Reconciled: not done (no dashboard or independent source supplied).
- Queries and checks: [queries](analysis_output/queries.json), [results](analysis_output/results.json), [check log](.ds-checks.log), [reproducible script](analysis_output/analyze.py).
