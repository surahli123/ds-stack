## Answer
Headline: -1.80 pp (overall CTR 30.42% → 28.62%; no interval, since there is no sampling model or control group)
Overall CTR fell 1.80 pp week over week. All of the drop is in desktop, where CTR fell about 3 pp. Mobile is exactly flat, and that flatness looks suspicious. [measured]

## What it means for the rollback decision
The mix and timing point to v3 as the likely cause of the desktop drop: -3.1 pp on desktop US and -2.9 pp on desktop other. This is an inference, because the rollout was 100% with no holdout group. Before deciding, find out why mobile shows zero change. If mobile is real and v3 doesn't affect it, v3 costs about 1.8 pp overall. If the mobile numbers are bad data, the overall effect could be larger or smaller than 1.8 pp.

## Why we believe it
- Alternatives considered:
  - Traffic mix shift (platform or country): ruled out. Search volume per segment is identical in both weeks (700k each), so the whole change is within-segment CTR. [measured]
  - Seasonality or a general downturn: mostly ruled out. The CTR step happens on 09-07 itself, and every day in the prior week is stable at about 0.36 on desktop. Mobile did not move. [measured]
  - Other concurrent releases or outages: ruled out only as far as the release_log goes. It has a single entry, the v3 rollout. [inferred]
  - Mobile not being served v3: possible, but I can't confirm it. Mobile rows are labelled v3, yet their clicks are unchanged. [guess]
- Checks run:
  - Segment decomposition (platform × country, before and after): pass. The change is concentrated in desktop. [measured]
  - Daily CTR trend: pass. There is a clean step on 09-07 and no pre-trend. [measured]
  - Mobile data integrity: fail. The 7 daily mobile click counts in week 2 match week 1 exactly, to the click (for example 8806, 9161, 8545 and so on). That is implausible for real data and suggests copied or stale rows. [measured]
  - Control group or holdout comparison: could not run. v3 went to 100% of traffic, so there is no concurrent v2 comparison. [measured]

## Caveats, and what would change the answer
- The mobile week-2 clicks look duplicated from week 1. If the real values differ, the overall effect and the "desktop only" conclusion both change.
- Without a holdout, any other change on 09-07, such as logging, UI or a desktop-specific event, would be mixed into the -1.80 pp. A desktop-only A/B or a brief partial rollback would settle causality.
- CTR is only one metric. Check downstream measures such as conversion or satisfaction before the final call.