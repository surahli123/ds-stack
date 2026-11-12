## Answer
Headline: can't tell [inferred]  
治疗组观测 CTR 为 31.200%，对照组为 30.000%，相差 +1.200 个百分点，但尚不能确认为治疗带来的提升。[measured；因果判断 inferred]
- Observed: +1.200 个百分点（95% 区间：+1.125 至 +1.275；点估计 measured，假设性区间 inferred）
- Adjusted: +1.200 个百分点（95% 区间：+1.125 至 +1.275），holding 日期构成 fixed，按每日等权标准化。[点估计 measured；假设性区间 inferred]
- Causal effect: not identified（需要核验随机分配、解释用户计数失衡，并取得按随机化单位记录的完整数据）。[inferred]

## What it means for 上线决策
尚未提供最小有意义提升，暂以 0 个百分点作为参考门槛。[guess] 观测区间虽全部高于该门槛，但分组失衡及区间假设未经核验，不能据此确认上线收益。[inferred]

## Why we believe it
- Alternatives considered:
  - 日期构成造成表面提升：ruled out 为唯一解释；14 天内治疗组 CTR 均更高，日期标准化后差值仍为 +1.200 个百分点。[measured]
  - 分流异常、漏记或活跃用户筛选：ruled in 为未排除的解释；治疗组每天用户计数均少 1,710，但无分配日志可追查。[inferred]
- Checks run:
  - 日期及分组覆盖：pass 两组各有 14 天记录，无重复日期分组、空值或计数越界。[measured]
  - 50/50 比例：flag 治疗组每日用户占比约 48.773%；若这些是独立随机分配用户，单日比例检验 p≈9.4×10⁻¹¹。[占比 measured；检验 inferred]
  - 用户聚类：could not run 无用户标识；每日每组 searches/users 均为 6，不能确认搜索之间独立。[measured]
  - 入库完整性：could not run 无完成标记或源日志，日期齐全不代表事件齐全。[inferred]

## Caveats, and what would change the answer
- 两个区间均假设每次搜索是独立二元点击试验；无法验证重复点击及用户内相关性，不能视为有效的实验因果区间。[inferred]
- users 跨日可能重复，累计值是用户日，未当作独立用户做总体分流检验。[inferred]
- 确认 CTR 口径、补充分配及事件日志、解释失衡并按随机化单位重算区间，可能改变结论；日期调整不能修复选择偏差。[inferred]

## Provenance
- Metric: CTR 暂定义为 Σclicks/Σsearches；提升为治疗减对照，乘以 100，单位为百分点；未找到 metrics.json，stated here [guess]。
- Data: warehouse.db 的 experiment_daily，筛选 ranker_boost；记录覆盖 2026-09-17 至 2026-09-30，最后完整入库日期无法确认。[measured]
- Reconciled: not done（无 dashboard 或独立源数据）；对照组 899,874/2,999,580，治疗组 891,051/2,855,940。[measured]
- Queries and checks: [SQL 查询](/private/tmp/ds-runs/751d516b08/analysis/queries.sql)、[计算与检查脚本](/private/tmp/ds-runs/751d516b08/analysis/analyze.py)、[结果日志](/private/tmp/ds-runs/751d516b08/analysis/analysis_results.json)。[measured]
