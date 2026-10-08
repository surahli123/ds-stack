The experiment's user split fails the sample-ratio check, so I can't give a trustworthy lift. The readout follows.

## Answer
Headline: can't tell
Treatment's raw CTR was 31.20% against 30.00% for control, a gap of +1.20 pp (measured). The user split is badly off the planned 50/50, so I can't trust that gap as a causal effect of the ranker.

## What it means for the ranker_boost launch decision
Don't use the +1.2 pp figure in the launch decision yet. Find out why treatment received 4.8% fewer users than control (inferred), then re-read the result.

## Why we believe it
- Alternatives considered:
  - Real lift from the ranker: not ruled in. The raw gap is +1.20 pp (measured), but arms that differ at assignment aren't comparable (inferred).
  - Random noise in the split: ruled out. Treatment has 475,990 users and control has 499,930, so treatment's share is 48.8% against a planned 50%. The p-value is about 1e-129 (measured).
  - Day-specific glitch: ruled out as the sole cause. The shortfall appears every day, at about 34.0k treatment users against 35.7k control (measured).
  - Cause of the mismatch (for example, treatment users being dropped or filtered, or a logging gap): can't be diagnosed. The table only holds daily aggregates by arm, with no user-level or segment data (measured).
  - Direction of bias: unknown. If the missing treatment users were disproportionately low-clickers, the true lift would be smaller than +1.2 pp. If they were something else, it could go either way (guess).
- Checks run:
  - srm: fail. Chi-square is 587 with p about 1e-129 on 499,930 vs 475,990 users.
  - completeness: could not run. It needs at least 3 prior periods in a series. The table has all 14 days (09-17 to 09-30) with 2 arm rows each, so the window looks fully loaded (measured, by inspection).
  - mix_shift: skipped. There are no segment breakdowns to decompose.
  - fanout: skipped. I ran no joins.

## Caveats, and what would change the answer
- The raw +1.2 pp is calculated as clicks/searches. The search counts also differ by arm because of the user gap. It is not a per-user CTR, and I have no interval for it.
- Finding and fixing the cause of the assignment mismatch, then re-reading with user-level data, would change the answer. User-level data would also let us compute a proper interval.
- If the cause turns out to be independent of user behavior, the +1.2 pp could stand. I can't confirm that from this table.