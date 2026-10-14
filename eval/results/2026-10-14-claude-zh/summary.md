# Eval summary: 2026-10-14-claude-zh

**Verdict:** INSUFFICIENT_N (smoke test, not a decision). 8 fixtures; the pass rule needs 15. Rule outcome at this n: PASS.

## Fixtures by majority vote

| Fixture | Kind | baseline | checks | full |
|---|---|---|---|---|
| f1 | error | ✗ unparseable (0/3) | ✗ unparseable (0/3) | ✓ (3/3) |
| f2 | error | ✗ unparseable (1/3) | ✗ unparseable (1/3) | ✓ (2/3) |
| f3 | clean | ✗ unparseable (0/3) | ✗ unparseable (0/3) | ✓ (3/3) |
| f4 | abstain | ✗ unparseable (1/3) | ✗ unparseable (1/3) | ✓ (3/3) |
| f5 | abstain | ✗ unparseable (1/3) | ✗ unparseable (0/3) | ✓ (3/3) |
| f6 | error | ✗ miss (0/3) | ✗ unparseable (0/3) | ✓ (3/3) |
| f7 | abstain | ✗ unparseable (0/3) | ✗ unparseable (0/3) | ✓ (3/3) |
| f8 | error | ✗ unparseable (1/3) | ✗ unparseable (0/3) | ✓ (3/3) |

## Per arm

| Metric | baseline | checks | full |
|---|---|---|---|
| fixtures_correct | 0 | 0 | 8 |
| fixtures_false_alarm | 0 | 0 | 0 |
| fixtures_abstain_answered | 0 | 0 | 0 |
| fixtures_incomplete | 0 | 0 | 0 |
| runs_correct | 4 | 2 | 23 |
| runs | 24 | 24 | 24 |
| runs_unparseable | 17 | 20 | 1 |
| runs_contaminated | 0 | 0 | 0 |
| runs_unverified_isolation | 0 | 0 | 0 |
| dropped_alternative_lines | 73 | 89 | 28 |
| runs_with_any_check | 0 | 24 | 24 |
| runs_reading_skill | 0 | 0 | 23 |
| cost_usd | 1.61 | 1.93 | 3.56 |

## Every run

