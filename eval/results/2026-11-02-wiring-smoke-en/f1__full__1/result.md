```
## Answer
Headline: -0.00 pp (-0.15 to +0.15) [check:mix_shift#1]
Overall CTR fell 2.10 pp (30.42% to 28.32%), but essentially all of it is a shift in traffic toward lower-CTR mobile; within-platform CTR is flat, so the drop is not attributable to v2 if v2 didn't itself change the platform mix. [check:mix_shift#1]
- Observed: -2.10 pp (-2.25 to -1.95) [check:mix_shift#1]
- Adjusted: -0.00 pp (-0.15 to +0.15), holding platform mix fixed [check:mix_shift#1]
- Causal effect: not identified (v2 launched to all traffic at once with no holdout; a randomized split or a staggered rollout would identify it)

## What it means for the rollback decision
The within-platform interval (-0.15 to +0.15 pp) rules out a v2 CTR loss larger than about 0.15 pp at fixed mix, so the 2.10 pp drop is not a reason to roll back on CTR grounds; the mix shift itself (mobile share 40.1% to 55.1%) needs an owner. [check:mix_shift#1]

## Why we believe it
- Alternatives considered:
  - Mix-shift (mobile share up): ruled in by mix effect -2.09 pp of the -2.10 pp, same result at platform x country grain (-2.09 pp) [check:mix_shift#1, check:mix_shift#2] [measured]
  - v2 lowered CTR within segments: ruled out at more than about 0.15 pp; point estimates are -0.02 pp desktop and +0.02 pp mobile [check:mix_shift#1] [measured]
  - v2 caused the mobile traffic increase (e.g. changed query volume or routing): not ruled out; mobile searches rose from 280,601 to 385,706 while desktop fell from 419,004 to 314,660 in the week v2 launched, and nothing here shows why; traffic-source or logging data, or a holdout, would decide it [q4] [inferred]
  - Data completeness: ruled out; all 14 days have 4 rows (platform x country) [check:completeness#2] [measured]
  - Seasonality / day of week: ruled out for the comparison; both windows are 7 full days covering each weekday once, but no earlier weeks were examined, so a seasonal mobile surge is not excluded [q3] [inferred]
  - Logging or definition change: not ruled out; release_log lists only the v2 rollout, but tracking changes might not be logged; engineering confirmation would decide it [q2] [inferred]
- Checks run:
  - mix_shift (platform): flag, mix-dominant, within-segment -0.00 pp [check:mix_shift#1]
  - mix_shift (platform x country): flag, same split at finer grain [check:mix_shift#2]
  - completeness: pass for 2026-10-04, 4 rows = 100% of median [check:completeness#2]
  - completeness (first call): fail, my spec omitted the 2026-10-04 row; rerun with the full series passes [check:completeness#1]

## Caveats, and what would change the answer
- No holdout: platform-level CTR being flat is consistent with v2 having no effect, but it cannot show causation either way; a v1 holdout would settle it.
- If v2 itself shifted users to mobile, the mix effect would be partly attributable to v2; the cause of the mix change is unexplained.
- Intervals assume independent searches (se_assumes_independent_units), so they are likely somewhat narrow.
- Only two weeks of data; no earlier baseline for trend or seasonality.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches) over search_daily, all platforms and countries, from stated here [guess]
- Data: search_daily, release_log, through 2026-10-04
- Reconciled: not done (no dashboard figure or metrics.json available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (34 numbers on 12 lines; 3 queries, 4 checks, 0 given); ds-verify: pass (0 fail, 0 could not verify, 0 warn, 20 pass)
```