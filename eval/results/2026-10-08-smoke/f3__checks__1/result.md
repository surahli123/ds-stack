## Answer
Headline: -1.80 percentage points (overall CTR 30.42% → 28.62%). Nothing else in the data explains it, but this is a before/after comparison with no control group, so there is no interval. [measured]

Overall CTR fell 1.80 pp week over week. All of the drop is on desktop, where CTR fell about 3 pp in both countries. Mobile CTR is unchanged. [measured]

## What it means for the rollback decision
v3 is the likely cause of the full −1.8 pp drop, and the harm is concentrated on desktop. [inferred] Rolling back, or at least rolling back on desktop, looks justified unless v3 delivers a benefit this data doesn't capture.

## Why we believe it
- Alternatives considered:
  - Traffic mix shift (more mobile, which has lower CTR): ruled out. Search volume shares are identical across the two weeks, and mix contributes 0.00 pp of the change. [measured]
  - Incomplete data in the latest week: ruled out. Both weeks have all 7 days with 4 rows each. [measured]
  - Country-specific effect: ruled out. Desktop fell in both US (37.1% → 34.0%) and other (34.7% → 31.8%). [measured]
  - A general decline in search behavior or seasonality: mostly ruled out. Mobile CTR is exactly flat in both countries, which argues against a site-wide shift. [inferred]
  - Other launches in the same week: ruled out as far as the data shows. release_log has only the v3 rollout. [measured]
- Checks run:
  - mix_shift: pass. The change is −1.80 pp within segments plus 0.00 pp from mix. Desktop US contributes −1.02 pp and desktop other −0.78 pp.
  - completeness: pass. 2026-09-13 has 4 rows, 100% of the trailing median.
  - srm: skipped. This is not a randomized experiment; v3 went to 100% of traffic.
  - fanout: skipped. No joins were used.

## Caveats, and what would change the answer
- There is no concurrent control, because v3 went to 100% of traffic. The causal reading rests on mobile being flat and on desktop dropping exactly when v3 launched. [inferred]
- Mobile clicks are identical to the prior week's, to the click. That is suspicious and may mean mobile was not actually served v3 or is logged differently. If mobile didn't get v3, the desktop-only drop is still attributable to v3, but the "v3 is neutral on mobile" reading would not hold. [guess]
- It's only one week of data. A client-side desktop change or tracking change at the same time, such as a UI or logging release not in release_log, would change the answer. A holdout of 5–10% on v2 for desktop would settle it.