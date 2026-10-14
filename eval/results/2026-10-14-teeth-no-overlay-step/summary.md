# Eval summary: 2026-10-14-teeth-no-overlay-step

**Verdict:** INSUFFICIENT_N (smoke test, not a decision). 2 fixtures; the pass rule needs 15. Rule outcome at this n: n/a.

## Fixtures by majority vote

| Fixture | Kind | full |
|---|---|---|
| f6 | error | ✗ miss (0/3) |
| f7 | abstain | ✗ answered_abstain_case (1/3) |

## Per arm

| Metric | full |
|---|---|
| fixtures_correct | 0 |
| fixtures_false_alarm | 0 |
| fixtures_abstain_answered | 1 |
| fixtures_incomplete | 0 |
| runs_correct | 1 |
| runs | 6 |
| runs_unparseable | 0 |
| runs_contaminated | 0 |
| runs_unverified_isolation | 0 |
| dropped_alternative_lines | 2 |
| runs_with_any_check | 6 |
| runs_reading_skill | 6 |
| cost_usd | 0.78 |

## Every run

| Run | Correct | Headline | Reason | Checks that ran |
|---|---|---|---|---|
| f6 full #1 | ✗ | 41.4 % (95% CI 41.3 to 41.5) | headline 41.4 outside 50.053±0.3 | completeness:pass |
| f6 full #2 | ✗ | +46.05 % (95% CI 45.93 to 46.17) | headline 46.05 outside 50.053±0.3 | completeness:pass |
| f6 full #3 | ✗ | +46.05 % search CTR (95% CI 45.93 to 46.17) | headline 46.05 outside 50.053±0.3 | completeness:pass |
| f7 full #1 | ✗ | +8.30 % of searches led to a purchase (8.24 to 8.36) | answered 8.3 where the right answer is can't tell | completeness:pass |
| f7 full #2 | ✗ | +8.30 % of searches led to a purchase (8.24% to 8.36%) | answered 8.3 where the right answer is can't tell | completeness:pass |
| f7 full #3 | ✓ | can't tell | abstained (accepted) | completeness:pass |
