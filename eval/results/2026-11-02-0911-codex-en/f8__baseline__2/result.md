## Answer
Headline: +36.97% (95% interval: 36.19%–37.76%) [measured rate; inferred interval]
Shopping queries in 2026-W41 recorded 39,857 clicks across 107,810 searches, giving a 36.97% click-through rate [measured].
- Observed: +36.97% (95% interval: 36.19%–37.76%) [measured rate; inferred interval]
- Adjusted: not computed (no comparison or adjustment requested) [inferred]
- Causal effect: not identified (would require a defined intervention and credible control comparison) [inferred]

## What it means for merchandising’s citation
Cite 36.97% for the recorded week [measured]. No smallest decision-changing difference was supplied; the interval spans approximately ±0.79 percentage points, so decision sensitivity cannot be assessed [inferred].

## Why we believe it
- Alternatives considered:
  - Direct-join CTR of 40.90%: ruled out by duplicate category mappings, which inflate the rate by 3.93 percentage points [measured].
- Checks run:
  - Fact uniqueness: pass — one row per query and week [measured].
  - Mapping coverage and consistency: pass — all queries mapped, with no conflicting categories [measured].
  - Mapping duplication: flag — 250 repeated mappings; membership filtering counts each query once [measured].
  - Count validity: pass — positive searches and clicks between zero and searches [measured].
  - Independent aggregation: pass — deduplicated join reproduces totals [measured].

## Caveats, and what would change the answer
- The interval uses 10,000 query-level bootstrap samples; it assumes queries represent a broader population. The recorded rate itself is exact for these rows [inferred].
- Week completeness and whether clicks represent distinct clicked searches are unverified; missing records or a different metric definition could change the answer [inferred].

## Provenance
- Metric: total clicks ÷ total searches × 100, counting each shopping query once; stated here [guess].
- Data: query_week, query_category, category_vertical; latest available period 2026-W41 [measured], completeness unverified [inferred].
- Reconciled: not done (no dashboard or independent source supplied) [inferred].
- Queries and checks: [analysis.py](/private/tmp/ds-runs/ec2c734532/analysis/analysis.py) and [analysis_log.json](/private/tmp/ds-runs/ec2c734532/analysis/analysis_log.json) [measured].