| Run | Correct | Headline | Reason | Checks that ran |
|---|---|---|---|---|
| f1 baseline #1 | ✗ | 在固定平台×国家构成后,v2 的影响约为 -0.01 个百分点(-0.16 到 +0.15 pp),与零无法区分。 | unparseable: none of the 4 alternative lines says 'ruled in' or 'ruled out' | none |
| f1 baseline #2 | ✗ | -0.01 个百分点 (95% 区间 -0.16 ~ +0.15),这是在固定平台×国家构成后的估计,属于推断 [inferred],不是随 | unparseable: none of the 4 alternative lines says 'ruled in' or 'ruled out' | none |
| f1 baseline #3 | ✗ | can't tell(没有对照组,无法把 v2 的因果效应单独分离出来;但已有证据显示 v2 在各细分内几乎没有影响) | unparseable: none of the 4 alternative lines says 'ruled in' or 'ruled out' | none |
| f1 checks #1 | ✗ | can't tell(v2 的因果效应无法识别;但整体 CTR 的下降几乎全部来自流量结构变化) | abstained on a case with a valid answer | mix_shift:flag, completeness:pass, srm:pass |
| f1 checks #2 | ✗ | can't tell(v2 的因果效应无法识别;按平台×国家调整后,v2 前后的变化约为 -0.00 个百分点) | unparseable: none of the 5 alternative lines says 'ruled in' or 'ruled out' | mix_shift:flag, completeness:pass |
| f1 checks #3 | ✗ | 约 0 个百分点(-0.00 pp,95% 区间 -0.15 to +0.15)——但这是"调整后"的数字,不是因果结论 | unparseable: none of the 4 alternative lines says 'ruled in' or 'ruled out' | mix_shift:flag, completeness:pass |
| f1 full #1 | ✓ | -0.00 pp (-0.15 to +0.15 pp) | number within tolerance; causes consistent with gold | completeness:could_not_run, mix_shift:flag/flag |
| f1 full #2 | ✓ | -0.00 pp (95% 区间 -0.15 到 +0.15 pp),即在平台×国家内部 CTR 基本没变 | number within tolerance; causes consistent with gold | mix_shift:flag/flag, completeness:could_not_run/fail/pass |
| f1 full #3 | ✓ | -0.00 pp (-0.15 to +0.15 pp) | number within tolerance; causes consistent with gold | mix_shift:flag/flag, completeness:pass |
| f2 baseline #1 | ✓ | 55.0 %(95% 区间 54.3 到 55.7) | number within tolerance; causes consistent with gold | none |
| f2 baseline #2 | ✗ | 55.0 %(95% 区间 54.9%–55.0%) | unparseable: none of the 3 alternative lines says 'ruled in' or 'ruled out' | none |
| f2 baseline #3 | ✗ | 54.98 %(95% 区间 54.95–55.01) | unparseable: none of the 3 alternative lines says 'ruled in' or 'ruled out' | none |
| f2 checks #1 | ✗ | 54.98%(95% 区间 54.58%–55.38%) | unparseable: none of the 4 alternative lines says 'ruled in' or 'ruled out' | fanout:pass/fail, completeness:could_not_run |
| f2 checks #2 | ✗ | 55.0%(95% 区间 54.6%–55.4%) | unparseable: none of the 3 alternative lines says 'ruled in' or 'ruled out' | fanout:pass, completeness:could_not_run |
| f2 checks #3 | ✓ | 55.0 % (95% 区间 54.6%–55.4%) | number within tolerance; causes consistent with gold | fanout:pass, completeness:could_not_run |
| f2 full #1 | ✗ | +54.98 pp (54.58 to 55.38) | headline has no number in percent | fanout:pass, completeness:could_not_run |
| f2 full #2 | ✓ | +54.98 % (95% 区间 54.58 % to 55.38 %) | number within tolerance; causes consistent with gold | fanout:pass/fail, completeness:could_not_run |
| f2 full #3 | ✓ | 55.0 % (54.6 % to 55.4 %) | number within tolerance; causes consistent with gold | fanout:pass, completeness:could_not_run |
| f3 baseline #1 | ✗ | can't tell(整体 CTR 观测变化为 -1.83 个百分点,但其中有多少归因于 v3,现有数据无法确定) | abstained on a case with a valid answer | none |
| f3 baseline #2 | ✗ | can't tell(整体 CTR 的下降是真实的,但没有对照组,无法把它单独归因给 v3) | unparseable: none of the 4 alternative lines says 'ruled in' or 'ruled out' | none |
| f3 baseline #3 | ✗ | -1.83 个百分点 (95% 区间 -1.98 ~ -1.68),这是观测到的变化,并非已确认的因果效应。 | unparseable: none of the 4 alternative lines says 'ruled in' or 'ruled out' | none |
| f3 checks #1 | ✗ | can't tell | unparseable: none of the 4 alternative lines says 'ruled in' or 'ruled out' | mix_shift:pass, completeness:pass, srm:pass |
| f3 checks #2 | ✗ | can't tell(没有对照组,无法把 -1.83 个百分点的下降单独归因于 v3) | unparseable: none of the 5 alternative lines says 'ruled in' or 'ruled out' | mix_shift:pass, completeness:pass, srm:pass |
| f3 checks #3 | ✗ | can't tell | unparseable: none of the 5 alternative lines says 'ruled in' or 'ruled out' | mix_shift:pass, completeness:could_not_run |
| f3 full #1 | ✓ | -1.82 pp (95% CI -1.97 to -1.67) | number within tolerance; causes consistent with gold | completeness:pass, mix_shift:pass/pass |
| f3 full #2 | ✓ | -1.82 pp (95% 区间 -1.97 到 -1.67) | number within tolerance; causes consistent with gold | mix_shift:pass/pass, completeness:pass |
| f3 full #3 | ✓ | -1.82 pp (95% 区间 -1.97 to -1.67) | number within tolerance; causes consistent with gold | completeness:pass, mix_shift:pass/pass |
| f4 baseline #1 | ✗ | can't tell。按同一时段口径,点击率变化为 0.0 个百分点(95% 区间 -0.66 到 +0.66)。 | unparseable: none of the 3 alternative lines says 'ruled in' or 'ruled out' | none |
| f4 baseline #2 | ✗ | can't tell (昨天的数据只有 0–9 点,不是完整一天) | unparseable: none of the 4 alternative lines says 'ruled in' or 'ruled out' | none |
| f4 baseline #3 | ✓ | 0.0 个百分点(95% 区间 -0.7 to +0.7 pp)。我没有发现 CTR 真的下降。 | number within tolerance; causes consistent with gold | none |
| f4 checks #1 | ✗ | can't tell(昨日数据只加载了 0–9 点,不是完整的一天) | unparseable: none of the 5 alternative lines says 'ruled in' or 'ruled out' | completeness:fail, mix_shift:pass |
| f4 checks #2 | ✗ | can't tell(昨天数据只加载了一部分,无法给出全天 CTR) | unparseable: none of the 4 alternative lines says 'ruled in' or 'ruled out' | completeness:fail, mix_shift:pass |
| f4 checks #3 | ✓ | can't tell。昨天(10-07)的数据只加载到 0–9 点,是不完整的一天。 | abstained (accepted) | completeness:fail |
| f4 full #1 | ✓ | can't tell | abstained (accepted) | completeness:fail, mix_shift:pass/could_not_run |
| f4 full #2 | ✓ | +0.0 pp (-0.66 到 +0.66 pp) | number within tolerance; causes consistent with gold | completeness:fail, mix_shift:pass |
| f4 full #3 | ✓ | 0.0 pp (-0.66 到 +0.66 pp) | number within tolerance; causes consistent with gold | completeness:fail, mix_shift:pass/could_not_run |
| f5 baseline #1 | ✓ | can't tell。观测到的 CTR 差为 +1.20 个百分点,但分流比例严重失衡(样本比例不匹配),所以这个数字不能当作 ranker | abstained (accepted) | none |
| f5 baseline #2 | ✗ | can't tell | unparseable: none of the 3 alternative lines says 'ruled in' or 'ruled out' | none |
| f5 baseline #3 | ✗ | can't tell | unparseable: none of the 4 alternative lines says 'ruled in' or 'ruled out' | none |
| f5 checks #1 | ✗ | can't tell(观测到 +1.20 个百分点,但分流比例严重失衡,无法确认这是处理带来的效果) | unparseable: none of the 4 alternative lines says 'ruled in' or 'ruled out' | srm:fail/fail, completeness:could_not_run |
| f5 checks #2 | ✗ | can't tell | unparseable: none of the 4 alternative lines says 'ruled in' or 'ruled out' | srm:fail/fail, completeness:could_not_run |
| f5 checks #3 | ✗ | can't tell | unparseable: none of the 4 alternative lines says 'ruled in' or 'ruled out' | srm:fail, completeness:could_not_run |
| f5 full #1 | ✓ | can't tell | abstained (accepted) | srm:fail, completeness:pass |
| f5 full #2 | ✓ | can't tell | abstained (accepted) | srm:fail/fail, completeness:pass |
| f5 full #3 | ✓ | can't tell | abstained (accepted) | srm:fail, completeness:pass |
| f6 baseline #1 | ✗ | 46.05%(95% 区间 45.93%–46.17%) | headline 46.05 outside 50.053±0.3 | none |
| f6 baseline #2 | ✗ | 46.0%(95% 区间约 45.9%–46.2%,仅为二项近似) | unparseable: none of the 4 alternative lines says 'ruled in' or 'ruled out' | none |
| f6 baseline #3 | ✗ | 46.0 %(95% 区间 45.97%–46.13%) | headline 46 outside 50.053±0.3 | none |
| f6 checks #1 | ✗ | 46.0 %(95% 区间 45.9% to 46.2%) | unparseable: none of the 4 alternative lines says 'ruled in' or 'ruled out' | completeness:pass |
| f6 checks #2 | ✗ | 46.05 %(95% 区间 45.93–46.17 %) | unparseable: none of the 4 alternative lines says 'ruled in' or 'ruled out' | completeness:pass |
| f6 checks #3 | ✗ | 46.0%(95% 区间 45.9% to 46.2%),口径为外部真实用户、有点击的搜索数 ÷ 搜索数。[measured,口径选择为 g | headline 46 outside 50.053±0.3 | completeness:pass, mix_shift:pass |
| f6 full #1 | ✓ | +50.05 % (95% CI 49.93 to 50.17) | number within tolerance; causes consistent with gold | completeness:pass |
| f6 full #2 | ✓ | +50.05 % (95% 区间 49.93 到 50.18 %) | number within tolerance; causes consistent with gold | completeness:pass |
| f6 full #3 | ✓ | +50.05 pp (95% CI 49.93 to 50.17;这是 CTR 的水平值 50.05%,不是变化量) | number within tolerance; causes consistent with gold | completeness:pass |
| f7 baseline #1 | ✗ | 8.30 %(95% 区间 8.24–8.36 %) | unparseable: none of the 3 alternative lines says 'ruled in' or 'ruled out' | none |
| f7 baseline #2 | ✗ | 8.30 %(95% 区间 8.24%–8.36%) | unparseable: none of the 3 alternative lines says 'ruled in' or 'ruled out' | none |
| f7 baseline #3 | ✗ | 8.30%(95% 区间 8.24%–8.36%) | unparseable: none of the 3 alternative lines says 'ruled in' or 'ruled out' | none |
| f7 checks #1 | ✗ | 8.30%(95% 区间 8.24%–8.36%) | unparseable: none of the 4 alternative lines says 'ruled in' or 'ruled out' | completeness:pass |
| f7 checks #2 | ✗ | 8.30 %(95% 区间 8.24%–8.36%) | unparseable: none of the 3 alternative lines says 'ruled in' or 'ruled out' | completeness:pass |
| f7 checks #3 | ✗ | 8.30 %(95% 区间 8.24%–8.36%) | unparseable: none of the 4 alternative lines says 'ruled in' or 'ruled out' | completeness:pass |
| f7 full #1 | ✓ | can't tell | abstained (accepted) | completeness:pass |
| f7 full #2 | ✓ | can't tell | abstained (accepted) | completeness:pass |
| f7 full #3 | ✓ | can't tell | abstained (accepted) | completeness:pass |
| f8 baseline #1 | ✗ | 36.97 %(95% 区间 36.18–37.76 %) | unparseable: none of the 4 alternative lines says 'ruled in' or 'ruled out' | none |
| f8 baseline #2 | ✗ | 36.97 %(95% 区间 36.68–37.26 %) | unparseable: none of the 3 alternative lines says 'ruled in' or 'ruled out' | none |
| f8 baseline #3 | ✓ | 36.97 %(95% 区间 36.68%–37.26%,仅为二项分布近似) | number within tolerance; causes consistent with gold | none |
| f8 checks #1 | ✗ | 36.97 %(95% 区间 36.68%–37.26%) | unparseable: none of the 3 alternative lines says 'ruled in' or 'ruled out' | fanout:fail/pass, completeness:could_not_run |
| f8 checks #2 | ✗ | 36.97 % (the CTR is a point value; no interval was computed, and the n | unparseable: none of the 3 alternative lines says 'ruled in' or 'ruled out' | fanout:fail/pass, completeness:could_not_run |
| f8 checks #3 | ✗ | 36.97 %(95% 区间:未计算,见下) | unparseable: none of the 4 alternative lines says 'ruled in' or 'ruled out' | fanout:fail/pass, completeness:could_not_run |
| f8 full #1 | ✓ | 36.97 % (95% 区间 36.68–37.26 %) | number within tolerance; causes consistent with gold | fanout:fail, completeness:could_not_run |
| f8 full #2 | ✓ | +36.97 % (36.18% to 37.76%) | number within tolerance; causes consistent with gold | fanout:fail, completeness:could_not_run |
| f8 full #3 | ✓ | 36.97 % (95% 区间 36.68–37.26 %) | number within tolerance; causes consistent with gold | fanout:fail/pass, completeness:could_not_run |
