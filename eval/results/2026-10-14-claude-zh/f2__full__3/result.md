## Answer
Headline: 55.0 % (54.6 % 至 55.4 %) [q6]
2026-W40 导航类(navigational)查询的点击率为 55.0%(32,878 次点击 / 59,800 次搜索),约为信息类查询 25.0% 的两倍多 [q6]。
- Observed: 55.0 % (54.6 % 至 55.4 %) [q6]
- Adjusted: not computed (这是单周的水平值,不是变化量,没有可调整的对比)
- Causal effect: not identified (这是描述性的比率,不涉及因果问题)

## What it means for 规划文档
可直接引用约 55%;区间宽度仅约 ±0.4 个百分点,远小于规划中通常关心的差异 [q6]。区间为按搜索次数做的二项正态近似,未考虑查询间的聚类,实际区间可能略宽 [inferred]。

## Why we believe it
- Alternatives considered:
  - 标签版本重复导致 join 放大(query_labels 共 1300 行对应 1000 个查询): ruled out,只取 is_current=1 后每个查询恰好一条标签 [q5] [measured]
  - 新旧标签版本(v1/v2)口径不同影响结果: ruled out,v1 与 v2 下导航类点击率分别为 55.0% 和 55.0%,无差异 [q7] [measured]
  - 混合结构/季节/星期效应: 不适用,只有单周数据、没有对比期 [q3] [inferred]
  - 数据不完整: 无法用历史周验证,但数据无异常(无点击数大于搜索数、无零搜索行) [q8] [measured]
- Checks run:
  - fanout: pass 1000 行连接后仍为 1000 行 [check:fanout#1]
  - completeness: could not run 表中只有 2026-W40 一周,无历史可比 [check:completeness#1]
  - mix_shift: skipped 没有比率变化,只有单周水平值
  - srm: skipped 非实验

## Caveats, and what would change the answer
- 未提供 metrics.json,点击率定义为本文自拟 [guess];若官方定义不同(例如按会话或去重点击),数字会变。
- "导航类"按当前标签(is_current=1)定义;若按 v1 的历史标签口径,导航类查询集合会不同(v1 非当前标签有 200 条为导航类)[q2]。
- 无法确认 W40 是否完整加载,也没有仪表盘可对账;若有则应核对。

## Provenance
- Metric: 点击率 = sum(clicks)/sum(searches),限定 intent='navigational' 且 is_current=1,周 2026-W40,来源 query_stats 连接 query_labels,stated here [guess]
- Data: query_stats, query_labels, through 2026-W40
- Reconciled: not done (没有仪表盘或其他可信来源可对账)
- Queries and checks: .ds-queries.log 和 .ds-checks.log
- Verified: verify_readout: pass (19 numbers on 7 lines; 5 queries, 2 checks, 0 given)