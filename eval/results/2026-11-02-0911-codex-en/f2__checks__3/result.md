## Answer
Headline: +54.98% (95% interval: 54.58%–55.38%) [measured]
Navigational queries recorded 32,878 clicks across 59,800 searches in 2026-W40, using current intent labels. [measured]
- Observed: +54.98% (95% interval: 54.58%–55.38%) [measured]
- Adjusted: not computed (requested a descriptive rate). [inferred]
- Causal effect: not identified (would require a defined intervention and credible comparison design). [inferred]

## What it means for the planning doc
Use 54.98% as the observed planning baseline, subject to unverified load completeness. [inferred] No smallest decision-changing difference was supplied, so whether the interval is sufficiently narrow cannot be assessed. [inferred]

## Why we believe it
- Alternatives considered:
  - Joining historical labels: ruled out because historical versions duplicate query IDs; current labels provide unique matches. [measured]
- Checks run:
  - fanout: pass; all 1,000 source rows matched exactly one current label. [measured]
  - completeness: could not run; no earlier periods available for comparison. [measured]
  - Count validity: pass; no missing, negative, or clicks-above-searches counts. [measured]
  - mix_shift and srm: skipped; no period comparison or experiment requested. [inferred]

## Caveats, and what would change the answer
- The Wilson interval assumes independent searches and that clicks count searches with a click; repeat clicks or correlated searches would require different uncertainty estimates. [guess]
- Current labels may differ from labels effective during W40; historical classification rules or incomplete loading could change the answer. [inferred]

## Provenance
- Metric: total clicks divided by total searches for `intent='navigational'` and `is_current=1`, expressed in percent; stated here [guess], because no metrics.json was provided.
- Data: `warehouse.db`: `query_stats`, `query_labels`; available through 2026-W40, last complete period unverified. [measured]
- Reconciled: not done (no dashboard or independent source supplied). [inferred]
- Queries and checks: `analysis_output/queries.json`, `analysis_output/calculate.py`, `analysis_output/result.json`, and `.ds-checks.log`. [measured]
