## Answer
Headline: can't tell
Overall CTR fell 1.83 pp week over week, and the data can't say how much of that v3 caused. The drop is entirely on desktop. v3 launched at 100% of traffic, so there is no control group.
- Observed: -1.83 pp (95% CI -1.98 to -1.68), from 30.44% to 28.61% [measured]
- Adjusted: -1.82 pp (95% CI -1.97 to -1.67), holding platform×country mix fixed. This is the within-segment effect. Mix explains only -0.01 pp. [measured]
- Causal effect: not identified. It would take a holdout or staggered rollout (some traffic kept on v2), or a same-week comparison of v2 and v3 traffic.

## What it means for the rollback decision
The 95% interval on the observed drop is -1.98 to -1.68 pp. It is well outside the 0.1 pp threshold the mix_shift check uses as a minimum effect, but that interval describes the week-over-week change, not v3's effect. The data supports "CTR fell on desktop when v3 launched." It does not support "v3 caused it" at any particular size. If a desktop-only regression of about 3 pp is unacceptable, a partial rollback or holdout on desktop is the safer way to settle it than a full rollback.

## Why we believe it
- Alternatives considered:
  - Traffic mix shift: ruled out. Search volume per segment is flat, and mix contributes -0.01 pp. [measured]
  - v3 hurts desktop only: consistent with the data, but not proven. Desktop fell about 3.0 pp (US -3.11, other -2.87), while mobile moved about 0 (-0.03 and -0.04, intervals include 0). [measured]
  - Another change on 2026-09-07 (desktop UI, logging or tracking, seasonality, a bot filter): not ruled out. release_log lists only v3, and ranker is perfectly collinear with week. [inferred]
  - A v3 effect that is real but smaller or larger than the observed change: not separable without a control. [inferred]
- Checks run:
  - mix_shift: pass. Within-segment -1.82 pp, mix -0.01 pp.
  - completeness: pass. 2026-09-13 has 4 of 4 segment rows, and every day in both weeks has 4 rows.
  - srm: skipped. There is no randomized assignment.
  - fanout: skipped. No joins were used.

## Caveats, and what would change the answer
- Intervals treat searches as independent, so they are probably too narrow. Clicks cluster by user, and I only have daily aggregates.
- Two weeks is too short to rule out a trend or a seasonal effect. I did not check earlier weeks.
- A desktop-specific tracking or UI change on 09-07 would explain the drop without v3. Ask the release owners and check the logging.
- Holdout data from any v2 traffic after 09-07 would give the causal number.

## Provenance
- Metric: CTR = clicks / searches, from search_daily [guess]. There is no metrics.json.
- Data: search_daily and release_log, through 2026-09-13 (complete).
- Reconciled: not done (no dashboard or source to compare against).
- Queries and checks: the queries were run inline and not logged. Check outputs are logged in `.ds-checks.log` as mix_shift#1 and completeness#1.