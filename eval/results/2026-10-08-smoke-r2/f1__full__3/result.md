```
## Answer
Headline: about 0.0 pp attributable to v2 (within-segment change −0.0001 pp; overall CTR fell 2.10 pp, from 30.42% to 28.32%)
Overall CTR fell 2.1 pp week over week, but essentially all of that is a shift in traffic mix from desktop to mobile. CTR within each platform and country segment didn't change.

## What it means for the rollback decision
These data give no CTR reason to roll back v2. The drop is a mix effect, not a ranking-quality effect. The open question is why mobile's share of searches rose from 40% to 55%, and whether it coincides with the rollout.

## Why we believe it
- Alternatives considered:
  - v2 lowered CTR (the PM's theory): ruled out as the driver. CTR in all four platform × country segments is identical across the weeks, to the 4th decimal (e.g. desktop US 37.08% vs 37.08%, mobile other 21.23% vs 21.23%) [measured]
  - Mix shift: ruled in. Mix explains −2.10 pp of the −2.10 pp (99.99%). Mobile's share of searches went from 40% to 55%, and mobile's CTR is about 15 pp lower than desktop's [measured]
  - Day-of-week or seasonality: ruled out. Both periods are full 7-day weeks, and daily search volume is flat (about 97k–103k/day) in both [measured]. Within-segment CTR being unchanged also leaves nothing for seasonality to explain [inferred]
  - Data incompleteness or logging change: ruled out. Every day has all 4 segment rows and total volume is stable [measured]. A subtle definition change can't be excluded from this table alone [guess]
  - Rollout caused the mobile mix shift: not ruled out. The shift began on the same day as the rollout, but 100% rollout means there's no concurrent control, so this is untestable here [inferred]
- Checks run:
  - completeness: pass. 2026-10-04 has 4 of 4 expected rows, and every day in both weeks has 4 rows
  - mix_shift: fail. The check flags a mix share of 100%. That is the finding: the change is mix, not rate. Within-segment change is −0.0001 pp
  - fanout: skipped. No joins were used
  - srm: skipped. This is a before/after comparison, not a randomized experiment

## Caveats, and what would change the answer
- The rollout was 100% at once, so there is no concurrent v1 control. This is a before/after comparison, and I can't exclude v2 causing the shift in platform mix (for example, a mobile app change that shipped the same day).
- If the mobile traffic jump is linked to v2 (a campaign, an app release, or a routing change on 2026-09-28), the answer changes. Check marketing and release logs for that date. The release_log table only lists the ranker rollout.
- Exactly identical within-segment CTRs before and after are unusually clean. Confirm that the v2 data isn't being logged or backfilled in a way that hides a real per-segment difference.
```