## Answer
Headline: can't tell

[measured] Overall CTR fell from 30.421% to 28.324%, but the change was only −0.008 percentage points after fixing the platform and country mix.
- Observed: −2.097 percentage points (95% interval: −2.248 to −1.946) [measured]
- Adjusted: −0.008 percentage points (95% interval: −0.163 to +0.148), holding platform × country search shares fixed at September 21–27 levels [measured]
- Causal effect: not identified (a concurrent randomized v1/v2 comparison would identify it; ranker version and week are completely confounded here) [inferred]

## What it means for rollback
The smallest decrease that would justify rollback was not provided; the adjusted interval includes decreases up to 0.163 percentage points, but does not bound v2’s causal effect. [inferred] These results do not establish that v2 caused the drop or that keeping it is harmless. [inferred]

## Why we believe it
- Alternatives considered:
  - Traffic composition: ruled in as an arithmetic explanation; mobile’s search share rose from 40.108% to 55.072%, and platform × country composition accounts for −2.089 percentage points of the observed change, using post-period stratum CTRs. [measured]
  - A uniform decline within segments: ruled out descriptively; two segments rose and two fell, with changes between −0.080 and +0.051 percentage points. [measured]
- Checks run:
  - Coverage: pass—all 14 dates have all four platform × country combinations. [measured]
  - Integrity: pass—no duplicate daily segment/ranker keys, null fields, nonpositive searches, or clicks outside zero to searches. [measured]
  - Rollout consistency: pass—only v1 before September 28 and only v2 afterward, matching `release_log`. [measured]
  - Causal identification: fail—no concurrent control, assignment records, or earlier trend history. [measured]
  - Decomposition: pass—composition plus adjusted change reproduces the observed change to numerical precision. [measured]

## Caveats, and what would change the answer
- Intervals assume independent binary click outcomes per search and fixed observed traffic weights; aggregate counts cannot verify those assumptions or account for user clustering. [inferred]
- Concurrent changes and unobserved query/user mix remain possible explanations. Platform mix could itself respond to v2, so adjustment could remove part of its effect. [inferred]
- Randomized holdout results and a specified rollback threshold would make the decision assessable. [inferred]

## Provenance
- Metric: `SUM(clicks) / SUM(searches)`, search-weighted CTR; stated here [guess], because no `metrics.json` was supplied.
- Data: `search_daily`, `release_log`, through 2026-10-04; daily coverage is complete, ingestion completeness is unverified. [measured]
- Reconciled: not done (no dashboard or independent source supplied). [measured]
- Queries and checks: [SQL and check results](analysis_output/queries_and_checks.json), [calculations](analysis_output/analyze.py), [results and interval assumptions](analysis_output/results.json). [measured]
