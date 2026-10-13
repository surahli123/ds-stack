## Answer
Headline: -1.83 percentage points (95% CI -1.98 to -1.68), as the raw week-over-week change in overall CTR. I'm treating nearly all of it as v3's effect, which is an inference, not something the data proves.

Overall CTR fell from 30.44% to 28.61%. The whole drop is on desktop, where US fell 3.1 pp and other countries fell 2.9 pp. Mobile didn't move: -0.03 pp in the US and -0.04 pp elsewhere.

## What it means for the rollback decision
The interval is -1.98 to -1.68 pp, so the drop is not noise. It would only fall below any plausible rollback threshold if something other than v3 explains most of it. I can't rule that out with this data, because v3 went to 100% at once and there was no concurrent v2 holdout. You didn't give a threshold, so I can't say whether -1.8 pp is large enough to roll back.

## Why we believe it
- Alternatives considered:
  - Traffic mix shift (platform or country): ruled out by search volume per segment being within about 1% between weeks. [measured]
  - Random day-to-day noise: ruled out by a step change on 09-07 (about 30.4% every day before, 28.3–28.9% every day after) and by the narrow interval. [measured]
  - Another change shipped on 09-07: partly ruled out, since release_log lists only the v3 rollout. [measured] Unlogged changes, outages or seasonality remain possible. [guess]
  - A desktop-specific external shock, such as a logging or tracking change: not ruled out. The desktop-only drop fits "v3 hurts desktop" and also fits a desktop-specific confound. [inferred]
  - A general external shock affecting both platforms: unlikely, since mobile is flat. [inferred]
- Checks run:
  - Pooled two-proportion CI on clicks and searches: pass. -1.83 pp, CI -1.98 to -1.68. The CI treats searches as independent, so the true interval is probably somewhat wider.
  - Segment breakdown by platform and country: flag. The effect is concentrated entirely in desktop.
  - Daily series, 14 days: pass. There is no pre-trend and the step lands exactly on 09-07.
  - Concurrent control or holdout: could not run. All traffic switched on one date.
  - Reconciliation against a dashboard: skipped, because none was provided.

## Caveats, and what would change the answer
- The attribution to v3 rests on timing alone. Only two weeks of data and no holdout mean time and treatment are confounded.
- A 5–10% holdout on v2, or a desktop-only check of instrumentation changes around 09-07, would settle it.
- If v3 truly affects only desktop, a desktop-only rollback is an option.
- The interval covers sampling noise only, not the confounding above.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches), stated here [guess]. There is no metrics.json.
- Data: search_daily and release_log in warehouse.db, 2026-08-31 to 2026-09-13, which is both full weeks.
- Reconciled: not done (no dashboard or source figure available).
- Queries and checks: ad hoc Python/sqlite3 runs in this session, not saved to a file.