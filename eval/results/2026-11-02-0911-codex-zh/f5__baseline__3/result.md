## Answer
Headline: can't tell [inferred]  
按点击数／搜索数计算，treatment CTR 为 31.200%，control 为 30.000%，观察提升约 1.200 个百分点，但尚不能确认因果改善。[measured / inferred]

- Observed: +1.200 个百分点（95% 区间：+1.125 至 +1.275；假设搜索独立）[measured]
- Adjusted: +1.200 个百分点（95% 区间：+1.125 至 +1.275；假设搜索独立），holding 日期权重 fixed（每天等权）[measured]
- Causal effect: not identified（需核验随机分配、解释人数失衡，并取得完整的分配及用户级结果数据）[inferred]

## What it means for 上线决策

未提供足以改变上线决策的最小提升阈值；若暂以 0 个百分点为阈值，上述条件区间全高于它。[guess / measured] 但分流异常尚未解释，且区间未处理用户内相关性，因此不足以支持因果收益驱动的上线决定。[inferred]

## Why we believe it

- Alternatives considered:
  - 日期构成造成表面提升：ruled out，日期等权调整后提升仍为 +1.200 个百分点。[measured]
  - 分流、筛选或漏数造成偏差：ruled in（尚不能排除），每天 treatment 均少 1,710 个用户，用户日占比仅 48.773%。[measured / inferred]
- Checks run:
  - 日期与重复行：pass，14 天、两组共 28 行，无重复日期分组。[measured]
  - 计数合法性：pass，计数为正且点击数不超过搜索数。[measured]
  - 50/50 比例：flag，若每日 users 是独立随机分配用户，首日比例检验 p≈9.3×10⁻¹¹；未将跨日用户重复计为独立样本。[measured / guess]
  - 用户聚类区间：could not run，缺少用户标识及用户级结果。[measured]
  - 数据入库完整性：could not run，缺少完成标记或源数据核对。[measured]

## Caveats, and what would change the answer

- 所列区间是假设每次搜索为独立伯努利试验的近似区间；每行搜索数均为用户数的 6 倍，现有汇总无法估计用户内相关性。[guess / measured]
- 日期调整不能修复选择偏差；查明人数失衡原因、确认指标口径并取得用户级数据后，结论及区间可能改变。[inferred]

## Provenance

- Metric: CTR = SUM(clicks) / SUM(searches)，from stated here [guess]；未找到 metrics.json。[measured]
- Data: warehouse.db 的 experiment_daily，ranker_boost，2026-09-17 至 2026-09-30；日期覆盖完整，最后完整入库周期未能确认。[measured]
- Reconciled: not done（未提供 dashboard 或独立源数据）。[measured]
- Queries and checks: [查询及检查日志](/private/tmp/ds-runs/f6a16b17dc/analysis/queries_and_checks.json)、[可复现脚本](/private/tmp/ds-runs/f6a16b17dc/analysis/analyze.py)。[measured]
