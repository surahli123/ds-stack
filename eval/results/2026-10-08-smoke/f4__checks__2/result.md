## Answer
Headline: can't tell. The like-for-like change so far is 0.0 pp, and the day is incomplete.
Yesterday's data covers only hours 0–9 of 24. The apparent drop (27.0% vs 29.83%, about −2.8 pp) comes from comparing a partial day with full days. [measured]

## What it means for the decision
Don't report a CTR drop to leadership. Re-check once the rest of 2026-10-07 has loaded. Hours 10–23 are the ones that could still change the answer.

## Why we believe it
- Alternatives considered:
  - Real CTR decline: ruled out for hours 0–9. Over those hours, 2026-10-07 CTR is 27.0%, and the prior 7 days' CTR for the same hours is also 27.0%. Each hour matches its own baseline (24% for hours 0–7, 31% for hours 8–9). [measured]
  - Partial-day artifact (hours 0–9 only vs full days): ruled in. Overnight hours have low CTR (24%) and carry a smaller share of the day's searches, so a day made up mostly of those hours shows a lower CTR. [measured]
  - A drop in hours 10–23: not ruled out, because there is no data for them. [measured]
- Checks run:
  - completeness: fail. 2026-10-07 has 10 of 24 hourly rows, 42% of the trailing median.
  - fanout, srm: skipped. No joins or experiment in this analysis.
  - mix_shift: skipped. The hour-matched comparison already shows no change, so I didn't run it.

## Caveats, and what would change the answer
- The load of 2026-10-07 may be delayed or failed. Once all 24 hours are present, redo the comparison against the 7-day full-day baseline of about 29.83%.
- The same-hour baseline uses 2026-09-30 to 2026-10-06. [measured]
- A drop confined to the afternoon or evening would only appear after those hours load.