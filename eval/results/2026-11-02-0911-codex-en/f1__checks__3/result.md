## Answer
Headline: can't tell [inferred]  
Overall CTR fell by 2.097 percentage points, almost entirely accounted for descriptively by traffic mix changes. [measured]
- Observed: −2.097 percentage points (95% interval: −2.248 to −1.946). [measured]
- Adjusted: −0.002 percentage points (95% interval: −0.153 to +0.148), holding platform × country shares fixed at their average across the two weeks. [measured]
- Causal effect: not identified; a randomized concurrent v1 holdout would identify it because version and week are completely confounded here. [inferred]

## What it means for the rollback
The smallest harmful change that would trigger rollback was not provided; the adjusted interval includes declines up to 0.153 percentage points, but does not bound causal harm. [measured/inferred] This comparison alone does not establish that rolling back v2 would recover CTR. [inferred]

## Why we believe it
- Alternatives considered:
  - Traffic composition: ruled in descriptively; increased share of lower-CTR mobile traffic accounts for −2.095 percentage points in the decomposition. [measured]
  - Broad within-segment deterioration: ruled out as the main descriptive explanation by the near-zero adjusted change. [inferred]
  - Calendar effects, unmeasured composition, or v2 affecting traffic mix: not ruled out; there is no concurrent control. [inferred]
- Checks run:
  - mix_shift: flag — composition dominates the observed decline (`mix_shift#1`). [measured]
  - completeness: pass — row-count checks from September 24 onward and search-volume checks at both week endpoints; no ingestion watermark establishes completeness. [measured/inferred]
  - completeness: could not run — September 21–23 lack sufficient preceding history. [measured]
  - Data validity: pass — no duplicate segment-day-ranker keys, missing fields, or invalid counts found. [measured]
  - fanout: skipped — no joins used. [measured]
  - srm: skipped — no randomized assignment data available. [measured]

## Caveats, and what would change the answer
- Intervals assume independent searches and binary click outcomes; aggregate data cannot verify these assumptions or account for repeated users. [inferred]
- Adjusting for mix could remove part of v2’s effect if v2 changed search frequency or composition. [inferred]
- A randomized holdout and an explicit rollback threshold would make the decision assessable. [inferred]

## Provenance
- Metric: sum(clicks) / sum(searches), from stated here [guess]; no `metrics.json` supplied.
- Data: `search_daily`, `release_log`; comparison covers September 21–27 versus September 28–October 4, 2026. Data present through October 4; final load completeness unverified. [measured]
- Reconciled: not done — no independent dashboard or source supplied. [measured]
- Queries and checks: `analysis_output/queries.jsonl`, `analysis_output/analyze.py`, `analysis_output/results.json`, `.ds-checks.log`. [measured]
