## Answer
Headline: can't tell [inferred]  
Treatment’s observed CTR was higher by 1.200 percentage points, but the user-count imbalance prevents a reliable causal conclusion. [measured; inferred]
- Observed: +1.200 percentage points (95% interval: +1.125 to +1.275; assumes independent searches). [measured]
- Adjusted: +1.200 percentage points (95% interval: +1.125 to +1.275; assumes independent searches), holding calendar-day mix fixed. [measured]
- Causal effect: not identified (requires validated randomized assignments and complete outcome capture, with the imbalance explained or corrected). [inferred]

## What it means for the launch decision
The smallest decision-changing improvement was not supplied; the nominal interval clears thresholds below +1.125 percentage points, overlaps thresholds within the interval, and falls below thresholds above +1.275. [measured] Do not use this interval alone to justify launch: it excludes assignment or logging bias and does not account for repeated searches by users. [inferred]

## Why we believe it
- Alternatives considered:
  - Calendar-day composition: ruled out as a material explanation by the unchanged day-adjusted lift. [measured]
  - Assignment, activity-selection, or logging imbalance: ruled in as unresolved possibilities by daily user-count split failures; these aggregates cannot distinguish the causes. [inferred]
- Checks run:
  - SRM: fail on every daily user-count split; first-day control/treatment counts were 35,700/33,990, p = 9.32×10⁻¹¹. These are observed users, not verified assignment counts. [measured]
  - Completeness: pass for final-day user and search volumes in both arms against trailing-day baselines; actual load completion is unverified. [measured; inferred]
  - Mix shift: pass; calendar-day mix contribution rounds to 0.000 percentage points. [measured]
  - Integrity: pass; no duplicate date/arm records or invalid counts found. [measured]
  - Fanout: skipped; no database joins used. [measured]

## Caveats, and what would change the answer
- Intervals assume binary, independent search outcomes; user-level records are needed for uncertainty that accounts for repeated users. [inferred]
- Summed daily users may repeat people, so pooled SRM is only diagnostic; daily checks also fail. [measured; inferred]
- Assignment logs, metric documentation, load confirmation, and the launch threshold would enable a stronger decision assessment. [inferred]

## Provenance
- Metric: CTR = summed clicks / summed searches; lift = treatment minus control, in percentage points, stated here [guess]; no metrics.json supplied. [measured]
- Data: warehouse.db → experiment_daily, filtered to ranker_boost, 2026-09-17 through 2026-09-30; last available day passes volume checks, but last complete period is unverified. [measured]
- Reconciled: not done (no independent dashboard or source supplied). [measured]
- Queries and checks: [queries](analysis_output/queries.json), [check results](analysis_output/checks.json), [reproducible script](analysis_output/analyze.py), and [.ds-checks.log](.ds-checks.log). [measured]
