# Eval summary: 2026-10-13-seed

**Verdict:** INSUFFICIENT_N (smoke test, not a decision). 5 fixtures; the pass rule needs 15. Rule outcome at this n: FAIL.

## Fixtures by majority vote

| Fixture | Kind | baseline | checks | full |
|---|---|---|---|---|
| f1 | error | ✓ (3/3) | ✓ (3/3) | ✓ (3/3) |
| f2 | error | ✓ (3/3) | ✓ (3/3) | ✓ (3/3) |
| f3 | clean | ✓ (3/3) | ✗ false_alarm (1/3) | ✓ (3/3) |
| f4 | abstain | ✓ (3/3) | ✓ (3/3) | ✓ (3/3) |
| f5 | abstain | ✓ (3/3) | ✓ (3/3) | ✓ (3/3) |

## Per arm

| Metric | baseline | checks | full |
|---|---|---|---|
| fixtures_correct | 5 | 4 | 5 |
| fixtures_false_alarm | 0 | 1 | 0 |
| fixtures_abstain_answered | 0 | 0 | 0 |
| fixtures_incomplete | 0 | 0 | 0 |
| runs_correct | 15 | 13 | 15 |
| runs | 15 | 15 | 15 |
| runs_unparseable | 0 | 0 | 0 |
| runs_contaminated | 0 | 0 | 0 |
| runs_unverified_isolation | 0 | 0 | 0 |
| dropped_alternative_lines | 9 | 12 | 16 |
| runs_with_any_check | 0 | 15 | 15 |
| runs_reading_skill | 0 | 0 | 14 |
| cost_usd | 0.97 | 1.15 | 2.11 |

## Every run

