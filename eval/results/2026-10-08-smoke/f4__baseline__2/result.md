## Answer
Headline: 0.0 percentage points (like-for-like, hours 0–9: 27.0% vs 27.0%)
There is no real drop. Yesterday's data stops at hour 9, and the apparent fall (27.0% vs 29.83%, about −2.8 pp) comes from comparing a partial day with full days.

## What it means for the decision
Don't report a CTR decline. Hold any reaction until yesterday's data is complete and the number can be re-checked.

## Why we believe it
- Alternatives considered:
  - Real CTR decline: ruled out. Each hour of yesterday's CTR matches the same hour in the prior 7 days (24% for hours 0–7, 31% for hours 8–9). [measured]
  - Partial-day mix effect: ruled in. Yesterday has only hours 0–9. The excluded hours 10–22 are all at the high 31% rate, so the partial day's blended CTR is lower. [measured]
  - Tracking or logging change: not seen. Every hour in the prior 7 days has a rate identical across days and no nulls, and clicks never exceed searches. I can't rule out a pipeline issue behind the missing hours 10–23. [inferred]
- Checks run:
  - Row and hour coverage per date: fail. 2026-10-07 has 10 of 24 hours; the prior 7 days have all 24.
  - Hour-matched comparison (hours 0–9, 09-30 to 10-06): pass. 27.0% vs 27.0%, a difference of 0.0 pp.
  - Full-day prior-7-day CTR: 29.83%. It is stable at 29.83–29.84% on every day. [measured]
  - Nulls and clicks > searches: pass. None.

## Caveats, and what would change the answer
- Hours 10–23 of 10-07 are missing, probably an incomplete load. Once they arrive, recheck. The expected full-day CTR is about 29.8% if the hourly pattern holds.
- This is hourly aggregate data only. I can't break it down by segment, platform or query type.
- Hours 8–9 had 4,200 searches each yesterday, versus the 1,400 in earlier hours. The baseline's hour-level search volumes weren't compared, so the hour-matched 27.0% rests on the CTR-by-hour pattern being stable. [inferred]