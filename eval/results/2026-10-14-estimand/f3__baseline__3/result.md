## Answer
Headline: can't tell. The observed change is -1.83 pp (±0.15), and the data can't separate v3's share of it from anything else that changed on 2026-09-07.

Overall CTR fell from 30.44% to 28.61%. The whole drop is on desktop, as a step on 09-07, and mobile did not move. The data has no control group, so I can't say how much of the drop v3 caused.

- Observed: -1.83 pp (95% CI -1.98 to -1.68) [measured]
- Adjusted: -1.83 pp (about ±0.15), holding platform and country mix fixed. The mix barely moved, so adjusting changes nothing. [measured]
- Causal effect: not identified. It would need a holdout or staggered rollout where some traffic stayed on v2, or a check that nothing else changed on desktop (logging, UI, click tracking) on 09-07.

## What it means for the rollback decision
The drop is real and not noise. Whether v3 caused it is unknown, so this data can't justify or rule out a rollback. A rollback or a v2 holdout on a slice of desktop traffic would answer it. If v3 caused the whole drop, the loss is about 1.8 pp overall, or about 3 pp on desktop.

## Why we believe it
- Alternatives considered:
  - Traffic mix shift (platform or country): ruled out. Search volume was 699,485 vs 699,266, and the platform and country shares were about the same each week. [measured]
  - Noise: ruled out. Desktop CTR was about 0.36 every day before 09-07 and about 0.33 every day after, so the change is a step with no overlap. [measured]
  - v3 hurts desktop only: still possible. Desktop fell 3.1 pp in the US and 2.9 pp elsewhere, while mobile moved by 0.04 pp or less. [measured]
  - A desktop-specific concurrent change (tracking, UI, an experiment): can't be ruled out. The same-day step is what you'd expect from a rollout, and also from a tracking change. [inferred]
  - Seasonality or a calendar effect such as the start of the school year: not tested, since there are only two weeks of data. The mobile stability argues against a site-wide cause. [guess]
- Checks run:
  - Mix and Simpson check by platform and country: pass. Overall CTR fell because desktop fell, not because of a mix change.
  - Daily trend: pass. There was no pre-trend, and the step lands exactly on 09-07.
  - Control group: fail. v3 went to 100% of traffic, so no v2 traffic exists after 09-07.
  - Release log: flag. It lists only the v3 rollout, so I can't see other changes.

## Caveats, and what would change the answer
- Before/after design with two weeks of data. Any desktop change on 09-07 is confounded with v3.
- A v2 holdout or a desktop-specific log check would settle it.
- The interval is for the observed difference only. It treats searches as independent and ignores clustering by user.
- There's no data on downstream quality, such as conversions or reformulations.

## Provenance
- Metric: CTR = clicks / searches, summed over rows, stated here [guess]. There is no metrics.json.
- Data: search_daily and release_log, through 2026-09-13.
- Reconciled: not done (no dashboard or source to compare against).
- Queries and checks: ad hoc Python/sqlite queries in this session. No saved files.