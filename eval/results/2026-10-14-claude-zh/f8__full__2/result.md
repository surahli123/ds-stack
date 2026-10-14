## Answer
Headline: +36.97 % (36.18% 至 37.76%) [q9]
2026-W41 购物垂直领域查询的点击率(CTR)为 36.97%(39,857 次点击 / 107,810 次搜索,900 个去重查询)。 [q9]
- Observed: +36.97 % (36.18% 至 37.76%) [q9]
- Adjusted: not computed (单周单一水平值,没有可比较的前后变化,不涉及构成调整)
- Causal effect: not identified (这是一个水平值而非变化,不涉及因果)

## What it means for 商品运营(Merchandising)引用该数字
若直接 join query_category,会得到 40.9%(56,422 / 137,945),虚高约 3.9 pp,必须使用去重后的 36.97%。 [q8, q9]

## Why we believe it
- Alternatives considered:
  - 直接 join 的重复计数(250 个查询在 2026-09-01 和 2026-10-09 被加载两次,分类相同): ruled in 为必须处理的问题,已通过按 query_id 去重解决 [q6, q8, q9] [measured]
  - 查询被重新分类导致口径不同: ruled out,两次加载的分类完全一致 [q6] [measured]
  - 不完整的周数据: ruled out 的证据不足,只有一周的数据,无法做历史对比 [q2] [inferred]
- Checks run:
  - fanout: fail 直接 join 使 900 行变为 1150 行(新增 250 行);已用 IN 子查询去重,结果为 900 行 / 900 个去重查询 [check:fanout#1] [q9]
  - completeness: could not run 表中只有 2026-W41 一周,没有更早的周可比较 [check:completeness#1]
  - mix_shift: skipped 只报告单周水平值,没有变化量

## Caveats, and what would change the answer
- 数据中只有 W41 一周,无法确认该周完整;如果该周未完整加载,CTR 可能变化。补充历史周数据可以验证。
- 区间按查询级别的比率线性化(delta method)计算,假设查询之间独立。
- CTR 定义为 clicks / searches 的汇总比率(不是各查询 CTR 的平均值),如商品运营使用另一口径需要重算。

## Provenance
- Metric: CTR = sum(clicks) / sum(searches),按 query_week 的 2026-W41,限定 vertical = 'shopping'(经 query_category 与 category_vertical 映射,按 query_id 去重), stated here [guess]
- Data: query_week, query_category, category_vertical, through 2026-W41
- Reconciled: not done (没有可对照的仪表盘或其他来源)
- Queries and checks: .ds-queries.log, .ds-checks.log
- Verified: verify_readout: pass (21 numbers on 6 lines; 4 queries, 2 checks, 0 given)