# Eval summary: 2026-11-02-0911-codex-zh

**Verdict:** INSUFFICIENT_N (smoke test, not a decision). 8 fixtures; the pass rule needs 15. Rule outcome at this n: FAIL.

## Fixtures by majority vote

| Fixture | Kind | baseline | checks | full |
|---|---|---|---|---|
| f1 | error | ✗ miss (0/3) | ✗ miss (0/3) | ✗ miss (0/3) |
| f2 | error | ✓ (3/3) | ✓ (3/3) | ✓ (3/3) |
| f3 | clean | ✗ false_alarm (0/3) | ✗ false_alarm (0/3) | ✗ false_alarm (0/3) |
| f4 | abstain | ✓ (3/3) | ✓ (3/3) | ✓ (3/3) |
| f5 | abstain | ✓ (3/3) | ✓ (3/3) | ✓ (3/3) |
| f6 | error | ✓ (2/3) | ✗ miss (0/3) | ✓ (3/3) |
| f7 | abstain | ✓ (3/3) | ✓ (3/3) | ✓ (3/3) |
| f8 | error | ✓ (3/3) | ✓ (3/3) | ✓ (3/3) |

## Per arm

| Metric | baseline | checks | full |
|---|---|---|---|
| fixtures_correct | 6 | 5 | 6 |
| fixtures_false_alarm | 1 | 1 | 1 |
| fixtures_abstain_answered | 0 | 0 | 0 |
| fixtures_incomplete | 0 | 0 | 0 |
| fixtures_not_executed | 0 | 0 | 0 |
| runs_correct | 17 | 15 | 18 |
| runs | 24 | 24 | 24 |
| runs_not_executed | 0 | 0 | 0 |
| runs_unparseable | 0 | 0 | 0 |
| runs_contaminated | 0 | 0 | 0 |
| runs_unverified_isolation | 24 | 24 | 24 |
| dropped_alternative_lines | 0 | 0 | 2 |
| runs_with_any_check | 0 | 24 | 22 |
| runs_reading_skill | 0 | 0 | 0 |
| cost_usd | 0 | 0 | 0 |

## Every run

