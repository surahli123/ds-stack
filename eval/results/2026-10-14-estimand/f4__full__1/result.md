## Answer
Headline: +0.0 pp (-0.66 to +0.66) on hours 0-9, the only hours logged for 2026-10-07 [q6, check:mix_shift#1]
The apparent -2.8 pp drop is a partial-day artifact: yesterday has only hours 0-9 loaded, and on those same hours CTR is 27.0% yesterday vs 27.0% over the previous 7 days [q3, q6]. Hours 10-23 of 2026-10-07 are missing, so the full-day CTR is unknown.
- Observed: -2.83 pp (-3.47 to -2.20), partial day (10 of 24 hours) vs 7 full days [q5, check:completeness#1]
- Adjusted: +0.0 pp (-0.66 to +0.66), holding hour of day fixed (hours 0-9 only) [check:mix_shift#1]
- Causal effect: not identified (no randomized test or intervention in the data; nothing to attribute)

## What it means for the decision to treat CTR as having dropped
No drop is visible: the like-for-like interval (-0.66 to +0.66 pp) [q6] excludes the -2.8 pp raw figure [q5] and says nothing about hours 10-23. Do not report a drop to leadership; the data cannot support the claim until the rest of the day lands. No threshold was given for what change would matter [guess].

## Why we believe it
- Alternatives considered:
  - Incomplete data for yesterday: ruled in, only 10 of 24 hourly rows are present vs 24 on each of the previous 7 days [q2, check:completeness#1] [measured]
  - Hour-of-day mix shift (low-CTR hours over-represented): ruled out as the cause of any real change, since the same hours match exactly; the raw gap comes from comparing 10 hours against 24 [check:mix_shift#1, q4] [measured]
  - Real CTR decline within hours 0-9: ruled out, within-segment change is +0.00 pp (-0.66 to +0.66) [check:mix_shift#1] [measured]
  - Day of week or seasonality: not ruled out, only 7 trailing days and no same-weekday history; previous days are flat at 29.83% daily [q2] [inferred]
  - Logging or definition change: not tested; the table has no metadata, but the identical hourly rates are consistent with no change in the hours present [q4] [inferred]
  - A real drop later in the day (hours 10-23): cannot be ruled in or out, no data [q2] [measured]
- Checks run:
  - completeness: fail 2026-10-07 has 10 rows, 42% of the 24-row baseline [check:completeness#1]
  - mix_shift: pass hours 0-9 split into two bands, overall change +0.00 pp, mix 0% [check:mix_shift#1]
  - fanout: skipped, no joins
  - srm: skipped, not an experiment

## Caveats, and what would change the answer
- Hours 10-23 of 2026-10-07 are not in the table. Reload or confirm the pipeline finished, then rerun on the full day. A real drop later in the day would change the answer.
- The mix_shift check treats the 7 prior days pooled; its interval assumes independent searches, which is likely too narrow.
- Hours 0-7 and 8-9 were pooled into two bands for the check; the per-hour data (q4) shows the same equal rates in every hour.
- Metric definition is my assumption (no metrics.json); a different CTR definition could change the level.

## Provenance
- Metric: Search CTR = sum(clicks)/sum(searches) over search_hourly, daily grain, expressed in percent [guess]
- Data: search_hourly, through 2026-10-06 (2026-10-07 incomplete, hours 0-9 only)
- Reconciled: not done (no dashboard or metrics.json available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (51 numbers on 12 lines; 5 queries, 2 checks, 0 given)