## Answer
Headline: can't tell
The naive treatment-minus-control CTR difference is +1.2 percentage points (30.00% → 31.20%). The arms don't have the 50/50 split they should, so I can't trust that number as the effect of the ranker.

## What it means for the launch decision
Don't use the +1.2 pp in the launch decision yet. Find out why treatment is missing about 24k users, then re-read the result on a clean assignment. The naive figure is positive and steady across days, but a broken split can produce or hide a lift like this.

## Why we believe it
- Alternatives considered:
  - Real lift of about +1.2 pp: ruled out as a trustworthy estimate by the sample-ratio mismatch (SRM). Control has 499,930 user-days and treatment has 475,990, a 51.2/48.8 split. That is about 24 standard errors from 50/50. [measured]
  - Random noise: ruled out. Daily CTR is consistently higher in treatment (about 31.2% vs 30.0%) on every one of the 14 days, and the plain binomial 95% interval is about ±0.1 pp. [measured]
  - Treatment dropping users who would have clicked less: possible and consistent with the SRM, but I can't confirm it with this table. [guess]
  - Novelty effect or time trend: ruled out. The gap is flat across the 14 days. [measured]
- Checks run:
  - Sample-ratio check on users: fail. Treatment is short by about 24k user-days, with a stable shortfall every day.
  - Searches per user in each arm: pass. Both arms are at 6.0, so exposure per user looks the same.
  - Daily consistency of CTR: pass. The direction is the same every day.
  - Per-user or clustered variance: could not run. The table only has daily aggregates, so the interval above treats searches as independent, which understates the true uncertainty.
  - Cause of the SRM (logging loss, bot filtering, or assignment bug): could not run. The data to check it isn't in the warehouse.

## Caveats, and what would change the answer
- The `users` column is a daily count, so the user totals above are user-days, not unique users.
- If the SRM is traced to something unrelated to behaviour, such as random logging loss, the +1.2 pp would be much more credible.
- If treatment is losing or filtering users in a way that depends on engagement, the true lift could be smaller, zero, or negative.
- Per-user data and the assignment logs would let me check the SRM cause and compute a correct interval.