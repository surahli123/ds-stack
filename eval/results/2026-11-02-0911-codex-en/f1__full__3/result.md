## Answer
Headline: -0.002 pp (95% interval: -0.153 to +0.148) [measured] [check:mix_shift#2]

CTR fell by 2.097 pp, with -2.094 pp assigned to mix and -0.002 pp to within-group change; interpreting the adjusted headline as attributable to v2 requires assuming v2 did not change traffic mix and no other factors changed within groups. [measured: decomposition; inferred: attribution assumptions] [check:mix_shift#2]

- Observed: -2.097 pp (95% interval: -2.248 to -1.946) [measured] [check:mix_shift#2]
- Adjusted: -0.002 pp (95% interval: -0.153 to +0.148), holding platform/country shares fixed at the average of the two weeks' shares [measured] [check:mix_shift#2]
- Causal effect: not identified (a concurrent randomized v1/v2 comparison would identify it; ranker and week are completely confounded here) [inferred] [q5]

## What it means for rollback
The smallest decline warranting rollback was not supplied; the adjusted interval includes no change and declines as large as 0.153 pp, so it cannot resolve a rollback threshold inside that range. [inferred] [check:mix_shift#2]

The aggregate drop alone does not justify attributing harm to v2; use a randomized comparison before making a causal rollback decision. [inferred] [q5]

## Why we believe it

- Alternatives considered:
  - Mix shift: ruled in by mobile share increasing from 40.11% to 55.07%, while mobile CTR stayed near 22% versus desktop near 36%; the mix component is -2.094 pp. [measured] [check:mix_shift#2, check:mix_shift#3]
  - Day-of-week imbalance: ruled out for calendar coverage because both windows contain a complete Monday–Sunday cycle; broader seasonality remains possible without earlier history. [inferred] [q4]
  - Missing days or duplicate aggregate cells: ruled out by complete daily coverage and unique date/platform/country/ranker keys; partial event ingestion remains unverified. [measured] [q4, q5, q6]
  - Logging or definition changes: ruled in as unresolved possibilities; the release log records only rollout and supplies no instrumentation audit. [inferred] [q1, q3]
  - v2 harm or another concurrent change: ruled in as unresolved possibilities because there is no concurrent control; stable adjusted CTR does not establish zero causal effect. [inferred] [q5]
- Checks run:
  - completeness: pass 2026-09-27: 4 rows = 100% of the trailing days (under 3 weeks of same-weekday history) median (4) [measured] [check:completeness#3]
  - completeness: pass 2026-10-04: 4 rows = 100% of the trailing days (under 3 weeks of same-weekday history) median (4) [measured] [check:completeness#4]
  - mix_shift: flag mix-dominant: overall change -2.10 pp = within-segment -0.00 pp (95% CI -0.15 to +0.15) + mix -2.09 pp (mix share 100%); report the mix shift as part of the answer [measured] [check:mix_shift#2]
  - Coarser platform check: flag adjusted -0.004 pp (95% interval: -0.154 to +0.147), consistent with platform/country adjustment. [measured] [check:mix_shift#3]
  - Count validity and uniqueness: pass no invalid counts or duplicate cells. [measured] [q2, q6]
  - fanout: skipped no joins used. [measured]
  - srm: skipped no randomized assignment data available. [measured] [q1, q5]

## Caveats, and what would change the answer

- Intervals assume independent searches and binomial click outcomes; user-level data and confirmation that clicks count searches with a click would validate this uncertainty model. [inferred]
- Adjusting for mix could remove part of v2's effect if v2 changed repeat-search behavior; randomized assignment with user-level outcomes would resolve this. [inferred]
- Traffic source, query intent, instrumentation audits, and ingestion watermarks are unavailable; these could change the adjusted result or its interpretation. [inferred]
- Specify the minimum rollback-worthy decline to make the decision criterion explicit. [inferred]

## Provenance

- Metric: SUM(clicks)/SUM(searches), all platform/country/ranker cells within each requested week, from search_daily at daily platform/country/ranker grain; stated here [guess]. No metrics.json is configured.
- Data: search_daily and release_log, through 2026-10-04; daily coverage is complete, ingestion completeness is not independently certified. [measured]
- Reconciled: not done (no dashboard or independent source supplied). [measured]
- Queries and checks: .ds-queries.log and .ds-checks.log; reproducible checks in run_checks.py. [measured]
- Verified: verify_readout: pass (35 numbers on 10 lines; 6 queries, 4 checks, 0 given)
