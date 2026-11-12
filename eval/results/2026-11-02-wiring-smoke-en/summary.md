# Eval summary: 2026-11-02-wiring-smoke-en

**Verdict:** INCOMPLETE (some cells lack the pre-registered run count). 3 fixtures; the pass rule needs 15. Rule outcome at this n: n/a.

## Fixtures by majority vote

| Fixture | Kind | full |
|---|---|---|
| f1 | error | ✗ incomplete (1/1) |
| f3 | clean | ✗ incomplete (1/1) |
| f6 | error | ✗ incomplete (1/1) |

## Per arm

| Metric | full |
|---|---|
| fixtures_correct | 0 |
| fixtures_false_alarm | 0 |
| fixtures_abstain_answered | 0 |
| fixtures_incomplete | 3 |
| fixtures_not_executed | 0 |
| runs_correct | 3 |
| runs | 3 |
| runs_not_executed | 0 |
| runs_unparseable | 0 |
| runs_contaminated | 0 |
| runs_unverified_isolation | 0 |
| dropped_alternative_lines | 0 |
| runs_with_any_check | 3 |
| runs_reading_skill | 3 |
| cost_usd | 0.46 |

## Every run

| Run | Correct | Headline | Reason | Checks that ran |
|---|---|---|---|---|
| f1 full #1 | ✓ | -0.00 pp (-0.15 to +0.15) | number within tolerance; causes consistent with gold | mix_shift:flag/flag, completeness:fail/pass |
| f3 full #1 | ✓ | -1.82 pp (-1.97 to -1.67) | number within tolerance; causes consistent with gold | completeness:could_not_run, mix_shift:pass/pass |
| f6 full #1 | ✓ | +50.05 % (49.93 to 50.18) | number within tolerance; causes consistent with gold | completeness:pass |
