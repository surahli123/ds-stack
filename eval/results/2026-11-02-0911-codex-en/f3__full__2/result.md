## Answer
Headline: -1.817 pp (95% CI: -1.967 to -1.667) [check:mix_shift#1] [measured]

The rollout coincided with a 1.817 pp adjusted CTR decline; attributing this to v3 requires the unverified assumption that CTR would otherwise have remained unchanged within segments. [check:mix_shift#1] [inferred]

- Observed: -1.827 pp (95% CI: -1.978 to -1.675). [check:mix_shift#1] [measured]
- Adjusted: -1.817 pp (95% CI: -1.967 to -1.667), holding platform × country × weekday shares fixed at their average across the two weeks. [check:mix_shift#1] [measured]
- Causal effect: not identified (a concurrent randomized v2 holdout, or a valid untreated comparison with credible parallel trends, would identify it). [q4] [inferred]

## What it means for the rollback decision
The smallest loss warranting rollback was not supplied: the descriptive interval lies entirely beyond any loss threshold below 1.667 pp, spans thresholds from 1.667 to 1.967 pp, and lies short of thresholds above 1.967 pp. [check:mix_shift#1] [inferred] This supports investigating the decline urgently, but does not establish that rollback would recover it; a randomized rollback comparison would resolve that decision. [inferred]

## Why we believe it

- Alternatives considered:
  - Observed traffic mix: ruled out as the main explanation; mix contributes only -0.010 pp, versus -1.817 pp within segments. [check:mix_shift#1] [measured]
  - Day-of-week composition: ruled out as the main explanation; weekday adjustment and the coarser platform × country adjustment both give -1.82 pp. Broader seasonality remains possible with only these weeks. [check:mix_shift#1, check:mix_shift#2, q3] [inferred]
  - Missing data: ruled out as an obvious explanation by all expected daily cells being present and stable search volumes; ingestion completeness is not independently certified. [q3, q6] [inferred]
  - Logging or definition changes: ruled in as unresolved possibilities; the release log records only the ranker rollout and contains no tracking audit. [q2] [inferred]
  - v3 regression: ruled in as a plausible explanation by timing and declines in both desktop country groups, but all platforms received treatment, so stable mobile performance is not an untreated control. [q4] [inferred]
  - Other simultaneous changes: ruled in as unresolved possibilities; no independent control or longer history is available. [q1, q3, q4] [inferred]
- Checks run:
  - completeness: pass 2026-09-06: 101241 rows = 101% of the trailing days (under 3 weeks of same-weekday history) median (100110) [check:completeness#1] [measured]
  - completeness: pass 2026-09-13: 101528 rows = 101% of the trailing days (under 3 weeks of same-weekday history) median (100524) [check:completeness#2] [measured]
  - mix_shift: pass overall change -1.83 pp = within-segment -1.82 pp (95% CI -1.97 to -1.67) + mix -0.01 pp (mix share 1%) [check:mix_shift#1] [measured]
  - mix_shift: pass overall change -1.83 pp = within-segment -1.82 pp (95% CI -1.97 to -1.67) + mix -0.01 pp (mix share 1%) [check:mix_shift#2] [measured]
  - Cell integrity: pass 56 unique daily platform-country cells; no duplicate cells or invalid counts. [q6] [measured]
  - fanout: skipped no joins used. [measured]
  - srm: skipped no randomized assignment data or concurrent experiment. [q1, q4] [measured]

## Caveats, and what would change the answer

- Intervals assume independent searches and binary click outcomes; repeated users, multiple clicks per search, and daily dependence may invalidate them. Event-level definitions and clustered uncertainty would resolve this. These intervals do not capture causal uncertainty. [inferred]
- The completeness check’s “rows” are search counts; daily cell coverage was checked separately. No load watermark or earlier baseline exists here to certify ingestion. [q3, q6] [measured]
- A tracking audit, query/traffic-source mix, longer history, and a randomized comparison could materially change attribution. Even mix adjustment may remove part of a total effect if the ranker changes subsequent search behavior. [inferred]

## Provenance

- Metric: SUM(clicks) / SUM(searches), weighted by searches, from daily platform-country-ranker aggregates in search_daily; all rows in 2026-08-31–2026-09-06 versus 2026-09-07–2026-09-13; stated here [guess]. DS_OVERLAY_DIR is unset, so no metrics.json definition is configured. [measured]
- Data: search_daily and release_log, through 2026-09-13; complete daily coverage, without independent ingestion certification. [q3, q6] [measured]
- Reconciled: not done (no dashboard or independent metric source supplied). [measured]
- Queries and checks: .ds-queries.log and .ds-checks.log; run_checks.py reproduces the checks. [measured]
- Verified: verify_readout: pass (38 numbers on 12 lines; 5 queries, 4 checks, 0 given)
