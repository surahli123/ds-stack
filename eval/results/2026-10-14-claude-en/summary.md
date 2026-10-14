# Eval summary: 2026-10-14-claude-en

**Verdict:** INSUFFICIENT_N (smoke test, not a decision). 8 fixtures; the pass rule needs 15. Rule outcome at this n: PASS.

## Fixtures by majority vote

| Fixture | Kind | baseline | checks | full |
|---|---|---|---|---|
| f1 | error | ✗ miss (1/3) | ✗ miss (0/3) | ✓ (3/3) |
| f2 | error | ✓ (3/3) | ✓ (3/3) | ✓ (2/3) |
| f3 | clean | ✗ false_alarm (0/3) | ✗ false_alarm (0/3) | ✓ (3/3) |
| f4 | abstain | ✓ (3/3) | ✓ (3/3) | ✓ (3/3) |
| f5 | abstain | ✓ (3/3) | ✓ (3/3) | ✓ (3/3) |
| f6 | error | ✗ miss (0/3) | ✗ miss (0/3) | ✓ (3/3) |
| f7 | abstain | ✗ answered_abstain_case (0/3) | ✗ answered_abstain_case (0/3) | ✓ (3/3) |
| f8 | error | ✓ (3/3) | ✓ (3/3) | ✓ (3/3) |

## Per arm

| Metric | baseline | checks | full |
|---|---|---|---|
| fixtures_correct | 4 | 4 | 8 |
| fixtures_false_alarm | 1 | 1 | 0 |
| fixtures_abstain_answered | 1 | 1 | 0 |
| fixtures_incomplete | 0 | 0 | 0 |
| runs_correct | 13 | 12 | 23 |
| runs | 24 | 24 | 24 |
| runs_unparseable | 0 | 0 | 1 |
| runs_contaminated | 0 | 0 | 0 |
| runs_unverified_isolation | 0 | 0 | 0 |
| dropped_alternative_lines | 17 | 18 | 25 |
| runs_with_any_check | 0 | 24 | 24 |
| runs_reading_skill | 0 | 0 | 22 |
| cost_usd | 1.54 | 1.85 | 3.37 |

## Every run

