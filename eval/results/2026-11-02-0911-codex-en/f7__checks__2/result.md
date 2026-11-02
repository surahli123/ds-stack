## Answer
Headline: can't tell  
Recorded conversions were 8.30% of searches, but whether these represent searches leading to a purchase is unverified. [measured; inferred]
- Observed: +8.30% (95% interval: 8.24%–8.36%), conversion/search proxy. [measured; interval inferred]
- Adjusted: not computed (no segment data or adjustment target). [measured]
- Causal effect: not identified (would require a defined intervention and randomized or credible quasi-experimental comparison). [inferred]

## What it means for Finance’s quarterly model
Finance’s smallest decision-changing difference was not supplied, so the interval cannot be assessed against that threshold. [measured] Use this proxy only after confirming the purchase definition and attribution window; the interval excludes those uncertainties. [inferred]

## Why we believe it
- Alternatives considered:
  - Conversion/search ratio: ruled in by 70,030 conversions divided by 843,738 searches. [measured]
  - Verified purchase share: ruled out as an established interpretation because purchase attribution and conversion definitions are absent. [inferred]
- Checks run:
  - Date coverage and count validity: pass; every requested day appears once, with nonmissing, nonnegative counts and conversions no greater than searches. [measured]
  - Completeness, October 5–7: could not run; insufficient preceding history. [measured]
  - Completeness, October 8–11: pass using search volume and trailing-day baselines; full loading remains unconfirmed. [measured; inferred]
  - Fanout, mix_shift, srm: skipped; no joins, rate comparison, or experiment. [measured]

## Caveats, and what would change the answer
- The Wilson interval assumes independent searches with a binary conversion outcome; aggregate data cannot verify this. [inferred]
- A purchase definition, search-level attribution, and confirmed loading would establish whether the proxy answers Finance’s question. [inferred]

## Provenance
- Metric: summed conversions / summed searches; interpreting conversions as searches resulting in purchases is stated here [guess]; no metrics.json supplied. [measured]
- Data: warehouse.db, search_daily_c, covering October 5–11, 2026; last complete period unverified. [measured]
- Reconciled: not done (no dashboard or independent source supplied). [measured]
- Queries and checks: analysis_output/queries.jsonl, analysis_output/analyze.py, analysis_output/results.json, and .ds-checks.log. [measured]