| Run | Correct | Headline | Reason | Checks that ran | Isolation | Skill read |
|---|---|---|---|---|---|---|
| f1 baseline #1 | ✗ | can't tell | abstained on a case with a valid answer | none | unverified (custom agent) | unverified (custom agent) |
| f1 baseline #2 | ✗ | can't tell [inferred] | abstained on a case with a valid answer | none | unverified (custom agent) | unverified (custom agent) |
| f1 baseline #3 | ✗ | can't tell | abstained on a case with a valid answer | none | unverified (custom agent) | unverified (custom agent) |
| f1 checks #1 | ✗ | can't tell [inferred] | abstained on a case with a valid answer | completeness:could_not_run/could_not_run/could_not_run/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass, mix_shift:flag | unverified (custom agent) | unverified (custom agent) |
| f1 checks #2 | ✗ | can't tell [inferred] | abstained on a case with a valid answer | completeness:could_not_run/could_not_run/could_not_run/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass, mix_shift:flag | unverified (custom agent) | unverified (custom agent) |
| f1 checks #3 | ✗ | can't tell [inferred] | abstained on a case with a valid answer | completeness:could_not_run/could_not_run/could_not_run/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass, mix_shift:flag | unverified (custom agent) | unverified (custom agent) |
| f1 full #1 | ✗ | can't tell [inferred] | abstained on a case with a valid answer | mix_shift:flag/flag/flag, completeness:pass/pass | unverified (custom agent) | unverified (custom agent) |
| f1 full #2 | ✗ | can't tell [inferred] | abstained on a case with a valid answer | mix_shift:flag/flag, completeness:could_not_run/could_not_run/could_not_run/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass | unverified (custom agent) | unverified (custom agent) |
| f1 full #3 | ✗ | can't tell [inferred] | abstained on a case with a valid answer | completeness:pass/pass/pass/pass, mix_shift:flag/flag/flag | unverified (custom agent) | unverified (custom agent) |
| f2 baseline #1 | ✓ | +54.98%(95% 区间:54.58%–55.38%;点估计 [measured],区间 [inferred]) | number within tolerance; causes consistent with gold | none | unverified (custom agent) | unverified (custom agent) |
| f2 baseline #2 | ✓ | +54.98% (95% interval: 54.58%–55.38%) [measured;区间为 inferred] | number within tolerance; causes consistent with gold | none | unverified (custom agent) | unverified (custom agent) |
| f2 baseline #3 | ✓ | +54.98% (95% interval: 54.58%–55.38%) [measured;区间 inferred] | number within tolerance; causes consistent with gold | none | unverified (custom agent) | unverified (custom agent) |
| f2 checks #1 | ✓ | +54.98% (95% interval: 54.58%–55.38%) [measured;区间 inferred] | number within tolerance; causes consistent with gold | completeness:could_not_run, fanout:fail/pass | unverified (custom agent) | unverified (custom agent) |
| f2 checks #2 | ✓ | +54.98% (95% interval: 54.58%–55.38%) [measured] | number within tolerance; causes consistent with gold | completeness:could_not_run, fanout:fail/pass | unverified (custom agent) | unverified (custom agent) |
| f2 checks #3 | ✓ | +54.98% (95% 区间:54.58%–55.38%) [measured;区间假设:guess] | number within tolerance; causes consistent with gold | completeness:could_not_run, fanout:fail/pass | unverified (custom agent) | unverified (custom agent) |
| f2 full #1 | ✓ | +54.98 % (95% CI: 54.58%–55.38%)   [measured] | number within tolerance; causes consistent with gold | completeness:could_not_run, fanout:pass | unverified (custom agent) | unverified (custom agent) |
| f2 full #2 | ✓ | +54.98 % (95% CI: 54.58%–55.38%)   [measured] | number within tolerance; causes consistent with gold | completeness:could_not_run, fanout:pass | unverified (custom agent) | unverified (custom agent) |
| f2 full #3 | ✓ | +54.98 % (95% CI: 54.58%–55.38%)   [measured] | number within tolerance; causes consistent with gold | completeness:could_not_run, fanout:pass | unverified (custom agent) | unverified (custom agent) |
| f3 baseline #1 | ✗ | can't tell | abstained on a case with a valid answer | none | unverified (custom agent) | unverified (custom agent) |
| f3 baseline #2 | ✗ | can't tell [inferred] | abstained on a case with a valid answer | none | unverified (custom agent) | unverified (custom agent) |
| f3 baseline #3 | ✗ | can't tell [inferred] | abstained on a case with a valid answer | none | unverified (custom agent) | unverified (custom agent) |
| f3 checks #1 | ✗ | can't tell | abstained on a case with a valid answer | completeness:could_not_run/could_not_run/could_not_run/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass, mix_shift:pass | unverified (custom agent) | unverified (custom agent) |
| f3 checks #2 | ✗ | can't tell [inferred] | abstained on a case with a valid answer | completeness:could_not_run/could_not_run/could_not_run/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass, mix_shift:pass | unverified (custom agent) | unverified (custom agent) |
| f3 checks #3 | ✗ | can't tell [inferred] | abstained on a case with a valid answer | completeness:could_not_run/could_not_run/could_not_run/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass, mix_shift:pass/pass | unverified (custom agent) | unverified (custom agent) |
| f3 full #1 | ✗ | can't tell [inferred] | abstained on a case with a valid answer | completeness:could_not_run/could_not_run/could_not_run/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass, mix_shift:pass/pass | unverified (custom agent) | unverified (custom agent) |
| f3 full #2 | ✗ | can't tell [inferred] | abstained on a case with a valid answer | completeness:could_not_run/pass/pass, mix_shift:pass/pass | unverified (custom agent) | unverified (custom agent) |
| f3 full #3 | ✗ | can't tell [inferred] | abstained on a case with a valid answer | mix_shift:pass/pass/pass, completeness:pass/pass | unverified (custom agent) | unverified (custom agent) |
| f4 baseline #1 | ✓ | can't tell | abstained (accepted) | none | unverified (custom agent) | unverified (custom agent) |
| f4 baseline #2 | ✓ | can't tell | abstained (accepted) | none | unverified (custom agent) | unverified (custom agent) |
| f4 baseline #3 | ✓ | can't tell [inferred] | abstained (accepted) | none | unverified (custom agent) | unverified (custom agent) |
| f4 checks #1 | ✓ | can't tell [inferred] | abstained (accepted) | completeness:could_not_run/could_not_run/could_not_run/pass/pass/pass/pass/fail, mix_shift:could_not_run/pass | unverified (custom agent) | unverified (custom agent) |
| f4 checks #2 | ✓ | can't tell | abstained (accepted) | completeness:pass/fail, mix_shift:could_not_run/pass | unverified (custom agent) | unverified (custom agent) |
| f4 checks #3 | ✓ | can't tell [inferred] | abstained (accepted) | completeness:fail, mix_shift:could_not_run/pass | unverified (custom agent) | unverified (custom agent) |
| f4 full #1 | ✓ | can't tell [inferred] | abstained (accepted) | completeness:could_not_run/could_not_run/could_not_run/could_not_run/pass/pass/pass/pass/fail, mix_shift:pass/pass | unverified (custom agent) | unverified (custom agent) |
| f4 full #2 | ✓ | can't tell [inferred] | abstained (accepted) | completeness:could_not_run/could_not_run/could_not_run/pass/pass/pass/pass/fail, mix_shift:pass/pass | unverified (custom agent) | unverified (custom agent) |
| f4 full #3 | ✓ | can't tell [inferred] | abstained (accepted) | completeness:could_not_run/could_not_run/could_not_run/could_not_run/pass/pass/pass/pass/fail, mix_shift:pass/pass | unverified (custom agent) | unverified (custom agent) |
| f5 baseline #1 | ✓ | can't tell [inferred] | abstained (accepted) | none | unverified (custom agent) | unverified (custom agent) |
| f5 baseline #2 | ✓ | can't tell [inferred] | abstained (accepted) | none | unverified (custom agent) | unverified (custom agent) |
| f5 baseline #3 | ✓ | can't tell [inferred] | abstained (accepted) | none | unverified (custom agent) | unverified (custom agent) |
| f5 checks #1 | ✓ | can't tell [inferred] | abstained (accepted) | completeness:pass/pass/pass/pass/pass/pass, srm:fail/fail/fail/fail/fail/fail/fail/fail/fail/fail/fail/fail/fail/fail/fail, mix_shift:pass | unverified (custom agent) | unverified (custom agent) |
| f5 checks #2 | ✓ | can't tell [inferred] | abstained (accepted) | completeness:pass/pass, srm:fail/fail, mix_shift:pass | unverified (custom agent) | unverified (custom agent) |
| f5 checks #3 | ✓ | can't tell [inferred] | abstained (accepted) | completeness:pass/pass/pass/pass, srm:fail/fail/fail/fail/fail/fail/fail/fail/fail/fail/fail/fail/fail/fail/fail, mix_shift:pass | unverified (custom agent) | unverified (custom agent) |
| f5 full #1 | ✓ | can't tell [inferred] | abstained (accepted) | srm:fail, completeness:pass/pass, mix_shift:pass/pass | unverified (custom agent) | unverified (custom agent) |
| f5 full #2 | ✓ | can't tell [inferred] | abstained (accepted) | srm:fail, completeness:pass/pass, mix_shift:pass/pass | unverified (custom agent) | unverified (custom agent) |
| f5 full #3 | ✓ | can't tell [inferred] | abstained (accepted) | srm:fail, completeness:could_not_run/could_not_run/could_not_run/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass/could_not_run/could_not_run/could_not_run/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass, mix_shift:pass/pass | unverified (custom agent) | unverified (custom agent) |
| f6 baseline #1 | ✓ | +50.05% (95% interval: 49.93%–50.18%) [measured;区间模型 inferred] | number within tolerance; causes consistent with gold | none | unverified (custom agent) | unverified (custom agent) |
| f6 baseline #2 | ✗ | can't tell | abstained on a case with a valid answer | none | unverified (custom agent) | unverified (custom agent) |
| f6 baseline #3 | ✓ | +50.05% (95% interval: 49.93%–50.18%) [measured;区间依赖 inferred 假设] | number within tolerance; causes consistent with gold | none | unverified (custom agent) | unverified (custom agent) |
| f6 checks #1 | ✗ | can't tell | abstained on a case with a valid answer | completeness:could_not_run/could_not_run/could_not_run/pass/pass/pass/pass/could_not_run/could_not_run/could_not_run/pass/pass/pass/pass | unverified (custom agent) | unverified (custom agent) |
| f6 checks #2 | ✗ | can't tell | abstained on a case with a valid answer | completeness:could_not_run/could_not_run/could_not_run/pass/pass/pass/pass | unverified (custom agent) | unverified (custom agent) |
| f6 checks #3 | ✗ | can't tell | abstained on a case with a valid answer | completeness:could_not_run/could_not_run/could_not_run/could_not_run/could_not_run/could_not_run/pass/pass/pass/pass/pass/pass/pass/pass | unverified (custom agent) | unverified (custom agent) |
| f6 full #1 | ✓ | +50.05 % (95% CI: 49.93%–50.18%)   [measured] | number within tolerance; causes consistent with gold | completeness:could_not_run/could_not_run/could_not_run/pass/pass/pass/pass | unverified (custom agent) | unverified (custom agent) |
| f6 full #2 | ✓ | +50.05 % (95% CI: 49.93%–50.18%)   [measured] | number within tolerance; causes consistent with gold | completeness:could_not_run | unverified (custom agent) | unverified (custom agent) |
| f6 full #3 | ✓ | +50.05 % (95% CI: 49.93%–50.18%)   [measured] | number within tolerance; causes consistent with gold | completeness:could_not_run/could_not_run/could_not_run/pass/pass/pass/pass | unverified (custom agent) | unverified (custom agent) |
| f7 baseline #1 | ✓ | can't tell | abstained (accepted) | none | unverified (custom agent) | unverified (custom agent) |
| f7 baseline #2 | ✓ | can't tell | abstained (accepted) | none | unverified (custom agent) | unverified (custom agent) |
| f7 baseline #3 | ✓ | can't tell | abstained (accepted) | none | unverified (custom agent) | unverified (custom agent) |
| f7 checks #1 | ✓ | can't tell | abstained (accepted) | completeness:could_not_run/could_not_run/could_not_run/pass/pass/pass/pass | unverified (custom agent) | unverified (custom agent) |
| f7 checks #2 | ✓ | can't tell | abstained (accepted) | completeness:could_not_run/could_not_run/could_not_run/pass/pass/pass/pass/could_not_run/could_not_run/could_not_run/pass/pass/pass/pass | unverified (custom agent) | unverified (custom agent) |
| f7 checks #3 | ✓ | can't tell | abstained (accepted) | completeness:could_not_run/could_not_run/could_not_run/pass/pass/pass/pass | unverified (custom agent) | unverified (custom agent) |
| f7 full #1 | ✓ | can't tell [inferred] | abstained (accepted) | none | unverified (custom agent) | unverified (custom agent) |
| f7 full #2 | ✓ | can't tell | abstained (accepted) | none | unverified (custom agent) | unverified (custom agent) |
| f7 full #3 | ✓ | can't tell [inferred] | abstained (accepted) | completeness:could_not_run | unverified (custom agent) | unverified (custom agent) |
| f8 baseline #1 | ✓ | +36.97%(95% 区间:36.68%–37.26%;条件性 Wilson 区间)[measured] | number within tolerance; causes consistent with gold | none | unverified (custom agent) | unverified (custom agent) |
| f8 baseline #2 | ✓ | +36.97% (95% 区间:36.68%–37.26%) [measured;区间为 inferred] | number within tolerance; causes consistent with gold | none | unverified (custom agent) | unverified (custom agent) |
| f8 baseline #3 | ✓ | +36.97 %(95% 区间:36.68%–37.26%;点值 [measured],区间 [inferred]) | number within tolerance; causes consistent with gold | none | unverified (custom agent) | unverified (custom agent) |
| f8 checks #1 | ✓ | +36.97%(95% 区间:36.68%–37.26%)[measured;区间 inferred] | number within tolerance; causes consistent with gold | completeness:could_not_run, fanout:fail/pass/pass | unverified (custom agent) | unverified (custom agent) |
| f8 checks #2 | ✓ | +36.97% (95% 区间:36.68%–37.26%) [measured] | number within tolerance; causes consistent with gold | completeness:could_not_run, fanout:fail/pass/pass | unverified (custom agent) | unverified (custom agent) |
| f8 checks #3 | ✓ | +36.97%(95% 区间:36.68%–37.26%)[measured;区间 inferred] | number within tolerance; causes consistent with gold | completeness:could_not_run, fanout:fail/pass/pass | unverified (custom agent) | unverified (custom agent) |
| f8 full #1 | ✓ | +36.97 % (95% CI: 36.68%–37.26%)   [measured] | number within tolerance; causes consistent with gold | completeness:could_not_run, fanout:fail/pass/pass | unverified (custom agent) | unverified (custom agent) |
| f8 full #2 | ✓ | +36.97% (95% CI: 36.68%–37.26%)   [measured] | number within tolerance; causes consistent with gold | completeness:could_not_run, fanout:pass/pass | unverified (custom agent) | unverified (custom agent) |
| f8 full #3 | ✓ | +36.97 % (95% CI: 36.68%–37.26%)   [measured] | number within tolerance; causes consistent with gold | completeness:could_not_run, fanout:fail/pass/pass | unverified (custom agent) | unverified (custom agent) |
