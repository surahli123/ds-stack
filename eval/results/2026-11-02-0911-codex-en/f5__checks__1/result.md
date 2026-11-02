## Answer
Headline: can't tell [inferred]

Treatment’s recorded CTR was 31.20% versus control’s 30.00%, an observed increase of 1.20 percentage points [measured].
- Observed: +1.200 percentage points (nominal 95% interval: +1.125 to +1.275) [measured]
- Adjusted: +1.200 percentage points (nominal 95% interval: +1.125 to +1.275), holding calendar-day weights fixed at the average of the arms’ weights [measured]
- Causal effect: not identified (requires verified random assignment and resolution of the recorded sample imbalance) [inferred]

## What it means for the launch decision
The smallest decision-changing lift was not supplied; the nominal interval excludes zero and clears any threshold below +1.125 percentage points [measured]. However, unresolved sample imbalance means this interval cannot establish a causal benefit sufficient for launch [inferred].

## Why we believe it
- Alternatives considered:
  - Calendar-day mix: ruled out as a material explanation; adjustment leaves the lift unchanged at reported precision [measured].
  - Selection or logging imbalance: ruled in as unresolved; recorded user counts depart from the planned split every day [inferred].
- Checks run:
  - SRM: fail — recorded user shares are 51.23% control and 48.77% treatment; each daily test has p < 0.0000000001 (`srm#2–15`) [measured].
  - Completeness: pass — daily search-volume checks for both arms from September 20 through September 30 (`completeness#4–14`, `#18–28`) [measured].
  - Completeness: could not run — September 17–19 lack sufficient earlier baseline history [measured].
  - Mix shift: pass — calendar-day composition contributes approximately zero percentage points (`mix_shift#1`) [measured].
  - Integrity: pass — no duplicate date/arm records or invalid count relationships found [measured].
  - Fanout: skipped — no joins used [measured].

## Caveats, and what would change the answer
- Intervals assume independent searches and binary click outcomes; repeated users and multiple clicks could invalidate them. User-level data would support appropriate uncertainty estimates [inferred].
- Daily `users` may represent activity rather than assignments; pooled counts may repeat users. Assignment logs would distinguish broken allocation from differential activity or missing records [inferred].
- Load-volume checks cannot certify ingestion completeness; verified load records, a metric definition, and the launch threshold would strengthen the decision [inferred].

## Provenance
- Metric: CTR = summed clicks / summed searches; treatment minus control, in percentage points, stated here [guess]; no `metrics.json` available [measured].
- Data: `warehouse.db`, `experiment_daily`, September 17–30, 2026; volume checks pass through September 30, but the last fully loaded period is unverified [measured].
- Reconciled: not done (no independent dashboard or source supplied) [measured].
- Queries and checks: [queries](artifacts/queries.json), [analysis script](artifacts/analyze.py), [results](artifacts/results.json), and [check log](.ds-checks.log) [measured].
