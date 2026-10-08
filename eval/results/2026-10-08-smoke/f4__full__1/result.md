## Answer
Headline: 0.0 pp (like-for-like, hours 0–9 only); the apparent −2.8 pp is not a real drop
The apparent drop (27.0% yesterday vs 29.8% over the prior 7 days) comes entirely from yesterday's data being partial. Only hours 0–9 are loaded, and within each hour band CTR is unchanged. [measured]

## What it means for the "search CTR is down" call
Don't report a drop or act on one. Re-check once the full day of 2026-10-07 has loaded. [inferred]

## Why we believe it
- Alternatives considered:
  - Incomplete day, so the mix of hours is skewed: ruled in. 2026-10-07 has 10 of 24 hourly rows (hours 0–9). Its mix is 57% low-traffic hours against 17% normally. Mix effect is −2.83 pp and the within-hour-band effect is 0.00 pp, so 100% of the gap is mix. [measured]
  - A real CTR decline: ruled out for the hours we have. Yesterday's hours 0–9 CTR is 27.0%, and the prior 7 days' hours 0–9 CTR is also 27.0%. The low-traffic hours (24%) and peak hours (31%) are each identical to baseline. [measured]
  - Day-of-week or seasonality: not needed to explain the gap. The prior 7 days are flat at 29.83–29.84% daily. [measured]
  - A logging or definition change: no sign in the loaded hours, since rates match exactly. This can't be checked for hours 10–23, which aren't loaded. [inferred]
- Checks run:
  - completeness: fail. 2026-10-07 has 10 rows, 42% of the trailing median of 24.
  - mix_shift: fail. The −2.83 pp change is +0.00 pp within-segment and −2.83 pp mix (100% mix). I merged hour 23 into the low-traffic segment because it has no rows yesterday.
  - fanout: skipped. No joins were used.
  - srm: skipped. This is not an experiment.

## Caveats, and what would change the answer
- Hours 10–23 of 2026-10-07 are missing, so the full-day CTR is unknown. If the load finishes and those hours show lower CTR, there could still be a real drop.
- The rates in the data are suspiciously constant (every hour in a band is identical). This may be synthetic or smoothed data, so confirm the source.
- Why the load stopped at hour 9 is unexplained. Ask the data owner whether the pipeline is delayed or broken.