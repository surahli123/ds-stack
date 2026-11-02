## Answer

Headline: can't tell [inferred]

Treatment’s observed CTR was higher by 1.20 percentage points, but the user-count imbalance prevents a trustworthy causal conclusion. [measured; inferred]

- Observed: +1.200 percentage points (95% interval: +1.125 to +1.275; assumes independent searches). [measured]
- Adjusted: +1.200 percentage points (95% interval: +1.125 to +1.275; assumes independent searches), holding date mix fixed using midpoint search weights. [measured]
- Causal effect: not identified (requires validated random assignment, an explanation of the imbalance, and complete outcomes by assigned unit). [inferred]

## What it means for the launch decision

The smallest lift that would change the decision was not supplied; the nominal interval exceeds zero and thresholds below +1.125 percentage points. [measured] Do not use that interval as causal evidence for launch until the imbalance is resolved. [inferred]

## Why we believe it

- Alternatives considered:
  - Date composition explains the lift: ruled out as a material explanation by the date-adjusted result. [measured]
  - Assignment, inclusion, or logging imbalance: ruled in as an unresolved explanation by daily user counts inconsistent with the planned split. [inferred]
- Checks run:
  - Completeness: pass; final-day row count and search volume match their trailing medians, but this does not certify upstream loading. [measured; inferred]
  - SRM: fail; every day has approximately 51.23% control versus 48.77% treatment users, with daily p-values below 10⁻¹⁰ under the assignment-count interpretation. [measured]
  - Mix shift: pass; date composition contributes approximately 0.000 percentage points. [measured]
  - Coverage and count validity: pass; both arms appear on every experiment date, with valid numerator/denominator bounds. [measured]
  - Fanout: skipped; no joins used. [measured]

## Caveats, and what would change the answer

- Daily `users` may represent active users rather than assigned users; assignment logs would distinguish broken allocation from differential activity or missing data. [inferred]
- Both intervals assume independent binary search outcomes; repeated users and multiple clicks could invalidate them. User-level outcomes would support appropriate uncertainty estimates. [inferred]
- Date adjustment cannot repair selection bias. Resolve the imbalance or rerun a validated experiment, and specify the minimum worthwhile lift. [inferred]

## Provenance

- Metric: CTR = total clicks / total searches; lift = treatment CTR minus control CTR, in percentage points, stated here [guess]; no `metrics.json` supplied.
- Data: `warehouse.db`, `experiment_daily`, filtered to `ranker_boost`, 2026-09-17 through 2026-09-30; final date passes completeness proxies, actual load completion unverified. [measured; inferred]
- Reconciled: not done (no dashboard or independent source supplied). [measured]
- Queries and checks: [queries and results](analysis_output/queries.json), [check results](analysis_output/checks.jsonl), [reproducible analysis](analysis_output/analyze.py), and `.ds-checks.log`. [measured]
