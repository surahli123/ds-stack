# Ranker v2 did not cause the CTR drop: keep it

## Answer

Do not roll back v2. Overall CTR fell 2.1 pp (30.4% to 28.3%) because mobile's share of searches rose from 40% to 55%. CTR inside each platform did not move.

## What it means for the decision

Dana, the data gives no reason to roll back by Thursday. Two follow-ups:

- Growth confirms what drove the mobile jump (owner: Growth; unconfirmed, see below).
- If you need certainty about v2 itself, run a 5% holdout for two weeks. This is my recommendation, and the only way to rule out a small v2 effect.

## Mix explains the whole drop

Desktop CTR was 36.0% in both weeks and mobile CTR was 22.0% in both weeks. Mobile converts worse than desktop, so a bigger mobile share lowers the overall rate. A mix decomposition (measured) splits the -2.1 pp into a within-platform effect of -0.0001 pp and a mix effect of -2.10 pp, so the drop is effectively all mix.

The pattern is not country-specific. US CTR went 31.3% to 29.2% and other countries 29.3% to 27.3%, both about -2 pp, which is what a platform shift across all countries would produce.

Data was complete: all 14 days present, 4 rows per day (platform x country), flat row counts. Source: `search_daily`, one week before and one week after v2 reached 100% on Sep 28.

## Why mobile traffic rose is not confirmed

Growth suggested an app store feature that week. That is a lead, not a finding (guess). Until Growth confirms, the cause of the traffic shift is open, though it does not change the v2 conclusion.

## Caveats

- Before/after only. v2 went to 100% at once, so there is no holdout. The comparison shows the drop coincided with a traffic shift, not that v2 had no effect.
- A v2 effect under about 0.3 pp would be invisible in this data.
- Only CTR was analyzed. Long clicks looked flat in a quick check that was not done properly, and reformulation rate was not checked. A v2 regression there would not show up here.
- CTR figures use the `search_daily` table denominator (all searches). The dashboard uses searches with results shown, which runs about 0.5 pp different, but the drop is the same in both. Quote dashboard figures when reporting externally.
