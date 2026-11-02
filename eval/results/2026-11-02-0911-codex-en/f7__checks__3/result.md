## Answer
Headline: can't tell

Recorded conversions were 8.30% of searches that week [measured], but whether these represent searches leading to purchases is unverified [inferred].

- Observed: +8.30% (95% interval: 8.24%–8.36%); ratio [measured], conditional Wilson interval [inferred].
- Adjusted: not computed (no segment or adjustment variables available) [measured].
- Causal effect: not identified (would require a randomized intervention or credible causal design) [inferred].

## What it means for Finance’s quarterly model
Use 8.30% only as a provisional conversion-to-search ratio [inferred]. Finance’s smallest decision-changing difference was not supplied, so the interval cannot be compared with that threshold; it also excludes uncertainty about purchase attribution [inferred].

## Why we believe it
- Alternatives considered:
  - Click-based denominator: ruled out by the requested search-based metric [inferred].
  - Conversions count purchase events rather than distinct purchasing searches: ruled in as unresolved because no attribution definition exists here [inferred].
- Checks run:
  - Completeness: could not run for October 5–7 because prior history was insufficient [measured].
  - Completeness: pass for October 8–11 using daily search volume and trailing-day baselines; this does not certify loading completeness [measured/inferred].
  - Date coverage and uniqueness: pass; every requested date appears once [measured].
  - Count integrity: pass; nonnegative conversions ≤ clicks ≤ searches throughout [measured].
  - Fanout, mix shift, SRM: skipped; no joins, period comparison, or experiment analyzed [measured].

## Caveats, and what would change the answer
- The interval assumes independent searches and one binary conversion outcome per search; neither is verified [inferred].
- Confirming purchase semantics, deduplication, attribution window, timezone, and completed loading would establish whether this proxy answers Finance’s question [inferred].

## Provenance
- Metric: summed conversions ÷ summed searches × 100 [measured]; interpretation as purchase share stated here [guess], with no `metrics.json` available.
- Data: `warehouse.db`, `search_daily_c`; available through October 11, 2026 [measured]; last complete period unverified [inferred].
- Reconciled: not done (no independent dashboard or source supplied) [measured].
- Queries and checks: [queries](analysis_output/queries.json), [calculation and validation](analysis_output/analyze.py), [results](analysis_output/results.json), [check log](.ds-checks.log).
