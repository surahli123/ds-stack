## Answer
Headline: can't tell

Yesterday (2026-10-07) isn't fully loaded, so a full-day CTR can't be computed yet. The apparent drop is an artifact of the partial day. On the 10 hours that are loaded (hours 0–9), CTR was 27.0%, identical to the same hours over the previous 7 days (27.0%), a 0.0 pp difference [measured].

## What it means for deciding whether to act on a CTR drop
The like-for-like gap is about 0 pp. The raw comparison (27.0% vs 29.83%, "−2.8 pp") only reflects that the loaded hours are mostly the low-CTR overnight hours. I don't have a smallest-change threshold for this decision. On current data there is nothing to act on, and the full day should be re-read once it loads.

## Why we believe it
- Alternatives considered:
  - Real CTR drop: ruled out for hours 0–9 by CTR of 27.0% vs 27.0% for the same hours in the prior 7 days [measured]. Hours 10–23 are unobserved, so a later drop is not excluded [inferred].
  - Partial-day / time-of-day mix artifact: ruled in. 2026-10-07 has 10 of 24 hourly rows. Overnight hours 0–7 run at 24% CTR and the daytime hours 8–23 at about 31% (e.g. 2026-10-06: 343/1428 vs 1328/4284) [measured].
  - Sampling noise: not assessed. The hourly rows are near-constant, so a 95% interval would not be meaningful [inferred].
- Checks run:
  - completeness: fail. 10 rows = 42% of the 24-row trailing median [check:completeness#1].
  - mix_shift: skipped. The hour-matched comparison already removes the mix effect.
  - fanout and srm: skipped. There are no joins and no experiment.

## Caveats, and what would change the answer
- The full-day figure needs the remaining hours (10–23) to load. Re-run once the 2026-10-07 data is complete.
- The hour-matched comparison covers only hours 0–9. A drop that began after hour 9 would not show up in it [inferred].
- The prior-7-day baseline (2026-09-30 to 2026-10-06) is stable at 29.83% daily [measured].

## Provenance
- Metric: CTR = sum(clicks) / sum(searches), stated here [guess]. There is no metrics.json.
- Data: `search_hourly`, through 2026-10-06, the last complete day. 2026-10-07 covers hours 0–9 only.
- Reconciled: not done (no dashboard or other source available).
- Queries and checks: the queries were run inline and not logged. The check result is in `.ds-checks.log` (completeness#1).