## Answer
Headline: can't tell [inferred]

无法确定该周有多少百分比的搜索关联了购买：仓库缺少购买记录，现有 conversions 仅表示加购。[q1] [inferred]

- Observed: not computed（缺少购买分子，无法计算比例或区间）[inferred]
- Adjusted: not computed（原始购买比例不可计算）[inferred]
- Causal effect: not identified（需要随机实验或其他可识别因果关系的设计）[inferred]

## What it means for 季度财务模型
当前无法提供购买转化率及其区间，不应将加购率填入购买率参数。[inferred] 财务尚未提供会改变模型决策的最小变化阈值，因此也无法判断估计精度是否足够。[inferred]

## Why we believe it

- Alternatives considered:
  - 用 conversions 代表购买：ruled out，metrics.json 明确规定它记录加购，且购买数据仅在订单系统中。[inferred]
  - 缺失购买数据：ruled in，指标注册表标为不可用，数据库结构仅包含搜索日汇总表。[q1] [measured]
  - 目标周日期缺失：ruled out，所有目标日期都有搜索汇总；这不证明订单完整或搜索已全部入库。[q2] [measured]
  - 流量构成、季节性、星期效应及日志口径变更：ruled in 为潜在影响因素；当前仅有单周汇总，无法排除或量化其影响。[q1, q2] [inferred]
- Checks run:
  - completeness: pass 2026-10-11: 123422 rows = 103% of the trailing days (under 3 weeks of same-weekday history) median (119469) [check:completeness#1] [measured]
  - completeness 范围：flag 上述 rows 输入为每日搜索数；检查仅识别末日搜索量异常下降，不能确认购买数据完整性。[q2] [inferred]
  - fanout: skipped 未进行关联。[inferred]
  - mix_shift: skipped 未估计跨期变化，且没有细分维度。[q1] [inferred]
  - srm: skipped 无实验分组。[q1] [inferred]

## Caveats, and what would change the answer

- 接入订单及搜索关联数据，明确购买成功状态、归因窗口、时区和去重规则，并等待归因窗口结束后，才能计算比例及适当区间。[inferred]
- 搜索与购买的关联比例不等于搜索带来的增量购买效应。[inferred]

## Provenance

- Metric: search_purchase_rate，from metrics.json，标记 available=false；精确分子、过滤和归因规则尚未给出。拟用“该周至少关联一次有效购买的搜索数／该周全部符合条件的搜索数”，搜索粒度，stated here [guess]
- Data: search_daily_c，覆盖 2026-10-05 至 2026-10-11；最后完整入库期未获确认，订单数据不在仓库中。[q1, q2] [measured]
- Reconciled: not done（没有购买数据或同口径购买率看板可供核对）[inferred]
- Queries and checks: .ds-queries.log、.ds-checks.log；结论文件 readout.md。[measured]
- Verified: verify_readout: pass (4 numbers on 1 lines; 2 queries, 1 checks, 0 given)
