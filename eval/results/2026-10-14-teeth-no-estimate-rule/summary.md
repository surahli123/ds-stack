# Eval summary: 2026-10-14-teeth-no-estimate-rule

**Verdict:** INSUFFICIENT_N (smoke test, not a decision). 3 fixtures; the pass rule needs 15. Rule outcome at this n: n/a.

## Fixtures by majority vote

| Fixture | Kind | full |
|---|---|---|
| f1 | error | ✓ (3/3) |
| f3 | clean | ✓ (2/3) |
| f6 | error | ✓ (3/3) |

## Per arm

| Metric | full |
|---|---|
| fixtures_correct | 3 |
| fixtures_false_alarm | 0 |
| fixtures_abstain_answered | 0 |
| fixtures_incomplete | 0 |
| runs_correct | 8 |
| runs | 9 |
| runs_unparseable | 0 |
| runs_contaminated | 0 |
| runs_unverified_isolation | 0 |
| dropped_alternative_lines | 3 |
| runs_with_any_check | 9 |
| runs_reading_skill | 9 |
| cost_usd | 1.3 |

## Every run

| Run | Correct | Headline | Reason | Checks that ran |
|---|---|---|---|---|
| f1 full #1 | ✓ | -0.00 pp (-0.15 to +0.15) within-segment change, the part of the CTR m | number within tolerance; causes consistent with gold | completeness:could_not_run, mix_shift:flag/flag |
| f1 full #2 | ✓ | -0.00 pp (-0.15 to +0.15) attributable to v2 after holding platform mi | number within tolerance; causes consistent with gold | completeness:pass, mix_shift:flag/flag |
| f1 full #3 | ✓ | -0.00 pp (-0.15 to +0.15) attributable to v2, as the within-platform C | number within tolerance; causes consistent with gold | mix_shift:flag/flag, completeness:pass |
| f3 full #1 | ✓ | -1.83 pp (95% CI -1.98 to -1.68) overall CTR change, week over week; t | number within tolerance; causes consistent with gold | mix_shift:pass, completeness:pass |
| f3 full #2 | ✓ | -1.83 pp (95% CI -1.98 to -1.68) | number within tolerance; causes consistent with gold | completeness:pass, mix_shift:pass/pass |
| f3 full #3 | ✗ | can't tell | abstained on a case with a valid answer | completeness:could_not_run, mix_shift:pass/pass |
| f6 full #1 | ✓ | 50.05 % (49.93 to 50.18) | number within tolerance; causes consistent with gold | completeness:fail/pass |
| f6 full #2 | ✓ | 50.05 % CTR (95% CI 49.93 to 50.17 %, binomial on the q5 counts) | number within tolerance; causes consistent with gold | completeness:pass |
| f6 full #3 | ✓ | 50.05 % search CTR (95% CI 49.93 to 50.17) | number within tolerance; causes consistent with gold | completeness:pass |
