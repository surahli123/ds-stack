## Answer
Headline: 55.0 %(95% 区间 54.3 到 55.7)
2026-W40 导航类查询的点击率约为 55.0%,即 32,878 次点击除以 59,800 次搜索。

- Observed: +55.0 %(54.3 到 55.7)[measured]
- Adjusted: not computed(这是单周的描述性指标,没有需要控制的比较对象)
- Causal effect: not identified(这里没有处理组或对照组,也不存在要识别的因果问题)

## What it means for 规划文档
可以直接使用约 55%。区间只有约 ±0.7 个百分点宽,所以只要规划里的决策阈值差距大于 1 个百分点,这个不确定性就不会改变结论。我不知道这个阈值是多少,需要你来定。

## Why we believe it
- Alternatives considered:
  - 把 query_labels 全表直接连接:ruled out。每个 query 有多个标签版本,直接连接会重复计算,还会混入旧标签。我只用了 is_current=1,这样每个 query 恰好对应一个标签 [measured]
  - 旧版标签(v1)的口径:ruled out,按它算出来会不同。导航类 v1 的 CTR 为 43.0%,v2 为 55.0%。v1 的 500 个 query 里有 200 个是已经被替换的标签 [measured]
  - 按 query 对各自的 CTR 取简单平均:ruled out,结果是 55.0%,与按次数加权的结果一致 [measured]
- Checks run:
  - 键唯一性:pass。query_stats 有 1000 行,对应 1000 个不同的 query,而且全是 W40。每个 query 恰好有一个当前标签,没有孤儿记录 [measured]
  - 数据质量:pass。没有空值,也没有点击数大于搜索数的行 [measured]
  - 区间:pass。对 query 聚类,用比率的 delta 法算标准误,约 0.35 个百分点 [measured]

## Caveats, and what would change the answer
- 当前导航类标签有 400 个 query。如果标签口径再变,结果会明显变动(旧标签口径下是 43%)[measured]
- 点击率的定义(点击数除以搜索数)是我按字面理解的,没有 metrics.json 可核对 [guess]
- 区间假设各 query 之间相互独立 [inferred]

## Provenance
- Metric: 导航类 CTR = sum(clicks)/sum(searches),标签取 is_current=1,来自 stated here [guess]
- Data: query_stats、query_labels,截至 2026-W40(库中只有这一周)
- Reconciled: not done(没有可对照的看板或 metrics.json)
- Queries and checks: 只在本次会话里运行过,没有保存到文件