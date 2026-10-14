# Eval summary: 2026-10-14-1326-validate-canary

**Verdict:** INVALID (1 of 1 runs didn't execute: not_isolated 1; nothing here measures the model or the skill). 1 fixtures; the pass rule needs 15. Rule outcome at this n: n/a.

## Fixtures by majority vote

| Fixture | Kind | baseline |
|---|---|---|
| f5 | abstain | ✗ not_executed (0/1) |

## Per arm

| Metric | baseline |
|---|---|
| fixtures_correct | 0 |
| fixtures_false_alarm | 0 |
| fixtures_abstain_answered | 0 |
| fixtures_incomplete | 0 |
| fixtures_not_executed | 1 |
| runs_correct | 0 |
| runs | 1 |
| runs_not_executed | 1 |
| runs_unparseable | 0 |
| runs_contaminated | 0 |
| runs_unverified_isolation | 1 |
| dropped_alternative_lines | 0 |
| runs_with_any_check | 0 |
| runs_reading_skill | 0 |
| cost_usd | 0 |

## Every run

| Run | Correct | Headline | Reason | Checks that ran | Isolation | Skill read |
|---|---|---|---|---|---|---|
| f5 baseline #1 | ✗ |  | execution failed: not_isolated | none | unverified (custom agent) | unverified (custom agent) |