| Run | Correct | Headline | Reason | Checks that ran |
|---|---|---|---|---|
| f1 baseline #1 | ✓ | ≈0.0 pp (about -0.8 to +0.3 pp at most, by the segment-adjusted estima | number within tolerance; causes consistent with gold | none |
| f1 baseline #2 | ✗ | can't tell. The data gives no sign that v2 lowered CTR, but a rollout  | abstained on a case with a valid answer | none |
| f1 baseline #3 | ✗ | can't tell | abstained on a case with a valid answer | none |
| f1 checks #1 | ✗ | can't tell (the data can't separate v2 from the week-to-week change in | abstained on a case with a valid answer | mix_shift:flag, completeness:pass |
| f1 checks #2 | ✗ | can't tell | abstained on a case with a valid answer | mix_shift:flag, completeness:pass |
| f1 checks #3 | ✗ | can't tell | abstained on a case with a valid answer | mix_shift:flag, completeness:pass |
| f1 full #1 | ✓ | -0.00 pp (-0.15 to +0.15) | number within tolerance; causes consistent with gold | mix_shift:flag/flag, completeness:pass |
| f1 full #2 | ✓ | -0.00 pp (-0.15 to +0.15) | number within tolerance; causes consistent with gold | mix_shift:flag/flag, completeness:pass |
| f1 full #3 | ✓ | -0.00 pp (-0.15 to +0.15) | number within tolerance; causes consistent with gold | completeness:pass, mix_shift:flag/flag |
| f2 baseline #1 | ✓ | 55.0 % (54.6 to 55.4 %) | number within tolerance; causes consistent with gold | none |
| f2 baseline #2 | ✓ | 54.98 % (95% CI 54.95 to 55.01, query-level bootstrap) | number within tolerance; causes consistent with gold | none |
| f2 baseline #3 | ✓ | 54.98 % (54.95 to 55.01) | number within tolerance; causes consistent with gold | none |
| f2 checks #1 | ✓ | 55.0 % (95% CI 54.6 to 55.4) | number within tolerance; causes consistent with gold | fanout:pass, completeness:could_not_run |
| f2 checks #2 | ✓ | 55.0 % (54.6 to 55.4 %) | number within tolerance; causes consistent with gold | completeness:could_not_run, fanout:pass |
| f2 checks #3 | ✓ | 55.0% (95% CI 54.6% to 55.4%) | number within tolerance; causes consistent with gold | completeness:could_not_run, fanout:pass |
| f2 full #1 | ✓ | 55.0 % (54.6 to 55.4) | number within tolerance; causes consistent with gold | fanout:could_not_run/pass, completeness:could_not_run/could_not_run |
| f2 full #2 | ✓ | 55.0 % (54.6 % to 55.4 %) | number within tolerance; causes consistent with gold | fanout:pass, completeness:could_not_run |
| f2 full #3 | ✗ | 55.0 % (54.6 to 55.4) | unparseable: none of the 4 alternative lines says 'ruled in' or 'ruled out' | fanout:pass, completeness:could_not_run |
| f3 baseline #1 | ✗ | can't tell. Overall CTR fell 1.83 pp, but a before/after comparison ca | abstained on a case with a valid answer | none |
| f3 baseline #2 | ✗ | can't tell | abstained on a case with a valid answer | none |
| f3 baseline #3 | ✗ | can't tell. The data can't separate v3 from anything else that changed | abstained on a case with a valid answer | none |
| f3 checks #1 | ✗ | can't tell | abstained on a case with a valid answer | mix_shift:pass, completeness:pass |
| f3 checks #2 | ✗ | can't tell | abstained on a case with a valid answer | mix_shift:pass, completeness:pass |
| f3 checks #3 | ✗ | can't tell | abstained on a case with a valid answer | mix_shift:pass, completeness:pass |
| f3 full #1 | ✓ | -1.82 pp (95% CI -1.97 to -1.67) | number within tolerance; causes consistent with gold | mix_shift:pass/pass, completeness:pass |
| f3 full #2 | ✓ | -1.82 pp (-1.97 to -1.67) | number within tolerance; causes consistent with gold | mix_shift:pass/pass, completeness:pass |
| f3 full #3 | ✓ | -1.82 pp (95% CI -1.97 to -1.67) | number within tolerance; causes consistent with gold | completeness:could_not_run, mix_shift:pass/pass |
| f4 baseline #1 | ✓ | can't tell. The apparent drop is not real on a like-for-like basis (ab | abstained (accepted) | none |
| f4 baseline #2 | ✓ | can't tell. The data doesn't show a real drop. | abstained (accepted) | none |
| f4 baseline #3 | ✓ | 0.0 pp (95% interval about -0.7 to +0.7 pp). There is no real drop in  | number within tolerance; causes consistent with gold | none |
| f4 checks #1 | ✓ | can't tell (the raw gap is a partial-day artifact; the like-for-like g | abstained (accepted) | completeness:fail, mix_shift:pass |
| f4 checks #2 | ✓ | 0.0 pp (95% interval -0.7 to +0.7 pp), like-for-like on hours 0–9 | number within tolerance; causes consistent with gold | completeness:fail, mix_shift:pass |
| f4 checks #3 | ✓ | can't tell | abstained (accepted) | completeness:fail, mix_shift:pass |
| f4 full #1 | ✓ | can't tell | abstained (accepted) | completeness:fail/fail, mix_shift:pass |
| f4 full #2 | ✓ | +0.0 pp (-0.66 to +0.66) | number within tolerance; causes consistent with gold | completeness:fail, mix_shift:pass |
| f4 full #3 | ✓ | 0.00 pp (-0.66 to +0.66 pp) | number within tolerance; causes consistent with gold | completeness:could_not_run/fail, mix_shift:pass |
| f5 baseline #1 | ✓ | can't tell | abstained (accepted) | none |
| f5 baseline #2 | ✓ | can't tell | abstained (accepted) | none |
| f5 baseline #3 | ✓ | can't tell (the arms are unbalanced, so the +1.20 pp gap can't be cred | abstained (accepted) | none |
| f5 checks #1 | ✓ | can't tell | abstained (accepted) | srm:fail, completeness:could_not_run |
| f5 checks #2 | ✓ | can't tell | abstained (accepted) | srm:fail, completeness:could_not_run |
| f5 checks #3 | ✓ | can't tell | abstained (accepted) | srm:fail, completeness:could_not_run/pass |
| f5 full #1 | ✓ | can't tell | abstained (accepted) | completeness:pass, srm:fail |
| f5 full #2 | ✓ | can't tell | abstained (accepted) | srm:fail, completeness:pass |
| f5 full #3 | ✓ | can't tell | abstained (accepted) | srm:fail, completeness:pass |
| f6 baseline #1 | ✗ | 46.1 % (95% CI 45.9 to 46.3) | headline 46.1 outside 50.053±0.3 | none |
| f6 baseline #2 | ✗ | 46.0% (95% CI 45.9% to 46.2%) | headline 46 outside 50.053±0.3 | none |
| f6 baseline #3 | ✗ | 46.0 % (95% CI 45.9 to 46.2), search CTR for 2026-10-05 to 2026-10-11  | headline 46 outside 50.053±0.3 | none |
| f6 checks #1 | ✗ | 46.0 % (95% CI 45.9 to 46.2), search CTR for 2026-10-05 to 2026-10-11, | headline 46 outside 50.053±0.3 | completeness:pass |
| f6 checks #2 | ✗ | 46.0 % (95% CI 45.9 to 46.2) | headline 46 outside 50.053±0.3 | completeness:pass |
| f6 checks #3 | ✗ | 46.0% (no interval; this is a full-population rate, not a sample estim | headline 46 outside 50.053±0.3 | completeness:pass |
| f6 full #1 | ✓ | +50.05 % CTR (95% CI 49.93 to 50.17) | number within tolerance; causes consistent with gold | completeness:pass |
| f6 full #2 | ✓ | 50.05 % (49.93 to 50.18 %) | number within tolerance; causes consistent with gold | completeness:pass |
| f6 full #3 | ✓ | +50.05 percent CTR (49.93 to 50.18) | number within tolerance; causes consistent with gold | completeness:pass |
| f7 baseline #1 | ✗ | 8.30 % of searches led to a purchase (95% CI 8.24 to 8.36) | answered 8.3 where the right answer is can't tell | none |
| f7 baseline #2 | ✗ | 8.30 % of searches led to a purchase (95% CI 8.24 to 8.36) | answered 8.3 where the right answer is can't tell | none |
| f7 baseline #3 | ✗ | 8.30 % of searches led to a purchase (95% CI 8.24 to 8.36) | answered 8.3 where the right answer is can't tell | none |
| f7 checks #1 | ✗ | 8.30 % of searches led to a purchase (95% CI 8.24 to 8.36 %) | answered 8.3 where the right answer is can't tell | completeness:pass |
| f7 checks #2 | ✗ | 8.30 percent (95% CI 8.24 to 8.36) | answered 8.3 where the right answer is can't tell | completeness:pass |
| f7 checks #3 | ✗ | 8.30 % (95% interval 8.24 to 8.36 %) | answered 8.3 where the right answer is can't tell | completeness:pass |
| f7 full #1 | ✓ | can't tell | abstained (accepted) | completeness:could_not_run |
| f7 full #2 | ✓ | can't tell | abstained (accepted) | completeness:pass |
| f7 full #3 | ✓ | can't tell | abstained (accepted) | completeness:pass |
| f8 baseline #1 | ✓ | 36.97 % (no interval: this is a full count, not a sample) | number within tolerance; causes consistent with gold | none |
| f8 baseline #2 | ✓ | 36.97 % (95% CI 36.68 to 37.26) | number within tolerance; causes consistent with gold | none |
| f8 baseline #3 | ✓ | 36.97 % (95% CI 36.68 to 37.26) | number within tolerance; causes consistent with gold | none |
| f8 checks #1 | ✓ | 36.97 % (95% CI 36.68 to 37.26) | number within tolerance; causes consistent with gold | fanout:pass/fail, completeness:could_not_run |
| f8 checks #2 | ✓ | 36.97 % (interval not computed; this is a full count of the data, not  | number within tolerance; causes consistent with gold | fanout:fail/pass, completeness:could_not_run |
| f8 checks #3 | ✓ | 36.97 % (no interval: this is a full-population rate, not a sample est | number within tolerance; causes consistent with gold | fanout:pass/fail, completeness:could_not_run |
| f8 full #1 | ✓ | +36.97 % click-through rate (95% CI 36.68 to 37.26) | number within tolerance; causes consistent with gold | fanout:fail, completeness:could_not_run |
| f8 full #2 | ✓ | 36.97 % (36.68 to 37.26) | number within tolerance; causes consistent with gold | fanout:fail/pass, completeness:could_not_run |
| f8 full #3 | ✓ | +36.97 % click-through rate (36.68 to 37.26) | number within tolerance; causes consistent with gold | fanout:fail/pass, completeness:could_not_run |
