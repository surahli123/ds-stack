I've found the cause: the "drop" comes from comparing a partial day with full days. I'm writing it up now.

## Answer
Headline: can't tell. The apparent drop is not real on a like-for-like basis (about 0.0 pp).

Yesterday's CTR looks 2.83 pp lower (27.00% vs 29.83%), but only because the data for 2026-10-07 stops at hour 9. Over the same hours 0–9, yesterday matches the previous 7 days at 27.0%.
- Observed: −2.83 pp (27.00% vs 29.83%; interval not computed, see caveats)
- Adjusted: 0.00 pp (interval not computed), holding hours of day (0–9) fixed. Daily values over those hours ranged from 26.99% to 27.02% across the baseline week.
- Causal effect: not identified (there was no intervention to test, and no drop remains to explain).

## What it means for the decision
Don't act on a CTR drop. The like-for-like change is about 0.00 pp, with daily noise of about ±0.02 pp in the baseline. Any decision threshold above a few hundredths of a point is not triggered. A full-day read for 10-07 is needed before saying anything about the whole day.

## Why we believe it
- Alternatives considered:
  - Partial-day / time-of-day mix artifact: ruled in. 10-07 has only hours 0–9, and hours 0–7 run at about 24% CTR while hours 8–22 run at about 31%. Yesterday's data contains only two of the high-CTR hours, so its daily total sits lower. [measured]
  - A real CTR decline: ruled out for hours 0–9. Hourly CTR yesterday is 24.0% for hours 0–7 and 31.0% for hours 8–9, the same as 10-06 (24.0% and 31.0%). [measured]
  - Traffic volume change: ruled out. Searches per hour are about 1400 off-peak and 4200 at peak, in line with prior days (1428 and 4284 on 10-06). [measured]
  - Duplicate rows: ruled out. No duplicate date-hour pairs. [measured]
  - A drop in hours 10–23 yesterday: can't be ruled in or out because there is no data for those hours. [inferred]
- Checks run:
  - Completeness by day: flag. Days 09-30 through 10-06 have 24 hours each; 10-07 has 10.
  - Same-hours comparison (hours 0–9): pass. 27.00% yesterday vs 27.00% for the prior 7 days pooled.
  - Hour-by-hour profile comparison: pass. It is flat and consistent across days.
  - Confidence interval: could not run. The table has hourly aggregates with no user or session grain, and the hourly values are nearly constant, so a binomial interval would not capture real variation.

## Caveats, and what would change the answer
- The data ends at 2026-10-07 hour 9. The warehouse load is probably incomplete or delayed. Re-check once the day is fully loaded.
- If hours 10–23 show lower CTR than usual, there could still be a real drop later in the day. The current data can't show that.
- I assumed "previous 7 days" means 09-30 to 10-06, which is the full data range.
- The intervals are not computed. The ±0.02 pp is only the observed day-to-day range.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches), pooled over the hours in scope. No metrics.json was present, so this definition is stated here [guess].
- Data: `search_hourly`, through 2026-10-06 (last complete day). 2026-10-07 is partial, covering hours 0–9.
- Reconciled: not done (no dashboard or other source available).
- Queries and checks: ad hoc Python/sqlite3 queries run in this session. They were not saved to a file.