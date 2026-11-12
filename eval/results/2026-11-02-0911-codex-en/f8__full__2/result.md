## Answer
Headline: +36.97% (95% interval: 36.68%–37.26%) [q8, q9] [measured; interval inferred]

Shopping queries recorded 39,857 clicks across 107,810 searches in 2026-W41. [q8] [measured]

- Observed: +36.97% (95% interval: 36.68%–37.26%) [q8, q9] [measured; interval inferred]
- Adjusted: not computed (a single weekly rate was requested). [inferred]
- Causal effect: not identified (would require a specified intervention and a randomized or credible comparison design). [inferred]

## What it means for Merchandising’s citation
Cite the recorded shopping CTR as 36.97%, conditional on confirming the extract is complete. [q8] [measured; recommendation inferred] No smallest decision-changing difference was supplied, so the interval’s practical precision cannot be assessed. [inferred]

## Why we believe it
- Alternatives considered:
  - Duplicate category mappings: ruled in; a direct join inflates CTR to 40.90%, while deduplication and membership filtering both give 36.97%. [q5, q6, q7, q8] [measured]
  - Conflicting categories or missing verticals: ruled out by zero category conflicts and complete mapping coverage. [q5, q6] [measured]
  - Incomplete loading or logging changes: ruled in as unresolved possibilities; historical data and load certification are unavailable. [q1, q2] [inferred]
  - Mix-shift, seasonality and weekday effects: ruled out as explanations requiring testing for this descriptive request; their influence on the rate itself remains untested. [inferred]
- Checks run:
  - fanout: fail — “join added 250 rows (fan-out)”; rejected direct join replaced with membership filtering. [check:fanout#2] [measured]
  - fanout: pass — “row counts consistent with a many_to_one left join” after deduplication. [check:fanout#1] [measured]
  - completeness: could not run — “could not run: need at least 3 earlier periods (trailing days (under 3 weeks of same-weekday history)) before 2026-W41, got 0”. [check:completeness#1] [measured]
  - Metric validity: pass — unique query-week records; no missing, negative, or above-search click counts. [q2] [measured]
  - mix_shift and srm: skipped — no rate comparison or experiment. [inferred]

## Caveats, and what would change the answer
- The Wilson interval assumes independent searches with binary click outcomes; repeated users or multiple clicks per search require a different uncertainty model. [inferred]
- Missing data are not covered by the interval; load certification would establish full-week coverage. [inferred]
- Confirm clicks/searches as the intended definition before publication. [guess]

## Provenance
- Metric: total clicks / total searches × 100 for 2026-W41 shopping queries, counting each query-week once using category membership; stated here [guess]. No metrics.json is configured.
- Data: query_week, query_category, category_vertical; latest recorded period 2026-W41, last complete period unverified. [q1, q2] [measured]
- Reconciled: not done (no independent dashboard or source supplied); deduplicated joins and membership filtering agree. [q6, q8] [measured]
- Queries and checks: `.ds-queries.log`, `.ds-checks.log`; saved readout: `readout.md`. [measured]
- Verified: verify_readout: pass (17 numbers on 7 lines; 7 queries, 3 checks, 0 given)
