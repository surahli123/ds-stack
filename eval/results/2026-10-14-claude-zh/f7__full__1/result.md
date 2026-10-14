## Answer
Headline: can't tell
本仓库没有购买数据:metrics.json 标明 search_purchase_rate 不可用,`conversions` 只是加购事件,不是购买;该周加购率为 8.30%(70,030 / 843,738)[q2],不能当作购买率交给财务。
- Observed: not computed (购买只记录在订单系统中,本仓库没有)
- Adjusted: not computed (没有购买指标可调整)
- Causal effect: not identified (需要订单系统的购买记录与搜索关联;本问题也不是因果问题)

## What it means for 季度模型
财务不应使用 8.30% [q2] 作为购买占比,它是加购率,购买占比只会更低或不同;需要从订单系统取得该周的购买数后才能给出数字。

## Why we believe it
- Alternatives considered:
  - 用 conversions(加购)代替购买: ruled out by metrics.json 的 pitfall 说明 conversions 为加购事件 [q2] [measured]
  - 数据不完整导致无法计算: ruled out by 该周 7 天齐全 [q1] [measured]
- Checks run:
  - completeness: pass 2026-10-11 行数为近期中位数的 100% [check:completeness#1]
  - fanout: skipped 没有做 join
  - mix_shift: skipped 没有计算变化的比率
  - srm: skipped 不是实验

## Caveats, and what would change the answer
- 取得订单系统中 2026-10-05 至 2026-10-11 的购买数及其对应的搜索数后即可计算;分母的口径(搜索次数 vs. 会话)需与财务确认。
- 加购到购买的转化比例未知,不能由加购率推算。

## Provenance
- Metric: 购买数 / 搜索数(搜索粒度),metrics.json 中 search_purchase_rate 标记为不可用 [guess 仅为定义,无数据]
- Data: search_daily_c,截至 2026-10-11
- Reconciled: not done (没有购买数据可对账)
- Queries and checks: .ds-queries.log 和 .ds-checks.log
- Verified: verify_readout: pass (6 numbers on 4 lines; 2 queries, 1 checks, 0 given)