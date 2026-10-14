## Answer
Headline: +0.0 pp (-0.66 to +0.66) [check:mix_shift#1]
The apparent 2.8 pp drop is an artifact: 2026-10-07 has only hours 0-9 loaded, and compared hour for hour against the previous 7 days CTR is unchanged [q2, q4, check:completeness#1, check:mix_shift#1].
- Observed: -2.83 pp (-3.47 to -2.20), partial-day 10-07 CTR 27.0% vs 29.83% for the 7 days 09-30 to 10-06 [q6]
- Adjusted: +0.0 pp (-0.66 to +0.66), holding hour of day fixed (hours 0-9 only) [check:mix_shift#1]
- Causal effect: not identified (no experiment or change under test; nothing to attribute)

## What it means for the decision to treat CTR as having dropped
The like-for-like interval of -0.66 to +0.66 pp [check:mix_shift#1] does not show a drop; it cannot exclude a change as large as 0.66 pp, though, and hours 10-23 of yesterday are not in the data, so nothing can be said about them. No alarm is warranted from this data; re-check once the day lands.

## Why we believe it
- Alternatives considered:
  - Data completeness (partial day): ruled in. 10-07 has 10 of 24 hours, 42% of the usual rows [check:completeness#1] [measured]
  - Hour-of-day mix: ruled in. Hours 0-9 are lower-CTR hours (about 24% overnight vs 31% at hours 8-9 [check:mix_shift#1]) and are compared against full-day 29.83% [q2, q5] [measured]
  - Real within-hour CTR decline: ruled out. Every hour 0-9 has identical CTR yesterday and in the prior 7 days (27.0% both) [q3, q4] [measured]
  - Day of week or seasonality: ruled out for the like-for-like comparison, which uses the same hours; not separately tested because the previous 7 days vary by under 0.01 pp [q2] [inferred]
  - Logging or definition change: no evidence; hourly rates are identical to the baseline [q4] [inferred]
- Checks run:
  - completeness: fail 2026-10-07 has 10 rows = 42% of the median 24 [check:completeness#1]
  - mix_shift: pass overall change +0.00 pp = within-segment +0.00 pp + mix +0.00 pp, run on two hour bands (0-7, 8-9) [check:mix_shift#1]
  - fanout: skipped, no joins used

## Caveats, and what would change the answer
- Only hours 0-9 of 10-07 exist; if the data is really complete (the day is simply short), the full-day view would be the -2.83 pp raw number. Confirm with the pipeline owner that ingestion for hours 10-23 is just late.
- The hour-band grain was two bands for the check; the hourly cells are identical, so a finer grain agrees [q4].
- The interval assumes independent searches; it ignores user-level clustering and is likely a bit narrow.
- The comparison window is 7 days of hours 0-9 only; reload yesterday's full day and rerun to settle it.

## Provenance
- Metric: CTR = sum(clicks)/sum(searches), search_hourly, daily grain, no filters, from stated here [guess] (no metrics.json available)
- Data: search_hourly, through 2026-10-06 (last complete day; 2026-10-07 partial)
- Reconciled: not done (no dashboard or other source available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (57 numbers on 11 lines; 5 queries, 2 checks, 0 given)