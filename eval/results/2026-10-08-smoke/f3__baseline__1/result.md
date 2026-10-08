## Answer
Headline: -1.80 pp overall CTR (30.42% → 28.62%), with no interval. Treat all of it as the upper bound for v3's effect.
Overall CTR fell 1.80 pp week over week. All of the drop is on desktop (about -3.0 pp, in both US and other). Mobile CTR didn't change at all. [measured]

## What it means for the rollback decision
v3 is the only logged change, and the drop starts the day it shipped, so rolling back is plausible for desktop. But this is a before/after comparison with no holdout, so I can't rule out a desktop-specific change that happened at the same time. If a quick desktop-only rollback or holdout is cheap, run that first to confirm.

## Why we believe it
- Alternatives considered:
  - Traffic mix shift (platform/country): ruled out. Searches per segment are identical in both weeks (700k total, same split), so the whole change is a within-segment CTR change. [measured]
  - Day-of-week or noise: ruled out. Desktop CTR was steady at 0.357–0.364 on every day of the first week. It stepped down to 0.327–0.334 on 09-07 and stayed there. Mobile is flat. [measured]
  - Desktop-only effect (the CTR change is concentrated in desktop): consistent with the data. Mobile is also on v3 with exactly 0 change, so v3 would have to hurt desktop only. [inferred]
  - Another change that hit desktop on 09-07 (UI, tracking, or a logging bug): not ruled out. The release_log has only the v3 entry, and there is no concurrent control group. [inferred]
- Checks run:
  - Mix-adjusted decomposition by platform and country: pass. Desktop US -3.09 pp, desktop other -2.89 pp, mobile 0.00 pp.
  - Daily trend for pre-existing drift: pass. No drift before 09-07.
  - Holdout or A/B comparison: could not run. v3 went to 100% of traffic and the data has no v2 rows after 09-07.
  - Significance interval: skipped. The data is daily aggregates, and the step is large and sharp relative to the day-to-day variation.

## Caveats, and what would change the answer
- Attribution rests on timing alone, so -1.80 pp is an upper bound for v3's effect.
- Mobile showing exactly 0.00 change is unusual for a ranker change. Check that mobile actually serves v3 and that mobile logging isn't stale.
- A desktop-side change on 09-07 (client release, click tracking, or a bot-filter change) would shrink v3's share.
- A desktop v2 holdout would settle the attribution.