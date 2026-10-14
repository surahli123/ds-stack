## Answer
Headline: -0.00 pp (-0.15 to +0.15) [check:mix_shift#1]
Overall CTR fell about 2.1 pp, but essentially all of it is a shift in traffic toward lower-CTR mobile; within each platform/country segment CTR did not move, so the drop is not attributable to v2's ranking, assuming v2 did not itself cause the traffic mix change. [check:mix_shift#1]
- Observed: -2.10 pp (-2.25 to -1.95) [check:mix_shift#1]
- Adjusted: -0.00 pp (-0.15 to +0.15), holding platform x country mix fixed [check:mix_shift#1]
- Causal effect: not identified (v2 went to all traffic with no holdout; a randomized split between the old and new ranker would identify it)

## What it means for the rollback decision
The within-segment interval of -0.15 to +0.15 pp is tiny next to the -2.10 pp headline drop, so the observed drop is not evidence against v2 and does not by itself justify rollback; no rollback threshold was given, and the interval only rules out within-segment harm larger than about 0.15 pp. [check:mix_shift#1] The mobile share of searches rose from 40% to 55% and that, not ranking quality, accounts for the drop. [check:mix_shift#2]

## Why we believe it
- Alternatives considered:
  - Mix-shift (more mobile traffic): ruled in, mix effect -2.09 pp of the -2.10 pp total, and a coarser platform-only grain agrees [check:mix_shift#1, check:mix_shift#2] [measured]
  - v2 lowered CTR (requester's cause): ruled out as a within-segment effect, since every segment's CTR is flat across the cutover [check:mix_shift#1] [measured]
  - v2 caused the mobile traffic shift (e.g. by changing what gets searched): not ruled out; the shift coincided with the rollout and the data cannot separate them [q4] [inferred]
  - Data completeness: ruled out, last day has full rows vs trailing median [check:completeness#1] [measured]
  - Seasonality / day of week: ruled out as the driver, both windows are full Mon-Sun weeks and the daily CTR steps down at 09-28 [q3] [inferred]
  - Logging or definition change: only one release-log entry, the v2 rollout [q2] [inferred]
- Checks run:
  - completeness: pass 2026-10-04 has full row count [check:completeness#1]
  - mix_shift (platform x country): flag mix share ~100% of the change [check:mix_shift#1]
  - mix_shift (platform only): flag same result at coarser grain [check:mix_shift#2]
  - fanout: skipped, no joins used
  - srm: skipped, not a randomized experiment

## Caveats, and what would change the answer
- No holdout: v2 may have caused the mobile mix change (e.g. different result quality changing who searches); a platform-level traffic log from before the rollout or an A/B holdout would settle it.
- Intervals assume independent searches; clustering by user would widen them.
- Only one week on each side; rollback threshold not specified.
- Metric definition is my assumption, not from a metrics file.

## Provenance
- Metric: CTR = sum(clicks)/sum(searches) from search_daily, all platforms and countries [guess]
- Data: search_daily, release_log, through 2026-10-04
- Reconciled: not done (no dashboard or metrics.json available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (21 numbers on 8 lines; 3 queries, 3 checks, 0 given)