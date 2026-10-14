## Answer
Headline: can't tell
本仓库没有购买数据:`conversions` 记录的是加入购物车事件,不是购买,所以无法算出"搜索到购买"的占比。[q2]
- Observed: not computed (购买只记录在订单系统,warehouse.db 里没有;只有加购率 8.30% 可作上界代理,不是答案) [q3]
- Adjusted: not computed (没有购买指标,无可调整的对象)
- Causal effect: not identified (这是描述性比率问题,不涉及因果;需要订单系统数据才能给出数值)

## What it means for 季度模型
不要把 8.30% 加购率填入季度模型当作购买转化率;真实购买率必然不高于加购口径,差距未知。需要订单系统按搜索归因的购买数,才能填入。 [q3]

## Why we believe it
- Alternatives considered:
  - 把 conversions 当作购买使用: ruled out by metrics.json 的 pitfalls 明确写明 conversions 是加购事件 [measured]
  - 数据不完整导致误判: ruled out by 2026-10-11 行数为趋势日中位数的 103%,七天齐全 [check:completeness#1] [measured]
  - mix-shift / 星期效应 / 口径变更: ruled out as 不适用,因为没有计算任何变化量,只有单周水平 [inferred]
- Checks run:
  - completeness: pass 2026-10-11 行数为趋势日中位数的 103% [check:completeness#1]
  - fanout: skipped 没有 join
  - mix_shift: skipped 没有比较两个时期,也没有分群表
  - srm: skipped 不是实验

## Caveats, and what would change the answer
- 若能提供订单系统中归因到搜索的购买数(2026-10-05 至 10-11),即可按 购买数/搜索数 计算。
- 加购率代理(70,030 / 843,738 = 8.30%)只是上界参考,购买占加购的比例未知。 [q3]

## Provenance
- Metric: search_purchase_rate(购买/搜索)在 metrics.json 中标记 available=false, from metrics.json
- Data: search_daily_c,through 2026-10-11
- Reconciled: not done (没有购买口径的可信来源可对账)
- Queries and checks: .ds-queries.log, .ds-checks.log
- Verified: verify_readout: pass (4 numbers on 4 lines; 2 queries, 1 checks, 0 given)