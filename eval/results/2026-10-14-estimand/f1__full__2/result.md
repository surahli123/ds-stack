## Answer
Headline: -0.00 pp (-0.15 to +0.15) [check:mix_shift#1]
Overall CTR fell 2.10 pp, but essentially all of it is a shift of traffic toward lower-CTR mobile; within platform, CTR did not move, if v2 did not itself change the platform mix [check:mix_shift#1].
- Observed: -2.10 pp (-2.25 to -1.95) [check:mix_shift#1]
- Adjusted: -0.00 pp (-0.15 to +0.15), holding platform mix fixed [check:mix_shift#1]
- Causal effect: not identified (the new ranker went to all traffic at once with no holdout; a randomized split or a holdout would identify it)

## What it means for the rollback decision
The within-platform interval of -0.15 to +0.15 pp [check:mix_shift#1] excludes any drop near the observed 2.10 pp [check:mix_shift#1], so the drop is not evidence v2 hurts CTR; I'd treat 0.1 pp as the smallest meaningful change [check:mix_shift#1], and the interval is slightly wider than that, so a small effect can't be excluded. Mobile share rose from 40.1% to 55.1% of searches [check:mix_shift#1].

## Why we believe it
- Alternatives considered:
  - Mix-shift (mobile share up): ruled in by mix share 99.8%, mobile CTR 22.0% vs desktop 36.0% [check:mix_shift#1] [measured]
  - v2 lowered CTR (PM's cause): not supported; within-platform change -0.00 pp, but not identified causally without a holdout [check:mix_shift#1] [measured]
  - Finer grain (country x platform) disagrees: ruled out, same result, within-segment -0.00 pp, mix -2.09 pp [check:mix_shift#2] [measured]
  - Data completeness (partial last day): ruled out, 2026-10-04 at 102% of median rows [check:completeness#2] [measured]
  - Day of week/seasonality: both windows are full Mon-Sun weeks; daily CTR is flat within each week and steps on 09-28 [q3] [inferred]
  - Cause of the mobile surge: unknown; it coincided with the rollout, and v2 or an unrelated traffic change could be behind it [q2, q4] [guess]
- Checks run:
  - completeness: pass 2026-10-04 has 101900 rows [check:completeness#2]
  - mix_shift (platform): flag mix explains the move [check:mix_shift#1]
  - mix_shift (country x platform): flag same conclusion [check:mix_shift#2]
  - fanout: skipped, no joins
  - srm: skipped, not a randomized experiment

## Caveats, and what would change the answer
- If v2 itself pushed users to mobile (e.g. a mobile UI change shipped with it), v2 would be indirectly responsible for the overall drop; check the release notes and the traffic source of the mobile increase.
- Intervals assume independent searches (se_assumes_independent_units), so they are likely somewhat narrow.
- One week before/after only; no holdout, so the causal effect is unidentified.

## Provenance
- Metric: CTR = sum(clicks)/sum(searches), search_daily, all platforms and countries, weekly, stated here [guess]
- Data: search_daily, release_log, through 2026-10-04
- Reconciled: not done (no dashboard or metrics.json available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (26 numbers on 11 lines; 3 queries, 3 checks, 0 given)