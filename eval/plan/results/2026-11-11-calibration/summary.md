# Plan eval: 2026-11-11-calibration

Verdict: INSUFFICIENT_N (smoke test, not a decision). 1 tasks; the rule needs 10. Rule outcome at this n: FAIL.

## Per arm

| Metric | baseline | full |
|---|---|---|
| runs | 3 | 3 |
| plans_written | 3 | 3 |
| turn1_score | 1.0 | 1.0 |
| turn2_score | 1.0 | 1.0 |
| mean_words | 794 | 898 |
| contaminated | 0 | 0 |
| cost_usd | 0.41 | 0.47 |

## Per task (mean score: plan / after the objection)

| Task | baseline | full |
|---|---|---|
| p2 | 1.00 / 1.00 · words [871, 790, 720] | 1.00 / 1.00 · words [775, 939, 979] |

## Every run

| Run | Plan got | After the objection got | Words |
|---|---|---|---|
| p2 baseline #1 | estimates at the user level, 3P users by their own pre-test behavior, tenants only as a stratum or for clustering | estimates at the user level, 3P users by their own pre-test behavior, tenants only as a stratum or for clustering | 871 |
| p2 baseline #2 | estimates at the user level, 3P users by their own pre-test behavior, tenants only as a stratum or for clustering | estimates at the user level, 3P users by their own pre-test behavior, tenants only as a stratum or for clustering | 790 |
| p2 baseline #3 | estimates at the user level, 3P users by their own pre-test behavior, tenants only as a stratum or for clustering | estimates at the user level, 3P users by their own pre-test behavior, tenants only as a stratum or for clustering | 720 |
| p2 full #1 | estimates at the user level, 3P users by their own pre-test behavior, tenants only as a stratum or for clustering | estimates at the user level, 3P users by their own pre-test behavior, tenants only as a stratum or for clustering | 775 |
| p2 full #2 | estimates at the user level, 3P users by their own pre-test behavior, tenants only as a stratum or for clustering | estimates at the user level, 3P users by their own pre-test behavior, tenants only as a stratum or for clustering | 939 |
| p2 full #3 | estimates at the user level, 3P users by their own pre-test behavior, tenants only as a stratum or for clustering | estimates at the user level, 3P users by their own pre-test behavior, tenants only as a stratum or for clustering | 979 |
