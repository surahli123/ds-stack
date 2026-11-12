## Answer
Headline: -1.82 pp (-1.97 to -1.67) [check:mix_shift#1]
Overall CTR fell from 30.44% to 28.61% week over week. Nearly all of that is a within-segment drop on desktop. It equals v3's effect only if nothing else changed on desktop that week [check:mix_shift#2, q4].
- Observed: -1.83 pp (-1.98 to -1.68) [check:mix_shift#1]
- Adjusted: -1.82 pp (-1.97 to -1.67), holding platform x country mix fixed [check:mix_shift#1]
- Causal effect: not identified (v3 went to 100% on 2026-09-07 with no concurrent control; a holdout or a staggered/A-B rollout would identify it) [q2, q4]

## What it means for the rollback decision
The whole interval is a loss of about 1.7 to 2.0 pp, well beyond the 0.1 pp minimum effect the check uses, so the drop is real, not noise [check:mix_shift#1]. This data doesn't show that v3 is the cause. It is the only logged change, though, and the loss is concentrated in desktop (-1.80 pp) while mobile is flat (-0.02 pp) [q2, check:mix_shift#2].

## Why we believe it
- Alternatives considered:
  - Mix-shift (platform/country): ruled out by mix effect of -0.01 pp, 1% of the change, at both grains [check:mix_shift#1, check:mix_shift#2] [measured]
  - Data completeness / logging: not ruled out; both weeks have 28 rows over 7 days with no zero-search or clicks>searches rows, but history is too short for a formal check, and a desktop click-logging change coinciding with v3 is not excluded [q6, check:completeness#1] [inferred]
  - Seasonality / day of week: not ruled out; windows are the same weekdays, but there is only one prior week, so a seasonal dip can't be separated [q3] [inferred]
  - Other concurrent change: not ruled out; release_log lists only v3, but other changes may not be logged [q2] [inferred]
  - v3 caused the drop (PM's view): not ruled out; consistent with timing and the desktop-only pattern, but no control group exists. Mobile also got v3 and did not move, so v3 would have to act on desktop only [q4, check:mix_shift#2] [inferred]
- Checks run:
  - completeness: could not run, needs at least 3 earlier periods [check:completeness#1]
  - mix_shift (platform x country): pass, overall -1.83 pp = within-segment -1.82 pp + mix -0.01 pp [check:mix_shift#1]
  - mix_shift (platform): pass, same result at the coarser grain [check:mix_shift#2]
  - fanout: skipped, no joins used
  - srm: skipped, not an experiment

## Caveats, and what would change the answer
- Before/after comparison with no control: any desktop-specific change in the same week would be counted as v3. A desktop holdout on v2 would settle it.
- Intervals assume independent searches; day-level variation and user clustering would widen them.
- Only one baseline week; week-to-week CTR noise is not estimated.
- CTR is clicks/searches as defined here, not a confirmed team metric.

## Provenance
- Metric: CTR = sum(clicks)/sum(searches) over search_daily, all platforms and countries, per week [guess]
- Data: search_daily, release_log, through 2026-09-13
- Reconciled: not done (no dashboard or metrics.json available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (25 numbers on 10 lines; 4 queries, 3 checks, 0 given); ds-verify: pass (0 fail, 0 could not verify, 0 warn, 19 pass)