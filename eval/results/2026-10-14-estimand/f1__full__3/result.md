Readout is written and verified; sending it now.

```
## Answer
Headline: -0.00 pp (-0.15 to +0.15) [check:mix_shift#1]
Overall CTR fell 2.10 pp, but essentially all of it is a shift in traffic toward mobile (lower-CTR); within platform, CTR did not move, if v2 did not itself change the platform mix. [check:mix_shift#1]
- Observed: -2.10 pp (-2.25 to -1.95) [check:mix_shift#1]
- Adjusted: -0.00 pp (-0.15 to +0.15), holding platform mix fixed [check:mix_shift#1]
- Causal effect: not identified (no randomized holdout; v1 and v2 never ran side by side, so a pre/post comparison only; a v1 holdout or A/B split would identify it)

## What it means for the rollback decision
The within-platform change is -0.00 pp, and its interval (-0.15 to +0.15 pp) excludes any drop larger than about 0.15 pp, so the data show no sign v2 lowered CTR on a like-for-like basis; the 2.10 pp headline drop is a mix effect. [check:mix_shift#1] No threshold for rollback was given, so the comparison is against the 2.10 pp observed drop.

## Why we believe it
- Alternatives considered:
  - Mix-shift: ruled in. Mobile share rose from 40.1% to 55.1% of searches, while mobile CTR (22.0%) is far below desktop (36.0%). Mix accounts for -2.09 pp [check:mix_shift#1] [measured]
  - Finer grain (platform x country) agrees: within-segment -0.00 pp (-0.15 to +0.15) [check:mix_shift#2] [measured]
  - v2 lowered CTR (PM's cause): not supported. Within-platform CTR is flat for desktop (36.05% to 36.01%) and mobile (22.02% to 22.06%) [q6] [measured]
  - Whether v2 caused the platform shift: not ruled out; no evidence either way in this data [guess]
  - Data completeness: ruled out. All 14 days have 4 rows each, and the last day is complete [check:completeness#2] [measured]
  - Day of week/seasonality: both windows are full Mon-Sun weeks of the same length [q3]; the data holds no earlier weeks, so a seasonal level can't be checked [inferred]
  - Logging/definition change: release_log lists only the v2 rollout on 2026-09-28 [q2] [measured]
- Checks run:
  - mix_shift (platform): flag, mix-dominant, within-segment -0.00 pp, mix -2.09 pp [check:mix_shift#1]
  - mix_shift (platform x country): flag, same split [check:mix_shift#2]
  - completeness: fail on first call (my spec omitted 2026-10-04 from the series; the error was mine, not the data's) [check:completeness#1]
  - completeness: pass on corrected rerun, 2026-10-04 has 4 rows [check:completeness#2]
  - fanout: skipped, no joins used
  - srm: skipped, not a randomized experiment

## Caveats, and what would change the answer
- Intervals assume independent searches (daily/user clustering would widen them); a user-level or day-level interval would settle it.
- If v2 itself pushed traffic toward mobile (e.g. app/UI change shipped with it), part of the drop would be v2-related; the traffic-source logs or a v1 holdout would settle it.
- Only one week on each side, no earlier weeks, so no seasonality baseline.
- CTR definition is my own; a metrics.json would confirm it.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches) over search_daily, grouped by week, platform and country [guess]
- Data: search_daily, release_log, through 2026-10-04
- Reconciled: not done (no dashboard or other source available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (33 numbers on 11 lines; 3 queries, 4 checks, 0 given)
```