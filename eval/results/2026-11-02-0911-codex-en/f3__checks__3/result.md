## Answer
Headline: can't tell [inferred]  
Overall CTR fell by 1.827 percentage points after rollout, but the amount attributable to v3 is not identified. [measured; inferred]

- Observed: −1.827 percentage points (95% interval: −1.978 to −1.675). [measured]
- Adjusted: −1.817 percentage points (95% interval: −1.966 to −1.667), holding platform × country shares fixed at their two-week midpoint. [measured]
- Causal effect: not identified; a randomized concurrent v2 holdout would identify it. [inferred]

## What it means for rollback
The adjusted interval excludes zero, but it measures association and cannot establish whether v3 exceeds any causal rollback threshold. [inferred] The smallest decision-changing drop was not supplied, so a threshold comparison remains unavailable. [measured]

## Why we believe it
- Alternatives considered:
  - Platform/country mix: ruled out as the main explanation; its decomposition contribution is −0.010 percentage points. [measured]
  - A coincident desktop-specific change: ruled in as an unresolved possibility; declines concentrate on desktop, but no untreated comparison exists. [inferred]
  - Mobile as an untreated control: ruled out; mobile also switched to v3. [measured]
- Checks run:
  - Completeness: pass for September 3–13; could not run for August 31–September 2 because earlier history is insufficient. [measured]
  - Mix shift: pass; adjustment leaves nearly the entire decline. [measured]
  - Duplicate keys and count validity: pass; no duplicates or invalid counts found. [measured]
  - Fanout: skipped; no joins used. [measured]
  - SRM: skipped; no randomized assignment or planned split supplied. [measured]

## Caveats, and what would change the answer
- Intervals assume independent binary search outcomes; repeated users and daily shocks could widen them. [inferred]
- Ranker and week are perfectly confounded; adjusting observed segments does not remove time confounding. [inferred]
- A randomized holdout, verified metric semantics, and a rollback threshold would enable a decision-oriented causal readout. [inferred]

## Provenance
- Metric: SUM(clicks) / SUM(searches), stated here; no metrics.json supplied. [guess]
- Data: `search_daily`, `release_log`, through September 13, 2026; row-count checks pass at both week endpoints, but source-load completion is unverified. [measured]
- Reconciled: not done; no dashboard or independent source supplied. [measured]
- Queries and checks: [SQL and results](analysis_output/queries.json), [check results](analysis_output/checks.json), [methods and assumptions](analysis_output/methods.md). [measured]
