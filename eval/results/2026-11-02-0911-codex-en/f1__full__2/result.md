## Answer
Headline: -0.002 pp (95% interval: -0.153 to +0.148) [measured] [check:mix_shift#1]

CTR fell from 30.421% to 28.324%, with -2.095 pp assigned to traffic mix and -0.002 pp to within-segment change; attributing the latter to the rollout assumes it did not change mix and no other factors affected CTR. [measured] [check:mix_shift#1] [inferred]

- Observed: -2.097 pp (95% interval: -2.248 to -1.946) [measured] [check:mix_shift#1]
- Adjusted: -0.002 pp (95% interval: -0.153 to +0.148), holding platform × country shares fixed at their between-week averages [measured] [check:mix_shift#1]
- Causal effect: not identified (a randomized concurrent holdout or a credible untreated comparison would identify it). [inferred]

## What it means for the rollback decision
The raw drop alone does not justify attributing harm to the ranker. [inferred] No rollback threshold was supplied: a harm threshold inside -0.153 to 0 pp remains unresolved even descriptively, while larger harm is outside this model’s interval but is not causally excluded. [check:mix_shift#1] [inferred]

## Why we believe it
- Alternatives considered:
  - Traffic mix: ruled in by mobile share rising from 40.109% to 55.072%; mix accounts for -2.095 pp of the decline. [measured] [check:mix_shift#1, check:mix_shift#2]
  - Unequal weekday coverage: ruled out by complete Monday–Sunday windows; broader seasonality remains unresolved. [q3] [inferred]
  - Missing days or segment cells: ruled out by all 14 dates having 4 cells and stable daily search volumes; undetected ingestion loss remains possible. [q3, q4] [measured]
  - Logging or definition changes: ruled in as an unexcluded possibility; the release log provides no instrumentation audit. [q1, q2] [inferred]
  - Ranker harm: ruled in as an unexcluded causal possibility, but ranker and week are perfectly confounded and the adjusted change is near zero. [q4] [inferred]
- Checks run:
  - completeness: pass 2026-09-27: 101828 rows = 102% of the trailing days (under 3 weeks of same-weekday history) median (99521.5) [check:completeness#1] [measured]
  - completeness: pass 2026-10-04: 101900 rows = 102% of the trailing days (under 3 weeks of same-weekday history) median (99762) [check:completeness#2] [measured]
  - mix_shift: flag mix-dominant: overall change -2.10 pp = within-segment -0.00 pp (95% CI -0.15 to +0.15) + mix -2.09 pp (mix share 100%); report the mix shift as part of the answer [check:mix_shift#1] [measured]
  - mix_shift: flag mix-dominant: overall change -2.10 pp = within-segment -0.00 pp (95% CI -0.15 to +0.15) + mix -2.09 pp (mix share 100%); report the mix shift as part of the answer [check:mix_shift#2] [measured]
  - Integrity: pass 56 unique daily segment/ranker cells, no null dimensions or invalid counts. [q5] [measured]
  - fanout: skipped (no joins). [measured]
  - srm: skipped (no randomized assignment data). [measured]

## Caveats, and what would change the answer
- Headline is descriptive, not an identified causal attribution; a randomized holdout would resolve attribution, including any effect on search mix. [inferred]
- Intervals assume independent Bernoulli searches and fixed segment weights; user clustering, multiple clicks per search, and daily shocks could change them. User-level data and a confirmed metric definition would resolve this. [inferred]
- Traffic source is unavailable; finer composition could change adjustment. Platform-only adjustment agrees: -0.004 pp (95% interval: -0.154 to +0.147). [check:mix_shift#2] [measured]
- Completeness checks use search counts as volume proxies, not ingestion certification; obtain load watermarks and longer history. [inferred]
- Supply the minimum rollback-worthy harm to establish a decision criterion. [inferred]

## Provenance
- Metric: SUM(clicks)/SUM(searches), search-weighted over all platform/country/ranker cells in each requested inclusive week, from search_daily; stated here [guess].
- Data: search_daily and release_log, through 2026-10-04; all requested dates present, ingestion completion not independently certified. [measured]
- Reconciled: not done (no dashboard or independent metric source provided). [measured]
- Queries and checks: `.ds-queries.log` and `.ds-checks.log`; reproducible checks in `run_checks.py`. [measured]
- Verified: verify_readout: pass (41 numbers on 12 lines; 5 queries, 4 checks, 0 given)
