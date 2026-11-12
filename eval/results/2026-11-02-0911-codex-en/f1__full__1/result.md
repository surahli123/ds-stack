## Answer
Headline: -0.002 pp (95% interval: -0.152 to +0.149) [check:mix_shift#1] [measured]

CTR fell by 2.097 pp, comprising -2.095 pp of mix change and -0.002 pp within comparable groups; attributing the latter to v2 requires assuming v2 did not change mix and no other time-varying factors affected CTR. [check:mix_shift#1] [inferred]

- Observed: -2.097 pp (95% interval: -2.248 to -1.946) [check:mix_shift#1] [measured]
- Adjusted: -0.002 pp (95% interval: -0.152 to +0.149), holding weekday × platform × country shares fixed at their two-week midpoint [check:mix_shift#1] [measured]
- Causal effect: not identified (a concurrent randomized v1/v2 holdout would identify it; the headline is descriptive adjustment) [q4] [inferred]

## What it means for rollback
The smallest rollback-worthy decline was not supplied; the adjusted interval includes no change and declines up to 0.152 pp, so it cannot exclude a smaller harmful change. [check:mix_shift#1] [inferred] This comparison alone does not justify attributing the drop to the ranker or rolling it back; use a randomized holdout and a specified decision threshold. [q4] [inferred]

## Why we believe it
- Alternatives considered:
  - Traffic mix: ruled in by mobile's share rising from 40.11% to 55.07%, with mobile CTR substantially below desktop CTR. [check:mix_shift#3] [measured]
  - Unequal weekday coverage: ruled out by complete Monday–Sunday windows and weekday-adjusted results; broader seasonality remains unresolved without longer history or a control. [q3, check:mix_shift#1] [inferred]
  - Missing daily cells: ruled out by all 14 dates having four segment rows and each weekly segment having seven rows; partial event ingestion remains unverified. [q3, q4] [measured]
  - Logging changes or other simultaneous changes: ruled in as unresolved possibilities; the release log records only the rollout and supplies no instrumentation audit. [q2] [inferred]
  - Ranker effect: ruled in as an unresolved possibility because ranker and week are perfectly confounded; stable adjusted CTR does not establish a zero total effect. [q4] [inferred]
- Checks run:
  - completeness: pass 2026-09-27: 4 rows = 100% of the trailing days (under 3 weeks of same-weekday history) median (4) [check:completeness#1] [measured]
  - completeness: pass 2026-10-04: 4 rows = 100% of the trailing days (under 3 weeks of same-weekday history) median (4) [check:completeness#2] [measured]
  - mix_shift: flag mix-dominant: overall change -2.10 pp = within-segment -0.00 pp (95% CI -0.15 to +0.15) + mix -2.10 pp (mix share 100%); report the mix shift as part of the answer [check:mix_shift#1] [measured]
  - mix_shift: flag mix-dominant: overall change -2.10 pp = within-segment -0.00 pp (95% CI -0.15 to +0.15) + mix -2.09 pp (mix share 100%); report the mix shift as part of the answer [check:mix_shift#2, check:mix_shift#3] [measured]
  - Grain sensitivity: pass adjusted changes are -0.002, -0.002 and -0.004 pp for weekday/platform/country, platform/country and platform; conclusions agree. [check:mix_shift#1, check:mix_shift#2, check:mix_shift#3] [measured]
  - Validity and uniqueness: pass zero invalid count rows or duplicate date/platform/country/ranker keys. [q5, q6] [measured]
  - fanout: skipped no joins performed. [measured]
  - srm: skipped no randomized assignment data or concurrent comparison arms. [q1, q4] [measured]

## Caveats, and what would change the answer
- Intervals assume independent searches and binary click outcomes; user-level data and confirmation that clicks count clicked searches are needed to validate uncertainty. [inferred]
- Adjusting for mix can remove part of the rollout's effect if the ranker changed repeat-search behavior; a randomized holdout would distinguish this from external traffic changes. [inferred]
- Traffic source, query intent, ingestion watermarks and longer history are unavailable; obtaining them could alter adjustment or completeness conclusions. [measured]

## Provenance
- Metric: SUM(clicks)/SUM(searches), search-weighted over all platform/country cells in search_daily, comparing 2026-09-21–2026-09-27 with 2026-09-28–2026-10-04; no additional filters, daily/platform/country/ranker grain; stated here [guess]. No metrics.json configured.
- Data: search_daily and release_log, through 2026-10-04; daily cell coverage complete, ingestion completeness unverified. [measured]
- Reconciled: not done (no independent dashboard or source supplied). [measured]
- Queries and checks: .ds-queries.log and .ds-checks.log; reproduction script analyze.py. [measured]
- Verified: verify_readout: pass (39 numbers on 12 lines; 6 queries, 5 checks, 0 given)
