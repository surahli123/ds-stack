# The CTR drop is a mobile traffic shift, not a ranker v2 effect: keep v2

## Answer

Don't roll back v2. Overall CTR fell 2.1 pp (30.4% to 28.3%), but CTR inside each platform did not move. The drop comes from mobile's share of searches rising from 40% to 55%, and mobile CTR is lower.

## What it means for the decision

Dana, the data gives no reason to roll back by Thursday. Two follow-ups:

- Growth confirms what drove the mobile jump. One possible cause is an app store feature that week, which is unconfirmed.
- If you want certainty about v2 itself, run a 5% holdout for two weeks. Nothing in the current data can rule out a small v2 effect (see Caveats).

## Why we believe it

**Platform mix explains the drop.** The table covers `search_daily` for the week before and the week after v2 reached 100% on Sep 28. Desktop CTR is 36.0% in both weeks and mobile CTR is 22.0% in both weeks. Mobile's share of searches went from 40% to 55%. Splitting the -2.1 pp gives a within-platform effect of -0.0001 pp and a mix effect of -2.10 pp (measured).

**The drop is not country-specific.** US CTR fell from 31.3% to 29.2% and other countries from 29.3% to 27.3%. Both fell about 2 pp, so country does not separate the weeks.

**The data is complete.** All 14 days are present, with 4 rows per day (platform by country) and flat row counts.

**v2 is not the cause as far as this data shows (inferred).** If v2 had hurt ranking quality, CTR within platform would have fallen. It didn't. This is a before-and-after comparison, so it supports "coincided with" and not "caused by".

## Caveats

- There is no holdout. v2 went to everyone at once, so the comparison is before and after only. A v2 effect under about 0.3 pp would not show up.
- Only CTR was analysed. Long clicks looked flat in a quick check that was not done properly. Reformulation rate was not checked.
- The cause of the mobile jump is unconfirmed (see the growth follow-up above).
- CTR definitions differ. The dashboard divides by searches with results shown and the table by all searches, which gives about 0.5 pp different levels. The drop is the same in both. The figures here come from the table. Quote the dashboard definition when reporting externally, and expect levels about 0.5 pp off these.
