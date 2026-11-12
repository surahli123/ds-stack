# Eval summary: 2026-11-02-0911-codex-en

**Verdict:** INSUFFICIENT_N (smoke test, not a decision). 8 fixtures; the pass rule needs 15. Rule outcome at this n: FAIL.

## Fixtures by majority vote

| Fixture | Kind | baseline | checks | full |
|---|---|---|---|---|
| f1 | error | ✗ miss (0/3) | ✗ miss (0/3) | ✗ miss (0/3) |
| f2 | error | ✓ (3/3) | ✓ (3/3) | ✓ (3/3) |
| f3 | clean | ✗ false_alarm (0/3) | ✗ false_alarm (0/3) | ✓ (2/3) |
| f4 | abstain | ✓ (3/3) | ✓ (3/3) | ✓ (3/3) |
| f5 | abstain | ✓ (3/3) | ✓ (3/3) | ✓ (3/3) |
| f6 | error | ✗ miss (1/3) | ✗ miss (0/3) | ✓ (3/3) |
| f7 | abstain | ✓ (3/3) | ✓ (3/3) | ✓ (3/3) |
| f8 | error | ✓ (3/3) | ✓ (3/3) | ✓ (3/3) |

## Per arm

| Metric | baseline | checks | full |
|---|---|---|---|
| fixtures_correct | 5 | 5 | 7 |
| fixtures_false_alarm | 1 | 1 | 0 |
| fixtures_abstain_answered | 0 | 0 | 0 |
| fixtures_incomplete | 0 | 0 | 0 |
| fixtures_not_executed | 0 | 0 | 0 |
| runs_correct | 16 | 15 | 20 |
| runs | 24 | 24 | 24 |
| runs_not_executed | 0 | 0 | 0 |
| runs_unparseable | 0 | 0 | 0 |
| runs_contaminated | 0 | 0 | 0 |
| runs_unverified_isolation | 24 | 24 | 24 |
| dropped_alternative_lines | 0 | 0 | 0 |
| runs_with_any_check | 0 | 24 | 21 |
| runs_reading_skill | 0 | 0 | 0 |
| cost_usd | 0 | 0 | 0 |

## Every run

