## Answer
Headline: can't tell。观测到的 CTR 差为 +1.20 个百分点,但分流比例严重失衡(样本比例不匹配),所以这个数字不能当作 ranker_boost 的因果效应。

处理组的 CTR 为 31.20%,对照组为 30.00%,高 1.20 个百分点;但处理组少了约 4.8% 的用户,分流本身已经出了问题。

- Observed: +1.20 个百分点 (95% 区间 +1.13 至 +1.27),按搜索次数汇总计算,未考虑用户层面的聚类 [measured]
- Adjusted: not computed(表里只有按日、按组的汇总数据,没有用户层面的协变量,无法对分流偏差做调整)
- Causal effect: not identified(需要找出并修复分流或日志丢失的原因,然后重跑或用用户层面的数据重新分析)

## What it means for the launch decision
观测区间(+1.13 至 +1.27)远高于任何合理的最小有意义变化,但这个区间只反映抽样噪声,不反映偏差。由于 SRM 的存在,真实效应可能是正的、接近零,甚至是负的,所以现在不应凭这个数字决定上线。

## Why we believe it
- Alternatives considered:
  - 随机分流有效、差异就是真实效应:ruled out,处理组用户占 48.77%,而设计是 50/50;z ≈ -24,不可能是偶然 [measured]
  - 处理组日志丢失或被过滤(例如低参与度用户缺失):仍然可能,这会抬高处理组 CTR,与偏差方向一致,我们无法排除 [inferred]
  - 处理本身导致部分用户流失(例如页面报错、不再曝光):仍然可能,同样会造成 SRM [guess]
  - 时间波动或新奇效应:基本排除,每天的差值都在 +1.1 到 +1.3 个百分点之间,没有明显趋势 [measured]
- Checks run:
  - 样本比例不匹配(SRM)检验:fail,处理组 475,990,对照组 499,930,z = -24.2
  - 每搜索用户数:pass,两组都是 6.0,没有差异
  - 逐日一致性:pass,14 天里每天差值都稳定为正
  - 用户层面的方差或聚类稳健的区间:could not run,只有汇总数据
  - 与仪表盘核对:skipped,没有可核对的来源

## Caveats, and what would change the answer
- "users" 是按日汇总的,可能同一用户在多天重复计数,所以 SRM 的 z 值只能当作量级参考,但 4.8% 的偏差远超这个误差。
- 区间把搜索当作独立样本,真实区间会更宽。
- 如果能查明分流缺口的原因(例如分桶日志、机器人过滤、处理组崩溃),并拿到完整的用户层面数据,结论可能改变。
- CTR 的定义是我假设的(点击 / 搜索),未经确认。

## Provenance
- Metric: CTR = clicks / searches,来自 stated here [guess];目录中没有 metrics.json
- Data: warehouse.db 的 experiment_daily 表,覆盖 2026-09-17 至 2026-09-30(共 14 天,完整)
- Reconciled: not done(没有仪表盘或其他来源可比对)
- Queries and checks: 在本次会话中用 Python 的 sqlite3 内联运行,没有保存成文件