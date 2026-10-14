## Answer
Headline: 46.0%（95% 区间约 45.9%–46.2%，仅为二项近似）
2026-10-05 至 10-11 这一周，外部真实流量的搜索 CTR 约为 46.0%。每日值稳定在 45.9%–46.2%。

- Observed: 46.05%（约 45.93%–46.17%），即 321,780 次有点击的搜索 ÷ 698,782 次外部搜索 [measured]
- Adjusted: not computed（只有一周数据，没有可比对象，也没有需要调整的混杂因素）
- Causal effect: not identified（这是单周水平值，不是变化量。要做归因，需要对照组或有明确上线时间点的前后对比）

## What it means for 每周业务回顾
这是一个水平值，不是变化量，所以没有决策阈值可以比较。若要写成环比，需要上周数据，而表里没有。±0.12pp 的区间只反映抽样误差。

## Why we believe it
- Alternatives considered:
  - 把 bot 和内部流量计入：全部流量 CTR 为 41.4%，会低估真实用户 CTR。bot 约 2%，内部约 67%，两者差异很大，所以排除 [measured]
  - 分母改用“有结果的搜索”：得到 50.05%，这是另一种口径，要看团队约定 [measured]
  - 用点击数 ÷ 搜索数：得到 64.5%，会大于“有点击的搜索”口径，因为一次搜索可以有多次点击，所以不用 [measured]
  - 平台差异：桌面端 46.06%，移动端 46.04%，差异可忽略 [measured]
- Checks run:
  - 日期覆盖：pass，7 天都有数据，每天 6 行（2 个平台 × 3 类流量）
  - 每日稳定性：pass，外部流量每日 CTR 在 45.88%–46.16% 之间
  - 与看板对账：could not run，没有看板数值

## Caveats, and what would change the answer
- 没有 metrics.json，CTR 口径是我的假设 [guess]：外部流量中“有点击的搜索数 ÷ 搜索数”。如果团队口径是含所有流量（41.4%）或以有结果的搜索为分母（50.1%），数字会不同。
- 区间假设各次搜索相互独立。同一用户的搜索会相关，实际区间会更宽。
- 表名带 `_v`，可能是视图，我没有核实其上游定义。

## Provenance
- Metric: CTR = sum(searches_with_click) / sum(searches)，限定 traffic_type='external'，口径来自 stated here [guess]
- Data: search_daily_v，覆盖 2026-10-05 至 10-11（共 7 天，均完整）
- Reconciled: not done（没有看板或其他来源数值）
- Queries and checks: 查询在本次会话中用 Python/sqlite3 内联运行，没有保存成文件