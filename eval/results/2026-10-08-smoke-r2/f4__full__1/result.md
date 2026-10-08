## Answer
Headline: can't tell (the apparent −2.8 pp is not a real drop; like-for-like it is 0.0 pp)

Yesterday's CTR reads 27.0% against 29.8% for the prior 7 days (−2.8 pp). That gap comes from incomplete data: 2026-10-07 only has hours 0–9, and the low-CTR overnight hours are overrepresented. [measured]

## What it means for the "is search CTR down?" decision
Don't report a drop. Matched on hours 0–9, yesterday's CTR is 27.0%, the same as the prior 7 days' 27.0%, so nothing has moved so far. The full-day number can't be known until the remaining hours load. [measured]

## Why we believe it
- Alternatives considered:
  - Real CTR decline: ruled out for hours 0–9 by the hour-matched comparison, 27.0% vs 27.0% (5,292/19,600 vs 37,044/137,200). [measured]
  - Mix shift across hours: this is what produces the gap. Hours 0–7 run at 24% CTR and hours 8–23 at 31%. A day with only hours 0–9 has a lower blended CTR by construction. [measured]
  - Data completeness: ruled in. 10 of 24 hourly rows are loaded (42% of normal). [measured]
  - Seasonality or day of week: the prior 7 days are flat at 29.83–29.84%, and each hour's CTR matches across days, so there is no day-of-week effect. [measured]
  - Logging or definition change: no sign of one. Hourly CTRs on 10-07 match the earlier days exactly (24% in hours 0–7, 31% in hours 8–9). [measured]
  - Hours 10–23 of 10-07 might still show a drop: can't be excluded, because that data isn't loaded. [inferred]
- Checks run:
  - completeness: fail. 10-07 has 10 rows, 42% of the trailing median of 24. My first call omitted the 10-07 row, so I reran it with the row included.
  - mix_shift: pass. Hour-matched, the change is +0.00 pp (within-segment 0.00, mix 0.00).
  - fanout: skipped, no joins. srm: skipped, not an experiment.

## Caveats, and what would change the answer
- Rerun once 10-07 has all 24 hours loaded (the load is probably delayed or still running). The full-day answer will come from that.
- If hours 10–23 come in near their usual 31% CTR, the day lands at about 29.8%, flat against the baseline. [inferred]
- I only checked CTR at the hour level. There is no platform, country, or source breakdown in this table.