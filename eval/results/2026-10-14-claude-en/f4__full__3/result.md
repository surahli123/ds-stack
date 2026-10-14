## Answer
Headline: 0.00 pp (-0.66 to +0.66 pp) [check:mix_shift#1]
There is no real drop. 2026-10-07 has only hours 0-9 loaded, so its CTR of 27.0% is a morning-only figure that can't be compared with the full-day 29.8%. Like-for-like hours show no change. [q1, check:completeness#2]
- Observed: -2.83 pp (-3.46 to -2.20 pp), 27.0% for the partial day vs 29.83% for the prior 7 full days. This gap comes from the partial day. [q1, q4]
- Adjusted: 0.00 pp (-0.66 to +0.66 pp), holding hour of day fixed (hours 0-9 only, vs the same hours in the prior 7 days) [check:mix_shift#1]
- Causal effect: not identified (no experiment or intervention; and no change was observed to explain)

## What it means for reporting the CTR drop to leadership
Don't report a drop. The like-for-like change is 0.00 pp, and the ±0.66 pp interval doesn't reach the observed -2.83 pp. A real drop smaller than about 0.66 pp can't be ruled out until the full day lands. [check:mix_shift#1, q1]

## Why we believe it
- Alternatives considered:
  - Partial-day / data completeness: ruled in. The day has 10 of 24 hourly rows (42% of the usual). [check:completeness#2] [measured]
  - Mix-shift across hours: ruled in as the entire gap. Hours 0-7 run at 24% and hours 8-9 at 31%. The missing afternoon and evening hours also run at 31%, so a morning-only day looks lower. [q2, q3] [measured]
  - Within-hour CTR decline (a real change): ruled out. Every hour from 0 to 9 has the same CTR yesterday as in the prior 7 days, within a ±0.66 pp noise floor. [q3, check:mix_shift#1] [measured]
  - Day of week/seasonality: not separately tested. The 7 prior days are flat at 29.83-29.84%. [q1] [inferred]
  - Logging/definition change: none seen, since hourly CTR is identical hour by hour. [q3] [inferred]
- Checks run:
  - completeness: fail. 2026-10-07 has 10 rows vs a median of 24. [check:completeness#2]
  - mix_shift: pass. Within-hour change is +0.00 pp and mix effect is +0.00 pp when restricted to hours 0-9. [check:mix_shift#1]
  - fanout: skipped, no joins.
  - srm: skipped, not an experiment.

## Caveats, and what would change the answer
- Yesterday's figure covers only hours 0-9, so the afternoon and evening hours could still differ. Re-run once the 2026-10-07 load finishes, or find out why hours 10-23 are missing.
- The interval treats searches as independent units, so it is likely somewhat too narrow.
- The hour-of-day baseline is only 7 days, with no same-weekday history.
- The Observed interval is my own two-proportion calculation from the q1 and q4 counts, not a logged check.

## Provenance
- Metric: search CTR = sum(clicks)/sum(searches), from search_hourly [guess]; no metrics.json available
- Data: search_hourly, through 2026-10-06 (2026-10-07 incomplete: hours 0-9 only)
- Reconciled: not done (no dashboard or other source available)
- Queries and checks: .ds-queries.log, .ds-checks.log
- Verified: verify_readout: pass (45 numbers on 11 lines; 4 queries, 2 checks, 0 given)