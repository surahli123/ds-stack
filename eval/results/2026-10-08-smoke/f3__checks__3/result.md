## Answer
Headline: can't tell

Overall CTR fell 1.80 pp (30.42% → 28.62%), and the drop is entirely on desktop. v3 is the likeliest cause, but this data can't separate it from anything else that changed the same week.

## What it means for the rollback decision
Don't treat 1.8 pp as proven v3 damage, and don't rule it out either. v3 went to 100% of traffic on 09-07, so there is no concurrent v2 group to compare against. Before deciding, run a holdout or a desktop-only A/B of v2 against v3.

## Why we believe it
- Alternatives considered:
  - Traffic mix shift (platform or country): ruled out. Searches per segment are identical in both weeks (desktop 420k, mobile 280k, 33/27/22/18% weights), so mix contributes 0.00 pp [measured].
  - Seasonality or a general decline: partly ruled out. Mobile CTR is exactly unchanged (US 22.66%, other 21.23%), so a site-wide cause is unlikely [measured]. A desktop-only external change, such as a UI change, tracking change or bot traffic, is not ruled out because the release log has only the v3 entry [inferred].
  - v3 causing the desktop drop: plausible but not isolable. Ranker is perfectly collinear with week, so v3 and any other desktop change that week can't be told apart. Desktop CTR fell 3.0 pp in US and 2.9 pp in other [measured].
  - Data glitch: the mobile series being exactly identical across a full week looks suspiciously clean. It could mean v3 never reached mobile, or a pipeline or logging problem [guess].
- Checks run:
  - mix_shift: pass. The -1.80 pp change is all within-segment (US desktop -1.02, other desktop -0.78, mobile 0), with 0% from mix.
  - completeness: could not run. The tool needs at least 3 prior periods and I only had weekly aggregates. I checked by hand instead: all 14 days are present with 4 platform/country rows each, so there are no missing days [measured].
  - srm: skipped. This isn't a randomized experiment, so there is no assignment split to check.
  - fanout: skipped. I ran no joins.

## Caveats, and what would change the answer
- A holdout or staggered rollout, or any desktop traffic still served by v2, would give a real causal estimate.
- Only one pre-period week is available. Week-over-week noise is unknown, so I can't give an interval.
- Mobile shows zero change. Confirm whether v3 actually serves mobile. If it does, "v3 hurts desktop only" needs an explanation. If it doesn't, the rollout wasn't truly 100% on mobile.
- If a desktop UI or tracking change shipped around 09-07, it would explain the drop and v3 could be innocent.