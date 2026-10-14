## Answer
Headline: can't tell
Treatment CTR is higher than control in the raw data, but the arms are not comparable because the user split is not 50/50, so the lift can't be trusted for launch. [check:srm#1]
- Observed: +1.20 pp (+1.13 to +1.27 pp) CTR, treatment 31.2% vs control 30.0% [q4]
- Adjusted: not computed (only daily arm-level totals exist; no segments to hold fixed, so mix_shift can't be run)
- Causal effect: not identified (needs a randomization that passes SRM, or the cause of the 51.2/48.8 split found and removed) [check:srm#1]

## What it means for the ranker_boost launch decision
The raw interval of +1.13 to +1.27 pp [q4] would clear any plausible launch threshold if the arms were comparable, but the user counts are 499,930 vs 475,990 [q2] with SRM p≈1e-129 [check:srm#1], so the interval measures an unknown selection mix, not the ranker. No launch threshold was given, so none is compared.

## Why we believe it
- Alternatives considered:
  - Real ranker effect (the requester's cause): not ruled in; the SRM failure means assignment or logging differs between arms [check:srm#1] [inferred]
  - Differential loss or filtering of treatment users (e.g. logging, bot filtering, or assignment bug): ruled in as the likely reason for the shortfall of treatment users, cause not identified [q2, check:srm#1] [inferred]
  - Incomplete data or missing days: ruled out, all 14 days present for both arms [check:completeness#1, q3] [measured]
  - Day-of-week or seasonality: ruled out as a driver of the gap, daily user and CTR gap is stable across both arms over the same 14 days [q3] [measured]
  - Mix-shift across segments: not testable, no segment columns [q1] [measured]
- Checks run:
  - srm: fail, chi2 587.26, observed share 0.512265 vs 0.487735, p 9.86e-130 [check:srm#1]
  - completeness: pass, 2026-09-30 has 2 rows, 100% of trailing median [check:completeness#1]
  - mix_shift: skipped, no segment dimension in experiment_daily [q1]
  - fanout: skipped, no joins performed

## Caveats, and what would change the answer
- The SRM cause must be found (assignment service, exposure logging, filters on treatment). If it is shown to be random-neutral (e.g. a logging drop uncorrelated with clicks), the +1.2 pp could be reinstated.
- Data are daily arm totals, so intervals treat searches as independent; user-level clustering would widen them.
- A per-user or per-segment table would allow mix and within-segment analysis.

## Provenance
- Metric: CTR = sum(clicks)/sum(searches) per arm, experiment_daily, 2026-09-17 to 2026-09-30, stated here [guess]
- Data: experiment_daily, through 2026-09-30
- Reconciled: not done (no dashboard or metrics.json available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (24 numbers on 8 lines; 4 queries, 2 checks, 0 given)