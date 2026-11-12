## Answer
Headline: can't tell [inferred]

Recorded treatment CTR was 31.20% versus 30.00% for control, a +1.20 percentage-point difference [measured].
- Observed: +1.200 percentage points (nominal 95% interval: +1.125 to +1.275) [measured]
- Adjusted: +1.200 percentage points (nominal 95% interval: +1.125 to +1.275), holding calendar-date mix fixed [measured]
- Causal effect: not identified (assignment records and an explanation of the recorded user imbalance would establish whether the randomized comparison remains valid) [inferred]

## What it means for the launch decision
The smallest decision-changing lift was not supplied; the nominal interval exceeds zero and thresholds below +1.125 percentage points [measured]. It does not establish a causal launch benefit until the imbalance and uncertainty assumptions are resolved [inferred].

## Why we believe it
- Alternatives considered:
  - Calendar-date composition explains the lift: ruled out by date adjustment leaving the difference essentially unchanged [measured].
  - Selection or differential logging explains the lift: ruled in as unresolved possibilities by treatment’s consistently lower recorded user counts; neither explanation is established [inferred].
- Checks run:
  - Calendar coverage: pass — all 14 dates contain both arms [measured].
  - Duplicate keys and count validity: pass — no duplicates, nulls, negative counts, or clicks exceeding searches [measured].
  - Recorded allocation balance: flag — treatment represents 48.773% of recorded user-days, with 1,710 fewer users every day [measured].
  - Daily consistency: pass — daily CTR differences range from +1.188 to +1.212 percentage points [measured].
  - Randomized assignment and user-clustered uncertainty: could not run — only daily aggregates are available [measured].

## Caveats, and what would change the answer
- Both intervals assume independent binary search outcomes [guess]; repeated searches per user can invalidate their coverage [inferred].
- Recorded daily users may differ from assigned users; the imbalance flags a problem but does not prove randomization failed [inferred].
- Assignment/exposure logs, user-level outcomes, a validated metric definition, and the launch threshold would permit a stronger decision [inferred].

## Provenance
- Metric: total clicks / total searches, from stated here [guess]; no `metrics.json` supplied [measured].
- Data: `experiment_daily`, filtered to `ranker_boost`, 2026-09-17 through 2026-09-30; all dates present, ingestion completeness unverified [measured].
- Reconciled: not done (no dashboard or independent source supplied) [measured].
- Queries and checks: [queries.sql](/private/tmp/ds-runs/e91c732c5e/analysis/queries.sql), [analysis.py](/private/tmp/ds-runs/e91c732c5e/analysis/analysis.py), [results.json](/private/tmp/ds-runs/e91c732c5e/analysis/results.json) [measured].