| Run | Correct | Headline | Reason | Checks that ran | Isolation | Skill read |
|---|---|---|---|---|---|---|
| f1 baseline #1 | ✗ | can't tell [inferred] | abstained on a case with a valid answer | none | unverified (custom agent) | unverified (custom agent) |
| f1 baseline #2 | ✗ | can't tell [inferred] | abstained on a case with a valid answer | none | unverified (custom agent) | unverified (custom agent) |
| f1 baseline #3 | ✗ | can't tell [inferred] | abstained on a case with a valid answer | none | unverified (custom agent) | unverified (custom agent) |
| f1 checks #1 | ✗ | can't tell [inferred] | abstained on a case with a valid answer | completeness:could_not_run/could_not_run/could_not_run/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass, mix_shift:flag | unverified (custom agent) | unverified (custom agent) |
| f1 checks #2 | ✗ | can't tell [inferred] | abstained on a case with a valid answer | completeness:could_not_run/could_not_run/could_not_run/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass, mix_shift:flag | unverified (custom agent) | unverified (custom agent) |
| f1 checks #3 | ✗ | can't tell [inferred] | abstained on a case with a valid answer | completeness:could_not_run/could_not_run/could_not_run/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass, mix_shift:flag | unverified (custom agent) | unverified (custom agent) |
| f1 full #1 | ✗ | -0.002 pp (95% interval: -0.152 to +0.149)   [measured] | ruled in a false cause: 'ranker effect' | completeness:pass/pass, mix_shift:flag/flag/flag | unverified (custom agent) | unverified (custom agent) |
| f1 full #2 | ✗ | -0.002 pp (95% interval: -0.153 to +0.148) [measured] | ruled in a false cause: 'ranker harm' | completeness:pass/pass, mix_shift:flag/flag | unverified (custom agent) | unverified (custom agent) |
| f1 full #3 | ✗ | -0.002 pp (95% interval: -0.153 to +0.148) [measured] | ruled in a false cause: 'v2 harm or another concurrent change' | completeness:pass/pass/pass/pass, mix_shift:flag/flag/flag | unverified (custom agent) | unverified (custom agent) |
| f2 baseline #1 | ✓ | +54.98% (95% interval: 54.58%–55.38%) [measured rate; inferred interva | number within tolerance; causes consistent with gold | none | unverified (custom agent) | unverified (custom agent) |
| f2 baseline #2 | ✓ | +54.98% (95% interval: 54.58%–55.38%) [measured; interval inferred] | number within tolerance; causes consistent with gold | none | unverified (custom agent) | unverified (custom agent) |
| f2 baseline #3 | ✓ | +54.98% (95% interval: 54.58%–55.38%) [measured; interval inferred] | number within tolerance; causes consistent with gold | none | unverified (custom agent) | unverified (custom agent) |
| f2 checks #1 | ✓ | +54.98% (95% interval: 54.58%–55.38%) [measured; interval inferred] | number within tolerance; causes consistent with gold | completeness:could_not_run, fanout:fail/pass | unverified (custom agent) | unverified (custom agent) |
| f2 checks #2 | ✓ | +54.98% (95% interval: 54.58%–55.38%) [measured; interval inferred] | number within tolerance; causes consistent with gold | completeness:could_not_run, fanout:fail/pass | unverified (custom agent) | unverified (custom agent) |
| f2 checks #3 | ✓ | +54.98% (95% interval: 54.58%–55.38%) [measured] | number within tolerance; causes consistent with gold | completeness:could_not_run, fanout:pass | unverified (custom agent) | unverified (custom agent) |
| f2 full #1 | ✓ | +54.98% (95% interval: 54.58%–55.38%)   [measured] | number within tolerance; causes consistent with gold | completeness:could_not_run, fanout:pass/fail | unverified (custom agent) | unverified (custom agent) |
| f2 full #2 | ✓ | +54.98% (95% interval: 54.58%–55.38%)   [measured] | number within tolerance; causes consistent with gold | completeness:could_not_run, fanout:pass | unverified (custom agent) | unverified (custom agent) |
| f2 full #3 | ✓ | +54.98 percent (no interval: stored totals; sampling model unspecified | number within tolerance; causes consistent with gold | completeness:could_not_run, fanout:pass | unverified (custom agent) | unverified (custom agent) |
| f3 baseline #1 | ✗ | can't tell [inferred] | abstained on a case with a valid answer | none | unverified (custom agent) | unverified (custom agent) |
| f3 baseline #2 | ✗ | can't tell [inferred] | abstained on a case with a valid answer | none | unverified (custom agent) | unverified (custom agent) |
| f3 baseline #3 | ✗ | can't tell | abstained on a case with a valid answer | none | unverified (custom agent) | unverified (custom agent) |
| f3 checks #1 | ✗ | can't tell [inferred] | abstained on a case with a valid answer | completeness:could_not_run/could_not_run/could_not_run/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass, mix_shift:pass | unverified (custom agent) | unverified (custom agent) |
| f3 checks #2 | ✗ | can't tell [inferred] | abstained on a case with a valid answer | completeness:pass/pass, mix_shift:pass | unverified (custom agent) | unverified (custom agent) |
| f3 checks #3 | ✗ | can't tell [inferred] | abstained on a case with a valid answer | completeness:could_not_run/could_not_run/could_not_run/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass, mix_shift:pass | unverified (custom agent) | unverified (custom agent) |
| f3 full #1 | ✗ | can't tell [inferred] | abstained on a case with a valid answer | completeness:pass/pass, mix_shift:pass/pass | unverified (custom agent) | unverified (custom agent) |
| f3 full #2 | ✓ | -1.817 pp (95% CI: -1.967 to -1.667)   [measured] | number within tolerance; causes consistent with gold | completeness:pass/pass, mix_shift:pass/pass | unverified (custom agent) | unverified (custom agent) |
| f3 full #3 | ✓ | -1.817 pp (95% interval: -1.967 to -1.667), adjusted association   [me | number within tolerance; causes consistent with gold | completeness:pass/pass, mix_shift:pass/pass/pass | unverified (custom agent) | unverified (custom agent) |
| f4 baseline #1 | ✓ | can't tell | abstained (accepted) | none | unverified (custom agent) | unverified (custom agent) |
| f4 baseline #2 | ✓ | can't tell | abstained (accepted) | none | unverified (custom agent) | unverified (custom agent) |
| f4 baseline #3 | ✓ | can't tell [inferred] | abstained (accepted) | none | unverified (custom agent) | unverified (custom agent) |
| f4 checks #1 | ✓ | can't tell [inferred] | abstained (accepted) | completeness:fail/pass, mix_shift:could_not_run/pass | unverified (custom agent) | unverified (custom agent) |
| f4 checks #2 | ✓ | can't tell [inferred] | abstained (accepted) | completeness:could_not_run/could_not_run/could_not_run/pass/pass/pass/pass/fail, mix_shift:could_not_run/pass | unverified (custom agent) | unverified (custom agent) |
| f4 checks #3 | ✓ | can't tell [inferred] | abstained (accepted) | completeness:fail/pass, mix_shift:could_not_run/pass | unverified (custom agent) | unverified (custom agent) |
| f4 full #1 | ✓ | can't tell [inferred] | abstained (accepted) | completeness:could_not_run/could_not_run/could_not_run/pass/pass/pass/pass/fail | unverified (custom agent) | unverified (custom agent) |
| f4 full #2 | ✓ | can't tell [inferred] | abstained (accepted) | completeness:fail/pass, mix_shift:pass/pass | unverified (custom agent) | unverified (custom agent) |
| f4 full #3 | ✓ | can't tell [inferred] | abstained (accepted) | completeness:pass/fail, mix_shift:pass/pass | unverified (custom agent) | unverified (custom agent) |
| f5 baseline #1 | ✓ | can't tell [inferred] | abstained (accepted) | none | unverified (custom agent) | unverified (custom agent) |
| f5 baseline #2 | ✓ | can't tell [inferred] | abstained (accepted) | none | unverified (custom agent) | unverified (custom agent) |
| f5 baseline #3 | ✓ | can't tell [inferred] | abstained (accepted) | none | unverified (custom agent) | unverified (custom agent) |
| f5 checks #1 | ✓ | can't tell [inferred] | abstained (accepted) | completeness:could_not_run/could_not_run/could_not_run/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass/could_not_run/could_not_run/could_not_run/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass, srm:fail/fail/fail/fail/fail/fail/fail/fail/fail/fail/fail/fail/fail/fail/fail, mix_shift:pass | unverified (custom agent) | unverified (custom agent) |
| f5 checks #2 | ✓ | can't tell [inferred] | abstained (accepted) | completeness:pass/pass, srm:fail/fail/fail/fail/fail/fail/fail/fail/fail/fail/fail/fail/fail/fail, mix_shift:pass | unverified (custom agent) | unverified (custom agent) |
| f5 checks #3 | ✓ | can't tell [inferred] | abstained (accepted) | completeness:pass/pass/pass/pass, srm:fail/fail/fail/fail/fail/fail/fail/fail/fail/fail/fail/fail/fail/fail/fail, mix_shift:pass | unverified (custom agent) | unverified (custom agent) |
| f5 full #1 | ✓ | can't tell [inferred] | abstained (accepted) | srm:fail/fail, completeness:could_not_run/could_not_run/could_not_run/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass/could_not_run/could_not_run/could_not_run/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass, mix_shift:pass/pass | unverified (custom agent) | unverified (custom agent) |
| f5 full #2 | ✓ | can't tell [inferred] | abstained (accepted) | srm:fail/fail, completeness:could_not_run/could_not_run/could_not_run/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass/could_not_run/could_not_run/could_not_run/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass, mix_shift:pass/pass | unverified (custom agent) | unverified (custom agent) |
| f5 full #3 | ✓ | can't tell [inferred] | abstained (accepted) | srm:fail, completeness:could_not_run/could_not_run/could_not_run/could_not_run/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass/could_not_run/could_not_run/could_not_run/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass/pass, mix_shift:pass/pass | unverified (custom agent) | unverified (custom agent) |
| f6 baseline #1 | ✓ | +50.05% (95% interval: 49.93%–50.18%) [measured; interval inferred] | number within tolerance; causes consistent with gold | none | unverified (custom agent) | unverified (custom agent) |
| f6 baseline #2 | ✗ | can't tell | abstained on a case with a valid answer | none | unverified (custom agent) | unverified (custom agent) |
| f6 baseline #3 | ✗ | +46.05% (95% interval: 45.93%–46.17%) [measured; provisional definitio | headline 46.05 outside 50.053±0.3 | none | unverified (custom agent) | unverified (custom agent) |
| f6 checks #1 | ✗ | +46.05% (95% interval: 45.93%–46.17%) [measured, conditional on defini | headline 46.05 outside 50.053±0.3 | completeness:could_not_run/could_not_run/could_not_run/pass/pass/pass/pass/could_not_run/could_not_run/could_not_run/pass/pass/pass/pass | unverified (custom agent) | unverified (custom agent) |
| f6 checks #2 | ✗ | can't tell | abstained on a case with a valid answer | completeness:could_not_run/could_not_run/could_not_run/pass/pass/pass/pass | unverified (custom agent) | unverified (custom agent) |
| f6 checks #3 | ✗ | can't tell [inferred] | abstained on a case with a valid answer | completeness:could_not_run/could_not_run/could_not_run/pass/pass/pass/pass | unverified (custom agent) | unverified (custom agent) |
| f6 full #1 | ✓ | +50.05% (95% interval: 49.93%–50.18%) [measured] | number within tolerance; causes consistent with gold | completeness:could_not_run/could_not_run/could_not_run/pass/pass/pass/pass | unverified (custom agent) | unverified (custom agent) |
| f6 full #2 | ✓ | +50.05% (95% interval: 49.93%–50.18%)   [measured] | number within tolerance; causes consistent with gold | completeness:could_not_run/could_not_run/could_not_run/pass/pass/pass/pass | unverified (custom agent) | unverified (custom agent) |
| f6 full #3 | ✓ | +50.05% (95% interval: 49.93%–50.18%)   [measured] | number within tolerance; causes consistent with gold | completeness:could_not_run/could_not_run/could_not_run/pass/pass/pass/pass | unverified (custom agent) | unverified (custom agent) |
| f7 baseline #1 | ✓ | can't tell | abstained (accepted) | none | unverified (custom agent) | unverified (custom agent) |
| f7 baseline #2 | ✓ | can't tell [inferred] | abstained (accepted) | none | unverified (custom agent) | unverified (custom agent) |
| f7 baseline #3 | ✓ | can't tell | abstained (accepted) | none | unverified (custom agent) | unverified (custom agent) |
| f7 checks #1 | ✓ | can't tell [inferred] | abstained (accepted) | completeness:could_not_run/could_not_run/could_not_run/pass/pass/pass/pass | unverified (custom agent) | unverified (custom agent) |
| f7 checks #2 | ✓ | can't tell | abstained (accepted) | completeness:could_not_run/could_not_run/could_not_run/pass/pass/pass/pass | unverified (custom agent) | unverified (custom agent) |
| f7 checks #3 | ✓ | can't tell | abstained (accepted) | completeness:could_not_run/could_not_run/could_not_run/pass/pass/pass/pass | unverified (custom agent) | unverified (custom agent) |
| f7 full #1 | ✓ | can't tell [inferred] | abstained (accepted) | none | unverified (custom agent) | unverified (custom agent) |
| f7 full #2 | ✓ | can't tell [inferred] | abstained (accepted) | none | unverified (custom agent) | unverified (custom agent) |
| f7 full #3 | ✓ | can't tell [inferred] | abstained (accepted) | none | unverified (custom agent) | unverified (custom agent) |
| f8 baseline #1 | ✓ | +36.97% (95% interval: 36.68%–37.26%) [measured rate; inferred interva | number within tolerance; causes consistent with gold | none | unverified (custom agent) | unverified (custom agent) |
| f8 baseline #2 | ✓ | +36.97% (95% interval: 36.19%–37.76%) [measured rate; inferred interva | number within tolerance; causes consistent with gold | none | unverified (custom agent) | unverified (custom agent) |
| f8 baseline #3 | ✓ | +36.97% (95% interval: 36.21%–37.75%) [measured estimate; inferred int | number within tolerance; causes consistent with gold | none | unverified (custom agent) | unverified (custom agent) |
| f8 checks #1 | ✓ | +36.97% (95% interval: 36.68%–37.26%) [measured; interval inferred] | number within tolerance; causes consistent with gold | completeness:could_not_run, fanout:fail/pass/pass | unverified (custom agent) | unverified (custom agent) |
| f8 checks #2 | ✓ | +36.97% (95% interval: 36.68%–37.26%) [measured rate; inferred interva | number within tolerance; causes consistent with gold | completeness:could_not_run, fanout:fail/pass/pass | unverified (custom agent) | unverified (custom agent) |
| f8 checks #3 | ✓ | +36.97% (95% interval: 36.68%–37.26%) [measured; interval inferred] | number within tolerance; causes consistent with gold | completeness:could_not_run, fanout:fail/pass/pass | unverified (custom agent) | unverified (custom agent) |
| f8 full #1 | ✓ | +36.97% (95% interval: 36.18%–37.76%)   [measured] | number within tolerance; causes consistent with gold | completeness:could_not_run, fanout:fail/pass/pass | unverified (custom agent) | unverified (custom agent) |
| f8 full #2 | ✓ | +36.97% (95% interval: 36.68%–37.26%)   [measured; interval inferred] | number within tolerance; causes consistent with gold | completeness:could_not_run, fanout:pass/fail | unverified (custom agent) | unverified (custom agent) |
| f8 full #3 | ✓ | +36.97 percent (95% interval: 36.68–37.26 percent)   [measured] | number within tolerance; causes consistent with gold | completeness:could_not_run, fanout:pass/pass | unverified (custom agent) | unverified (custom agent) |
