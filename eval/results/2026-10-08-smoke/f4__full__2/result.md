## Answer
Headline: 0.0 pp (like-for-like, hours 0–9 only)
The apparent drop is an artifact. Yesterday has only hours 0–9 loaded, and its 27.0% CTR is identical to 27.0% for the same hours over the previous 7 days. The full-day CTR was about 29.8% on each of those days.

## What it means for the decision
There is no evidence of a CTR decline, so don't act on the 27.0% vs 29.8% gap (about −2.8 pp). Re-read yesterday once its data has fully loaded before telling leadership anything has moved.

## Why we believe it
- Alternatives considered:
  - Real CTR decline: ruled out. Hours 0–9 on 10-07 have CTR 27.0% (5,292 clicks / 19,600 searches), and the same hours over 09-30 to 10-06 also have 27.0% (37,044 / 137,200). [measured]
  - Partial-day data: ruled in as the cause. 10-07 has 10 of 24 hourly rows, and the other days have 24. The missing hours are the high-traffic daytime ones. [measured]
  - Mix shift across hours: ruled out. The hour-of-day mix is the same (57% night hours 0–7 and 43% hours 8–9). Within-segment CTR is 24% and 31% in both periods, so mix and rate effects are both 0.0 pp. [measured]
  - Day-of-week or seasonality: ruled out as the driver. The prior 7 days all sit between 29.83% and 29.84%, and the like-for-like gap is zero. [measured]
  - Logging or definition change: no sign of one. Hourly CTR per segment is unchanged, but I can't see upstream pipelines. [inferred]
- Checks run:
  - completeness: fail. 10-07 has 10 rows, 42% of the trailing median of 24. This is why the headline uses the matched hours instead of the full day.
  - mix_shift: pass. It reports +0.00 pp overall, with mix share 0%. My first run used mistyped inputs, and I discarded it and reran with the actual query values.
  - fanout: skipped. No joins were used.
  - srm: skipped. This isn't an experiment.

## Caveats, and what would change the answer
- Hours 10–23 of yesterday aren't in the table, so I can't speak to the full day. If those hours load and show lower CTR, there is a real drop, and I would size it from the full 24 hours.
- The data is suspiciously regular: identical values per hour and near-constant daily CTR. It may be synthetic or aggregated, and a pipeline problem is possible. Confirm with the data owner that the 10-07 load is just delayed.
- This covers only the 10 loaded hours, and other segments (platform, country) don't exist in this table.