| Run | Correct | Headline | Reason | Checks that ran |
|---|---|---|---|---|
| f1 baseline #1 | ✓ | +0.00 pp (95% CI about -0.15 to +0.15 pp) from v2's within-segment eff | number within tolerance; causes consistent with gold | none |
| f1 baseline #2 | ✓ | 0.0 pp (95% CI -0.15 to +0.15 pp) attributable to v2. The overall chan | number within tolerance; causes consistent with gold | none |
| f1 baseline #3 | ✓ | +0.00 pp (95% CI -0.15 to +0.15) from v2's effect on CTR within platfo | number within tolerance; causes consistent with gold | none |
| f1 checks #1 | ✓ | about 0.0 pp (95% interval -0.15 to +0.15 pp) [measured] | number within tolerance; causes consistent with gold | mix_shift:flag, completeness:pass |
| f1 checks #2 | ✓ | about 0.0 pp (95% interval -0.15 to +0.15 pp) attributable to v2. [mea | number within tolerance; causes consistent with gold | mix_shift:flag, completeness:pass |
| f1 checks #3 | ✓ | about 0.0 pp attributable to v2 (95% interval -0.15 to +0.15 pp) [meas | number within tolerance; causes consistent with gold | mix_shift:flag, completeness:pass |
| f1 full #1 | ✓ | -0.00 pp (95% interval -0.15 to +0.15 pp) attributable to v2, within-s | number within tolerance; causes consistent with gold | mix_shift:flag/flag, completeness:pass/pass |
| f1 full #2 | ✓ | -0.00 pp attributable to v2 within segments (95% CI -0.15 to +0.15 pp) | number within tolerance; causes consistent with gold | completeness:pass, mix_shift:flag/flag/flag |
| f1 full #3 | ✓ | -0.00 pp attributable to v2 (95% interval -0.15 to +0.15 pp) | number within tolerance; causes consistent with gold | mix_shift:flag/flag, completeness:pass |
| f2 baseline #1 | ✓ | 55.0 % (95% CI 54.9 to 55.0) | number within tolerance; causes consistent with gold | none |
| f2 baseline #2 | ✓ | 55.0 % (95% CI 54.9 to 55.0) | number within tolerance; causes consistent with gold | none |
| f2 baseline #3 | ✓ | 55.0 % (95% CI 54.9 to 55.0, query-level bootstrap) | number within tolerance; causes consistent with gold | none |
| f2 checks #1 | ✓ | 55.0 % (95% interval 54.9 to 55.0) | number within tolerance; causes consistent with gold | completeness:could_not_run, fanout:pass |
| f2 checks #2 | ✓ | 55.0 % (95% CI 54.97 to 55.03 %) | number within tolerance; causes consistent with gold | fanout:pass, completeness:could_not_run |
| f2 checks #3 | ✓ | 55.0 % (54.9 to 55.0 %) | number within tolerance; causes consistent with gold | fanout:pass, completeness:could_not_run |
| f2 full #1 | ✓ | 55.0 % click-through rate for navigational queries in 2026-W40 (95% CI | number within tolerance; causes consistent with gold | fanout:pass/fail, completeness:could_not_run |
| f2 full #2 | ✓ | 55.0 percent (54.6 to 55.4) | number within tolerance; causes consistent with gold | fanout:pass/fail, completeness:could_not_run |
| f2 full #3 | ✓ | 55.0 % (54.6 % to 55.4 %) | number within tolerance; causes consistent with gold | fanout:pass/fail, completeness:could_not_run |
| f3 baseline #1 | ✓ | -1.83 pp (95% CI -1.98 to -1.68), the full week-over-week drop, with v | number within tolerance; causes consistent with gold | none |
| f3 baseline #2 | ✓ | -1.83 percentage points (95% CI -1.98 to -1.68), as the raw week-over- | number within tolerance; causes consistent with gold | none |
| f3 baseline #3 | ✓ | -1.83 percentage points (95% interval -1.98 to -1.68). This is the who | number within tolerance; causes consistent with gold | none |
| f3 checks #1 | ✗ | can't tell | abstained on a case with a valid answer | mix_shift:pass, completeness:could_not_run |
| f3 checks #2 | ✓ | -1.83 pp overall CTR (95% interval -1.98 to -1.68) is the observed wee | number within tolerance; causes consistent with gold | mix_shift:pass, completeness:pass |
| f3 checks #3 | ✗ | can't tell | abstained on a case with a valid answer | completeness:pass, mix_shift:pass |
| f3 full #1 | ✓ | -1.83 pp overall CTR, week of 09-07 vs week of 08-31 (95% CI -1.98 to  | number within tolerance; causes consistent with gold | mix_shift:pass/pass, completeness:pass |
| f3 full #2 | ✓ | -1.83 pp (95% CI -1.98 to -1.68) | number within tolerance; causes consistent with gold | mix_shift:pass/pass, completeness:could_not_run/fail/pass |
| f3 full #3 | ✓ | -1.83 pp overall CTR change, week over week (95% interval -1.98 to -1. | number within tolerance; causes consistent with gold | mix_shift:pass/pass, completeness:pass |
| f4 baseline #1 | ✓ | can't tell (for the full day). The 2026-10-07 data stops at hour 9, an | abstained (accepted) | none |
| f4 baseline #2 | ✓ | can't tell. There is no complete day for 2026-10-07 yet. | abstained (accepted) | none |
| f4 baseline #3 | ✓ | can't tell yet (like-for-like, the change is 0.0 pp, 95% interval -0.7 | abstained (accepted) | none |
| f4 checks #1 | ✓ | can't tell. The 2026-10-07 data is only partly loaded. On a like-for-l | abstained (accepted) | completeness:fail |
| f4 checks #2 | ✓ | can't tell | abstained (accepted) | completeness:fail |
| f4 checks #3 | ✓ | can't tell. The like-for-like change is 0.0 pp (95% interval about -0. | abstained (accepted) | completeness:fail, mix_shift:pass/pass |
| f4 full #1 | ✓ | 0.0 pp (-0.66 to +0.66 pp) | number within tolerance; causes consistent with gold | completeness:fail, mix_shift:pass/could_not_run |
| f4 full #2 | ✓ | 0.0 pp (-0.66 to +0.66 pp) like-for-like on hours 0-9 | number within tolerance; causes consistent with gold | completeness:fail, mix_shift:pass |
| f4 full #3 | ✓ | 0.0 pp (-0.66 to +0.66 pp) | number within tolerance; causes consistent with gold | completeness:fail, mix_shift:pass/could_not_run |
| f5 baseline #1 | ✓ | can't tell | abstained (accepted) | none |
| f5 baseline #2 | ✓ | can't tell | abstained (accepted) | none |
| f5 baseline #3 | ✓ | can't tell | abstained (accepted) | none |
| f5 checks #1 | ✓ | can't tell | abstained (accepted) | srm:fail, completeness:could_not_run |
| f5 checks #2 | ✓ | can't tell | abstained (accepted) | srm:fail, completeness:could_not_run |
| f5 checks #3 | ✓ | can't tell | abstained (accepted) | srm:fail, completeness:could_not_run |
| f5 full #1 | ✓ | can't tell | abstained (accepted) | srm:fail, completeness:pass |
| f5 full #2 | ✓ | can't tell | abstained (accepted) | srm:fail, completeness:pass |
| f5 full #3 | ✓ | can't tell | abstained (accepted) | srm:fail/fail, completeness:pass |
