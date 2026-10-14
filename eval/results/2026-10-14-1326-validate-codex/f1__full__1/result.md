## Answer
Headline: -0.0023 pp (95% interval: -0.153 to +0.148) [check:mix_shift#1] [measured]

CTR fell by 2.0968 pp, decomposed into -2.0945 pp from traffic mix and -0.0023 pp within platform/country segments; the headline is descriptive and would inform attribution only if v2 did not change mix and no other time-varying factors affected CTR. [check:mix_shift#1] [inferred]

- Observed: -2.0968 pp (95% interval: -2.248 to -1.946) [check:mix_shift#1] [measured]
- Adjusted: -0.0023 pp (95% interval: -0.153 to +0.148), holding platform/country shares fixed at their two-week midpoint [check:mix_shift#1] [measured]
- Causal effect: not identified (a concurrent randomized v1/v2 holdout, measuring traffic changes as well as CTR, would identify it). [inferred]

## What it means for the rollback decision
The minimum loss that would trigger rollback was not supplied; the adjusted interval includes both no change and losses up to 0.153 pp, so smaller decision thresholds remain unresolved. [check:mix_shift#1] [inferred]
The aggregate drop alone does not justify attributing harm to v2; use a randomized comparison before treating this adjustment as evidence for or against rollback. [inferred]

## Why we believe it

- Alternatives considered:
  - Traffic mix: ruled in as an arithmetic explanation; mobile share rose from 40.109% to 55.072%, and platform-only adjustment gives -0.0036 pp (95% interval: -0.154 to +0.147), agreeing with platform/country adjustment. [check:mix_shift#1, check:mix_shift#2] [measured]
  - Country mix alone: ruled out as the explanation; country-only adjustment leaves -2.0949 pp (95% interval: -2.246 to -1.944), because it does not hold platform fixed. [check:mix_shift#3] [inferred]
  - Unequal weekday coverage: ruled out; both windows contain every weekday once. Broader seasonality remains unresolved with only two weeks. [q2] [inferred]
  - Missing days or segment cells: ruled out in the supplied extract; all four segments have seven days in each week, with stable daily search totals. Upstream completeness is unverified. [q2, q4] [measured]
  - Logging or definition changes: ruled in as an unresolved possibility; valid counts and a release log containing only the rollout cannot establish unchanged instrumentation. [q3, q5] [inferred]
  - v2 as the cause: ruled in as an unresolved possibility; version and week coincide completely, and there is no concurrent control. [q2, q3] [inferred]
- Checks run:
  - completeness: pass 2026-09-27: 101828 rows = 102% of the trailing days (under 3 weeks of same-weekday history) median (99521.5) [check:completeness#2] [measured]
  - completeness: pass 2026-10-04: 101900 rows = 102% of the trailing days (under 3 weeks of same-weekday history) median (99762) [check:completeness#3] [measured]
  - completeness: could not run: need at least 3 earlier periods (trailing days (under 3 weeks of same-weekday history)) before 2026-09-21, got 0 [check:completeness#1] [measured]
  - mix_shift: flag mix-dominant: overall change -2.10 pp = within-segment -0.00 pp (95% CI -0.15 to +0.15) + mix -2.09 pp (mix share 100%); report the mix shift as part of the answer [check:mix_shift#1, check:mix_shift#2] [measured]
  - mix_shift: pass overall change -2.10 pp = within-segment -2.09 pp (95% CI -2.25 to -1.94) + mix -0.00 pp (mix share 0%) [check:mix_shift#3] [measured]
  - Integrity: pass zero invalid counts or duplicate date/platform/country/ranker keys. [q5] [measured]
  - fanout: skipped (no joins). [measured]
  - srm: skipped (no randomized assignment data). [measured]

## Caveats, and what would change the answer

- Intervals assume independent searches and binomial click outcomes; user clustering and multiple clicks per search cannot be checked from these aggregates. User/session data and the authoritative metric definition would resolve this. [inferred]
- Adjustment can remove part of the total effect if the ranker changed repeat-search behavior or traffic composition; randomized assignment before exposure would resolve attribution. Traffic source and query intent are unavailable. [inferred]
- No load watermark, earlier history, or instrumentation audit is available; completeness checks use search volumes, although their output calls these “rows.” These checks detect gross volume anomalies, not missing upstream events. [inferred]

## Provenance

- Metric: SUM(clicks)/SUM(searches), weighted across daily platform/country/ranker cells in search_daily, with only the requested date filters; from stated here [guess]. DS_OVERLAY_DIR is unset, so no metrics.json is configured. [measured]
- Data: search_daily and release_log; comparison 2026-09-21–2026-09-27 versus 2026-09-28–2026-10-04, through 2026-10-04 (last populated date; completeness supported by coverage and volume checks, not a load watermark). [measured]
- Reconciled: not done (no independent dashboard or trusted metric source supplied). [measured]
- Queries and checks: .ds-queries.log and .ds-checks.log; aggregate analysis reproduced by analyze.py. [measured]
- Verified: verify_readout: pass (44 numbers on 12 lines; 4 queries, 6 checks, 0 given)
