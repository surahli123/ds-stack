## Answer
Headline: ≈0.0 pp (about −0.8 to +0.3 pp at most, by the segment-adjusted estimate; −0.8 pp is its lower bound). Treat this as a before/after estimate, not a proven causal effect.

Overall CTR fell about 2.1 pp, but almost all of the drop comes from traffic shifting to mobile, which has a lower CTR. Within each platform and country, CTR did not change.

- Observed: −2.10 pp (±0.15; 30.42% → 28.32%) [measured]
- Adjusted: −0.01 pp (±0.16), holding platform×country mix fixed at week-1 mix [measured]. Using the week-2 mix gives +0.03 pp (±0.15) [measured].
- Causal effect: not identified. There was no concurrent control group, because v2 went to 100% of traffic at once. The adjusted figure is a before/after estimate, and it would only be causal if nothing else changed. Identifying it needs a holdout or a staggered rollout, or an explanation of the mobile shift.

## What it means for the rollback decision
The mix-adjusted interval of roughly ±0.16 pp rules out a v2 CTR loss larger than about 0.2 pp, so about 2 pp of the observed drop is not attributable to v2. If a loss of about 0.5 pp would be enough to roll back, this data doesn't support rolling back. The caveat is that we can't tell whether v2 itself caused the mobile shift.

## Why we believe it
- Alternatives considered:
  - v2 lowered CTR: ruled out as the main driver. Each of the four segments shows a flat CTR change, within ±0.1 pp [measured].
  - Traffic mix shift (Simpson's-paradox pattern): ruled in. Mobile's share of searches rose from about 40% to about 55%, and mobile CTR is about 22% against about 36% on desktop [measured].
  - Whether v2 caused the mobile shift (for example through search UX or routing): not ruled out. There is no evidence either way in this data [guess].
  - Other concurrent changes (campaign, seasonality, app release): not ruled out. release_log lists only the v2 rollout, and the data has no other information about the week [inferred].
- Checks run:
  - Segment-level CTR before and after: pass. All four segments are flat.
  - Total searches week over week: pass. 699.6k vs 700.4k, so volume is stable.
  - Standardization with both weeks' mixes: pass. Both give about 0 pp.
  - Day-level trend check: skipped. I only eyeballed the daily totals, which are steady, and didn't test them.
  - Control group or holdout: could not run. v2 was at 100% of traffic from 2026-09-28.

## Caveats, and what would change the answer
- Only one week before and one week after, so week-to-week variation isn't estimated. The intervals reflect sampling noise only and are likely too narrow.
- The platform mix shifted abruptly on exactly the rollout date. That coincidence deserves an explanation. If v2 or its release caused it, the mix shift is itself a v2 effect.
- Segments are coarse. Query-type or user-level shifts within a segment could still hide an effect.
- A clean holdout, or the cause of the mobile surge, would change this answer.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches), from stated here [guess]. No metrics.json was present.
- Data: search_daily and release_log, through 2026-10-04 (both weeks complete).
- Reconciled: not done (no dashboard or other source available to compare against).
- Queries and checks: run inline in Python against warehouse.db. No script or log file was saved.