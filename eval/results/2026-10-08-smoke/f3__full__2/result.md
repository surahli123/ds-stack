## Answer
Headline: -1.80 pp
Overall CTR fell from 30.42% to 28.62% (-1.80 pp). All of that drop comes from desktop, where CTR fell about 3 pp, and none of it from mix. I'm attributing it to v3 by inference, since there was no control group.

## What it means for the rollback decision
Your PM is probably right. v3 looks like it hurts desktop (-3.0 pp in US, -2.9 pp elsewhere), and desktop is 60% of traffic. That points toward rolling back, or at least rolling back on desktop. Mobile is unchanged, so check whether v3 actually serves mobile before deciding there. [inferred]

## Why we believe it
- Alternatives considered:
  - Mix shift (platform or country share): ruled out. Segment weights are identical in both weeks (33/27/22/18%), so mix contributes +0.00 pp and within-segment change is -1.80 pp. [measured]
  - Seasonality or day of week: ruled out as far as I can tell. Both weeks cover Monday to Sunday, and daily search volumes match day for day across the two weeks. [measured]
  - Data completeness or logging: ruled out for volume. Every day has all 4 segment rows, and searches are unchanged. Mobile clicks are exactly identical week to week, which is unusually clean, so I can't rule out a logging or labeling quirk there. [measured/inferred]
  - Ranker v3 (the PM's cause): ruled in, but only by timing. The drop starts on 2026-09-07 and is confined to desktop, with no change on mobile. There was no holdout, since v3 went to 100% of traffic at once. [inferred]
  - Another change on 2026-09-07: not ruled out. `release_log` has only the v3 entry, but it may be incomplete. [guess]
- Checks run:
  - completeness: pass. The last day, 2026-09-13, has 4 rows, which is 100% of the trailing median.
  - mix_shift: pass. Overall -1.80 pp = within-segment -1.80 pp + mix +0.00 pp.
  - fanout: skipped. I ran no joins.
  - srm: skipped. This was not an experiment, so there are no assignment counts.

## Caveats, and what would change the answer
- This is a before/after comparison with no concurrent control. The roughly -1.8 pp is the observed change, and v3's share of it rests on timing and the desktop-only pattern.
- I gave no interval because the counts are huge, so sampling noise is only about 0.1 pp. The real uncertainty is causal, not statistical.
- Mobile being exactly flat is odd. If v3 doesn't actually reach mobile, the true v3 effect on desktop is the -3 pp figure, not a blended number.
- A holdout, a staggered rollout, or a check for other 2026-09-07 changes (UI, tracking, or a desktop client release) would settle the attribution.
- One week of data on each side. I haven't checked for novelty effects or whether the drop is growing or shrinking.