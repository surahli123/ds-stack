## Answer
Headline: can't tell
这个仓库没有购买记录,所以算不出搜索到购买的占比。metrics.json 标明 search_purchase_rate 不可用,购买只记录在订单系统里。search_daily_c.conversions 统计的是加入购物车事件,不是购买。[measured]
- Observed: not computed (购买数据不在 warehouse.db 中)
- Adjusted: not computed (没有购买数据可供调整)
- Causal effect: not identified (这是描述性指标,没有实验设计;需要订单系统中按搜索归因的购买记录)

## What it means for 季度模型
不要把 conversions(加购)当作购买率填入财务模型。需要从订单系统取得 2026-10-05 至 2026-10-11 的购买数,再与同期搜索量(本周每日搜索量见 [q2])按同一口径相除。[given]

## Why we believe it
- Alternatives considered:
  - 用 conversions 作为购买的替代: ruled out,metrics.json 明确警告其为加购事件而非购买 [measured]
  - 数据未加载完整: ruled out,周内最后一天 2026-10-11 行数为趋势中位数的 103% [check:completeness#1] [measured]
- Checks run:
  - completeness: pass 2026-10-11 行数为趋势中位数的 103% [check:completeness#1]
  - mix_shift: skipped 没有可计算的比率变化
  - fanout: skipped 没有做连接
  - srm: skipped 不是实验

## Caveats, and what would change the answer
- 若订单系统能提供按搜索会话归因的购买数,即可按"购买会话数 ÷ 搜索数"计算。分母用搜索次数还是会话,需先与搜索分析团队确认。
- 加购不等于购买,二者之间的转化率未知,不能互相换算。

## Provenance
- Metric: 搜索到购买占比 = 购买数 ÷ 搜索数,metrics.json 中标记为不可用(available: false),from metrics.json
- Data: search_daily_c(date, searches, clicks, conversions),through 2026-10-11
- Reconciled: not done (没有购买数可与任何来源对账)
- Queries and checks: .ds-queries.log, .ds-checks.log
- Verified: verify_readout: pass (2 numbers on 2 lines; 1 queries, 1 checks, 1 given)