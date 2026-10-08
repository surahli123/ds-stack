## Answer
Headline: 0.0 percentage points (like-for-like, hours 00–09)
There is no real CTR drop. Yesterday's data stops at hour 9, and the apparent fall is a partial-day artifact. Over the same hours, CTR is 27.0% yesterday and 27.0% in the prior 7 days. (measured)

## What it means for the decision
Don't escalate or investigate a CTR regression on this evidence. The naive comparison, 27.0% against the 29.83% full-day average, is −2.83 pp. It is misleading because it compares a partial day to full days. Yesterday's full-day number can't be known until the remaining hours load.

## Why we believe it
- Alternatives considered:
  - Real CTR decline: ruled out. Hours 0–9 CTR matches the prior 7 days' hours 0–9 at 27.0% (137,200 searches in the prior-days window). [measured]
  - Partial-day / time-of-day mix: ruled in. 2026-10-07 has only 10 of 24 hours (0–9). Early hours run at about 24% CTR and hours 8–9 at 31%, so a truncated day looks lower than a full day. [measured]
  - Duplicate rows or nulls distorting the figures: ruled out. There are no duplicate date/hour rows and no null searches. [measured]
  - Whether the missing hours (10–23) will also match: could not be determined, because the data isn't there. [guess]
- Checks run:
  - Row coverage per day: fail. 2026-10-07 has only hours 0–9, while the other days have 24.
  - Same-hours comparison (hours 0–9, 09-30 to 10-06 vs 10-07): pass. Both are 27.0%, a difference of 0.0 pp.
  - Duplicates, nulls, clicks > searches: pass. None found.
  - Day-to-day stability: pass. Full-day CTR ran 29.83–29.84% on every prior day.

## Caveats, and what would change the answer
- The remaining hours (10–23) for 10/07 are missing. This may be an incomplete pipeline load or an extract cut off mid-day. If they land with a lower CTR, there could still be a real drop later in the day. (inferred)
- Hourly CTR is identical on every day, to the decimal, which is unusually clean. It suggests synthetic or aggregated data, so check the source if exact precision matters. (inferred)
- The like-for-like result uses no sampling, so I have no interval. It is an exact computation on the rows present.
- Reload or confirm the full 10/07 data and re-run the comparison.