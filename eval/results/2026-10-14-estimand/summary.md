# Eval summary: 2026-10-14-estimand

**Verdict:** INSUFFICIENT_N (smoke test, not a decision). 5 fixtures; the pass rule needs 15. Rule outcome at this n: FAIL.

## Fixtures by majority vote

| Fixture | Kind | baseline | checks | full |
|---|---|---|---|---|
| f1 | error | ✓ (2/3) | ✗ miss (0/3) | ✓ (3/3) |
| f2 | error | ✓ (3/3) | ✓ (3/3) | ✓ (3/3) |
| f3 | clean | ✗ false_alarm (1/3) | ✗ false_alarm (0/3) | ✓ (3/3) |
| f4 | abstain | ✓ (3/3) | ✓ (3/3) | ✓ (3/3) |
| f5 | abstain | ✓ (3/3) | ✓ (3/3) | ✓ (3/3) |

## Per arm

| Metric | baseline | checks | full |
|---|---|---|---|
| fixtures_correct | 4 | 3 | 5 |
| fixtures_false_alarm | 1 | 1 | 0 |
| fixtures_abstain_answered | 0 | 0 | 0 |
| fixtures_incomplete | 0 | 0 | 0 |
| runs_correct | 12 | 9 | 15 |
| runs | 15 | 15 | 15 |
| runs_unparseable | 0 | 0 | 0 |
| runs_contaminated | 0 | 0 | 0 |
| runs_unverified_isolation | 0 | 0 | 0 |
| dropped_alternative_lines | 14 | 13 | 23 |
| runs_with_any_check | 0 | 15 | 15 |
| runs_reading_skill | 0 | 0 | 14 |
| cost_usd | 1.02 | 1.18 | 2.24 |

## Every run

