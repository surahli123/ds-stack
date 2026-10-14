I ran the checks and have what I need. Here is the readout.

```
## Answer
Headline: can't tell
Overall CTR fell 1.83 pp week over week, and the entire drop is on desktop. The data can't say how much of it v3 caused, because every user moved to v3 on the same day.
- Observed: -1.83 pp (-1.98 to -1.68), 30.44% → 28.61%
- Adjusted: -1.82 pp (-1.97 to -1.67), holding platform × country mix fixed
- Causal effect: not identified (it needs a concurrent control, such as a holdout on v2 or a staged rollout; the drop isn't attributed to v3 until then)

## What it means for the rollback decision
The drop is real and not a mix artifact: -1.7 to -2.0 pp, well above the 0.1 pp minimum effect the check uses. The rollback decision turns on whether v3 caused it, and this data can't show that. A v2 holdout, or a staged re-rollout, would show it. The PM's theory is plausible but unproven.

## Why we believe it
- Alternatives considered:
  - Traffic mix shift (platform/country): ruled out. Mix explains -0.01 pp, about 1% of the change [measured]
  - Incomplete data in the latest week: ruled out. All 7 days have the expected 4 segment rows [measured]
  - v3 hurting desktop only: still possible. Desktop CTR fell 2.7–3.1 pp (US 37.1→34.0, other 34.8→31.9), and mobile was flat (22.7→22.6, 21.2→21.2) [measured]. Whether the ranker acts differently by platform is [guess]
  - A concurrent desktop-specific change (UI, logging, seasonality, a bot filter): not ruled out. The release log has only the v3 entry, but it may be incomplete [guess]
  - Normal day-to-day noise: ruled out. Every v2 day was 30.1–30.8% and every v3 day was 28.3–28.9%, with no overlap, and the step lands exactly on 09-07 [measured]
- Checks run:
  - mix_shift: pass. Within-segment -1.82 pp, mix -0.01 pp [check:mix_shift#1]
  - completeness: pass. 2026-09-13 has 4 rows, 100% of the trailing median [check:completeness#1]
  - srm: skipped. There is no randomized assignment, so there is no split to test
  - fanout: skipped. No joins were used

## Caveats, and what would change the answer
- The ranker label is perfectly confounded with the week: v2 only before 09-07 and v3 only after, with no overlap.
- The intervals treat searches as independent, so they are probably a little too narrow. The day-to-day spread suggests the real interval is still far from zero.
- This is one pre-week against one post-week.
- A desktop-only effect is a lead, not evidence of cause. A holdout, or a check of desktop-specific changes made on 09-07, would settle it.
- I have no CTR definition from metrics.json, and no threshold for what drop would trigger a rollback.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches), pooled over days and segments [guess]; there is no metrics.json
- Data: search_daily and release_log, through 2026-09-13, which is complete
- Reconciled: not done (no dashboard or other source available)
- Queries and checks: the checks are logged in .ds-checks.log in the analysis directory. The SQL ran ad hoc in Python and was not logged.
```