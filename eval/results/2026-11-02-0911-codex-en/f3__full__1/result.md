## Answer
Headline: can't tell [inferred]

Overall CTR fell from 30.441% to 28.615%, a decline of 1.827 pp coinciding with the rollout; the amount attributable to v3 is not identified. [q6] [measured] [inferred]

- Observed: -1.827 pp (95% CI: -1.978 to -1.675). [check:mix_shift#1] [measured]
- Adjusted: -1.817 pp (95% CI: -1.966 to -1.667), holding platform × country shares fixed at their two-week midpoint; descriptive, not causal. [check:mix_shift#1] [measured]
- Causal effect: not identified (a randomized v2 holdout, or a credible unaffected comparison with supported parallel trends, would identify it). [q3] [inferred]

## What it means for the rollback decision
The rollback threshold was not supplied; the adjusted interval indicates a descriptive decline of 1.667–1.966 pp, but cannot establish whether causal harm exceeds your decision threshold. [check:mix_shift#1] [inferred]

These data warrant investigating the desktop decline and running a randomized comparison; they do not establish that reverting the ranker would recover CTR. [q4, q7] [inferred]

## Why we believe it
- Alternatives considered:
  - Platform/country mix: ruled out as the main explanation; mix contributes only -0.010 pp of the observed decline. [check:mix_shift#1] [measured]
  - Unequal weekday coverage: ruled out by complete Monday–Sunday windows; broader seasonality remains possible without earlier history. [q3, q5] [inferred]
  - Missing daily segment records: ruled out by all expected daily cells and unique keys; partial event ingestion remains unverified. [q3, q5] [inferred]
  - Logging or definition changes: ruled in as an unresolved alternative; the database has no instrumentation audit, and the release log only records the rollout. [q1, q2] [inferred]
  - Ranker regression: ruled in as a candidate, not established; desktop CTR falls while mobile is nearly flat, but both platforms received treatment. Mobile is not an untreated control. [q3, q4, q7] [inferred]
- Checks run:
  - completeness: pass 2026-09-06: 4 rows = 100% of the trailing days (under 3 weeks of same-weekday history) median (4) [check:completeness#1] [measured]
  - completeness: pass 2026-09-13: 4 rows = 100% of the trailing days (under 3 weeks of same-weekday history) median (4) [check:completeness#2] [measured]
  - mix_shift: pass overall change -1.83 pp = within-segment -1.82 pp (95% CI -1.97 to -1.67) + mix -0.01 pp (mix share 1%) [check:mix_shift#1] [measured]
  - mix_shift: pass overall change -1.83 pp = within-segment -1.82 pp (95% CI -1.97 to -1.67) + mix -0.01 pp (mix share 1%) [check:mix_shift#2] [measured]
  - Grain sensitivity: pass platform-only and platform × country decompositions agree. [check:mix_shift#1, check:mix_shift#2] [measured]
  - Integrity: pass no null/invalid metric rows or duplicate daily segment-ranker keys. [q5] [measured]
  - fanout: skipped no joins used. [measured]
  - srm: skipped no randomized assignment or concurrent holdout. [q3] [measured]

## Caveats, and what would change the answer
- Intervals assume independent searches and binomial clicks. User clustering and multiple clicks per search cannot be assessed from these aggregates; event-level metric validation and clustered inference could change the intervals. [inferred]
- Attributing the adjusted decline to v3 requires assuming no concurrent within-segment changes and no treatment-induced mix changes; these assumptions are untested. [inferred]
- Row coverage supports apparent completeness through 2026-09-13, but no ingestion watermark or independent click totals verify full event capture. Audit desktop logging and ingestion before acting. [inferred]

## Provenance
- Metric: SUM(clicks) / SUM(searches), search-weighted across all platform/country/ranker rows in each requested week, from search_daily; stated here [guess]. No metrics.json was supplied via DS_OVERLAY_DIR.
- Data: search_daily and release_log; last apparently complete period 2026-09-13, based on daily coverage rather than a certified watermark. [measured] [inferred]
- Reconciled: not done (no independent dashboard or trusted metric totals supplied). [measured]
- Queries and checks: .ds-queries.log and .ds-checks.log; reproducible checks in analyze.py. [measured]
- Verified: verify_readout: pass (32 numbers on 9 lines; 7 queries, 4 checks, 0 given)
