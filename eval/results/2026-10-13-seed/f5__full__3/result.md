## Answer
Headline: can't tell
The arms are not comparable: treatment got 48.8% of users against a planned 50% [check:srm#1], so the raw CTR gap (0.3120 treatment vs 0.3000 control) [q4] can't be trusted as a lift.

## What it means for the launch decision
No smallest change that would alter the launch decision was given, so the raw gap can't be compared with a threshold. Until the cause of the user shortfall is found, a positive CTR lift can't be claimed or ruled out.

## Why we believe it
- Alternatives considered:
  - Real lift from the ranker: not ruled in; the raw CTR gap exists [q4] but the SRM failure means the arms differ in who is in them [check:srm#1] [measured]
  - Assignment or logging problem (e.g. treatment losing users, or a bucketing bug): ruled in as the likely cause; the shortfall is steady each day [check:srm#2] [inferred]
  - Incomplete data or missing days: ruled out, all 14 days present for both arms [check:completeness#1] [measured]
  - Day of week / seasonality: ruled out as a driver of the imbalance, the same split appears every day [q3] [inferred]
  - Mix-shift: skipped; no segment columns exist in the table [q1] [measured]
- Checks run:
  - srm: fail 51.2% control vs 48.8% treatment, p far below 0.001 [check:srm#1]
  - srm (single-day grain): fail same split on day level [check:srm#2]
  - completeness: pass 2026-09-30 has all expected rows [check:completeness#1]
  - mix_shift: skipped, no segment dimensions in experiment_daily [q1]
  - fanout: skipped, no joins used

## Caveats, and what would change the answer
- Only daily aggregates exist, so I can't test whether the missing treatment users differ (for example heavier or lighter searchers). Per-user assignment logs would settle that.
- Searches per user are equal in both arms [q4], so the imbalance isn't visible there; that doesn't show the missing users are random.
- No threshold for launch was provided; one is needed to read any interval later.
- Once the cause is fixed or the affected users are identified, rerun the lift with a two-proportion interval.

## Provenance
- Metric: CTR = sum(clicks) / sum(searches) per arm, from experiment_daily [guess]; no metrics.json available
- Data: experiment_daily (ranker_boost), through 2026-09-30
- Reconciled: not done (no dashboard or other source available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (8 numbers on 3 lines; 3 queries, 3 checks, 0 given)