## Answer
Headline: +54.98 % (95% 区间 54.58 % 至 55.38 %) [q5]
2026-W40 导航类(navigational)查询的点击率为 54.98%:59,800 次搜索、32,878 次点击,按每条查询的当前标签(is_current=1)统计 [q5]。
- Observed: +54.98 % (54.58 % 至 55.38 %) [q5]
- Adjusted: not computed (单周单一指标,没有前后对比,无需调整)
- Causal effect: not identified (这是描述性水平值,不是变化量,无因果问题)

## What it means for 营销规划文档
规划文档可引用约 55%(区间 54.6%–55.4%)作为 W40 导航类查询点击率;未给出会改变决策的阈值。若误用未过滤的标签连接,会得到 44.99%,低估约 10 个百分点 [q6]。

## Why we believe it
- Alternatives considered:
  - 标签表重复行(含历史版本)使连接扇出、污染口径: ruled in(未过滤连接得 44.99%,多出 300 行),已通过 is_current=1 排除 [q6, check:fanout#2] [measured]
  - 标签版本 v1 与 v2 导致口径不同: ruled out,当前标签中 v1 的 CTR 54.98%、v2 的 54.99%,基本一致 [q7] [measured]
  - 数据不完整/周期未落地: ruled out 的证据不足,只有一周数据,无法与往期比较 [q3] [inferred]
  - 日内/星期季节性: 未检验,仅单周数据 [guess]
- Checks run:
  - fanout: pass 过滤 is_current=1 后 1000 行连接后仍为 1000 行 [check:fanout#1]
  - fanout: fail 未过滤连接时右表 1300 行对应 1000 个键,新增 300 行;该口径已弃用 [check:fanout#2]
  - completeness: could not run 仅有 2026-W40 一周,缺少 3 个更早周期 [check:completeness#1]
  - mix_shift: skipped 只报告单周水平值,没有前后变化

## Caveats, and what would change the answer
- 区间按"每次搜索为独立伯努利"的二项近似计算,未考虑同一查询内的相关性,真实区间会略宽;如有逐查询数据可做聚类估计。
- 指标定义是我自己设的(点击数/搜索数,汇总到导航类查询),没有 metrics.json;若营销口径是"各查询 CTR 的平均",数值会不同。
- 标签以 is_current=1 为准;若营销要用 W40 当时的历史标签,结果会不同。
- 仅一周数据,无法核对完整性,也无法与仪表盘对账。

## Provenance
- Metric: 点击率 = sum(clicks)/sum(searches),按 query_stats 与 query_labels(is_current=1, intent='navigational')连接,周粒度 2026-W40,stated here [guess]
- Data: query_stats, query_labels, through 2026-W40(仅有该周,完整性未能验证)
- Reconciled: not done (没有仪表盘或其他可信来源可比对)
- Queries and checks: .ds-queries.log 与 .ds-checks.log
- Verified: verify_readout: pass (28 numbers on 9 lines; 4 queries, 3 checks, 0 given)