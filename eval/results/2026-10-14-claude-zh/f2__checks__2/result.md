```
## Answer
Headline: 55.0%(95% 区间 54.6%–55.4%)
2026-W40 导航类查询(navigational)的点击率为 55.0%,即 59,800 次搜索中有 32,878 次点击。
- Observed: +55.0 %(点击率,非变化量)(54.6%–55.4%)
- Adjusted: not computed(这是单一水平值,没有需要调整的对比)
- Causal effect: not identified(这是描述性指标,没有干预或对照设计)

## What it means for 营销规划文档
可直接引用约 55%。如果规划决策只在点击率相差 1 个百分点以上时才会改变,那么 ±0.4 个百分点的区间足够窄。但这个区间只反映抽样波动,不含标签口径和数据完整性的不确定性。

## Why we believe it
- Alternatives considered:
  - 把 query_labels 中的所有标签版本都联结进来:会让一个查询匹配多行,并把已作废的旧标签算进去,得到 45.0%,是错的。已排除,依据是只取 is_current=1,每个查询恰好一行 [measured]
  - 标签版本不同导致口径差异:v1 当前标签的点击率为 55.0%,v2 为 55.0%,没有差异 [measured]
  - 旧标签(is_current=0)口径:这些查询的当前标签已被改动,不应使用 [inferred]
- Checks run:
  - fanout: pass 用 is_current=1 联结后,1000 行对应 1000 行,没有增减(此处按我的口径输入,不是自动取数)
  - completeness: could not run 库里只有 2026-W40 一周,没有历史周可对比,无法确认该周是否完整加载
  - mix_shift / srm: skipped 没有两期对比,也不是实验

## Caveats, and what would change the answer
- 没法验证 W40 是否完整加载;如果该周数据只加载了一部分,数值会有偏差。
- 若用所有标签版本联结而不限制 is_current,点击率会变成 45.0%,所以必须用当前标签。
- 区间按二项分布近似计算,没考虑不同查询之间的相关性,实际区间可能略宽。
- "点击率"的定义是 clicks/searches(按搜索次数加权),不是各查询点击率的平均值。

## Provenance
- Metric: 点击率 = sum(clicks)/sum(searches),限定 intent='navigational' 且 is_current=1,来自 stated here [guess](没有 metrics.json)
- Data: query_stats、query_labels,截至 2026-W40(库里只有这一周)
- Reconciled: not done(没有可对照的仪表盘或其他来源)
- Queries and checks: 检查记录在 .ds-checks.log(fanout#1、completeness#1);查询是在会话中直接执行的,未另存为文件
```