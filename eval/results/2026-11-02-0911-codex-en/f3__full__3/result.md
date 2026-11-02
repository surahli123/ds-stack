## Answer
Headline: -1.817 pp (95% interval: -1.967 to -1.667), adjusted association [check:mix_shift#1] [measured]

CTR fell by 1.827 pp after rollout; attributing the adjusted decline to v3 assumes no concurrent changes or underlying trend and no ranker effect on traffic mix. [check:mix_shift#1] [inferred]

- Observed: -1.827 pp (95% interval: -1.978 to -1.675). [check:mix_shift#1] [measured]
- Adjusted: -1.817 pp (95% interval: -1.967 to -1.667), holding platform × country × weekday shares fixed at their between-week averages. [check:mix_shift#1] [measured]
- Causal effect: not identified (a randomized concurrent v2 holdout, or a credible untreated comparison with validated parallel trends, would identify it). [q4] [inferred]

## What it means for the rollback decision
The adjusted interval lies entirely beyond any decline threshold smaller than 1.667 pp, but it is not an interval for v3’s causal effect. [check:mix_shift#1] [inferred]

The smallest decline that warrants rollback was not supplied; these results support investigating the desktop regression urgently, but cannot establish that rollback will recover the lost CTR. [q4] [inferred]

## Why we believe it

- Alternatives considered:
  - Measured traffic mix: ruled out as the main explanation; its contribution is -0.010 pp, versus -1.817 pp within segments. Traffic source and query mix are unavailable. [check:mix_shift#1] [measured]
  - Unequal weekday composition: ruled out as the main explanation by matching full Monday–Sunday windows and weekday adjustment; broader seasonality remains possible. [q2, check:mix_shift#1] [inferred]
  - Missing dates or segment rows: ruled out in this extract; all 14 dates contain all 4 platform-country cells, with no duplicate keys or invalid counts. Missing events within cells remain untested. [q2, q5] [measured]
  - Logging or definition changes: ruled in as unresolved possibilities; the release log records only the ranker rollout, and there is no instrumentation audit or independent metric source. [q1, q3] [inferred]
  - v3 regression: ruled in as a candidate, not established; desktop CTR fell about 3.00 pp while mobile fell 0.04 pp, but both platforms received v3, so mobile is not an untreated control. [q4, check:mix_shift#3] [inferred]
  - Other time-varying causes: ruled in as unresolved possibilities; ranker version and comparison week are perfectly confounded. [q4] [inferred]
- Checks run:
  - completeness: pass 2026-09-06: 4 rows = 100% of the trailing days (under 3 weeks of same-weekday history) median (4) [check:completeness#1] [measured]
  - completeness: pass 2026-09-13: 4 rows = 100% of the trailing days (under 3 weeks of same-weekday history) median (4) [check:completeness#2] [measured]
  - mix_shift: pass overall change -1.83 pp = within-segment -1.82 pp (95% CI -1.97 to -1.67) + mix -0.01 pp (mix share 1%) [check:mix_shift#1] [measured]
  - mix_shift: pass overall change -1.83 pp = within-segment -1.82 pp (95% CI -1.97 to -1.67) + mix -0.01 pp (mix share 1%) [check:mix_shift#2] [measured]
  - mix_shift: pass overall change -1.83 pp = within-segment -1.82 pp (95% CI -1.97 to -1.67) + mix -0.01 pp (mix share 1%) [check:mix_shift#3] [measured]
  - Grain sensitivity: pass weekday-platform-country, platform-country, and platform adjustment agree; the finest cell has 17,398 searches. [check:mix_shift#1, check:mix_shift#2, check:mix_shift#3] [measured]
  - Count validity and uniqueness: pass 56 rows, 56 distinct daily segment-ranker keys, zero invalid rows. [q5] [measured]
  - fanout: skipped no joins were used. [measured]
  - srm: skipped no randomized assignment data or simultaneous control exists in this extract. [q1, q4] [measured]

## Caveats, and what would change the answer

- Intervals use independent Bernoulli searches and fixed segment weights; repeated users or multiple clicks per search could invalidate this uncertainty model. Event definitions and user-level data would resolve this. [inferred]
- Row coverage supports completeness through the requested end date, but no ingestion watermark or event reconciliation confirms it. [inferred]
- Adjustment is descriptive, not causal identification. A randomized holdout and an instrumentation audit would distinguish ranker effects from concurrent changes; longer history would help assess seasonality. [inferred]

## Provenance

- Metric: SUM(clicks) / SUM(searches), weighted by searches across daily platform-country-ranker aggregates, with no filters beyond the two requested date windows, from search_daily; stated here [guess]. DS_OVERLAY_DIR is unset, so no metrics.json definition is available.
- Data: search_daily and release_log, through 2026-09-13; last complete period by observed date/cell coverage, not an ingestion watermark. [q2] [inferred]
- Reconciled: not done (no dashboard or independent trusted source provided). [measured]
- Queries and checks: .ds-queries.log and .ds-checks.log; analyze.py reproduces checks from logged aggregates. [measured]
- Verified: verify_readout: pass (46 numbers on 15 lines; 5 queries, 5 checks, 0 given)
