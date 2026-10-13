## Answer
Headline: -1.83 percentage points (95% interval -1.98 to -1.68). This is the whole week-over-week change, not a separate v3 estimate.
Overall CTR fell from 30.44% to 28.61%. The whole drop is on desktop, and mobile CTR did not move. The data can't separate v3 from anything else that changed on 2026-09-07. [measured]

## What it means for the rollback decision
The interval is about -1.7 to -2.0 points. If v3 caused all of it, that is a clear loss. I don't know your rollback threshold, so I can't say whether it is exceeded. Because v3 went to 100% of traffic, the data can't prove the drop is v3 rather than something else that week. A holdout or a staged rollback test would settle it.

## Why we believe it
- Alternatives considered:
  - Traffic mix shift (platform or country): ruled out. Search volume per segment is within about 1% week over week, and CTR fell within the desktop segments, not through mix. [measured]
  - Mobile also affected: ruled out. Mobile US went from 22.66% to 22.63% and mobile other from 21.23% to 21.19%. [measured]
  - Desktop fell by 3.1 points (US) and 2.9 points (other). [measured]
  - A gradual or pre-existing trend: ruled out as the main driver. Daily CTR was flat at about 30.0–30.8% for all 7 days before the rollout, then dropped to about 28.3–28.9% on day one and stayed there. [measured]
  - A concurrent non-v3 change that hit desktop on 09-07: not ruled out. release_log lists only the v3 rollout, but it may be incomplete. [inferred]
  - Seasonality or a calendar effect: not ruled out. There is no prior-year data and only 2 weeks of history. [guess]
  - v3 as the cause: consistent with the sharp step on the rollout date, but ranker is perfectly confounded with time. There was no control group. [inferred]
- Checks run:
  - Pre/post two-proportion z-interval on pooled clicks/searches: pass. The result is -1.83 points with a tight interval. It assumes searches are independent and ignores day-to-day variation.
  - Segment breakdown (platform × country): flag. The effect is concentrated on desktop.
  - Daily series: pass. It shows a step change on the rollout date, with no ramp.
  - Concurrent control: could not run. All traffic switched to v3 at once.

## Caveats, and what would change the answer
- Only 2 weeks of data are available, and the pre-period has no v3 traffic. Anything else that changed on 09-07 would be counted as v3's effect.
- Check for desktop-only events on 09-07, such as a UI change, logging change, bot filtering or an experiment. If one exists, the v3 estimate shrinks.
- A short holdout of v2 for desktop would give a causal estimate.
- The interval reflects sampling noise only. Real uncertainty is larger because of the confounding above.

## Provenance
- Metric: CTR = sum(clicks)/sum(searches), pooled over all segments. No metrics.json was present, so this definition is stated here. [guess]
- Data: search_daily and release_log, through 2026-09-13.
- Reconciled: not done (no dashboard or source figure available).
- Queries and checks: run inline in this session and not saved to a file. They are reproducible from the grouped sums by date, platform, country and ranker.