## Answer
Headline: -0.00 pp (-0.15 to +0.15) [check:mix_shift#1]
Overall CTR fell 2.10 pp, but essentially all of it is a shift in traffic toward lower-CTR mobile; within-platform/country CTR did not move, so v2's own effect on CTR looks like zero, assuming v2 did not itself cause the traffic mix change. [check:mix_shift#1]
- Observed: -2.10 pp (-2.25 to -1.95) [check:mix_shift#1]
- Adjusted: -0.00 pp (-0.15 to +0.15), holding platform x country mix fixed [check:mix_shift#1]
- Causal effect: not identified (no concurrent control: v2 went to all traffic on one day, so a holdout or staggered/randomized rollout would identify it)

## What it means for the rollback decision
The within-segment interval (-0.15 to +0.15 pp) excludes any v2 CTR loss near the 2.10 pp drop, so the drop is not evidence against v2; rolling back would not be expected to recover it unless the mobile mix shift is itself caused by v2. [check:mix_shift#1]

## Why we believe it
- Alternatives considered:
  - Mix shift (mobile share 40.1% to 55.1%): ruled in as the explanation of the drop; mix effect -2.09 pp of -2.10 pp [check:mix_shift#1, check:mix_shift#2] [measured]
  - Mix shift check at coarser grain (platform only): agrees, within-segment -0.00 pp [check:mix_shift#2] [measured]
  - v2 lowered CTR within segments (PM's cause): ruled out as a material effect; per-segment CTR unchanged to within 0.15 pp [check:mix_shift#1] [measured]
  - Data completeness: ruled out, last day has all expected rows [check:completeness#1] [measured]
  - Day of week / seasonality: ruled out as main driver, both windows are full Mon-Sun weeks and the CTR step happens exactly on 2026-09-28 [q3] [inferred]
  - Logging/definition change: ruled out as far as visible; release_log lists only the v2 rollout [q2] [inferred]
  - v2 caused the mobile traffic increase (e.g. via surfaces/traffic routing): not ruled out; the mix shift began the same day as v2 and no data here separates them [q3] [guess]
- Checks run:
  - mix_shift (platform x country): flag, mix explains ~100% of the change [check:mix_shift#1]
  - mix_shift (platform): flag, same conclusion at coarser grain [check:mix_shift#2]
  - completeness: pass [check:completeness#1]
  - fanout: skipped, no joins used
  - srm: skipped, not a randomized experiment

## Caveats, and what would change the answer
- The mix shift coincides with the rollout day; if v2 drives users to mobile (or changes search volume by platform), v2 could still be indirectly responsible. Check what else changed 2026-09-28 (mobile app release, campaigns, routing) or compare with a holdout.
- Intervals assume independent units (check notes this); user-level clustering would widen them.
- Only one week on each side; no concurrent control.
- Only 4 segment cells (platform x country); other mix dimensions are not in the data.

## Provenance
- Metric: CTR = sum(clicks)/sum(searches) over search_daily, pooled across all rows per week, stated here [guess]
- Data: search_daily, release_log, through 2026-10-04
- Reconciled: not done (no dashboard or metrics.json available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (20 numbers on 9 lines; 2 queries, 3 checks, 0 given)