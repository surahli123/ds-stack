# Eval summary: 2026-10-14-calibration-baseline-2

**Verdict:** INSUFFICIENT_N (smoke test, not a decision). 2 fixtures; the pass rule needs 15. Rule outcome at this n: n/a.

## Fixtures by majority vote

| Fixture | Kind | baseline |
|---|---|---|
| f7 | abstain | ✗ answered_abstain_case (0/3) |
| f8 | error | ✓ (3/3) |

## Per arm

| Metric | baseline |
|---|---|
| fixtures_correct | 1 |
| fixtures_false_alarm | 0 |
| fixtures_abstain_answered | 1 |
| fixtures_incomplete | 0 |
| runs_correct | 3 |
| runs | 6 |
| runs_unparseable | 0 |
| runs_contaminated | 0 |
| runs_unverified_isolation | 0 |
| dropped_alternative_lines | 2 |
| runs_with_any_check | 0 |
| runs_reading_skill | 0 |
| cost_usd | 0.36 |

## Every run

| Run | Correct | Headline | Reason | Checks that ran |
|---|---|---|---|---|
| f7 baseline #1 | ✗ | 8.30 % of searches led to a purchase (95% CI 8.24 to 8.36) | answered 8.3 where the right answer is can't tell | none |
| f7 baseline #2 | ✗ | 8.30 % of searches led to a purchase (95% CI 8.24 to 8.36 %) | answered 8.3 where the right answer is can't tell | none |
| f7 baseline #3 | ✗ | 8.30 % of searches led to a purchase (95% CI 8.24 to 8.36) | answered 8.3 where the right answer is can't tell | none |
| f8 baseline #1 | ✓ | 36.97 % (95% CI 36.68 to 37.26) | number within tolerance; causes consistent with gold | none |
| f8 baseline #2 | ✓ | 37.0 % (95% CI 36.2 to 37.8) | number within tolerance; causes consistent with gold | none |
| f8 baseline #3 | ✓ | 36.97 percent (36.7 to 37.3) | number within tolerance; causes consistent with gold | none |
