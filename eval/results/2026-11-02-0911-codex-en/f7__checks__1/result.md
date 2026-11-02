## Answer

Headline: can't tell [inferred]

Recorded conversions were 8.30% of searches during October 5–11, but their equivalence to purchases is unverified [measured; inferred limitation].

- Observed: +8.30% (95% interval: 8.24%–8.36%), conversion-to-search ratio [measured; interval inferred].
- Adjusted: not computed (no segment or user-level data) [measured].
- Causal effect: not identified (attributed purchases establish conversion; a randomized comparison would identify incremental impact) [inferred].

## What it means for the quarterly model

Use 8.30% only provisionally, conditional on conversions representing distinct searches with a purchase [inferred]. Finance’s smallest decision-changing difference was not supplied, so the interval cannot be assessed against that threshold [inferred].

## Why we believe it

- Alternatives considered:
  - Conversion-to-search ratio: ruled in by 70,030 conversions divided by 843,738 searches [measured].
  - Verified purchase share: ruled out as an established interpretation because purchase definitions and attribution records are absent [inferred].
- Checks run:
  - Completeness: could not run for October 5–7 because earlier history was insufficient [measured].
  - Completeness: pass for October 8–11 using search volume and trailing-day baselines; this does not certify loading or conversion maturity [measured; inferred limitation].
  - Date coverage, uniqueness, and count validity: pass [measured].
  - Fanout, mix shift, and SRM: skipped; no joins, period comparison, or experiment [measured].

## Caveats, and what would change the answer

- The interval assumes independent searches and one conversion per converted search; repeated users and multiple purchases cannot be assessed [inferred].
- The interval excludes attribution errors and missing data; the recorded ratio itself is exact for these aggregates [inferred].
- A purchase definition, attribution window, deduplication rules, and load confirmation would establish whether this is the requested share [inferred].

## Provenance

- Metric: total conversions / total searches for October 5–11 inclusive [measured]; treating conversions as distinct searches leading to purchases is stated here [guess]. No metrics.json was present [measured].
- Data: `warehouse.db`, `search_daily_c`, through October 11; last complete period unverified [measured].
- Reconciled: not done (no dashboard or independent source supplied) [measured].
- Queries and checks: [queries](analysis_output/queries.json), [results](analysis_output/results.json), [reproducible script](analysis_output/analyze.py), [.ds-checks.log](.ds-checks.log) [measured].
