## Answer
Headline: can't tell(观测到 +1.20 个百分点,但分流比例严重失衡,无法确认这是处理带来的效果)
处理组 CTR 为 31.2%,对照组为 30.0%,观测差 +1.20pp。但分流检验失败,所以这个差值不能当作因果提升。
- Observed: +1.20 pp(95% 区间 +1.13 至 +1.27 pp)[measured]。CTR = 点击 / 搜索,处理组 31.20%,对照组 30.00%。区间把每次搜索当作独立样本,而同一用户的搜索彼此相关,所以真实区间会更宽。
- Adjusted: not computed(表里只有按日汇总的 arm 级数据,没有用户层或分群字段,无法对任何因素做调整)
- Causal effect: not identified(需要查明分流失衡的原因并修复,或拿到用户层分配日志,然后重新分析或重跑实验)

## What it means for 上线决策
我没有拿到最小可接受提升的阈值。即使按名义区间,+1.13 至 +1.27pp 也只是在"分流正常"的前提下才成立,而这个前提已被检验推翻。因此现在不应把 +1.2pp 作为上线依据。

## Why we believe it
- Alternatives considered:
  - 处理确实提升了 CTR:未排除。观测差为正,但只有在两组可比时才能这样解读 [inferred]
  - 随机分流有问题(比如处理组流失用户、机器人过滤或日志丢失):未排除,这是分流比例失衡最可能的原因,但本库无法验证 [guess]
  - 纯偶然造成的失衡:已排除。p 值约 1e-130,而且每天比例都稳定在 51.2/48.8 [measured]
  - 按日期混合变化(mix shift)导致的差异:基本排除。每天的两组规模和 CTR 都几乎不变,没有时间趋势 [measured]
- Checks run:
  - srm: fail。用户数 499,930 比 475,990,占比 51.23% 对 48.77%,预期 50/50,chi2=587,p≈1e-130 [check:srm#1]。搜索数同样失衡 [check:srm#2]
  - completeness: could not run。只有 2 个更早的周期可用,而检查要求至少 3 个;不过 14 天都有两个 arm 的数据行,看起来是完整的
  - mix_shift: skipped。没有分群数据可拆
  - fanout: skipped。没有做 join

## Caveats, and what would change the answer
- 处理组比预期少约 2.4% 的用户。如果流失的用户本来点击率偏低或偏高,真实提升会和 +1.2pp 差很多,方向无法判断。
- 每组每天的用户数和搜索数几乎是固定值(每个用户约 6 次搜索),这像是模拟数据或经过处理的汇总数据,应先确认数据来源。
- 只要查明失衡原因、并确认失衡与点击行为无关,+1.2pp 才可以重新作为参考。
- 我没有做用户层面的聚类标准误差,因此上面的区间偏窄。

## Provenance
- Metric: CTR = clicks / searches,汇总整个实验期,来源是 stated here [guess](目录里没有 metrics.json)
- Data: experiment_daily,2026-09-17 至 2026-09-30,共 14 天
- Reconciled: not done(没有可对照的看板或其他数据源)
- Queries and checks: 检查结果记录在 checks/ 运行时生成的 .ds-checks.log(srm#1、srm#2、completeness#1)。查询是在命令行直接执行的,没有单独的查询日志。