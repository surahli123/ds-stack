## Answer

Don't roll back ranker v2. Overall CTR fell 2.1 pp (30.4% to 28.3%), but CTR inside each platform did not move. Mobile, which has lower CTR, grew from 40% to 55% of searches.

## What it means for the decision

Dana, the data gives no reason to roll back by Thursday (inferred from the measurements below). Two follow-ups:

- Growth confirms what drove the mobile jump. They suspect an app store feature that week, which is unconfirmed.
- If you need certainty about v2 itself, run a 5% holdout for two weeks. A rollback would not give that answer either, since it is another before/after comparison.

## Mix explains the whole drop

Desktop CTR was 36.0% in both weeks and mobile CTR was 22.0% in both weeks (measured, `search_daily`, week before vs week after the Sep 28 launch to 100%). Mobile share of searches rose from 40% to 55%. A mix decomposition splits the -2.10 pp overall change into a within-platform effect of -0.0001 pp and a mix effect of -2.10 pp, so the drop is essentially all mix.

Country does not explain it. US fell 31.3% to 29.2% and other countries fell 29.3% to 27.3%, about 2 pp each, so the drop is the same in both.

The data was complete: all 14 days present, 4 rows per day (platform x country), flat row counts.

## Caveats

- No holdout. v2 went to everyone at once, so this is a before/after comparison. It shows the drop coincided with the traffic shift. It does not show v2 had no effect.
- A v2 effect under about 0.3 pp would not show up in this data.
- Only CTR was checked. Long clicks looked flat in a quick check that was not done properly, and reformulation rate was not looked at. If v2 hurt quality, those metrics are where it would show, so check them before Thursday if time allows.
- The cause of the mobile jump is unconfirmed.

## Appendix: CTR definition

The dashboard computes CTR on searches with results shown. The `search_daily` table uses all searches. Levels differ by about 0.5 pp, but the drop is the same under both. Use the dashboard definition when reporting.
