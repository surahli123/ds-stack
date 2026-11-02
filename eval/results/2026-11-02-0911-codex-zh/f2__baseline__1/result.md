## Answer
Headline: +54.98%（95% 区间：54.58%–55.38%；点估计 [measured]，区间 [inferred]）
2026-W40 按当前标签识别的导航类查询共有 59,800 次搜索、32,878 次点击，点击率为 54.98%。[measured]
- Observed: +54.98%（95% 区间：54.58%–55.38%）[measured；区间 inferred]
- Adjusted: not computed（本次计算描述性点击率，无需协变量调整）[inferred]
- Causal effect: not identified（未指定干预或对照；识别因果效应需要随机实验或可信的准实验设计）[inferred]

## What it means for 营销规划
规划文档可采用 54.98% 作为该周按当前标签计算的点击率。[measured] 未提供会改变决策的最小差异，因此无法判断上述区间是否足够精确。[inferred]

## Why we believe it
- Alternatives considered:
  - 混用历史标签：ruled out；未筛选当前版本会得到 44.99%，其中包含过期的导航标签。[measured]
  - 对查询点击率简单取平均：ruled out；该值为 55.01%，不符合总点击数除以总搜索次数的口径。[measured]
- Checks run:
  - 标签唯一性：pass 每个查询恰有一个当前标签，且版本均为最新。[measured]
  - 查询周记录重复：pass 未发现重复。[measured]
  - 计数有效性：pass 无缺失、非整数、非正搜索数或点击数超出搜索数。[measured]
  - 数据库完整性：pass SQLite 检查返回 ok。[measured]
  - 周数据完整性：could not run 缺少加载水位或每日记录，无法确认整周完整。[inferred]

## Caveats, and what would change the answer
- 区间采用 Wilson 方法，假设每次搜索为独立的点击／未点击试验；聚合数据无法验证该假设。已记录数据的描述性比率本身没有抽样误差。[inferred]
- 使用当前标签；若要求当周生效标签，需要标签生效时间才能重新计算。[inferred]

## Provenance
- Metric: 导航类当前标签（`is_current=1`）对应的总点击数 ÷ 总搜索次数 × 100%，from stated here [guess]；未提供 metrics.json。
- Data: `query_stats`、`query_labels`；最新记录期间为 2026-W40 [measured]，最后完整期间无法确认 [inferred]。
- Reconciled: not done（未提供仪表盘或独立来源）[inferred]
- Queries and checks: [SQL 查询](queries.sql)、[计算脚本](analysis.py)、[结果与检查日志](results.json)。[measured]
