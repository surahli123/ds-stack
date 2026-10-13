## Answer
Headline: about 0.0 pp (95% interval −0.15 to +0.15 pp) [measured]
Overall CTR fell 2.10 pp (30.42% to 28.32%) [measured]. Essentially all of that is a shift in traffic toward mobile, which has a lower CTR. Within-segment CTR didn't move (−0.002 pp), so nothing here points to v2 as the cause. [measured]

## What it means for the rollback decision
The interval rules out any v2 effect larger than about 0.15 pp within platform and country segments. The roughly 2.1 pp drop is almost entirely mix, so it isn't a reason to roll back. That holds only if the mix shift isn't itself caused by v2, which this data can't separate. [inferred]

## Why we believe it
- Alternatives considered:
  - Traffic mix shift (mobile share 40% → 55%): ruled in. It accounts for −2.09 pp of the −2.10 pp, or 99.9%. [measured]
  - v2 lowering CTR within segments: ruled out at the 0.15 pp level. Per-segment CTR changes are −0.02 to +0.01 pp, and all four segments are flat. [measured]
  - v2 causing the mobile shift (for example by changing platform routing or UX): not ruled out. There is no mechanism evidence in the data. [guess]
  - Other time effects such as seasonality or a concurrent change: not ruled out. v2 went to 100% of traffic with no holdout, so ranker is perfectly confounded with week. Only one release_log entry exists. [inferred]
- Checks run:
  - mix_shift: flag. Mix-dominant (100% mix share) [check:mix_shift#1].
  - completeness: pass. 2026-10-04 has 4 of 4 expected rows, 100% of the trailing median [check:completeness#1]. I ran it for the last day only. All 14 days have 4 rows each.
  - srm: skipped. This is not a randomized experiment.
  - fanout: skipped. There were no joins.

## Caveats, and what would change the answer
- The interval assumes independent searches, so it is likely somewhat too narrow, because searches cluster by user and day.
- The interval covers within-segment effects only. If v2 drove the mobile traffic increase, part of the mix effect would count as v2's.
- A holdout or a staggered rollout would settle causation. Finding out why mobile share rose would too.
- Only two weeks of data, with the segments limited to platform × country.

## Provenance
- Metric: CTR = clicks / searches, from the table's `clicks` and `searches` columns. There is no metrics.json, so this definition is stated here [guess].
- Data: search_daily and release_log, through 2026-10-04 (complete).
- Reconciled: not done (no dashboard or source figure provided).
- Queries and checks: the check outputs are logged in `.ds-checks.log` (mix_shift#1, completeness#1). The aggregation queries were run inline and not saved as separate query files.