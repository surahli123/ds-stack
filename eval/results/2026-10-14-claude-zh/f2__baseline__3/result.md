```
## Answer
Headline: 54.98 %(95% 区间 54.95–55.01)
2026-W40 导航类(navigational)查询的点击率约为 55.0%:搜索 59,800 次,点击 32,878 次。

- Observed: 54.98 %(95% 区间 54.95–55.01),按查询做自助法重抽样得到
- Adjusted: not computed(这是描述性指标,没有需要控制的对比)
- Causal effect: not identified(这里没有要估计的处理效应,只是报告一个水平值)

## What it means for 营销规划文档
可以直接引用“导航类查询点击率约 55%”。这个区间很窄(±0.03 个百分点),远小于规划中任何有意义的偏差。主要风险在口径,不在抽样误差。

## Why we believe it
- Alternatives considered:
  - 用旧标签(包含已被取代的 label_version 1 记录):结果会变成 43.0%,所以必须只用 is_current=1 的标签 [measured]
  - 标签版本 1 与 2 之间存在系统差异:排除。只看 v1 为 54.98%,只看 v2 为 54.99% [measured]
  - 重复标签或重复统计行:排除。每个查询只有一条当前标签,每个 (query_id, week) 只有一行 [measured]
- Checks run:
  - 完整性:pass,1000 个查询全部有当前标签,没有 clicks>searches、负数或空值
  - 唯一性:pass,没有重复的当前标签和重复的周数据行
  - 标签版本敏感性:pass,见上
  - 自助法区间:pass,2000 次重抽样,按查询聚类

## Caveats, and what would change the answer
- 点击率定义为总点击数 / 总搜索数(按搜索量加权),而不是各查询点击率的简单平均;如果营销想要后者,数字会不同 [inferred]
- 结果依赖于用当前标签,不能用历史标签;若使用旧标签,答案会变成 43.0% [measured]
- 表里只有 W40 一周的数据,所以没法看趋势或与其他周对比。
- 区间只反映抽样波动,没有反映标签本身是否分类正确。

## Provenance
- Metric: 点击率 = sum(clicks)/sum(searches),限定 intent='navigational' 且 is_current=1,周=2026-W40;来源:stated here [guess](目录里没有 metrics.json)
- Data: query_stats、query_labels,覆盖 2026-W40(表中仅此一周)
- Reconciled: not done(没有可对照的仪表盘或其他数据源)
- Queries and checks: 仅在本次会话的命令中运行,没有保存到文件
```