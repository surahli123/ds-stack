## Answer
Headline: can't tell
Overall CTR fell 1.83 pp week over week, but v3 went to 100% of traffic at once. With no holdout, I can't separate v3 from anything else that changed the same day.
- Observed: -1.83 pp (95% CI -1.98 to -1.68) [measured]
- Adjusted: -1.83 pp, holding the platform and country mix fixed. The mix is essentially unchanged, so adjusting changes nothing. [measured]
- Causal effect: not identified (it would need a holdout or staged rollout, or a log of other changes from 2026-09-07)

## What it means for the rollback decision
The drop is real and large. The interval of -1.98 to -1.68 pp is nowhere near zero, and the same-day timing makes v3 the prime suspect. But that is a before/after comparison, not proof of cause. I'd treat a drop of even 0.5 pp as grounds for a rollback test, which this clears easily. The ssensible step is a short 50/50 holdout of v2 against v3 rather than a blind rollback.

## Why we believe it
- Alternatives considered:
  - Traffic mix shift (platform or country): ruled out. Search volume per segment is flat, within ±1% for every segment. [measured]
  - Concurrent change affecting desktop only: not ruled out. The drop is entirely on desktop, at -3.00 pp (±0.20). Mobile is flat at -0.04 pp (±0.22). Either v3 only hurts desktop, or something else hit desktop that week. [inferred]
  - Seasonality or a data glitch: unlikely. The week before is steady (daily CTR 0.30–0.31). Every day after the rollout is lower (0.283–0.289), a clean step on 09-07. [measured]
  - Random noise: ruled out. The interval excludes zero by a wide margin. [measured]
- Checks run:
  - Daily CTR by ranker: pass. It steps down exactly at the rollout date.
  - Segment decomposition: flag. The effect is concentrated in desktop (US -3.1 pp, other -2.9 pp).
  - Control group: could not run. No v2 traffic exists after 09-07, so mobile is the only partial comparison, and v3 shipped there too.

## Caveats, and what would change the answer
- Only one release is logged, but other changes (UI, tracking, bots, instrumentation) may not be recorded. A desktop-side change on 09-07 would explain the data equally well.
- The intervals treat searches as independent, so they are probably too narrow. Users repeat searches.
- A desktop-only effect from a ranker change would be unusual, which makes the desktop-only pattern worth checking against a desktop client or logging change.
- One week of post-rollout data. A novelty effect or later recovery is possible.

## Provenance
- Metric: CTR = clicks / searches, pooled over all rows in each week, with intervals from a two-proportion normal approximation. This is stated here, not taken from metrics.json (no such file exists) [guess].
- Data: search_daily (56 rows) and release_log, through 2026-09-13.
- Reconciled: not done (no dashboard or other source to compare against).
- Queries and checks: ad-hoc Python/SQLite run inline; not saved to a file.