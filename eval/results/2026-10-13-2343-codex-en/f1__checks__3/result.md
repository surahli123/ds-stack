## Answer

Headline: can't tell [inferred]

Overall CTR fell from 30.421% to 28.324%, a decline of 2.097 percentage points, but the amount attributable to v2 is unidentified. [measured; inferred attribution limit]

- Observed: −2.097 percentage points (95% interval: −2.248 to −1.946). [measured]
- Adjusted: −0.002 percentage points (95% interval: −0.153 to +0.148), holding platform × country shares fixed at their average across both weeks. [measured]
- Causal effect: not identified; a randomized concurrent v1 holdout would identify it. Version and week are completely confounded here. [inferred]

## What it means for rollback

The rollback threshold was not supplied; the adjusted interval includes losses up to 0.153 percentage points, but it cannot bound v2’s causal harm. [measured; inferred limitation] These data alone justify neither attributing the drop to v2 nor concluding that v2 is harmless. [inferred]

## Why we believe it

- Alternatives considered:
  - Traffic composition: ruled in as an arithmetic explanation; mobile’s search share rose from 40.108% to 55.072%, and the platform-country mix component is −2.095 percentage points. [measured]
  - A large decline within platform-country groups: ruled out descriptively under the stated interval assumptions; the adjusted interval spans zero. [inferred]
  - Other time changes, or v2 itself changing search composition: ruled in as unresolved possibilities; there is no concurrent control. [inferred]
- Checks run:
  - completeness#1 and #2: pass — both week endpoints have expected row counts; limited history required trailing-day baselines. [measured]
  - mix_shift#1: flag — composition accounts for almost all the aggregate decline. [measured]
  - Grid/count integrity: pass — all expected daily segments present, unique keys, valid counts. [measured]
  - fanout: skipped — no joins.
  - srm: skipped — no randomized assignment data.

## Caveats, and what would change the answer

- Intervals assume independent searches and binary click outcomes; repeated users or multiple clicks per search could invalidate them. [inferred]
- Adjusting search composition could remove part of v2’s effect if v2 changed that composition. [inferred]
- Row completeness does not establish ingestion completeness without a load watermark. [inferred]
- A randomized holdout, verified metric definition, and explicit rollback threshold would make the decision assessable. [inferred]

## Provenance

- Metric: `SUM(clicks) / SUM(searches)`, from stated here [guess]; no `metrics.json` supplied.
- Data: `search_daily`, `release_log`; compared September 21–27 with September 28–October 4, 2026; structurally complete through October 4, ingestion completeness unverified. [measured]
- Reconciled: not done (no dashboard or independent source supplied).
- Queries and checks: [queries](analysis_output/queries.json), [check results and assumptions](analysis_output/results.json), [reproducible analysis](analysis_output/analyze.py), and [check log](.ds-checks.log).
