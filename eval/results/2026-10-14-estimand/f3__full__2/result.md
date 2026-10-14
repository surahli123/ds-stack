Finished the analysis and the readout passed verification. Final readout:

## Answer
Headline: -1.82 pp (-1.97 to -1.67) [check:mix_shift#1]
Overall CTR fell from 30.44% to 28.61% week over week, and nearly all of it is a within-segment drop that coincided with the v3 rollout, if nothing else changed on 2026-09-07 [check:mix_shift#1].
- Observed: -1.83 pp (-1.98 to -1.68) [check:mix_shift#1]
- Adjusted: -1.82 pp (-1.97 to -1.67), holding platform x country mix fixed [check:mix_shift#1]
- Causal effect: not identified (v3 went to all traffic at once, so there is no concurrent control; a holdback or randomized comparison of the old and new ranker would identify it)

## What it means for the rollback decision
The whole interval is a loss of at least 1.67 pp, far above the 0.1 pp minimum effect the check uses [check:mix_shift#1]; the loss is concentrated on desktop (-3.0 pp, 36.04% to 33.04%) while mobile is flat (-0.04 pp) [check:mix_shift#2]. That pattern supports rolling back or fixing v3 on desktop, but it is timing-based evidence, not a randomized result.

## Why we believe it
- Alternatives considered:
  - Mix-shift (platform/country traffic mix): ruled out, mix is -0.01 pp of -1.83 pp (1%) at both grains [check:mix_shift#1, check:mix_shift#2] [measured]
  - Incomplete data / day of week: ruled out, 4 rows every day in both full 7-day Mon-Sun weeks [q6, check:completeness#1] [measured]
  - Seasonality: the daily CTR is stable around 30.5% for 7 days then steps down to about 28.6% on 09-07 with no drift [q3]; only 2 weeks of history, so longer seasonality is untested [inferred]
  - Other changes the same day: release_log lists only the v3 rollout [q2]; it may not record logging or desktop-specific changes [guess]
  - Requester's cause (v3): consistent, since the step lands exactly on the rollout day and the ranker label flips v2 to v3 [q3]; not proven causal [inferred]
- Checks run:
  - completeness: pass, 2026-09-13 has 4 rows = 100% of the trailing median [check:completeness#1]
  - mix_shift: pass, within-segment -1.82 pp, mix -0.01 pp [check:mix_shift#1]
  - mix_shift (coarser grain, platform): pass, agrees at -1.82 pp [check:mix_shift#2]
  - fanout: skipped, no joins were used
  - srm: skipped, not an experiment

## Caveats, and what would change the answer
- Before/after with no control: any desktop-only change on 2026-09-07 (tracking, UI, traffic source) would be counted as v3. Confirm with engineering, or hold back v3 for a slice of desktop.
- Intervals assume independent searches (the check notes this); user-level clustering would widen them.
- Only two weeks of data; a novelty or learning effect in v3 could change the long-run effect.
- CTR is a proxy; if v3 lowers clicks by removing low-value ones, user success might not fall. Check downstream metrics.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches) over search_daily, all platforms and countries, weekly, from stated here [guess]
- Data: search_daily, release_log, through 2026-09-13
- Reconciled: not done (no dashboard or metrics.json available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (33 numbers on 11 lines; 3 queries, 3 checks, 0 given)