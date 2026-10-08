## Answer
Headline: 0.0 percentage points (like-for-like, hours 0–9). The apparent drop of about −2.8 pp is not a real drop.
Yesterday (2026-10-07) has only hours 0–9 loaded. Its CTR of 27.0% is being compared with 29.83% for the previous 7 full days, but on those same hours the previous 7 days also ran 27.0%. [measured]

## What it means for the decision
Don't report a CTR decline: there's no evidence of one so far. Re-check once the full day of 2026-10-07 has loaded, and treat any earlier "CTR is down" read as a partial-day artifact.

## Why we believe it
- Alternatives considered:
  - Partial day with a different hour-of-day mix: ruled in. Yesterday has only hours 0–9, which are the low-CTR hours (about 24% overnight and 31% at hours 8–9, versus about 30% for the full day). The like-for-like rate is 27.0% against 27.0%. [measured]
  - Real within-hour CTR change: ruled out. Every loaded hour of yesterday matches the 7-day average for the same hour (24.0% for hours 0–7, 31.0% for hours 8–9). [measured]
  - Data completeness or a late pipeline load: ruled in as the cause. Yesterday has 10 of 24 hours, 42% of the usual row count. Hours 10–23 are missing. [measured]
  - Day-of-week or seasonality: ruled out as a driver. The 7 full days all sit at 29.83% ±0.01 pp, with no weekday pattern. [measured]
  - Logging or definition change: ruled out for the loaded hours, because their per-hour rates are identical to the baseline. Hours 10–23 can't be checked because they aren't loaded. [inferred]
- Checks run:
  - completeness: fail. 2026-10-07 has 10 rows, 42% of the trailing median of 24. I first ran it without yesterday's row count and it reported "no rows loaded". The rerun with the correct count gave the 42% result. The failure is why the headline is the like-for-like figure and not −2.8 pp.
  - mix_shift: pass. Over hours 0–9 the change is +0.00 pp, with 0% from mix and 0% within-segment. This is a matched-hours comparison, so it shows no change on those hours. The raw gap came from comparing partial-day hours to full-day hours. [measured]
  - fanout: skipped. No joins were used.
  - srm: skipped. This isn't an experiment.

## Caveats, and what would change the answer
- Hours 10–23 of 2026-10-07 aren't in the warehouse, so a drop later in the day can't be ruled out. A full-day load could change the answer.
- No interval is given. The matched hours are identical to the baseline, so there is no measured difference to put an interval around.
- The −2.8 pp figure (27.0% against 29.83%) is arithmetically correct but compares unlike hours. Don't quote it.
- Hours 8–9 on 2026-10-07 have 4,200 searches each, three times the 1,400 of hours 0–7. The baseline shows the same step, so it looks like normal daily traffic, but I didn't check it further.