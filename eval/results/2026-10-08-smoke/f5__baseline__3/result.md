## Answer
Headline: can't tell

The raw data shows treatment CTR (clicks per search) at 31.20% against 30.00% for control, a gap of +1.20 pp. But the arms are not a clean 50/50 split, so I wouldn't trust that number for the launch decision.

## What it means for the launch decision
Don't launch on the +1.2 pp figure yet. Treatment has about 5% fewer users than control, so the arms may not be comparable, and the cause needs to be found first.

## Why we believe it
- Alternatives considered:
  - Real ranker effect: not ruled out. The gap is large next to its naive noise (±0.08 pp at 95%, treating searches as independent) and appears every day [measured]. The SRM below stops me from attributing it to the ranker.
  - Chance: ruled out for the CTR gap, since it is about 15 times the naive interval [measured]. Ruled out as the explanation for the user imbalance, since that is about 48 standard deviations from 50/50 [measured].
  - Biased assignment or logging that drops treatment users (for example, bot filtering or crashes in the new ranker): not ruled out. It would fit the user shortfall, and I have no assignment logs to test it [guess].
  - Different search volume per user: ruled out. Both arms average 6.0 searches per user [measured].
- Checks run:
  - Sample ratio (users, 50/50 expected): fail. Control has 499,930 users and treatment 475,990, which is a 51.2% / 48.8% split.
  - Daily consistency: pass. Treatment CTR is above control on all 14 days (about 31.2% vs 30.0%) [measured].
  - Date coverage: pass. Both arms cover 2026-09-17 to 2026-09-30 with no gaps [measured].
  - User-level variance or clustered interval: could not run. The table has only daily aggregates per arm.
  - Segment or novelty checks: could not run for the same reason.

## Caveats, and what would change the answer
- If the user shortfall is explained as harmless (for example, a known logging gap unrelated to behavior), the +1.2 pp (31.2% vs 30.0%) would become credible. The true interval would still be wider than ±0.08 pp, because clicks cluster within users.
- The CTR here is clicks divided by searches. If the launch metric is per-user CTR or clicked-search rate, the number could differ.
- The daily `users` counts look nearly constant, so they may not be unique users across days. That makes the user-level checks even weaker.
- Needed to settle it: user-level assignment and exposure logs, and the cause of the 24k-user gap.