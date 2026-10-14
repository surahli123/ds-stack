# Eval summary: 2026-10-14-calibration-baseline

**Verdict:** INSUFFICIENT_N (smoke test, not a decision). 3 fixtures; the pass rule needs 15. Rule outcome at this n: n/a.

## Fixtures by majority vote

| Fixture | Kind | baseline |
|---|---|---|
| f6 | error | ✗ miss (0/3) |
| f7 | abstain | ✓ (3/3) |
| f8 | error | ✓ (3/3) |

## Per arm

| Metric | baseline |
|---|---|
| fixtures_correct | 2 |
| fixtures_false_alarm | 0 |
| fixtures_abstain_answered | 0 |
| fixtures_incomplete | 0 |
| runs_correct | 6 |
| runs | 9 |
| runs_unparseable | 0 |
| runs_contaminated | 0 |
| runs_unverified_isolation | 0 |
| dropped_alternative_lines | 7 |
| runs_with_any_check | 0 |
| runs_reading_skill | 0 |
| cost_usd | 0.53 |

## Every run

| Run | Correct | Headline | Reason | Checks that ran |
|---|---|---|---|---|
| f6 baseline #1 | ✗ | 46.05 % (95% CI 45.93 to 46.17) — search CTR for 2026-10-05 to 2026-10 | headline 46.05 outside 50.053±0.3 | none |
| f6 baseline #2 | ✗ | 46.0 % (95% CI 45.9 to 46.2) | headline 46 outside 50.053±0.3 | none |
| f6 baseline #3 | ✗ | 46.0 % (95% CI 45.9 to 46.2), CTR for 2026-10-05 to 2026-10-11, extern | headline 46 outside 50.053±0.3 | none |
| f7 baseline #1 | ✓ | can't tell. Purchases aren't logged in this warehouse, so the purchase | abstained (accepted) | none |
| f7 baseline #2 | ✓ | can't tell | abstained (accepted) | none |
| f7 baseline #3 | ✓ | can't tell | abstained (accepted) | none |
| f8 baseline #1 | ✓ | 38.3 % (95% CI 37.5 to 39.1) | number within tolerance; causes consistent with gold | none |
| f8 baseline #2 | ✓ | 38.3 % (95% CI 37.5 to 39.1) | number within tolerance; causes consistent with gold | none |
| f8 baseline #3 | ✓ | 38.3 % (95% CI 37.5 to 39.1) | number within tolerance; causes consistent with gold | none |
