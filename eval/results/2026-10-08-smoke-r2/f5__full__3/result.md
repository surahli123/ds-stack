```
## Answer
Headline: can't tell
The raw CTR is 31.20% for treatment against 30.00% for control, a gap of +1.20 percentage points. The arms failed the sample-ratio check, so I can't treat that gap as the effect of the ranker.

## What it means for the ranker_boost launch decision
Don't launch on the +1.2 pp figure. Assignment or logging has to be explained first, because a split that is off by this much can bias the CTR comparison in either direction.

## Why we believe it
- Alternatives considered:
  - Treatment truly improved CTR: not ruled in. The raw gap is +1.20 pp (899,874 clicks on 2,999,580 searches for control; 891,051 on 2,855,940 for treatment), but the SRM failure means the arms may not be comparable [measured].
  - Random noise in the split: ruled out. Control has 51.2% of users and treatment 48.8%, against a planned 50/50, with p≈1e-129 [measured].
  - Treatment drops or filters some users: plausible but untested. Examples are a crash, a slow ranker, or exclusion of low-engagement users. Any of these would lose users non-randomly and inflate CTR [inferred].
  - Day-of-week or seasonality: ruled out as the source of the gap. Treatment CTR is above control on every one of the 14 days, and the user counts per arm are stable day to day [measured].
  - Incomplete data: ruled out. All 14 days have both arms present [measured].
  - Segment mix shift: could not be tested. The table has no platform, country, or source breakdown [measured].
- Checks run:
  - srm: fail. chi2 587.3, p 9.9e-130, observed shares 0.512 / 0.488.
  - completeness: pass. The final day, 2026-09-30, has 2 rows, which is 100% of the trailing median. I fed the check my own count of rows per day, so it only confirms both arms are present each day.
  - mix_shift: skipped. There are no segment columns.
  - fanout: skipped. I ran no joins.

## Caveats, and what would change the answer
- Only daily aggregates were available, with no user-level data or assignment logs, so I can't find which users are missing from treatment.
- If the engineering team explains the user deficit (for example, a known logging bug that is independent of user behavior) and fixes it, a rerun could give a trustworthy lift. The raw +1.2 pp would then be the starting estimate, with no interval yet.
- Searches per user are identical in both arms (6.0), so the shortfall is in users, not in search volume per user [measured].
```