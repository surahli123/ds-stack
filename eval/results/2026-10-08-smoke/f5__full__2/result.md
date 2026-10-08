## Answer
Headline: can't tell
Treatment's raw CTR is 31.2% against control's 30.0%, a gap of +1.20 percentage points (±0.07 pp, 95% CI, naive). The arms fail the sample-ratio check, so I can't tell whether that gap is the ranker's effect. [measured]

## What it means for the ranker_boost launch decision
Don't use +1.2 pp as the launch number. Find out why treatment has about 4.8% fewer users than control, then re-read the result. [inferred]

## Why we believe it
- Alternatives considered:
  - Real treatment effect: not ruled in. The raw gap is +1.20 pp and consistent every day (+1.1 to +1.3 pp), but the arms aren't comparable while the SRM fails. [measured]
  - Biased assignment or logging, such as treatment users being dropped or filtered: not ruled out. Treatment has 475,990 user-days against control's 499,930 (48.8% vs 51.2%). The gap is exactly constant day to day, which suggests a systematic cause rather than noise. [measured]
  - If the missing treatment users were disproportionately low-clickers, CTR would be inflated: plausible, but I have no user-level data to test it. [guess]
  - Day of week or seasonality: ruled out as the cause of the gap. Both arms share the same dates and show the same weekly wobble, and the lift is steady across days. [measured]
  - Incomplete data: ruled out. All 14 days have both arms' rows. [measured]
  - Segment mix shift: could not test. The table has no platform, country or other segment columns. [inferred]
- Checks run:
  - srm: **fail**. Observed shares were 51.23% control and 48.77% treatment against a planned 50/50 (chi2 587, p≈1e-129). The tool says the arms are not comparable until the cause is found.
  - completeness: pass. 2 rows per day for all 14 days, ending 09-30. My first two runs used the wrong target date and failed; the corrected run passed.
  - mix_shift: skipped. There are no segment dimensions in the data.
  - fanout: skipped. No joins were done.

## Caveats, and what would change the answer
- The data is daily aggregates only: users, searches and clicks per arm. I can't check for dropped users, bots, or a triggering or exposure filter that applies to one arm.
- The CI treats searches as independent. Searches from the same user are correlated, so the true interval is wider. Users are summed across days, so they are user-days.
- If the assignment or logging owner finds and fixes the cause of the mismatch, or shows it is unrelated to click behavior, the +1.2 pp could stand. A rerun or re-cut at the user level would settle it.