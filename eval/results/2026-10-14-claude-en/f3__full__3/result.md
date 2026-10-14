## Answer
Headline: -1.82 pp (95% CI -1.97 to -1.67) [check:mix_shift#1]
Overall CTR fell from 30.44% to 28.61% week over week, and nearly all of it is within-segment change concentrated on desktop; this is an association with the v3 rollout, not a proven v3 effect, and it holds only if nothing else changed on 2026-09-07 [q3, check:mix_shift#1].
- Observed: -1.83 pp (95% CI -1.98 to -1.68) [check:mix_shift#1]
- Adjusted: -1.82 pp (95% CI -1.97 to -1.67), holding platform x country mix fixed [check:mix_shift#1]
- Causal effect: not identified (v3 went to all traffic at once, so there is no concurrent control; a v2-vs-v3 holdout or staggered rollout would identify it)

## What it means for the v3 rollback decision
The whole interval (-1.97 to -1.67 pp) is well beyond the 0.1 pp minimum effect used by the check [check:mix_shift#1], so the drop is real and not noise or mix. Whether v3 caused it is the open part: desktop CTR fell 36.04% to 33.04% (-1.80 pp) while mobile was flat at -0.02 pp, which fits a desktop-specific v3 problem but also any desktop-only change on the same date [check:mix_shift#2].

## Why we believe it
- Alternatives considered:
  - Mix-shift (platform, country): ruled out; mix effect is -0.01 pp, about 1% of the change, at both grains [check:mix_shift#1, check:mix_shift#2] [measured]
  - Seasonality/day of week: ruled out as a cause of the size; both windows are Mon-Sun, 7 days, and daily search volume is similar (about 100k/day) [q3] [inferred]; no earlier history was run, so a seasonal dip is not excluded directly [guess]
  - Data completeness: ruled out; every day in both weeks has 4 segment rows and volumes are in line [q3] [measured]
  - Logging/definition change: not ruled out; release_log lists only the v3 rollout [q2] but tracking changes may not be logged [guess]
  - Requester's cause (v3): ruled in as consistent but not established; the drop starts exactly on the v3 date [q3], and it is desktop only [q4] [inferred]
- Checks run:
  - completeness: could not run: needs 3 earlier same-weekday periods and the table has only 2 weeks of data in the window [check:completeness#1]
  - mix_shift (platform x country): pass; -1.83 pp = within-segment -1.82 + mix -0.01 [check:mix_shift#1]
  - mix_shift (platform): pass; same total, mix -0.01 pp [check:mix_shift#2]
  - fanout: skipped; no joins used
  - srm: skipped; not an experiment

## Caveats, and what would change the answer
- No concurrent control: only a v2 holdout or desktop-specific change log would separate v3 from other changes on 2026-09-07.
- The interval assumes independent searches; repeat users make it somewhat too narrow, but the effect is about 10x the interval half-width.
- Only two weeks are available, so no baseline for normal week-to-week CTR variation.
- Desktop-only drop: check whether v3 behaves differently on desktop (layout, result types), which would be more actionable than a full rollback.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches), search_daily, all platforms and countries, from stated here [guess]
- Data: search_daily, release_log, through 2026-09-13
- Reconciled: not done (no dashboard or metrics.json available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (29 numbers on 11 lines; 3 queries, 3 checks, 0 given)