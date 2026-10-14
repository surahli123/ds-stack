## Answer
Headline: can't tell. The data can't separate v3 from anything else that changed that week.
Overall CTR fell 1.83 pp week over week, and v3 may be responsible. It shipped to 100% of traffic at once, so there is no concurrent v2 group to compare against.
- Observed: −1.83 pp (95% CI −1.98 to −1.68). CTR went from 30.44% to 28.61%, on 699,485 and 699,266 searches. [measured]
- Adjusted: −1.83 pp (about the same interval), holding platform and country mix fixed. [inferred] I didn't run a formal standardization. The segment shares barely moved between weeks, so mix explains essentially none of the drop.
- Causal effect: not identified. It would take a holdout or a staggered rollout where some traffic stayed on v2. The data has none.

## What it means for the rollback decision
The drop is real and not noise, and the whole interval lies far from zero. But it is a before/after comparison, so it shows an upper-bound-style association, not v3's effect. The drop is concentrated on desktop, so the next step is to check what else changed on desktop that week. If a ≥0.5 pp loss matters to you, the observed drop clears that bar. Whether v3 caused it is still unproven.

## Why we believe it
- Alternatives considered:
  - Traffic mix shift (platform/country): ruled out. Segment search volumes were nearly identical across the two weeks, and every segment's CTR is lower or flat. [measured]
  - Random noise: ruled out. The interval excludes zero by a wide margin, and daily CTR sits below the v2 days on every v3 day. [measured]
  - Desktop-only confound (tracking change, UI change, seasonality, a release not in the log): not ruled out. Desktop fell 3.00 pp (CI −3.20 to −2.80) in both US (−3.1 pp) and other countries (−3.0 pp). Mobile was flat at −0.04 pp (CI −0.26 to +0.18). v3 hit every user at once, so a ranker that only hurts desktop and a desktop-specific event look the same in this data. [inferred]
  - Seasonal or week-to-week variation: can't assess. Only two weeks of data, and no earlier history to see normal weekly variation. [measured]
- Checks run:
  - Segment mix stability: pass. Shares are stable.
  - Platform split: flag. The effect is entirely on desktop.
  - Concurrent control group: could not run. All traffic switched on 2026-09-07.
  - Release log for other changes: pass. It has one entry, the v3 rollout. It may be incomplete.

## Caveats, and what would change the answer
- A v2 holdout or a staggered rollout would identify the causal effect.
- Check for desktop-specific changes that week (UI, logging or click-tracking, bot traffic).
- Look at earlier weeks' desktop CTR to see whether a 3 pp swing is normal.
- Intervals treat searches as independent. Searches by the same user are clustered, so the true intervals are somewhat wider.
- If desktop is where v3 matters, a desktop-only rollback or A/B test is the cheapest way to get a real answer.

## Provenance
- Metric: CTR = clicks / searches, stated here [guess]. There is no metrics.json.
- Data: `search_daily` and `release_log`, through 2026-09-13.
- Reconciled: not done (no dashboard or other source provided).
- Queries and checks: ad hoc Python/SQLite run in this session. Nothing is saved to a file.