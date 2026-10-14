## Answer
Headline: 55.0 % (54.6 to 55.4) [q5]
In 2026-W40, navigational queries (current labels) got 32,878 clicks on 59,800 searches, a click-through rate of 55.0% [q5]. The interval is a binomial approximation that ignores clustering by query.
- Observed: 55.0 % (54.6 to 55.4) [q5]
- Adjusted: not computed (single level, no comparison)
- Causal effect: not identified (no comparison or intervention asked)

## What it means for the planning doc
Quote about 55% for navigational CTR in W40. Informational queries are far lower at 25.0% [q5], so do not use the blended rate of 37.0% [q1]. Using an unfiltered join with the labels table would give 45.0% [q6], which is wrong.

## Why we believe it
- Alternatives considered:
  - Duplicate label rows inflating the number: ruled in as a hazard, handled by filtering is_current=1, which gives 1000 labels for 1000 queries [q3]; the unfiltered join gives 45.0% [q6] [measured]
  - Label version mix (v1 vs v2): ruled out, since navigational CTR is 55.0% under v1 and 55.0% under v2 [q4] [measured]
  - Bad rows (clicks above searches, zero searches): ruled out [q7] [measured]
- Checks run:
  - fanout: pass, the is_current=1 join is many_to_one with 1000 rows in and out [check:fanout#2]
  - completeness: could not run, only one week is in the table [check:completeness#2]
  - mix_shift: skipped, there is no comparison period
  - srm: skipped, there is no experiment

## Caveats, and what would change the answer
- Only W40 is in query_stats, so completeness is unverified and there is no trend.
- Labels are current labels as of now (is_current=1); the labels at the time of W40 may have differed. Superseded v1 rows were excluded.
- CTR is clicks divided by searches, summed over queries (a pooled rate). The mean of per-query CTRs would differ.

## Provenance
- Metric: CTR = sum(clicks)/sum(searches) for queries with intent='navigational' and is_current=1, week 2026-W40 [guess]; no metrics.json (DS_OVERLAY_DIR unset)
- Data: query_stats, query_labels, through 2026-W40 (completeness could not be verified)
- Reconciled: not done (no dashboard available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (21 numbers on 7 lines; 6 queries, 2 checks, 0 given)