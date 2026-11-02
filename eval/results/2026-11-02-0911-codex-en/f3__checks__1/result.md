## Answer
Headline: can't tell [inferred]

Overall CTR fell by 1.83 percentage points after rollout, but the amount attributable to v3 is not identified. [measured; inferred]
- Observed: −1.827 percentage points (95% interval: −1.978 to −1.675). [measured]
- Adjusted: −1.817 percentage points (95% interval: −1.966 to −1.667), holding platform × country shares fixed at their average across both weeks. [measured]
- Causal effect: not identified; a randomized concurrent v2 holdout would identify it. [inferred]

## What it means for rollback
The smallest decline that would trigger rollback has not been specified; the adjusted interval indicates a decline, but cannot establish whether v3 exceeds any causal harm threshold. [inferred] These data justify investigating the desktop decline, but do not establish that rollback would recover it. [inferred]

## Why we believe it
- Alternatives considered:
  - Platform/country mix: ruled out as the main explanation; its decomposition contribution is only −0.010 percentage points. [measured]
  - Desktop-specific deterioration: ruled in descriptively; desktop CTR declined while mobile was approximately stable. [measured]
  - Concurrent changes or logging issues: ruled in as unresolved alternatives; the database has no untreated comparison or independent measurement validation. [inferred]
  - Mobile as a control: ruled out as an established untreated control because it also received v3. [measured; inferred]
- Checks run:
  - Mix shift: pass; adjustment leaves almost all the observed decline. [measured]
  - Completeness: pass for daily row counts from September 3–13 and search-volume checks at both week endpoints; could not run for August 31–September 2 because earlier history is insufficient. [measured]
  - Integrity: pass; no duplicate dimension keys, missing required fields, or invalid counts detected. [measured]
  - Fanout: skipped; no joins used. [measured]
  - SRM: skipped; no randomized assignment data available. [measured]

## Caveats, and what would change the answer
- Intervals assume independent searches and fixed adjustment weights; user clustering and temporal variation are not captured. They are not causal-effect intervals. [inferred]
- Ranker and week coincide perfectly, preventing separation of rollout effects from other time effects. [measured; inferred]
- A randomized holdout, verified logging, and an explicit rollback threshold would make the decision assessable. [inferred]

## Provenance
- Metric: `SUM(clicks) / SUM(searches)`, stated here [guess]; no `metrics.json` supplied, and click-count semantics are unverified.
- Data: `search_daily`, `release_log`, through September 13, 2026; completeness heuristics pass at both week endpoints, but authoritative load completion is unverified. [measured; inferred]
- Reconciled: not done (no dashboard or independent source supplied). [measured]
- Queries and checks: [queries and results](analysis_output/queries.json), [check log](.ds-checks.log), [methodology](analysis_output/methodology.txt), [analysis script](analysis_output/analyze.py). [measured]
