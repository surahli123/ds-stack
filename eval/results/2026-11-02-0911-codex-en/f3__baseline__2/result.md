## Answer
Headline: can't tell [inferred]  
Overall CTR fell from 30.44% to 28.61%, a 1.83 percentage point decline after rollout [measured].
- Observed: −1.827 percentage points (95% interval: −1.978 to −1.675) [measured]
- Adjusted: −1.818 percentage points (95% interval: −1.967 to −1.668), holding the pre-rollout platform × country search mix fixed [measured]
- Causal effect: not identified (a concurrent randomized v2/v3 comparison would identify it; ranker and week are perfectly confounded here) [inferred]

## What it means for rollback
The smallest decline that would trigger rollback was not supplied, so a numerical threshold comparison is unavailable [measured]. The adjusted interval excludes zero, but it measures a before/after association; it cannot establish whether v3’s causal effect crosses your rollback threshold [inferred].

## Why we believe it
- Alternatives considered:
  - Platform/country mix shift as the main explanation: ruled out by its −0.009 percentage point contribution to the overall change [measured].
  - Desktop-specific deterioration: ruled in by declines of −3.107 points in US desktop and −2.872 elsewhere, versus −0.031 and −0.043 on mobile [measured].
  - Another contemporaneous desktop change: ruled in as an unresolved possibility; the release log does not establish the absence of other changes [inferred].
- Checks run:
  - Coverage and integrity: pass—all 14 days contain four strata; no duplicate keys, nulls, or invalid counts [measured].
  - Treatment overlap: fail—only v2 before rollout and v3 afterward; mobile also received v3 [measured].
  - Uncertainty sensitivity: pass—paired-weekday jackknife gives an adjusted 95% interval of −1.878 to −1.757 points, also excluding zero [measured].
  - Parallel trends: could not run—only one pre-rollout week and no untreated group [measured].

## Caveats, and what would change the answer
- Primary intervals assume independent binary click outcomes per search; aggregate counts cannot verify this or account for repeated users [inferred].
- Adjustment covers platform and country only; query mix, tracking changes, and other time effects remain unresolved [inferred].
- A randomized comparison, validated metric definition, and explicit rollback threshold would make the decision assessable [inferred].

## Provenance
- Metric: total clicks / total searches, from stated here [guess]; no metrics.json supplied [measured].
- Data: warehouse.db tables `search_daily` and `release_log`, through 2026-09-13; daily coverage is complete, ingestion completeness unverified [measured].
- Reconciled: not done (no independent dashboard or source supplied) [measured].
- Queries and checks: [queries.sql](/private/tmp/ds-runs/64d2a78b22/analysis/queries.sql), [analysis.py](/private/tmp/ds-runs/64d2a78b22/analysis/analysis.py), and [results.json](/private/tmp/ds-runs/64d2a78b22/analysis/results.json) [measured].
