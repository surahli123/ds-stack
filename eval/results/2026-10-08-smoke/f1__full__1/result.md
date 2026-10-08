Quick status: both checks are done, so I'm writing up the result now.

## Answer
Headline: about 0.0 pp (-0.0001 pp within-segment) attributable to v2, out of a -2.10 pp overall CTR change (30.42% → 28.32%) [measured]
Overall CTR fell 2.10 pp, and almost all of that (-2.10 pp, about 100%) comes from traffic moving from desktop to mobile. Within every platform×country segment, CTR is unchanged to four decimal places.

## What it means for the rollback decision
The data doesn't support rolling back v2 on CTR grounds. The drop comes from a shift in traffic mix toward lower-CTR mobile, and v2 shows no measurable within-segment effect. The open question is what caused the mobile shift (see caveats).

## Why we believe it
- Alternatives considered:
  - v2 lowered CTR (the PM's view): ruled out as the main driver. Within-segment CTR is identical before and after in all 4 segments (e.g. desktop US 37.08% → 37.08%, mobile other 21.23% → 21.23%). Within-segment effect is -0.0001 pp [measured]
  - Mix shift: ruled in. Mobile share of searches went from 40% to 55%. Desktop US fell from 33% to 24.8% of searches. Mix effect is -2.10 pp, 99.99% of the change [measured]
  - Seasonality / day of week: ruled out. Both weeks cover Mon–Sun, and daily volumes match day for day (about 100k per day). The CTR step happens on 09-28 [measured]; I did not look at prior weeks for a seasonal pattern [inferred]
  - Incomplete data or a logging change: ruled out for incompleteness, since all 14 days are present with steady volume [measured]. A logging or definition change is unlikely, since segment CTRs are flat to 4 decimals, but I can't verify it from this table [inferred]
  - v2 itself caused the mobile shift (for example through a client or routing change): not ruled out. There was no holdout, and total volume is flat while the platform split moved on the rollout date [guess]
- Checks run:
  - mix_shift: fail. Flags a mix-dominated change: -2.10 pp overall = -0.00 pp within-segment + -2.10 pp mix. This is why the answer attributes the drop to mix and not v2
  - completeness: pass. 2026-10-04 has 102% of the trailing median rows, and all 14 days are present
  - fanout: skipped. No joins were used
  - srm: skipped. This is not a randomized experiment (100% rollout, no control arm)

## Caveats, and what would change the answer
- There is no concurrent control, since v2 went to 100% at once. A v2 effect that is the same in every segment is still unlikely to show up as exactly zero. Even so, a hidden effect that shifted who searches on mobile can't be excluded.
- Check why mobile share jumped on 09-28 (a mobile campaign, an app release, an outage or change on desktop, or a v2 side effect). If it traces to v2, the rollback question reopens.
- The data is only 2 weeks at segment level. Other segments, such as new vs returning users, could hide differences.
- A holdout or staggered rollout would settle causality directly.