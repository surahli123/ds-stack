## Answer
Headline: +50.05% (95% interval: 49.93%–50.18%) [q3] [measured]

For 2026-10-05 through 2026-10-11, 321,780 of 642,880 external searches with results had a click; CTR was 50.05%. [q3] [measured]

- Observed: +50.05% (95% interval: 49.93%–50.18%) [q3] [measured]
- Adjusted: not computed (the request is for the weekly level, without a comparison or standardization target). [inferred]
- Causal effect: not identified (an intervention and randomized or credible quasi-experimental comparison would be needed). [inferred]

## What it means for the weekly business review
Report 50.05% as the weekly CTR level, not a change. [q3] [measured]
No decision threshold or smallest meaningful change was supplied, so the interval cannot establish whether action is warranted. [inferred]

## Why we believe it
- Alternatives considered:
  - Counting every click or including searches without results: ruled out by metrics.json; those alternatives yield 70.07% and 46.05%, respectively. [q3] [measured]
  - Missing dates or duplicate aggregate cells: ruled out by seven dates and 42 unique cells across 42 rows. [q4] [measured]
  - Partial ingestion: not ruled out; daily volumes are consistent, but historical coverage and load-status evidence are limited. [q2] [inferred]
  - Mix-shift, seasonality, and day of week: not ruled out as influences on the level; no change or cause is being estimated. [inferred]
  - Logging changes: not ruled out; the database contains no logging audit. No cause was proposed by the requester. [q1] [inferred]
- Checks run:
  - completeness: could not run — could not run: need at least 3 earlier periods (trailing days (under 3 weeks of same-weekday history)) before 2026-10-05, got 0 [check:completeness#1] [measured]
  - completeness: could not run — could not run: need at least 3 earlier periods (trailing days (under 3 weeks of same-weekday history)) before 2026-10-06, got 1 [check:completeness#2] [measured]
  - completeness: could not run — could not run: need at least 3 earlier periods (trailing days (under 3 weeks of same-weekday history)) before 2026-10-07, got 2 [check:completeness#3] [measured]
  - completeness: pass — 2026-10-08: 92198 rows = 100% of the trailing days (under 3 weeks of same-weekday history) median (92199) [check:completeness#4] [measured]
  - completeness: pass — 2026-10-09: 89429 rows = 97% of the trailing days (under 3 weeks of same-weekday history) median (92198.5) [check:completeness#5] [measured]
  - completeness: pass — 2026-10-10: 91570 rows = 99% of the trailing days (under 3 weeks of same-weekday history) median (92198) [check:completeness#6] [measured]
  - completeness: pass — 2026-10-11: 93893 rows = 102% of the trailing days (under 3 weeks of same-weekday history) median (91884) [check:completeness#7] [measured]
  - Count validity: pass — no null or invalid search numerators/denominators. [q2] [measured]
  - fanout: skipped — no joins. [inferred]
  - mix_shift: skipped — no rate change estimated. [inferred]
  - srm: skipped — no experiment. [inferred]

## Caveats, and what would change the answer
- The Wilson interval assumes independent searches; repeated users may widen uncertainty. It describes an underlying rate, while the recorded week's ratio is exact. User-level data would support clustered uncertainty. [inferred]
- Completeness checks use search volumes; their output calls these “rows.” Load confirmation and earlier history would strengthen completeness assurance; late or corrected records could change the answer. [inferred]

## Provenance
- Metric: SUM(searches_with_click) / SUM(searches_with_results) × 100, search grain, traffic_type = 'external', inclusive requested dates; from metrics.json in the configured overlay. Excludes bot/internal traffic and searches without results. [inferred]
- Data: search_daily_v, through 2026-10-11; all requested dates present, last complete period not independently certified. [q4] [measured]
- Reconciled: not done (no dashboard value for this week is available; metrics.json records an earlier definition reconciliation). [inferred]
- Queries and checks: .ds-queries.log and .ds-checks.log; SQL and interval calculation are logged. [measured]
- Verified: verify_readout: pass (39 numbers on 13 lines; 4 queries, 7 checks, 0 given)
