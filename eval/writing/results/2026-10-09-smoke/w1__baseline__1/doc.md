# Ranker v2: CTR drop readout

**For:** Dana | **Decision due:** Thursday | **Question:** roll back v2?

## Recommendation

**Don't roll back v2 on this evidence.** The CTR drop is explained by a shift in traffic toward mobile, not by a change in how either platform performs. Two follow-ups would firm this up (below).

## What happened

Overall CTR fell from 30.4% (week before v2 reached 100% on Sep 28) to 28.3% (week after), down 2.1 pp.

| | Week 1 | Week 2 |
|---|---|---|
| Desktop CTR | 36.0% | 36.0% |
| Mobile CTR | 22.0% | 22.0% |
| Mobile share of searches | 40% | 55% |
| **Overall CTR** | **30.4%** | **28.3%** |

Within each platform, CTR did not move. Mobile simply converts to clicks at a lower rate than desktop, and it became a much larger part of traffic. Splitting the change into a within-platform part and a traffic-mix part gives:

- Within-platform effect: -0.0001 pp
- Mix effect: -2.10 pp

That is essentially 100% mix. If v2 had hurt ranking quality, we would expect CTR to fall inside at least one platform, and it didn't.

## What I ruled out

- **Missing data:** all 14 days present, 4 rows per day (platform x country), row counts flat.
- **Country:** US fell 31.3% to 29.2% and other fell 29.3% to 27.3%. Both dropped about 2 pp, so country doesn't explain it.

## Open items

1. **Why did mobile jump from 40% to 55%?** Growth thinks there may have been an app store feature that week. This is **not confirmed**. Growth needs to confirm. It doesn't change the v2 conclusion, but it tells us whether the shift is temporary.
2. **Can we be certain about v2 itself?** Not from this data (see limits). If you want certainty, run a **5% holdout for two weeks**.

## Limits of this analysis

- **Before/after only.** v2 went to everyone at once and there is no holdout, so it can't separate v2 from anything else that changed that week.
- **Small effects are invisible.** A v2 effect under about 0.3 pp would not show up here.
- **CTR only.** I did not properly check long clicks or reformulation rate. A quick look suggested long clicks were flat, but that is not a real check. A ranker can hurt quality without moving CTR, so this is the biggest gap.
- **CTR definition:** the figures above come from the table, where the denominator is all searches. The dashboard uses searches with results shown, which runs about 0.5 pp different. The size of the drop is the same under both. When quoting numbers elsewhere, use the dashboard definition. I haven't restated the table above on that basis.
