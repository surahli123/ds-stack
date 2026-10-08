# Eval summary: 2026-10-08-smoke-r2

**Verdict:** INSUFFICIENT_N (smoke test, not a decision). 5 fixtures; the pass rule needs 15. Rule outcome at this n: FAIL.

## Fixtures by majority vote

| Fixture | Kind | baseline | checks | full |
|---|---|---|---|---|
| f1 | error | ✓ (3/3) | ✓ (3/3) | ✓ (3/3) |
| f2 | error | ✓ (3/3) | ✓ (3/3) | ✓ (3/3) |
| f3 | clean | ✓ (3/3) | ✓ (2/3) | ✓ (3/3) |
| f4 | abstain | ✓ (3/3) | ✓ (3/3) | ✓ (3/3) |
| f5 | abstain | ✓ (3/3) | ✓ (3/3) | ✓ (3/3) |

## Per arm

| Metric | baseline | checks | full |
|---|---|---|---|
| fixtures_correct | 5 | 5 | 5 |
| fixtures_false_alarm | 0 | 0 | 0 |
| fixtures_abstain_answered | 0 | 0 | 0 |
| fixtures_incomplete | 0 | 0 | 0 |
| runs_correct | 15 | 14 | 15 |
| runs | 15 | 15 | 15 |
| runs_unparseable | 0 | 0 | 0 |
| runs_contaminated | 0 | 0 | 0 |
| dropped_alternative_lines | 8 | 14 | 16 |
| runs_with_any_check | 0 | 15 | 15 |
| runs_reading_skill | 0 | 0 | 14 |
| cost_usd | 0.97 | 1.14 | 1.34 |

## Every run

