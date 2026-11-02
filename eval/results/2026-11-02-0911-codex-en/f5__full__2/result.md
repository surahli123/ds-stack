## Answer
Headline: can't tell [inferred]  
Treatment’s observed CTR was +1.200 pp higher, but the unexplained user-count imbalance prevents attributing that gap to treatment. [check:mix_shift#1, check:srm#2] [inferred]

- Observed: +1.200 pp (95% CI +1.125 to +1.275; nominal, independent-search assumption). [check:mix_shift#1] [measured]
- Adjusted: +1.200 pp (95% CI +1.125 to +1.275; nominal), holding the arms’ average date distribution of searches fixed. [check:mix_shift#1] [measured]
- Causal effect: not identified (requires validated random assignment, an explanation for the imbalance, and complete outcome capture). [inferred]

## What it means for the launch decision
If any positive lift would justify launch, the nominal observed interval clears that threshold; the actual minimum worthwhile lift was not supplied. [guess] This does not establish a causal improvement: hold the CTR-based launch decision pending an assignment and logging audit. [inferred]

## Why we believe it
- Alternatives considered:
  - Calendar mix, seasonality and day of week: ruled out as explanations based on different observation windows; both arms cover the same dates, and date versus week adjustment agrees, with +0.000 pp calendar-mix contribution at reported precision. [q4, check:mix_shift#1, check:mix_shift#2] [inferred]
  - Population mix or selection: ruled in as unresolved; recorded user totals differ substantially, and no platform, country or traffic-source dimensions are available. [q1, check:srm#2] [inferred]
  - Missing whole days: ruled out by daily coverage; partial or arm-specific missingness remains possible despite stable volumes. [q4] [inferred]
  - Logging or definition changes: ruled in as unresolved; no assignment ledger, logging history or authoritative metric definition is available. [q1] [inferred]
  - Genuine treatment improvement: ruled in as possible by the positive observed gap, but not distinguished from selection or logging bias. [check:mix_shift#1] [inferred]
- Checks run:
  - srm: fail first-day recorded users are 35,700 control versus 33,990 treatment; p=9.32e-11 under equal allocation. These may be active users rather than assignments. [check:srm#2] [measured]
  - srm: fail pooled daily users also mismatch; its significance is unreliable if users recur across days. [check:srm#1] [inferred]
  - completeness: pass volume checks where history permits; could not run for the first three days of each arm because earlier history is unavailable. Stable volume does not certify ingestion completeness. [check:completeness#1, check:completeness#2, check:completeness#3, check:completeness#17, check:completeness#28] [inferred]
  - mix_shift: pass date and week decompositions agree; population-segment checks could not run because dimensions are absent. [check:mix_shift#1, check:mix_shift#2, q1] [measured]
  - validity: pass one aggregate per date and arm; no null, negative or out-of-range metric counts. [q4] [measured]
  - fanout: skipped (no joins). [measured]

## Caveats, and what would change the answer
- Nominal intervals assume binary click outcomes and independent searches. Confirm click semantics and obtain user-level outcomes for uncertainty at the randomization unit. [inferred]
- Obtain unique assignment counts, allocation rules and ingestion reconciliation; resolving the imbalance could change the causal conclusion. [inferred]
- Confirm the CTR definition and minimum worthwhile lift before deciding. [inferred]

## Provenance
- Metric: sum(clicks)/sum(searches), treatment minus control in pp, pooled over daily arm aggregates for ranker_boost, 2026-09-17 through 2026-09-30 inclusive; stated here [guess]. No metrics.json configured.
- Data: warehouse.db, experiment_daily, through 2026-09-30; all requested dates present, last complete period not independently certified. [q4] [measured]
- Reconciled: not done (no dashboard or independent source supplied). [measured]
- Queries and checks: .ds-queries.log and .ds-checks.log; reproducible aggregate checks in analyze.py. [measured]
- Verified: verify_readout: pass (12 numbers on 5 lines; 2 queries, 9 checks, 0 given)
