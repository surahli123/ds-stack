## Answer
Headline: 0.0 pp (95% interval about −0.7 to +0.7 pp). There is no real drop in CTR.

The apparent drop is an artifact. The data for 2026-10-07 stops after hour 9, so yesterday is a partial day, and the 7-day baseline is a full 24-hour day.

- Observed: −2.83 pp (about −3.5 to −2.2). This is partial-day CTR of 27.00% (5,292 clicks / 19,600 searches, hours 0–9) against the prior 7 full days at 29.83%. [measured]
- Adjusted: 0.00 pp (about −0.7 to +0.7), holding hour of day fixed. The prior 7 days over hours 0–9 have CTR of 27.00%, the same as yesterday. Every hour matches its baseline hourly rate (24% overnight, 31% from hour 8). [measured]
- Causal effect: not identified. Nothing was changed on purpose here, and with no difference to explain there is nothing to attribute.

## What it means for the CTR-drop decision
The like-for-like interval of about ±0.7 pp covers zero, so there is no evidence of a drop to act on. Don't escalate on the −2.8 pp figure. A drop would only show once the full day is loaded and the interval excludes zero.

## Why we believe it
- Alternatives considered:
  - Real CTR decline: ruled out. Hour-by-hour rates are identical to the baseline. [measured]
  - Partial-day / time-of-day mix: ruled in. Yesterday has only hours 0–9. Those include 8 low-CTR overnight hours (24%) and only 2 of the 14 high-CTR daytime hours (31%). [measured]
  - Late-loading data (pipeline lag): ruled in as the likely cause of the missing hours 10–23. [inferred]
  - Traffic-mix or bot change: not testable, because the table has no segment columns. [guess]
- Checks run:
  - Row completeness per day: flag. 2026-10-07 has 10 of 24 hours, and the other days have 24.
  - Like-for-like hours 0–9, yesterday vs prior 7 days: pass. Both are 27.00%.
  - Per-hour CTR comparison: pass. All 10 hours match the baseline exactly.
  - Interval: a binomial normal approximation that treats searches as independent, so it is rough. Real-world day-to-day variation is likely wider than it shows. The data is also suspiciously uniform: many hours have identical counts, which suggests it is synthetic or aggregated.

## Caveats, and what would change the answer
- Hours 10–23 of 10-07 are missing. If they load with CTR clearly below 31%, a real drop would appear.
- The baseline has only 7 days, and I did not check for weekday effects.
- I did not look at segments (device, query type), because the table doesn't have them.

## Provenance
- Metric: CTR = clicks / searches, summed over the period. This is my own definition, because there is no metrics.json. [guess]
- Data: search_hourly, through 2026-10-07 hour 9. The last complete day is 2026-10-06.
- Reconciled: not done (no dashboard or other source available).
- Queries and checks: run inline in Python/sqlite3 against warehouse.db. They were not saved to a file.