| Run | Correct | Headline | Reason | Checks that ran |
|---|---|---|---|---|
| f1 baseline #1 | ✓ | about 0 pp (measured: within-segment CTR is unchanged, so the v2 effec | number within tolerance; causes consistent with gold | none |
| f1 baseline #2 | ✓ | about 0.0 pp attributable to v2 (within-segment change: 0.00 pp in all | number within tolerance; causes consistent with gold | none |
| f1 baseline #3 | ✓ | 0.0 percentage points attributable to v2 on a like-for-like basis. The | number within tolerance; causes consistent with gold | none |
| f1 checks #1 | ✓ | about 0.0 pp attributable to v2 (within-platform change -0.0001 pp, me | number within tolerance; causes consistent with gold | mix_shift:fail, completeness:pass |
| f1 checks #2 | ✓ | about 0.0 pp attributable to v2 (within-segment effect -0.0001 pp, rou | number within tolerance; causes consistent with gold | mix_shift:fail, completeness:pass |
| f1 checks #3 | ✓ | about 0.0 pp attributable to v2 (within-segment effect -0.0001 pp). Th | number within tolerance; causes consistent with gold | mix_shift:fail, completeness:pass |
| f1 full #1 | ✓ | about 0.0 pp attributable to v2 (within-segment effect -0.0001 pp; the | number within tolerance; causes consistent with gold | mix_shift:fail, completeness:pass |
| f1 full #2 | ✓ | -0.00 pp attributable to v2 (within-segment effect -0.0001 pp; overall | number within tolerance; causes consistent with gold | mix_shift:fail, completeness:pass |
| f1 full #3 | ✓ | about 0.0 pp attributable to v2 (within-segment change -0.0001 pp; ove | number within tolerance; causes consistent with gold | completeness:pass, mix_shift:fail |
| f2 baseline #1 | ✓ | 55.0 % (pooled clicks ÷ searches) | number within tolerance; causes consistent with gold | none |
| f2 baseline #2 | ✓ | 55.0 % click-through rate for navigational queries in 2026-W40 | number within tolerance; causes consistent with gold | none |
| f2 baseline #3 | ✓ | 55.0 % click-through rate for navigational queries in 2026-W40 | number within tolerance; causes consistent with gold | none |
| f2 checks #1 | ✓ | 55.0 % (32,878 clicks / 59,800 searches) | number within tolerance; causes consistent with gold | fanout:pass, completeness:could_not_run |
| f2 checks #2 | ✓ | 55.0 % (navigational click-through rate, 2026-W40) | number within tolerance; causes consistent with gold | fanout:pass, completeness:could_not_run |
| f2 checks #3 | ✓ | 55.0% click-through rate for navigational queries in 2026-W40 | number within tolerance; causes consistent with gold | fanout:pass, completeness:could_not_run |
| f2 full #1 | ✓ | 54.98 % click-through rate for navigational queries in 2026-W40 | number within tolerance; causes consistent with gold | fanout:pass, completeness:could_not_run |
| f2 full #2 | ✓ | 55.0 % click-through rate for navigational queries in 2026-W40 (32,878 | number within tolerance; causes consistent with gold | fanout:pass/fail, completeness:could_not_run |
| f2 full #3 | ✓ | 55.0% (click-through rate of navigational queries, 2026-W40) | number within tolerance; causes consistent with gold | fanout:pass, completeness:could_not_run |
| f3 baseline #1 | ✓ | -1.80 pp overall CTR (30.42% → 28.62%), with no interval. Treat all of | number within tolerance; causes consistent with gold | none |
| f3 baseline #2 | ✓ | -1.80 pp (overall CTR 30.42% → 28.62%; essentially all of it attribute | number within tolerance; causes consistent with gold | none |
| f3 baseline #3 | ✓ | -1.80 pp (overall CTR 30.42% → 28.62%; no interval, since there is no  | number within tolerance; causes consistent with gold | none |
| f3 checks #1 | ✓ | -1.80 percentage points (overall CTR 30.42% → 28.62%). Nothing else in | number within tolerance; causes consistent with gold | mix_shift:pass, completeness:pass |
| f3 checks #2 | ✓ | -1.80 pp (overall CTR 30.42% → 28.62%; no interval, since the data is  | number within tolerance; causes consistent with gold | mix_shift:pass, completeness:could_not_run |
| f3 checks #3 | ✗ | can't tell | abstained on a case with a valid answer | mix_shift:pass, completeness:could_not_run |
| f3 full #1 | ✓ | -1.80 pp overall CTR, week over week (30.42% → 28.62%). I can't separa | number within tolerance; causes consistent with gold | completeness:pass, mix_shift:pass |
| f3 full #2 | ✓ | -1.80 pp (week-over-week CTR change, 30.42% → 28.62%). This is the who | number within tolerance; causes consistent with gold | completeness:pass, mix_shift:pass |
| f3 full #3 | ✓ | -1.80 pp (no statistical interval: this is a single before/after compa | number within tolerance; causes consistent with gold | mix_shift:pass, completeness:could_not_run |
| f4 baseline #1 | ✓ | can't tell | abstained (accepted) | none |
| f4 baseline #2 | ✓ | 0.0 percentage points (like-for-like, hours 0–9: 27.0% vs 27.0%) | number within tolerance; causes consistent with gold | none |
| f4 baseline #3 | ✓ | 0.0 percentage points (like-for-like, hours 00–09) | number within tolerance; causes consistent with gold | none |
| f4 checks #1 | ✓ | can't tell. The like-for-like change is 0.0 pp, and the full-day drop  | abstained (accepted) | completeness:fail |
| f4 checks #2 | ✓ | can't tell. The like-for-like change so far is 0.0 pp, and the day is  | abstained (accepted) | completeness:fail |
| f4 checks #3 | ✓ | 0.0 percentage points (like-for-like, hours 0–9: 27.0% yesterday vs 27 | number within tolerance; causes consistent with gold | completeness:fail |
| f4 full #1 | ✓ | can't tell (the apparent -2.8 pp is not a real drop; like-for-like it  | abstained (accepted) | completeness:fail/fail, mix_shift:pass |
| f4 full #2 | ✓ | 0.0 percentage points (like-for-like, hours 0–9). The apparent drop of | number within tolerance; causes consistent with gold | completeness:fail/fail, mix_shift:could_not_run/pass |
| f4 full #3 | ✓ | 0.0 percentage points on a like-for-like basis (hours 0–9 of 2026-10-0 | number within tolerance; causes consistent with gold | completeness:fail, mix_shift:pass |
| f5 baseline #1 | ✓ | can't tell | abstained (accepted) | none |
| f5 baseline #2 | ✓ | can't tell | abstained (accepted) | none |
| f5 baseline #3 | ✓ | can't tell | abstained (accepted) | none |
| f5 checks #1 | ✓ | can't tell | abstained (accepted) | srm:fail, completeness:pass |
| f5 checks #2 | ✓ | can't tell | abstained (accepted) | srm:fail/fail, completeness:could_not_run |
| f5 checks #3 | ✓ | can't tell | abstained (accepted) | srm:fail, completeness:could_not_run |
| f5 full #1 | ✓ | can't tell | abstained (accepted) | srm:fail, completeness:pass |
| f5 full #2 | ✓ | can't tell | abstained (accepted) | srm:fail, completeness:pass |
| f5 full #3 | ✓ | can't tell | abstained (accepted) | srm:fail, completeness:pass |
