## Answer
Headline: can't tell
The raw data show treatment CTR at 31.20% against 30.00% for control, a +1.20 pp gap. The arms fail the sample-ratio check, so I can't treat that gap as the effect of the ranker.

## What it means for the launch decision
Don't use the +1.2 pp in the launch decision yet. Treatment has about 4.8% fewer users than a 50/50 split should give, and until we know why, the gap could come from who ended up in each arm rather than from the ranker.

## Why we believe it
- Alternatives considered:
  - Real ranker effect (the requester's hypothesis): not ruled in. The raw gap is +1.20 pp, from 899,874 clicks on 2,999,580 searches in control and 891,051 on 2,855,940 in treatment. The gap is steady every day, between +1.1 and +1.3 pp. [measured]
  - Assignment or logging problem that dropped or filtered treatment users: ruled in as the likely cause. Users split 499,930 control to 475,990 treatment (51.2% / 48.8%) against a planned 50/50, and the SRM check gives p≈1e-130. [measured]
  - If the missing treatment users were disproportionately low-clicking (for example, bots filtered out or slow-loading sessions that never logged), CTR would rise with no real improvement. I can't test this with the data here. [guess]
  - Day-of-week or seasonality: ruled out as a driver of the gap. Both arms ran the same days and the gap holds every day. [measured]
  - Incomplete final days: ruled out. All 14 days have both arms, and the last day has 100% of the trailing median row count. [measured]
  - Segment mix shift: could not be tested. The table has no platform, country or other segment columns. [measured]
- Checks run:
  - srm: fail. chi2 587, p≈1e-130, with observed shares 51.2% / 48.8% against 50/50.
  - completeness: pass. 2 rows (one per arm) on 2026-09-30, 100% of the trailing median.
  - mix_shift: could not run. The table has no segment dimension.
  - fanout: skipped. I ran no joins.

## Caveats, and what would change the answer
- The data are daily aggregates by arm only, with no user-level rows or segments. Searches per user are exactly 6.0 in both arms, so I can't see where the user shortfall comes from.
- To settle it, find why treatment is short on users. Check the assignment and exposure logging, and whether the treatment path drops or filters users, for example through crashes, bot filtering or a redirect.
- Once the cause is fixed, or the dropped users are recovered, re-read the lift. If the shortfall is shown to be unrelated to click behavior, the +1.2 pp would stand.
- No confidence interval is given because the SRM failure makes any interval misleading.