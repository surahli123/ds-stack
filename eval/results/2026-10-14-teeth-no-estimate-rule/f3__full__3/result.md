Readout is written and verified, so here it is.

```
## Answer
Headline: can't tell
Overall CTR fell 1.83 pp week over week (95% CI -1.98 to -1.68) [check:mix_shift#1], but all of the drop is on desktop (-1.80 pp of it) while mobile is flat (-0.02 pp) [check:mix_shift#2]; because v3 went to 100% of traffic at once with no holdout, the share due to v3 versus something else that changed on desktop that week cannot be separated from this data [q4, q2].

## What it means for the rollback decision
The observed drop is far outside noise (CI -1.98 to -1.68 pp, noise floor 0.15 pp) [check:mix_shift#1], so any plausible rollback threshold is exceeded by the raw change, but that change is a before/after comparison, not a v3 effect; I would not call the rollback from this alone. No rollback threshold was given in the request.

## Why we believe it
- Alternatives considered:
  - Mix-shift (platform x country): ruled out; mix explains -0.01 pp of -1.83 pp (1%), same at platform grain [check:mix_shift#1, check:mix_shift#2] [measured]
  - Data completeness: ruled out for the weeks; each week has 7 days x 4 segment rows and the weeks have near-equal search volume (699,485 vs 699,266) [q3, q4] [measured]
  - Seasonality / day of week: ruled out as a driver; both windows are Mon-Sun, and every day of week 2 (0.2831-0.2885) sits below every day of week 1 (0.3006-0.3075) [q3] [measured]
  - Logging or definition change: not ruled out; release_log lists only the v3 rollout, so desktop-only tracking changes would not appear there [q2] [inferred]
  - Requester's cause (v3 caused the drop): ruled in as possible, not confirmed; v3 start coincides exactly with the drop, but the ranker is perfectly confounded with week (v2 only in week 1, v3 only in week 2) [q4] [measured]. Mobile also moved to v3 yet CTR was flat there, so v3 would have to hurt desktop only [q6] [inferred]
- Checks run:
  - completeness: could not run; only 1 earlier period available, 2 weeks total [check:completeness#1]
  - mix_shift (platform x country): pass; within-segment -1.82 pp, mix -0.01 pp [check:mix_shift#1]
  - mix_shift (platform): pass; same split, desktop -1.80 pp, mobile -0.02 pp [check:mix_shift#2]
  - fanout: skipped; no joins were used
  - srm: skipped; not a randomized experiment

## Caveats, and what would change the answer
- No holdout or staggered rollout: a v3 holdout (or v2 vs v3 on desktop in the same days) would identify the effect.
- Check whether anything else changed on desktop the week of 2026-09-07 (client release, tracking, UI, traffic source); a desktop-only cause would clear v3.
- Interval assumes independent searches (se_assumes_independent_units); the real interval is somewhat wider. Only two weeks, so no baseline week-to-week variability was estimated.
- Clicks and searches counted as logged in search_daily; bot or dedup filtering unknown.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches) from search_daily, all platforms and countries, weekly; stated here [guess] (no metrics.json; DS_OVERLAY_DIR unset)
- Data: search_daily, release_log, through 2026-09-13
- Reconciled: not done (no dashboard or source figure available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (30 numbers on 9 lines; 4 queries, 3 checks, 0 given)
```