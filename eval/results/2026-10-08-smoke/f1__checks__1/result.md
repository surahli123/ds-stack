## Answer
Headline: about 0.0 pp attributable to v2 (within-platform change −0.0001 pp, measured). The overall drop of −2.10 pp (30.42% → 28.32%) is almost entirely a shift in platform mix.
Overall CTR fell 2.10 pp week over week. Within each platform, CTR didn't move (desktop 36.03% → 36.03%, mobile 22.02% → 22.02%). Mobile's share of searches rose from 40% to 55%, and mobile has the lower CTR.

## What it means for the decision
This data gives no reason to roll back v2 on CTR grounds. It also can't show that v2 helps, because there was no holdout: v2 went to 100% of traffic at once. The mix shift itself has an unexplained cause that should be found.

## Why we believe it
- Alternatives considered:
  - v2 lowered CTR within platforms: ruled out by the flat per-platform CTR in both weeks [measured]
  - Platform mix shift: ruled in. The mix_shift check attributes 100% of the change to mix (−2.10 pp), with desktop weight falling from 0.60 to 0.45 [measured]
  - Country mix: US and other have the same search volumes in both rankers, and each country's CTR is lower under v2 (US 31.3% → 29.2%, other 29.3% → 27.3%). That is the same platform-mix effect and I didn't separate it further [measured]
  - Whether v2 caused the mobile traffic shift: not determined. It may be coincidental timing, a traffic-routing or tracking change, or a marketing push [guess]
- Checks run:
  - mix_shift: fail. It flags that the change is driven by mix, not by within-segment rates.
  - completeness: pass. 2026-10-04 is fully loaded (4 rows, 100% of the trailing median).
  - srm: skipped. There was no randomized split, because v2 went to 100% of traffic.
  - fanout: skipped. No joins were used.

## Caveats, and what would change the answer
- It is a before/after comparison with no control group, so v2's effect is only identified by assuming nothing else changed within platforms. That is plausible given the flat rates, but I didn't verify it.
- I used only platform, country and ranker. Other segments or query types could hide a within-segment effect.
- If the mobile traffic jump turns out to be caused by v2 (for example, a change to how search is surfaced), the mix effect would count toward v2. Check this with the engineering and marketing release logs, which contain only one entry.
- One week of data per period.