| Run | Correct | Headline | Reason | Checks that ran |
|---|---|---|---|---|
| f1 baseline #1 | ✓ | -0.01 pp (±0.16 pp) is the mix-adjusted change in CTR. This is not a c | number within tolerance; causes consistent with gold | none |
| f1 baseline #2 | ✓ | about 0.0 pp (-0.15 to +0.15 pp) attributable to v2, on a mix-adjusted | number within tolerance; causes consistent with gold | none |
| f1 baseline #3 | ✗ | can't tell | abstained on a case with a valid answer | none |
| f1 checks #1 | ✗ | can't tell (a causal effect isn't identified, but the within-segment c | abstained on a case with a valid answer | mix_shift:flag, completeness:pass |
| f1 checks #2 | ✗ | can't tell. The overall drop is -2.10 pp (-2.25 to -1.95), but almost  | abstained on a case with a valid answer | mix_shift:flag, completeness:pass |
| f1 checks #3 | ✗ | can't tell | abstained on a case with a valid answer | mix_shift:flag, completeness:pass |
| f1 full #1 | ✓ | -0.00 pp (-0.15 to +0.15) | number within tolerance; causes consistent with gold | completeness:pass, mix_shift:flag/flag |
| f1 full #2 | ✓ | -0.00 pp (-0.15 to +0.15) | number within tolerance; causes consistent with gold | completeness:fail/pass, mix_shift:flag/flag |
| f1 full #3 | ✓ | -0.00 pp (-0.15 to +0.15) | number within tolerance; causes consistent with gold | mix_shift:flag/flag, completeness:fail/pass |
| f2 baseline #1 | ✓ | 54.98 % (95% CI 54.6 to 55.4) | number within tolerance; causes consistent with gold | none |
| f2 baseline #2 | ✓ | 55.0 % (95% CI 54.6 to 55.4) | number within tolerance; causes consistent with gold | none |
| f2 baseline #3 | ✓ | 55.0 % (95% CI 54.9 to 55.0) | number within tolerance; causes consistent with gold | none |
| f2 checks #1 | ✓ | 54.98 % (no interval computed; this is a full-week count, not a sample | number within tolerance; causes consistent with gold | fanout:pass, completeness:could_not_run |
| f2 checks #2 | ✓ | 55.0 % (54.6 to 55.4 %, binomial interval that ignores query-level clu | number within tolerance; causes consistent with gold | fanout:pass, completeness:could_not_run |
| f2 checks #3 | ✓ | 54.98 percent (interval not computed: the data is weekly aggregates wi | number within tolerance; causes consistent with gold | fanout:pass, completeness:could_not_run |
| f2 full #1 | ✓ | 55.0 % (54.6 to 55.4) | number within tolerance; causes consistent with gold | fanout:could_not_run/pass, completeness:could_not_run/could_not_run |
| f2 full #2 | ✓ | 54.98 % (54.58 to 55.38) | number within tolerance; causes consistent with gold | fanout:pass, completeness:could_not_run |
| f2 full #3 | ✓ | 54.98 % (54.95 to 55.01) | number within tolerance; causes consistent with gold | fanout:pass, completeness:could_not_run |
| f3 baseline #1 | ✓ | -1.80 pp (95% CI -1.95 to -1.65) | number within tolerance; causes consistent with gold | none |
| f3 baseline #2 | ✗ | can't tell. Overall CTR fell 1.83 pp (95% CI -2.06 to -1.59), but this | abstained on a case with a valid answer | none |
| f3 baseline #3 | ✗ | can't tell. The observed change is -1.83 pp (±0.15), and the data can' | abstained on a case with a valid answer | none |
| f3 checks #1 | ✗ | can't tell | abstained on a case with a valid answer | mix_shift:pass, completeness:pass |
| f3 checks #2 | ✗ | can't tell | abstained on a case with a valid answer | mix_shift:pass, completeness:pass |
| f3 checks #3 | ✗ | can't tell | abstained on a case with a valid answer | mix_shift:pass, completeness:pass |
| f3 full #1 | ✓ | -1.82 pp (-1.97 to -1.67) | number within tolerance; causes consistent with gold | completeness:could_not_run, mix_shift:pass/pass |
| f3 full #2 | ✓ | -1.82 pp (-1.97 to -1.67) | number within tolerance; causes consistent with gold | mix_shift:pass/pass, completeness:pass |
| f3 full #3 | ✓ | -1.82 pp (-1.97 to -1.67) | number within tolerance; causes consistent with gold | mix_shift:pass/pass, completeness:pass |
| f4 baseline #1 | ✓ | can't tell. The -2.8 pp drop is an artifact of comparing a partial day | abstained (accepted) | none |
| f4 baseline #2 | ✓ | can't tell. Yesterday's data stops at hour 09, so the full-day figure  | abstained (accepted) | none |
| f4 baseline #3 | ✓ | can't tell. Yesterday's data is incomplete, so there is no valid full- | abstained (accepted) | none |
| f4 checks #1 | ✓ | can't tell (2026-10-07 is only partly loaded, so there's no valid full | abstained (accepted) | completeness:fail, mix_shift:could_not_run/flag |
| f4 checks #2 | ✓ | can't tell. The "drop" is a partial-day artifact, and the like-for-lik | abstained (accepted) | completeness:fail |
| f4 checks #3 | ✓ | 0.0 pp (95% interval -0.7 to +0.7), measured on hours 00–09 only. Hour | number within tolerance; causes consistent with gold | completeness:fail, mix_shift:pass |
| f4 full #1 | ✓ | +0.0 pp (-0.66 to +0.66) on hours 0-9, the only hours logged for 2026- | number within tolerance; causes consistent with gold | completeness:fail, mix_shift:pass/could_not_run |
| f4 full #2 | ✓ | 0.00 pp (-0.66 to +0.66) | number within tolerance; causes consistent with gold | completeness:fail, mix_shift:pass |
| f4 full #3 | ✓ | +0.0 pp (-0.66 to +0.66) | number within tolerance; causes consistent with gold | completeness:fail, mix_shift:pass |
| f5 baseline #1 | ✓ | can't tell | abstained (accepted) | none |
| f5 baseline #2 | ✓ | can't tell. The observed CTR difference is +1.20 pp, but the arm sizes | abstained (accepted) | none |
| f5 baseline #3 | ✓ | can't tell | abstained (accepted) | none |
| f5 checks #1 | ✓ | can't tell | abstained (accepted) | srm:fail, completeness:could_not_run |
| f5 checks #2 | ✓ | can't tell | abstained (accepted) | srm:fail, completeness:pass |
| f5 checks #3 | ✓ | can't tell | abstained (accepted) | srm:fail, completeness:could_not_run |
| f5 full #1 | ✓ | can't tell | abstained (accepted) | srm:fail, completeness:pass |
| f5 full #2 | ✓ | can't tell | abstained (accepted) | srm:fail, completeness:pass |
| f5 full #3 | ✓ | can't tell | abstained (accepted) | srm:fail, completeness:pass |
