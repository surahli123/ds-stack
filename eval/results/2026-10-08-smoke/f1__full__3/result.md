## Answer
Headline: about 0.0 pp attributable to v2 (within-segment effect −0.0001 pp; the interval is not computed). Overall CTR fell 2.10 pp, from 30.42% to 28.32%.

Nearly all of the drop is a shift in traffic from desktop to mobile, which has a lower CTR. Within each platform and country, CTR did not change under v2 (measured).

## What it means for the rollback decision
The data gives no reason to roll back v2 on CTR grounds. The drop comes from the traffic mix, not from v2. Because v2 went to 100% of traffic at once, there is no control group, so this is not a clean test of v2.

## Why we believe it
- Alternatives considered:
  - Mix shift (mobile share rose from 40% to 55%): ruled in. It explains −2.10 of the −2.10 pp (99.99%), and CTR in each of the four platform and country segments is flat to the 4th decimal (e.g. desktop US 37.08% before and after) [measured].
  - v2 hurt ranking quality: ruled out as a CTR driver. The within-segment effect is −0.0001 pp [measured]. It cannot be fully separated from other changes that happened the same week, since v2 shipped to everyone with no holdout [inferred].
  - Seasonality and day of week: ruled out. Both weeks cover Monday to Sunday, and daily search volume is nearly identical (about 100k per day) [measured].
  - Data completeness: ruled out. Both weeks have 4 rows per day, and the last day matches the trailing median [measured].
  - Logging or definition change: no evidence. The release log has only the v2 rollout entry [measured]. I can't see the instrumentation itself [guess].
  - Why mobile share rose: unknown. It could be a marketing push, a mobile release, or v2 changing who searches. I did not investigate it [guess].
- Checks run:
  - mix_shift: fail. The overall change is −2.10 pp, of which −2.10 pp is mix and −0.00 pp is within-segment. The failure is the finding, and it changes the answer from "v2 caused it" to "mix shift caused it".
  - completeness: pass. 2026-10-04 has 4 rows, 100% of the trailing median.
  - fanout: skipped. I ran no joins.
  - srm: skipped. This is a before/after comparison, not a randomized experiment.

## Caveats, and what would change the answer
- Ranker is perfectly confounded with time. v1 only appears before 09-28 and v2 only after, so a v2 effect is identified only by assuming within-segment CTR would have stayed flat without it.
- If v2 itself pushed users toward mobile, which I can't rule out, some of the mix shift would be a v2 effect. Checking where the mobile traffic growth came from would settle it.
- Segments are coarse (platform and country). Effects inside finer segments, such as query type, are not visible here.
- A holdout of 5–10% of traffic on v1 would give a clean estimate with an interval.