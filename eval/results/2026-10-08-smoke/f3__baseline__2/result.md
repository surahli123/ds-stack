## Answer
Headline: −1.80 pp (overall CTR 30.42% → 28.62%; essentially all of it attributed to v3, with no control group)

Overall CTR fell 1.80 percentage points week over week, and the whole drop is a roughly 3 pp CTR fall on desktop, in both US and other countries, starting the day v3 launched. Mobile CTR did not change.

## What it means for the rollback decision
Measured: the drop is real and it is concentrated on desktop. Inferred: v3 is the likely cause, because the timing matches exactly. I'd treat it as a reason to roll back or run a holdback on desktop. Nothing here shows v3 hurts mobile.

## Why we believe it
- Alternatives considered:
  - Traffic mix shift (more mobile, which has lower CTR): ruled out. Searches are 700,000 in both weeks, and the platform and country splits are identical [measured].
  - Country-specific effect: ruled out. Desktop fell by about 3.1 pp in the US (37.08% → 33.99%) and 3.0 pp elsewhere (34.74% → 31.85%) [measured].
  - Gradual trend or noise: ruled out. Desktop CTR was flat at about 0.357–0.364 daily through 09-06, then stepped down to about 0.327–0.334 on 09-07 and stayed there. The day-to-day pattern in the two weeks is otherwise the same [measured].
  - An unrelated change that day (seasonality, tracking, an outage): not ruled out. The release log has only the v3 rollout. v3 went to 100% of traffic at once, so there is no concurrent v2 control [inferred].
  - Mobile unaffected by v3: plausible but odd. Mobile clicks and searches are identical week to week (34,899 and 26,751 clicks for US and other), so the mobile data may be copied or carried over, or v3 may not apply to mobile. I can't tell which [guess].
- Checks run:
  - Week-over-week CTR by platform, country and ranker: pass. It shows the desktop-only drop above.
  - Mix-versus-rate decomposition: pass. All of the change comes from the rate, none from mix.
  - Daily CTR series by platform: pass. It shows a step change on 09-07.
  - Control or A/B holdback comparison: could not run. No v2 traffic exists after 09-07.
  - Mobile data integrity: fail. The two weeks match exactly, which looks suspicious.

## Caveats, and what would change the answer
- The attribution rests on timing alone. A holdback, or a desktop-only A/B test of v2 against v3, would confirm or overturn it.
- If the mobile data is actually duplicated, the true overall change and the mobile effect are unknown. The mobile effect could be a real drop that is being masked.
- Only one week is available on each side, and CTR is not the same as search quality. Check downstream metrics such as task success and revenue before deciding.