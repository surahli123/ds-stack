## Answer
Headline: can't tell yet (like-for-like, the change is 0.0 pp, 95% interval −0.7 to +0.7 pp)
The apparent drop is an artifact. Yesterday's data stops at hour 9, and that window is mostly low-CTR overnight hours. Hour for hour, CTR matches the previous 7 days.

## What it means for the leadership update
A real drop would need to be about 0.7 pp or more for the interval to show it, and the interval includes zero. So there is no evidence of a drop. Leadership shouldn't be told CTR fell 2.8 pp. I'd re-run once yesterday's full 24 hours have loaded.

## Why we believe it
- Alternatives considered:
  - Real CTR decline: ruled out for hours 0–9. CTR is 27.0% yesterday vs 27.0% over the prior 7 days in the same hours, and each hour's CTR matches its usual value (24.0% overnight, 31.0% at hours 8–9). [measured]
  - Partial-day / hour-mix artifact: ruled in. Yesterday has 10 of 24 hours. Raw CTR is 27.0% vs 29.83% for the prior full days (a −2.8 pp gap), because overnight hours (24%) make up 80% of the window's hours but only about 28% of the volume in a full day. [measured]
  - A drop after hour 9: can't be assessed, since there is no data. [inferred]
- Checks run:
  - Row completeness by date: flag. 2026-10-07 has only hours 0–9. All other dates have 24 hours. [measured]
  - Hour-matched comparison (hours 0–9, 2026-09-30 to 2026-10-06, 137,200 searches, vs 19,600 yesterday): pass. Difference 0.00 pp, interval ±0.66 pp (normal approximation for two proportions). [measured]
  - Per-hour CTR on 10-06 vs 10-07: pass. They match. [measured]
  - Compared against a dashboard: could not run. No dashboard was available.

## Caveats, and what would change the answer
- Hours 10–23 of 2026-10-07 are missing. A pipeline delay or a real late-day drop would show up once they load. [inferred]
- The hourly counts are very regular, almost constant within each hour band. The interval treats searches as independent, so it may be too narrow or too wide. [inferred]
- If the full-day data shows CTR below roughly 29.2%, that would be a real drop, and I'd re-run. [inferred]
- "Previous 7 days" is taken as 2026-09-30 to 2026-10-06. [guess]

## Provenance
- Metric: CTR = clicks / searches, summed over the hours compared. This is stated here, with no metrics.json present. [guess]
- Data: search_hourly, through 2026-10-06 complete. 2026-10-07 is partial (hours 0–9).
- Reconciled: not done (no dashboard or metrics.json available)
- Queries and checks: ad hoc inline Python/sqlite3 in this session, not saved to a file.