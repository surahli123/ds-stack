## Answer
Headline: +54.98 pp (54.58 至 55.38) [q9]
2026-W40 导航类(navigational)查询的点击率为 54.98%(点击 32,878 / 搜索 59,800),口径为当前有效标签(is_current=1)[q6]。这是一个水平值,不是变化量;"+"仅表示为正数。[measured]
- Observed: +54.98 pp (54.58 至 55.38) [q9]
- Adjusted: not computed (问题问的是单周水平值,没有前后对比,不涉及混合变化)
- Causal effect: not identified (问题不涉及因果,没有随机化或对照设计)

## What it means for 营销规划文档
可引用约 55%(区间 54.6%–55.4%,约 ±0.4pp)[q9]。但若采用旧版标签(v1),该数为 43.0% [q7],标签口径的影响远大于抽样误差,文档里需注明口径。[measured]

## Why we believe it
- Alternatives considered:
  - 标签版本口径:v1 全量标签得 43.0% [q7],当前标签得 54.98% [q6]。每个 query 恰有一条当前标签 [q4],故选当前标签;当前行内 v1 与 v2 标签的导航类 CTR 一致(均约 55.0%)[q5] [measured]
  - 连接导致行重复:ruled out,连接前后均 1000 行 [check:fanout#1] [measured]
  - 数据不完整:无法用历史周验证,但本周 1000 个 query 均有记录,且没有 clicks>searches 的行 [q8] [measured]
- Checks run:
  - fanout: pass 行数一致 [check:fanout#1]
  - completeness: could not run 表中只有 2026-W40 一周,没有历史周可比 [check:completeness#1]
  - mix_shift: skipped 单周水平值,没有前后对比

## Caveats, and what would change the answer
- 区间按二项分布、把每次搜索当独立样本计算,未考虑同一 query 内的聚类,真实区间会更宽。[inferred]
- completeness 无法验证:若 W40 数据尚未完全落库,数值可能变化;需要更早的周数据或加载日志才能确认。
- CTR 定义为 sum(clicks)/sum(searches)(按搜索量加权);若营销要的是各 query CTR 的简单平均,数值会不同。[guess]
- 标签口径:若营销认可的是 v1 标签,答案是 43.0% [q7]。

## Provenance
- Metric: 导航类 CTR = sum(clicks)/sum(searches),query_stats 与 query_labels(intent='navigational', is_current=1)按 query_id 连接,周=2026-W40 [guess];未找到 metrics.json($DS_OVERLAY_DIR 未设置)
- Data: query_stats, query_labels, through 2026-W40
- Reconciled: not done (没有可对照的看板或其他来源)
- Queries and checks: .ds-queries.log, .ds-checks.log
- Verified: verify_readout: pass (22 numbers on 7 lines; 6 queries, 2 checks, 0 given)