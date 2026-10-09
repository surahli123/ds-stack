# Writing eval: 2026-10-09-smoke

**Verdict:** INSUFFICIENT_N (smoke test, not a decision). 3 tasks; the rule needs 10. Rule outcome at this n: FAIL.

## Per arm

| Metric | baseline | full |
|---|---|---|
| runs | 9 | 9 |
| docs_written | 9 | 9 |
| skim_score | 0.963 | 0.889 |
| full_score | 0.889 | 0.944 |
| docs_with_no_lint_fail | 2 | 9 |
| mean_lint_fails | 0.78 | 0.0 |
| mean_words | 423 | 356 |
| contaminated | 0 | 0 |
| cost_usd | 0.49 | 0.72 |

## Per task (mean reader score: skim / full)

| Task | baseline | full |
|---|---|---|
| w1 | 1.00 / 1.00 · words [403, 504, 411] | 1.00 / 1.00 · words [352, 374, 309] |
| w2 | 1.00 / 0.92 · words [497, 554, 492] | 1.00 / 1.00 · words [551, 498, 466] |
| w3 | 0.89 / 0.75 · words [282, 339, 325] | 0.67 / 0.83 · words [221, 217, 217] |

## Every run

| Run | Skim got | Full got | Lint | Words |
|---|---|---|---|---|
| w1 baseline #1 | the drop is mix, not v2, don't roll back, -2.1 pp | the drop is mix, not v2, don't roll back, -2.1 pp, no holdout, before/after only | D2 D3 | 403 |
| w1 baseline #2 | the drop is mix, not v2, don't roll back, -2.1 pp | the drop is mix, not v2, don't roll back, -2.1 pp, no holdout, before/after only | D2 D3 | 504 |
| w1 baseline #3 | the drop is mix, not v2, don't roll back, -2.1 pp | the drop is mix, not v2, don't roll back, -2.1 pp, no holdout, before/after only | D2 D3 | 411 |
| w1 full #1 | the drop is mix, not v2, don't roll back, -2.1 pp | the drop is mix, not v2, don't roll back, -2.1 pp, no holdout, before/after only | - | 352 |
| w1 full #2 | the drop is mix, not v2, don't roll back, -2.1 pp | the drop is mix, not v2, don't roll back, -2.1 pp, no holdout, before/after only | D13 | 374 |
| w1 full #3 | the drop is mix, not v2, don't roll back, -2.1 pp | the drop is mix, not v2, don't roll back, -2.1 pp, no holdout, before/after only | - | 309 |
| w2 baseline #1 | recommend the hybrid (option C), approve the budget by Oct 20, about $18k per quarter | recommend the hybrid (option C), approve the budget by Oct 20, about $18k per quarter, judge drift | D13 D2 D3 | 497 |
| w2 baseline #2 | recommend the hybrid (option C), approve the budget by Oct 20, about $18k per quarter | recommend the hybrid (option C), about $18k per quarter, judge drift | D13 D2 D3 | 554 |
| w2 baseline #3 | recommend the hybrid (option C), approve the budget by Oct 20, about $18k per quarter | recommend the hybrid (option C), approve the budget by Oct 20, about $18k per quarter, judge drift | D2 | 492 |
| w2 full #1 | recommend the hybrid (option C), approve the budget by Oct 20, about $18k per quarter | recommend the hybrid (option C), approve the budget by Oct 20, about $18k per quarter, judge drift | D3 | 551 |
| w2 full #2 | recommend the hybrid (option C), approve the budget by Oct 20, about $18k per quarter | recommend the hybrid (option C), approve the budget by Oct 20, about $18k per quarter, judge drift | - | 498 |
| w2 full #3 | recommend the hybrid (option C), approve the budget by Oct 20, about $18k per quarter | recommend the hybrid (option C), approve the budget by Oct 20, about $18k per quarter, judge drift | - | 466 |
| w3 baseline #1 | daily job failing since the schema rename, Oct 6-8 missing | daily job failing since the schema rename, finish load_events.py writer, then rerun Oct 6-8, Oct 6-8 missing, blocked on prod bucket access | - | 282 |
| w3 baseline #2 | daily job failing since the schema rename, finish load_events.py writer, then rerun Oct 6-8, Oct 6-8 missing | finish load_events.py writer, then rerun Oct 6-8, Oct 6-8 missing, blocked on prod bucket access | - | 339 |
| w3 baseline #3 | daily job failing since the schema rename, finish load_events.py writer, then rerun Oct 6-8, Oct 6-8 missing | finish load_events.py writer, then rerun Oct 6-8, Oct 6-8 missing | D2 D3 | 325 |
| w3 full #1 | finish load_events.py writer, then rerun Oct 6-8, Oct 6-8 missing | finish load_events.py writer, then rerun Oct 6-8, Oct 6-8 missing, blocked on prod bucket access | - | 221 |
| w3 full #2 | finish load_events.py writer, then rerun Oct 6-8, Oct 6-8 missing | finish load_events.py writer, then rerun Oct 6-8, Oct 6-8 missing, blocked on prod bucket access | - | 217 |
| w3 full #3 | daily job failing since the schema rename, Oct 6-8 missing | daily job failing since the schema rename, finish load_events.py writer, then rerun Oct 6-8, Oct 6-8 missing, blocked on prod bucket access | - | 217 |
