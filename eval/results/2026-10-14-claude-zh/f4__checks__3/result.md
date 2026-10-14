## Answer
Headline: can't tell。昨天(10-07)的数据只加载到 0–9 点,是不完整的一天。
昨天的 CTR 看起来下降,是因为数据缺了白天 CTR 较高的时段。在同样的 0–9 点范围内比较,没有可测出的下降。

- Observed: 27.00% vs 前 7 天全天 29.83%,即 −2.83 个百分点(没有区间:这是整天与半天的比较,不可比)[measured]
- Adjusted: 0.00 个百分点(没有计算区间,两侧在这个范围内都恰好是 27.00%),保持小时段构成不变(只比较 0–9 点)[measured]。昨天 0–9 点是 27.00%(5,292/19,600),前 7 天同时段是 27.00%(37,044/137,200)。
- Causal effect: not identified(这是观测数据,没有实验或对照设计。而且在同时段比较下也看不到变化,没有要解释的效应)

## What it means for 是否把 CTR 下降当作真实问题上报
−2.83 个百分点是数据缺口造成的,不能当作真实下降上报。同时段下降约为 0,所以现在没有需要处理的搜索质量问题。要判断是否需要行动,必须等昨天 24 小时数据全部加载完。

## Why we believe it
- Alternatives considered:
  - 昨天真实 CTR 下降:目前无证据支持。0–9 点与前 7 天同时段完全一致,均为 27.00% [measured]。10–23 点还没有数据,无法排除后面几个小时才出问题 [inferred]。
  - 小时构成差异(mix)造成的下降:确认是主因。数据显示 0–7 点 CTR 是 24%,8 点之后是 31%。昨天缺失了 10–23 点这些高 CTR 时段,把全天均值拉低了 [measured]。
  - 搜索量或点击量异常:ruled out。昨天各小时的搜索量和点击量与前 7 天同小时的均值一致 [measured]。
- Checks run:
  - completeness: fail。10-07 只有 10 行,是前 7 天中位数 24 行的 42%,未达 90% 的门槛 [check:completeness#1]。
  - mix_shift: skipped。已经直接做了同小时对比,结果为 0.00,分解不会带来新信息。
  - srm / fanout: skipped。没有实验分流,也没有 join。

## Caveats, and what would change the answer
- 昨天 10–23 点的数据还没加载,晚些时候的真实情况未知。
- 小时级数据非常规整(同小时数值几乎完全一样),可能是汇总表或模拟数据,请确认数据源。
- 数据加载完成后,用全天数据重算。如果全天 CTR 低于约 29.8%,才说明有真实下降。

## Provenance
- Metric: 搜索 CTR = clicks / searches,按小时汇总后再加总,来自 stated here [guess](没有 metrics.json)
- Data: search_hourly,截至 2026-10-06(最后一个完整日);10-07 只到 09 点
- Reconciled: not done(没有仪表盘或其他来源可对账)
- Queries and checks: 检查结果记录在 .ds-checks.log(completeness#1);查询是在命令行里直接运行的,没有单独记录