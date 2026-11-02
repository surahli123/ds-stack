## Answer
Headline: can't tell [inferred]
Treatment’s observed CTR was 31.20% versus 30.00%, a +1.20 percentage-point difference, but causal improvement is not established [measured; inferred].
- Observed: +1.200 percentage points (nominal 95% interval: +1.125 to +1.275) [measured]
- Adjusted: +1.200 percentage points (nominal 95% interval: +1.125 to +1.275), holding the date distribution fixed [measured]
- Causal effect: not identified (validated random assignment, complete outcome capture, and assignment-level data would identify it) [inferred]

## What it means for the launch decision
The smallest decision-changing improvement was not provided; if it is zero, the nominal observed interval clears it [inferred]. This does not establish a launch-worthy causal benefit because allocation balance and uncertainty at the randomization unit remain unverified [inferred].

## Why we believe it
- Alternatives considered:
  - Different date mix: ruled out as a material explanation by essentially unchanged date-adjusted lift [measured].
  - Selection or differential logging: ruled in as unresolved possibilities by treatment’s 48.77% share of recorded user-days despite the stated 50/50 split [inferred].
- Checks run:
  - Coverage: pass — all 14 dates have both arms [measured].
  - Duplicate rows and count validity: pass — no duplicate date/experiment/arm keys, null counts, negative counts, or clicks exceeding searches [measured].
  - Allocation balance: flag — treatment has 1,710 fewer recorded users every day; daily nominal 50/50 tests give p < 10⁻¹⁰, conditional on these being assignment counts [measured; inferred].
  - Assignment and clustered uncertainty: could not run — no assignment records or user-level outcomes [measured].

## Caveats, and what would change the answer
- Intervals assume independent binary outcomes per search; repeated users or multiple clicks can invalidate that assumption [inferred].
- Daily user counts cannot establish unique assignment totals; the imbalance could reflect activity after assignment [inferred].
- Assignment logs, ingestion reconciliation, the authoritative CTR definition, and a launch threshold would resolve the key uncertainties [inferred].

## Provenance
- Metric: total clicks / total searches, from stated here [guess].
- Data: `warehouse.db`, `experiment_daily`, September 17–30, 2026; last recorded date September 30, completeness unverified [measured].
- Reconciled: not done (no dashboard or independent source supplied) [measured].
- Queries and checks: [analysis.py](/private/tmp/ds-runs/3b13cb7ea6/analysis/analysis.py); outputs in [analysis_results.json](/private/tmp/ds-runs/3b13cb7ea6/analysis/analysis_results.json) [measured].
