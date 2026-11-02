## Answer
Headline: can't tell [inferred]

Treatment's recorded CTR was higher by +1.200 pp, but the unresolved user-count imbalance prevents attributing that difference to treatment. [check:mix_shift#1, check:srm#1] [inferred]

- Observed: +1.200 pp (95% interval: +1.125 to +1.275), nominal independent-search interval. [check:mix_shift#1] [measured]
- Adjusted: +1.200 pp (95% interval: +1.125 to +1.275), holding calendar-day search mix fixed; same independence assumption. [check:mix_shift#1] [measured]
- Causal effect: not identified (requires validated random assignment, an explanation of the imbalance, and complete outcomes for assigned users). [inferred]

## What it means for the launch decision
The launch threshold was not supplied; if any positive lift suffices, the nominal observed interval clears that threshold, but it does not establish a positive causal effect. [check:mix_shift#1] [inferred]

Do not approve launch on this CTR result alone; resolve the imbalance and compare a valid causal interval with the minimum worthwhile lift. [inferred]

## Why we believe it
- Alternatives considered:
  - Calendar mix, seasonality and day of week: ruled out as the material observed explanation by concurrent dates and agreeing daily and weekly adjustments; estimated mix contribution rounds to +0.000 pp. [check:mix_shift#1, check:mix_shift#2] [inferred]
  - Assignment or selection imbalance: ruled in as unresolved; summed daily users are 499,930 control versus 475,990 treatment, inconsistent with the planned equal split if these are independent assignments. [q2, check:srm#1] [inferred]
  - Missing data or changed logging/definitions: ruled in as unresolved possibilities; stable daily volumes cannot detect systematic arm-specific omissions, and no loading or instrumentation audit is available. [q1, q3] [inferred]
  - Treatment improvement: ruled in as a possible explanation of higher recorded CTR, but not isolated from selection or logging differences. [check:mix_shift#1, check:srm#1] [inferred]
  - Platform, country or traffic-source mix: ruled in as untested alternatives; those dimensions are absent. [q1] [inferred]
- Checks run:
  - srm: fail sample ratio mismatch: observed shares [0.512265, 0.487735] vs expected [0.5, 0.5]: chi2 587.26, p 9.86e-130; arms are not comparable until the cause is found [check:srm#1] [measured]
  - completeness: pass 2026-09-30: 214260 rows = 100% of the trailing days (under 3 weeks of same-weekday history) median (214260) [check:completeness#15] [measured]
  - completeness: pass 2026-09-30: 204000 rows = 100% of the trailing days (under 3 weeks of same-weekday history) median (204000) [check:completeness#29] [measured]
  - completeness: could not run for the opening days because earlier history is insufficient; later days pass volume checks, which use searches as underlying event counts. [q4] [measured]
  - mix_shift: pass overall change +1.20 pp = within-segment +1.20 pp (95% CI +1.12 to +1.27) + mix +0.00 pp (mix share 0%) [check:mix_shift#1, check:mix_shift#2] [measured]
  - fanout: skipped (no joins). [measured]
  - Count validity: pass no null, negative or impossible counts under the assumed binary-click definition; one row per date and arm. [q3, q4] [measured]

## Caveats, and what would change the answer
- Daily users may recur or represent active users rather than assignments; the SRM p-value is conditional on independent assignment counts. Obtain unique assignment records and eligibility/exposure definitions. [inferred]
- Searches can cluster within users; nominal intervals may understate uncertainty. User-level outcomes are needed for assignment-unit inference. [inferred]
- Confirm CTR's denominator and whether clicks represent searches with a click; supply the launch threshold and logging/load audits. [inferred]

## Provenance
- Metric: sum(clicks)/sum(searches), search-weighted within each arm, filtering experiment='ranker_boost' and dates 2026-09-17 through 2026-09-30 inclusive, from experiment_daily; stated here [guess]. No metrics.json was available because DS_OVERLAY_DIR was unset. [measured]
- Data: experiment_daily, through 2026-09-30; last available period passes volume checks, but load completeness is not independently certified. [q1, q2, check:completeness#15, check:completeness#29] [measured]
- Reconciled: not done (no dashboard or independent source supplied). [measured]
- Queries and checks: .ds-queries.log and .ds-checks.log; reproduction script: analyze.py. [measured]
- Verified: verify_readout: pass (31 numbers on 9 lines; 4 queries, 5 checks, 0 given)
