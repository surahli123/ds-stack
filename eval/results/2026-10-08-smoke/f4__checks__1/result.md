## Answer
Headline: can't tell. The like-for-like change is 0.0 pp, and the full-day drop isn't a valid number.

Yesterday's data stops at hour 9 (10 of 24 hours loaded). Over those same hours, CTR was 27.0% yesterday and 27.0% in the prior 6 days, so there is no measurable drop. [measured]

## What it means for the decision
Don't report a drop to leadership. The apparent fall of about 2.8 pp (27.0% vs 29.83%) comes from comparing a partial, overnight-heavy day with full days. Re-check once 2026-10-07 has fully loaded.

## Why we believe it
- Alternatives considered:
  - Real CTR drop: ruled out for hours 0–9 by identical hourly CTR (24% overnight, 31% at hours 8–9, both matching the baseline). [measured]
  - Partial-day/time-of-day mix artifact: ruled in. Hours 0–7 have lower CTR (24%) than daytime (31%), and the loaded hours are mostly those low-CTR hours. [measured]
  - Drop in the unloaded hours 10–23: can't be ruled out, since there is no data for them. [guess]
  - Baseline: I used the prior 6 days (10-01 to 10-06) for the like-for-like comparison. The previous 7 days (09-30 to 10-06) run 29.83–29.84% daily, so the baseline is stable. [measured]
- Checks run:
  - completeness: fail. 2026-10-07 has 10 rows, which is 42% of the trailing median of 24.
  - mix_shift: skipped. The hour-matched comparison already shows no change, so I did not run it.
  - fanout, srm: skipped. There were no joins and no experiment.

## Caveats, and what would change the answer
- Once the remaining hours load, the final full-day number may differ. A real drop would show up in hours 10–23.
- Find out why the load stopped at hour 9: a pipeline delay or an outage. If it is an outage, it could affect the hours that are missing.
- The data has only hourly aggregates, so I can't break it down by segment or platform.