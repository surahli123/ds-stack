```
## Answer
Headline: 36.97 % (95% 区间 36.68–37.26 %) [q10]
2026-W41 购物垂类(apparel/electronics/home)查询的点击率为 36.97%:900 个查询、107,810 次搜索、39,857 次点击 [q10]。
- Observed: 36.97 % (36.68–37.26 %) [q10]
- Adjusted: not computed (单周单点值,没有前后对比,无需调整)
- Causal effect: not identified (这是描述性水平值,不涉及因果问题)

## What it means for 商品运营(merchandising)引用该数字
引用 36.97% 即可;若直接连接 query_category 而不去重,会得到 40.9%(56,422/137,945),偏高约 3.9 pp,不应使用 [q11, q10]。请求中没有给出决策阈值,故无法与阈值比较。

## Why we believe it
- Alternatives considered:
  - query_category 重复加载导致重复计数(250 个重复行,涉及 250 个购物查询): ruled in,已按 query_id 去重 [q2, q11, check:fanout#1] [measured]
  - 同一查询被重新分类到不同类目/垂类: ruled out,没有 query_id 对应多个类目 [q9] [measured]
  - 垂类映射重复或缺失: ruled out,5 个类目各只映射一次,3 个属购物 [q3, q4, q5] [measured]
  - 数据不完整/周期问题: ruled out 于本周内:2000 个查询每个都有一行 [q6] [inferred]
  - 混合变化/季节性: not applicable,单周水平值,没有对比 [inferred]
- Checks run:
  - fanout(原始连接): fail 连接新增 250 行,已通过去重解决 [check:fanout#1]
  - fanout(去重后): pass 2000 行对 2000 个键 [check:fanout#2]
  - completeness: could not run 表里只有 W41,没有历史周可比较 [check:completeness#1]
  - mix_shift / srm: skipped,无前后对比,也不是实验

## Caveats, and what would change the answer
- query_week 只含 W41,无法核对该周是否完整加载;若有缺失,需要补充历史周数据来确认。
- 点击率定义为我的假设(点击/搜索,按搜索次数加权),未找到 metrics.json;若运营采用按查询平均的 CTR,数字会不同。
- 区间用二项正态近似,假设搜索之间独立,实际上同一用户的相关性会让区间偏窄。
- 未与任何看板核对。

## Provenance
- Metric: CTR = sum(clicks)/sum(searches),W41,垂类=shopping,按 query_id 去重后的类目,来自 stated here [guess]
- Data: query_week, query_category, category_vertical, through 2026-W41
- Reconciled: not done (没有可用的看板或 metrics.json)
- Queries and checks: .ds-queries.log, .ds-checks.log
- Verified: verify_readout: pass (24 numbers on 9 lines; 8 queries, 3 checks, 0 given)
```