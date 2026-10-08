## Answer
Headline: can't tell
Treatment's CTR (clicks per search) was higher by 1.20 percentage points (30.00% → 31.20%, naive 95% interval ±0.07pp). The arms are badly unbalanced for a 50/50 split, so I can't trust that number as the causal effect. [measured]

## What it means for the launch decision
Don't use +1.2pp as the launch number yet. First find out why treatment has about 4.8% fewer users than control. If the cause is benign, the lift is probably real. If it's not, the lift could be partly or wholly an artifact. [inferred]

## Why we believe it
- Alternatives considered:
  - Random noise in the CTR gap: ruled out. The gap is 1.2pp against a standard error of about 0.04pp, and it shows up on every one of the 14 days. [measured]
  - Clean 50/50 randomization: ruled out. Treatment has 48.77% of user-days (475,990 vs 499,930), a sample-ratio-mismatch chi-square of about 587. [measured]
  - Treatment dropping or excluding low-CTR users, which would inflate CTR: not ruled out. It would fit the pattern, but the data here can't confirm or exclude it. [guess]
  - A different amount of searching per user: ruled out. Both arms have exactly 6.0 searches per user. [measured]
- Checks run:
  - CTR lift, pooled over the 14 days: pass. +1.20pp. [measured]
  - Interval: pass, with a limit. ±0.07pp assumes searches are independent. It is too narrow if searches cluster within users, and only daily aggregates are available to check that. [measured]
  - Sample ratio (SRM): fail. See above.
  - Day-by-day consistency: pass. Daily rows are stable and show no novelty or ramp pattern. [measured]
  - User-level analysis: could not run. The table holds only daily aggregates, with no user IDs or assignment logs.

## Caveats, and what would change the answer
- The SRM failure is the main problem. If the assignment or logging team finds a benign cause, such as a logging bug that is independent of user behavior, the +1.2pp stands. If treatment lost or filtered users in a way tied to behavior, the true lift is unknown.
- Daily user counts may include repeat users, so they are not unique users.
- Clicks per user is also higher (1.87 vs 1.80). That is the same lift expressed per user, not an independent confirmation.
- Pulling the assignment-level data would let us check the SRM and give a user-level interval.