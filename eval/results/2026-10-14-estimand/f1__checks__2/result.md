## Answer
Headline: can't tell. The overall drop is -2.10 pp (-2.25 to -1.95), but almost none of it shows up inside platform and country segments.

Overall CTR fell from 30.42% to 28.32%. Nearly all of that is traffic shifting toward mobile, which has a much lower CTR. CTR within each segment didn't move.

- Observed: -2.10 pp (-2.25 to -1.95) [measured]
- Adjusted: -0.00 pp (-0.15 to +0.15), holding platform×country mix fixed [measured]
- Causal effect: not identified. v2 went to 100% of traffic with no concurrent v1 holdout. A before/after comparison can't separate v2 from the simultaneous mix shift. A 5–10% v1 holdout, or a randomized test, would identify it.

## What it means for the rollback decision
The segment-level effect of v2 is within ±0.15 pp of zero. The drop is about 2.1 pp, so the data doesn't support rolling back to recover it. A mix-held-fixed harm of 0.15 pp or more can't be excluded. I used 0.1 pp as the smallest change that matters; that's the check's default, not a threshold the team has set. Whether v2 itself caused the mobile shift is untested.

## Why we believe it
- Alternatives considered:
  - Segment mix shift: ruled in as the main driver. Mobile share of searches rose from 40% to 55%, with desktop CTR about 36% and mobile about 22%, and mix accounts for -2.09 of -2.10 pp [measured].
  - v2 lowering CTR within segments: mostly ruled out. The within-segment effect is -0.002 pp (-0.15 to +0.15), and each of the 4 segments moved less than 0.02 pp [measured].
  - v2 causing the mobile shift (for example through latency or UI changes): not ruled out. There's no data on it, and a coincident marketing or traffic-source change would look the same [guess].
  - Incomplete data in the later week: ruled out. Row counts are full for every day [measured].
- Checks run:
  - mix_shift: flag. Mix is 100% of the change, and the check says to report it [check:mix_shift#1].
  - completeness: pass. 2026-10-04 has 4 rows, 100% of the trailing median [check:completeness#1].
  - srm: skipped. This isn't a randomized experiment.
  - fanout: skipped. No joins were used.

## Caveats, and what would change the answer
- Both weeks are pre/post with no control. Other changes in the same week are possible, though release_log lists only the v2 rollout.
- The intervals treat searches as independent. Real intervals are probably wider because of clustering by user and day.
- Segments are only platform×country. Query-type or user-level mix could hide a v2 effect.
- A v1 holdout, or the cause of the mobile traffic shift, would change the answer.

## Provenance
- Metric: CTR = clicks / searches, summed over the week. This definition is stated here [guess]; no metrics.json was found.
- Data: search_daily and release_log, through 2026-10-04.
- Reconciled: not done (no dashboard or source figure provided).
- Queries and checks: the checks are logged in .ds-checks.log (mix_shift#1, completeness#1). The queries were run inline, so there's no query log.