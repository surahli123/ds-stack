```
## Answer
Headline: 54.98%(95% 区间 54.58%–55.38%)
2026-W40 导航类查询(navigational)的点击率约为 55.0%,即 59,800 次搜索中有 32,878 次点击。[measured]
- Observed: +54.98%(95% 区间 54.58%–55.38%),这是点击数除以搜索数的比率,不是变化量。[measured]
- Adjusted: not computed(这是单周的水平值,没有对比项,没有需要控制的变量)
- Causal effect: not identified(这个问题不涉及因果;如果要问干预的效果,需要随机实验或有对照的前后对比)

## What it means for 市场部规划文档
可以直接引用"导航类查询点击率约 55%"。如果规划里的决策阈值与 55% 相差不到约 0.4 个百分点,这个数就分不出高低;差距更大时,区间足够窄,结论是稳的。[inferred]

## Why we believe it
- Alternatives considered:
  - 联结 query_labels 时不过滤 is_current,会因一个查询有多个标签版本而重复计数:已排除。做法是只取 is_current=1,此时 1000 个查询各对应唯一一条当前标签,联结后行数不变。[measured]
  - 不过滤 is_current 的写法会得到 44.99%(600 个查询行,混入了旧标签),差距约 10 个百分点,所以不能用:已排除。[measured]
  - 标签版本 v1 与 v2 的口径差异:已排除。当前导航类查询中 v1(300 个)点击率为 54.98%,v2(100 个)为 54.99%,基本一致。[measured]
  - 区间只按"搜索次数独立"的二项分布计算,没有考虑同一查询内部的相关性,所以可能偏窄:未排除。[inferred]
- Checks run:
  - fanout:pass,按 is_current=1 联结后左表 1000 行,联结后仍为 1000 行(fanout#1)。作为对照,同一检查对不过滤标签的联结(1500 行对 1000 个键)报 fail(fanout#2),确认了过滤的必要性。
  - completeness:could not run,表里只有 W40 一周,没有历史周可对比,无法确认该周是否完整加载。
  - mix_shift:skipped,这是单周水平值,没有前后对比。
  - srm:skipped,这不是实验。

## Caveats, and what would change the answer
- W40 是否完整加载未能验证。若该周数据缺失,比率可能偏移。[inferred]
- 点击率的口径是"总点击数 ÷ 总搜索数"(按搜索量加权),不是各查询点击率的简单平均。若规划文档要的是后者,数值会不同。[guess]
- 导航类取的是当前标签(is_current=1)。若按历史标签分类,结果会不同(见上)。
- 区间可能偏窄(见上)。

## Provenance
- Metric: 点击率 = sum(clicks) / sum(searches),stated here [guess];目录里没有 metrics.json。
- Data: query_stats、query_labels(is_current=1),仅有 2026-W40 一周,未能验证其完整性。
- Reconciled: not done(没有可对账的看板或其他来源)
- Queries and checks: 检查结果记录在工作目录的 .ds-checks.log(fanout#1、fanout#2、completeness#1);SQL 查询是在会话中直接运行的,没有单独保存日志。
```