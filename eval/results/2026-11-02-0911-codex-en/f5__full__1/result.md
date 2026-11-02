## Answer
Headline: can't tell [inferred]

Treatment’s observed CTR was higher by +1.200 pp, but the unresolved split imbalance prevents a trustworthy treatment-effect conclusion. [check:mix_shift#1, check:srm#2] [inferred]

- Observed: +1.200 pp (95% interval +1.125 to +1.275), nominal two-proportion interval assuming independent searches. [check:mix_shift#1] [measured]
- Adjusted: +1.200 pp (95% interval +1.125 to +1.275), holding calendar-day search mix fixed; same independence assumption. [check:mix_shift#1] [measured]
- Causal effect: not identified (requires validated assignment counts and an explanation or correction of the imbalance, plus user-level outcomes for valid uncertainty). [check:srm#2] [inferred]

## What it means for the launch decision

The nominal interval excludes zero, but cannot establish that treatment improved CTR; hold the launch decision pending an assignment and logging audit. [check:mix_shift#1, check:srm#2] [inferred] The smallest launch-worthy lift was not supplied, so comparison with the actual decision threshold remains unavailable. [inferred]

## Why we believe it

- Alternatives considered:
  - Assignment or selection imbalance: ruled in as unresolved; daily user totals differ materially, and even the opening day fails the nominal split check. These counts are not verified unique assignments. [q3, check:srm#2] [inferred]
  - Calendar mix and day-of-week effects: ruled out as explanations of the observed gap by simultaneous coverage and unchanged day- and week-adjusted estimates. Other seasonal interactions remain untested. [q4, check:mix_shift#1, check:mix_shift#2] [inferred]
  - Platform, country, or traffic-source mix: ruled in as unexcluded alternatives; no such fields exist. [q1] [inferred]
  - Missing days: ruled out by complete date coverage; partial or differential ingestion remains ruled in as unexcluded without load metadata. [q3] [inferred]
  - Logging or definition changes: ruled in as unexcluded; no instrumentation history or authoritative metric definition is available. [q1] [inferred]
  - Treatment benefit: ruled in as possible, but the positive observed association does not resolve the allocation concern. [check:mix_shift#1, check:srm#2] [inferred]
- Checks run:
  - srm: fail sample ratio mismatch: observed shares [0.512269, 0.487731] vs expected [0.5, 0.5]: chi2 41.96, p 9.32e-11; arms are not comparable until the cause is found [check:srm#2] [measured]
  - srm: fail pooled daily-user screen also fails; repeat users may invalidate its nominal significance, so the opening-day check is the stronger diagnostic. [check:srm#1, check:srm#2] [inferred]
  - completeness: pass volume screens for each arm from September 20 onward; could not run for earlier dates because baseline history is insufficient. These screens do not certify ingestion completeness. [check:completeness#4, check:completeness#14, check:completeness#18, check:completeness#28, check:completeness#1, check:completeness#15] [measured]
  - mix_shift: pass overall change +1.20 pp = within-segment +1.20 pp (95% CI +1.12 to +1.27) + mix +0.00 pp (mix share 0%) [check:mix_shift#1] [measured]
  - mix_shift: pass coarser weekly grouping agrees; demographic and acquisition mix could not run because those dimensions are absent. [check:mix_shift#2, q1] [measured]
  - fanout: skipped (no joins). [measured]
  - integrity: pass no duplicate date-arm rows or invalid/null counts found. [q2, q3] [measured]

## Caveats, and what would change the answer

- Intervals assume independent binary search outcomes; repeated searches per user and multiple clicks could invalidate them. Obtain user-level assignment and outcome data and confirm click semantics. [inferred]
- Determine whether `users` means assigned or active users; activity differences cannot substitute for a true assignment SRM test. Audit exclusions and ingestion, then rerun the causal analysis or experiment. [inferred]
- Confirm the CTR definition and minimum launch-worthy lift before deciding. [inferred]

## Provenance

- Metric: summed clicks / summed searches, search-weighted across daily arm aggregates for ranker_boost from September 17–30 inclusive; from stated here [guess]. No metrics.json was configured.
- Data: experiment_daily in warehouse.db, through 2026-09-30; every date is present, but the last fully loaded period cannot be independently certified. [q3] [measured]
- Reconciled: not done (no dashboard or independent source supplied). [measured]
- Queries and checks: .ds-queries.log and .ds-checks.log; reproducible aggregate checks in analyze.py. [measured]
- Verified: verify_readout: pass (21 numbers on 6 lines; 4 queries, 10 checks, 0 given)
