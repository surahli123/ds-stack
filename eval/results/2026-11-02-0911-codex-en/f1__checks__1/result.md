## Answer

Headline: can't tell [inferred]

Overall CTR fell from 30.421% to 28.324%, a 2.097 percentage-point drop almost entirely accounted for arithmetically by traffic mix. [measured]

- Observed: −2.097 percentage points (95% interval: −2.248 to −1.946). [measured]
- Adjusted: −0.002 percentage points (95% interval: −0.153 to +0.148), holding platform × country shares fixed at the average of the two weeks’ shares. [measured]
- Causal effect: not identified; a concurrent randomized v1/v2 comparison would identify it, because ranker version and week are completely confounded here. [inferred]

## What it means for rollback

The smallest loss that would trigger rollback was not supplied; the adjusted interval includes losses up to 0.153 percentage points, but it is not a causal interval. [measured/inferred] These data do not establish that rollback would recover the observed loss; use a randomized comparison against your decision threshold. [inferred]

## Why we believe it

- Alternatives considered:
  - Traffic composition: ruled in by a −2.095 percentage-point mix component, reflecting increased weight on lower-CTR mobile traffic. [measured]
  - A large decline within platform/country segments: ruled out descriptively by the near-zero adjusted change and its interval, subject to the assumptions below. [inferred]
  - Other time effects or v2-induced changes in search frequency: ruled in as unresolved possibilities; no concurrent control distinguishes them. [inferred]
- Checks run:
  - `mix_shift`: flag — traffic mix dominates the observed decline. [measured]
  - `completeness`: pass for September 24–October 4; could not run for September 21–23 because earlier history is insufficient. [measured]
  - Count validity and duplicate keys: pass — no invalid counts or duplicate date/platform/country/ranker keys found. [measured]
  - `fanout`: skipped — no joins used. [measured]
  - `srm`: skipped — no randomized assignment or planned split available. [measured]

## Caveats, and what would change the answer

- Intervals assume independent binary click outcomes per search and fixed adjustment weights; repeated users, correlated searches, or multiple clicks per search could invalidate them. [inferred]
- Adjusting for traffic mix does not establish causality and could remove part of v2’s effect if v2 changed search frequency. [inferred]
- Row-count completeness checks cannot verify fully loaded underlying events; ingestion metadata and a metric contract would strengthen validation. [inferred]
- A randomized holdout with user-level outcomes and a specified rollback threshold would make the decision identifiable. [inferred]

## Provenance

- Metric: `SUM(clicks) / SUM(searches)`, comparing September 21–27 with September 28–October 4; stated here [guess], because no `metrics.json` was provided.
- Data: `search_daily`, `release_log`, through October 4, 2026; latest date passes row-count completeness, but source completeness is unverified. [measured/inferred]
- Reconciled: not done — no dashboard or independent source supplied. [measured]
- Queries and checks: [queries](analysis_output/queries.json), [check results](analysis_output/checks.json), [reproducible script](analysis_output/analyze.py), and `.ds-checks.log`. [measured]
