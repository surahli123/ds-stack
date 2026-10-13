## Answer
Headline: can't tell (for the full day). The 2026-10-07 data stops at hour 9, and the hours it does cover show 0.0 pp change.

The apparent drop is an artifact: the 10-07 row set is a partial day (hours 0–9). Its CTR is 27.0% against 29.83% for the full prior days, a gap of about −2.8 pp. Over the same hours 0–9 the prior 6 days (09-30 to 10-06) average 27.0% too, so the like-for-like change is 0.0 pp. [measured]

## What it means for the "CTR is down" decision
There's no evidence of a real drop. Hours 0–9 show 0.0 pp against a baseline of the same hours, so a change worth acting on would have to show up in hours 10–23, which we don't have. [measured] Don't report −2.8 pp to leadership.

## Why we believe it
- Alternatives considered:
  - Real CTR drop: ruled out for hours 0–9 by identical hourly CTR in yesterday's data and the prior days (24.0% in hours 0–7, 31.0% in hours 8–9) [measured]. Hours 10–23 are untested.
  - Partial-day / time-of-day mix artifact: ruled in. Overnight hours run about 24% and daytime hours about 31%. A day that stops at hour 9 has mostly overnight traffic, so its CTR is lower [measured].
  - Pipeline lag (late-arriving data): ruled in as the likely cause of the missing hours, but I can't confirm it. [inferred]
- Checks run:
  - Row counts per day: flag. 10-07 has 10 hourly rows and every other day has 24.
  - Hour-matched comparison (hours 0–9): pass. 27.0% vs 27.0%, with 137,200 baseline searches.
  - Nulls and clicks > searches: pass. None found.
  - Interval: could not run. Each hour has exactly the same counts every day, so there is no day-to-day variance to build a 95% interval from.

## Caveats, and what would change the answer
- The 10-07 data is incomplete, and I'm not sure why. If hours 10–23 land later, rerun the comparison on the full day.
- The prior-day baseline is suspiciously uniform: every hour has identical counts each day. That could mean synthetic or aggregated data, so check upstream.
- Today is 10-13, so six days have passed and the data still ends at 10-07 hour 9. This suggests the pipeline is stalled, not just slow.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches), stated here [guess]. No metrics.json was present.
- Data: `search_hourly`, through 2026-10-06 (last complete day). 2026-10-07 is complete only through hour 9.
- Reconciled: not done (no dashboard or other source available).
- Queries and checks: ad-hoc Python/sqlite3 queries run inline in this session. They are not saved to a file.