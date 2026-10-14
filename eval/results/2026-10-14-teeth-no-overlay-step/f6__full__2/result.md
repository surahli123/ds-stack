## Answer
Headline: +46.05 % (95% CI 45.93 to 46.17) [q6]
Search CTR for 2026-10-05 to 2026-10-11 was 46.05%, defined as searches with a click divided by searches, external traffic only. [q6]
- Observed: +46.05 % (95% CI 45.93 to 46.17) [q6]
- Adjusted: not computed (no prior week in the table, so there is no change to decompose)
- Causal effect: not identified (this is a level, not a change; no intervention is being evaluated)

## What it means for the weekly business review
The number is a level with a ±0.12 pp interval [q6]. The definition matters far more than the noise: counting bot and internal traffic gives 41.41%, and counting clicks instead of searches with a click gives 64.47% [q5].

## Why we believe it
- Alternatives considered:
  - Bots and internal traffic included: ruled in as a definition risk. All-traffic CTR is 41.41% vs 46.05% external; bots click on only 1.97% of searches [q5] [measured]
  - Clicks per search instead of searches with a click: ruled in as a definition risk. It gives 64.47% for external traffic, and internal exceeds 100% [q5] [measured]
  - Incomplete week: ruled out by 7 of 7 days present with 6 rows each [q4, check:completeness#1] [measured]
  - Day-of-week or intra-week drift: ruled out as a concern for the weekly level; daily external CTR stays within 45.88 to 46.16% [q7] [measured]
- Checks run:
  - completeness: pass 2026-10-11 has 6 rows, 100% of the trailing median [check:completeness#1]
  - mix_shift: skipped, the table only holds this one week, so there is no comparison period
  - fanout: skipped, no joins were used
  - srm: skipped, not an experiment

## Caveats, and what would change the answer
- No metrics.json exists, so the definition is my choice. If the WBR uses all traffic, report 41.41%; if it uses clicks per search, 64.47% [q5]. Confirm with the metric owner.
- The table starts on 2026-10-05, so there is no week-over-week comparison. Another week of data would give one.
- The interval treats searches as independent. Repeat users make it somewhat optimistic.

## Provenance
- Metric: searches_with_click / searches, traffic_type = 'external', summed over the week, stated here [guess]
- Data: search_daily_v, through 2026-10-11
- Reconciled: not done (no dashboard or metrics.json available)
- Queries and checks: .ds-queries.log and .ds-checks.log
- Verified: verify_readout: pass (22 numbers on 9 lines; 4 queries, 1 checks, 0 given)