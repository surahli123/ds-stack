## Answer
Headline: can't tell. Yesterday's data stops at hour 09, so the full-day figure doesn't exist yet.

The apparent drop is a partial-day artifact: on a like-for-like basis (hours 00–09) CTR is flat, 0.0 pp against the previous 7 days.
- Observed: -2.83 pp (about -3.5 to -2.2), 27.00% on partial-day 2026-10-07 vs 29.83% for the full-day average of 09-30 to 10-06. [measured] That comparison is not like-for-like.
- Adjusted: 0.00 pp (about -0.65 to +0.65), holding hours of day 00–09 fixed. [measured] Both periods come to 27.00%. The interval is a binomial approximation. [inferred]
- Causal effect: not identified (nothing was intervened on, and there's no evidence of a change to explain).

## What it means for the decision
There's no evidence of a CTR decline, so don't report a drop. Any real change would need to be larger than about 0.65 pp to show up in this partial data. Re-check once yesterday's full-day data has landed.

## Why we believe it
- Alternatives considered:
  - Real CTR decline: ruled out for hours 00–09, where the rate matches the prior 7 days at 27.0%. [measured] Hours 10–23 of yesterday are untested. [measured]
  - Partial-day / time-of-day mix: ruled in. Yesterday only has hours 0–9, and the overnight hours 0–7 run at 24% CTR against about 31% in the daytime hours 8+. [measured]
  - Data pipeline lag or incomplete load: ruled in as likely, since the data stops at hour 09. [inferred] I haven't confirmed the reason.
- Checks run:
  - Row counts per date: flag. 10-07 has 10 of 24 hours, and the other days have 24.
  - Hour-matched comparison: pass. 27.00% vs 27.00%, and every hour's searches and clicks equal the prior-day pattern.
  - Nulls and clicks > searches: pass. None found.

## Caveats, and what would change the answer
- Hours 10–23 of 10-07 are missing, so a real drop in the afternoon or evening can't be ruled out.
- Hourly values are identical across hours 0–7 and across hours 8–11 on every day. That looks synthetic or smoothed, so I'd check how the table is built. [guess]
- The interval treats searches as independent, which understates the uncertainty.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches), stated here [guess]. There is no metrics.json.
- Data: search_hourly, through 2026-10-06 (complete) plus 2026-10-07 hours 00–09 (partial).
- Reconciled: not done (no dashboard or other source available).
- Queries and checks: run inline in Python with sqlite3. They aren't saved to a file.