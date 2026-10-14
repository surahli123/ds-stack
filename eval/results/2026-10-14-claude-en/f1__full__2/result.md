## Answer
Headline: -0.00 pp (-0.15 to +0.15) [check:mix_shift#1]
Overall CTR fell 2.10 pp, but essentially all of it is a shift of traffic toward lower-CTR mobile; within-segment CTR is flat, so v2 accounts for about 0 pp if v2 did not itself change the platform mix [check:mix_shift#1].
- Observed: -2.10 pp (-2.25 to -1.95) [check:mix_shift#1]
- Adjusted: -0.00 pp (-0.15 to +0.15), holding platform x country mix fixed [check:mix_shift#1]
- Causal effect: not identified (v2 went to all traffic at once with no holdout; a randomized holdout or a staggered rollout would identify it)

## What it means for the rollback decision
The within-segment effect of v2 is bounded to about ±0.15 pp [check:mix_shift#1], far below the 2.10 pp drop [check:mix_shift#1], so the CTR drop is not a reason to roll back; a loss of 0.3 pp or more would be needed to matter (this threshold is my assumption, not given) [check:mix_shift#1].

## Why we believe it
- Alternatives considered:
  - Mix-shift: ruled in as the explanation; mobile share of searches rose from 40.1% to 55.1% while mobile CTR (22.0%) is far below desktop (36.0%), giving -2.09 pp of mix effect [check:mix_shift#2] [measured]
  - v2 lowered CTR (PM's cause): ruled out as the main driver; within-segment change is -0.00 pp in all four platform x country cells [check:mix_shift#1] [measured]
  - Mix shift caused by v2 itself: not ruled out; the data has no information on why mobile share rose [q4] [guess]
  - Data completeness: ruled out; all 14 days have the full 4 segment rows [check:completeness#1] [measured]
  - Seasonality / day of week: ruled out; both windows are Mon-Sun, 7 days each, and v1 daily CTR was stable across the prior week [q3] [inferred]
  - Logging or definition change: ruled out for the release log, which shows only the v2 rollout on 2026-09-28 [q2] [measured]
- Checks run:
  - mix_shift (platform x country): flag, mix explains ~100% of the drop [check:mix_shift#1]
  - mix_shift (platform, coarser): flag, agrees with finer grain [check:mix_shift#2]
  - completeness: pass [check:completeness#1]
  - fanout: skipped, no joins were used
  - srm: skipped, not an experiment

## Caveats, and what would change the answer
- Before/after with no concurrent control; v1 and v2 never ran side by side, so ranker and week are confounded. A v1 holdout would settle it.
- If v2 caused the move to mobile (for example through app or UI changes shipped with it), the drop would partly be v2's; traffic source data by day would settle it.
- The intervals assume independent searches, so they are somewhat too narrow.
- Rollback threshold of 0.3 pp is the tool default, not a business number.

## Provenance
- Metric: CTR = sum(clicks)/sum(searches) over search_daily, all platforms and countries, from stated here [guess]
- Data: search_daily, release_log, through 2026-10-04
- Reconciled: not done (no dashboard or metrics.json available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (24 numbers on 10 lines; 3 queries, 3 checks, 0 given)