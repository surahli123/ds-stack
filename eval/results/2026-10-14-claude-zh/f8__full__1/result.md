## Answer
Headline: 36.97 % (95% 区间 36.68–37.26 %) [q9]
2026-W41 购物垂类(apparel/electronics/home)的点击率为 36.97%,基于 900 个去重查询、107,810 次搜索、39,857 次点击 [q9]。
- Observed: +36.97 % (95% 区间 36.68–37.26 %) [q9]
- Adjusted: not computed (单一周、单一水平值,没有前后对比,无需 mix_shift)
- Causal effect: not identified (这是一个水平值而非变化量,不涉及因果)

## What it means for 商品运营引用该数字
直接连表会得到 40.9%(56,422/137,945),比正确值虚高约 3.9 pp,因为 250 个查询在 query_category 中被重复加载 [q10, check:fanout#1]。应引用 36.97%,区间半宽约 0.3 pp [q9]。

## Why we believe it
- Alternatives considered:
  - 连表重复计数(query_category 重复行): ruled in,已用 IN 子查询去重修正,900 个查询而非 1150 行 [q9, q10, check:fanout#1] [measured]
  - 重复行是否为改分类: ruled out,重复行的分类完全相同(仅 loaded_at 由 2026-09-01 变为 2026-10-09)[q7] [measured]
  - 数据不完整/日志口径变化: ruled out 部分,W41 共 2000 个查询,每个查询一行,无 clicks>searches 或 searches=0 的行 [q2, q11] [measured]
  - 混合偏移/季节性: 不适用,仅一周的水平值 [inferred]
- Checks run:
  - fanout: fail 右表 2250 行对应 2000 个键,有 250 个重复键;已通过去重规避,最终数字不受影响 [check:fanout#1]
  - completeness: could not run 没有更早的历史周(需要至少 3 个) [check:completeness#1]
  - mix_shift: skipped 没有比较期,无变化量
  - srm: skipped 非实验

## Caveats, and what would change the answer
- 区间为按搜索次数的二项近似,未计入查询间的聚类,实际区间可能略宽。
- W41 是否完整无法由历史验证;若上游仍在补数,数值会变。
- CTR 定义(点击/搜索,按搜索加权)为本人假设,若商品运营要按查询平均,数值会不同。
- 无 metrics.json、无仪表盘可对账。

## Provenance
- Metric: CTR = sum(clicks)/sum(searches),按去重后的购物垂类查询,2026-W41,来自 query_week,stated here [guess]
- Data: query_week, query_category, category_vertical,through 2026-W41
- Reconciled: not done (无仪表盘或 metrics.json)
- Queries and checks: .ds-queries.log, .ds-checks.log
- Verified: verify_readout: pass (27 numbers on 8 lines; 5 queries, 2 checks, 0 given)