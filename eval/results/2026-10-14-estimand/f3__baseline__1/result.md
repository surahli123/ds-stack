## Answer
Headline: -1.80 pp (95% CI -1.95 to -1.65)
Overall CTR fell from 30.44% to 28.64% week over week. The drop is entirely on desktop, and the data can't separate v3 from anything else that changed that week.
- Observed: -1.80 pp (-1.95 to -1.65), measured. This is a two-proportion interval on 699k searches per week.
- Adjusted: -1.80 pp (about -1.95 to -1.65), holding platform × country mix fixed. Mix is essentially unchanged, so adjusting changes nothing. Measured.
- Causal effect: not identified. A control group of v2 traffic during the v3 week would identify it, as would a holdout or A/B split. Rollout was 100% on a single date, so there is none.

## What it means for the rollback decision
A drop of this size, about 1.8 pp or 6% relative, is large next to the week-to-week noise, which is under 0.15 pp. If v3 caused even half of it, the effect would still be material. I can't confirm v3 is the cause, but it is the only change in `release_log` and the timing matches exactly. I'd treat rollback, or a short holdout re-test, as the safe default. That is a judgement call, not a measured result.

## Why we believe it
- Alternatives considered:
  - Traffic mix shift (platform/country): ruled out. Searches per segment are within about 1% week over week, and the mix is stable [measured].
  - Seasonality or a gradual trend: mostly ruled out. The v2 week is flat at 30.1–30.8% daily, and the step happens on 09-07 and holds for all 7 days. I only have two weeks, so I can't rule out a seasonal effect [measured].
  - Another release or event: ruled out only as far as `release_log` goes. It lists one entry, and an unlogged change could still explain this [inferred].
  - Effect concentrated by segment: desktop US went from 37.1% to 34.0% (-3.1 pp) and desktop other from 34.8% to 31.9% (-2.9 pp). Mobile is flat (US 22.7% → 22.6%, other 21.2% → 21.2%) [measured].
  - Mobile as a control group: not valid. It assumes v3 has no effect on mobile, which I can't verify [inferred].
- Checks run:
  - Mix stability: pass.
  - Pre-period flatness: pass. Daily CTR is within ±0.4 pp.
  - Step timing: pass. The drop lines up with the rollout date.
  - Concurrent control: could not run, because there was no v2 traffic after 09-07.
  - Significance: pass. The interval is ±0.15 pp.

## Caveats, and what would change the answer
- Only one week before and one week after, with no holdout.
- Clicks are not quality-weighted. A lower CTR could come with better results, for example fewer wasted clicks.
- Desktop-only impact points to a desktop-specific cause, such as a v3 interaction with the desktop UI or a desktop logging change. Both are worth checking.
- A holdout of 5–10% of traffic on v2 would give a clean causal estimate.

## Provenance
- Metric: CTR = clicks / searches, summed over all segments, stated here [guess]. No `metrics.json` exists.
- Data: `search_daily` and `release_log`, 2026-08-31 to 2026-09-13.
- Reconciled: not done (no dashboard or other source available).
- Queries and checks: ad hoc Python/sqlite3 in this session, not saved to a file.