## Answer
Headline: can't tell
观测到处理组 CTR 高 1.20 个百分点,但分流比例严重偏离 50/50(样本比例失衡),所以这 1.2 个百分点不能当作 ranker_boost 的因果效应。

- Observed: +1.20 个百分点 (95% 区间 +1.13 ~ +1.27;处理组 31.20% vs 对照组 30.00%) [measured]。区间按搜索次数做二项近似,没有按用户聚类,实际会偏宽。
- Adjusted: not computed(库里只有按天、按组汇总的数据,没有用户级或分群字段,无法对失衡的来源做调整)
- Causal effect: not identified(需要找出分流失衡的原因并修复,或拿到用户级分配日志,在确认两组可比后重新分析或重跑实验)

## What it means for 上线决策
我没有拿到"最小可接受提升"的阈值。观测区间(+1.13 ~ +1.27 个百分点)很窄,但它只反映抽样噪声,不反映分流偏差。偏差有多大不知道,所以现在不应凭这个数字决定上线。

## Why we believe it
- Alternatives considered:
  - 真实的排序效果:未排除,与观测一致 [inferred]
  - 分流/日志缺陷导致处理组丢失用户(样本比例失衡):无法排除,而且有证据支持。对照组用户 499,930,处理组 475,990,占比 51.2% / 48.8%,偏离 50/50,z≈24 [measured]。如果丢失的用户恰好是低点击用户,CTR 会被虚高 [guess]
  - 每天的波动或新奇效应:基本排除。处理组每天都比对照组高约 1.2 个百分点,日间很稳定 [measured]。只看汇总数据,看不出效应随时间的变化
- Checks run:
  - 样本比例(SRM)检验:fail,z≈24,p 远小于 0.001
  - 每用户搜索次数:pass,两组都是 6.0,没有搜索量差异
  - 逐日一致性:pass,14 天中处理组每天都更高
  - 用户级方差/聚类区间:could not run,没有用户级数据
  - 实验期完整性:pass,14 天 × 2 组 = 28 行,无缺失日期

## Caveats, and what would change the answer
- 失衡来源未知(分配 bug、机器人过滤、某些客户端崩溃等),要排查分流和曝光日志。
- 只有汇总数据,没法按用户分层或做聚类标准误。
- 修复并确认比例回到 50/50 后,如果 CTR 提升仍在,结论才可以用于上线。

## Provenance
- Metric: CTR = clicks / searches,汇总整个实验期,stated here [guess](没有 metrics.json)
- Data: experiment_daily,2026-09-17 至 2026-09-30(完整的 14 天)
- Reconciled: not done(没有仪表盘或其他数据源可对照)
- Queries and checks: 在本次会话中直接用 Python 的 sqlite3 查询并计算,没有保存成文件