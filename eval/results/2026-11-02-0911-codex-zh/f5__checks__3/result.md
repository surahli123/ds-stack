## Answer
Headline: can't tell [inferred]  
治疗组观察 CTR 高出约 1.200 个百分点，但用户计数偏离计划分流，尚不能认定是治疗导致的改善。[measured/inferred]
- Observed: +1.200 个百分点（95% 区间：+1.125 至 +1.275；假设搜索相互独立）[measured]
- Adjusted: +1.200 个百分点（95% 区间：+1.125 至 +1.275；同上假设），holding 日期构成 fixed，使用两组日期权重的均值。[measured]
- Causal effect: not identified（需要去重随机分配记录、曝光及日志核对，解释分流异常，并按随机化单位估计不确定性）。[inferred]

## What it means for 上线决策
尚未提供足以改变上线决定的最小提升阈值；若暂以 0 个百分点为门槛，观察区间完全高于它。[guess/measured] 但该区间不涵盖选择偏差，当前证据不足以据此上线。[inferred]

## Why we believe it
- Alternatives considered:
  - 日期构成差异解释提升：ruled out，日期混合贡献约为 0.000 个百分点，调整后差异基本不变。[measured]
  - 分流、筛选或漏记异常：ruled in 为待排查解释，每日用户计数均偏离计划比例；具体原因未识别。[measured/inferred]
- Checks run:
  - completeness: pass，两组末日搜索量及用户量均与近期中位数一致；这不能证明日志全部入库。[measured/inferred]
  - 日期覆盖与计数合法性: pass，实验期日期与组别组合齐全，点击数未超过搜索数。[measured]
  - srm: fail，汇总用户日占比为控制组 51.2265%、治疗组 48.7735%；逐日检查均失败，p < 10⁻¹⁰。这里检查的是表内用户计数，尚非经核实的随机分配人数。[measured]
  - mix_shift: pass，未发现日期构成主导差异。[measured]
  - fanout: skipped，查询未使用连接。[measured]

## Caveats, and what would change the answer
- 区间采用独立二项近似；重复用户、用户内搜索相关性可能使区间过窄，汇总表无法校正。[inferred]
- users 跨日可能重复，汇总 SRM 不能视为正式分配检验；逐日异常也可能来自治疗影响活跃度。[inferred]
- 补充分配与曝光明细、确认 CTR 口径、解释异常并提供上线阈值后，可重新判断。[inferred]

## Provenance
- Metric: Σclicks / Σsearches；未找到 metrics.json，口径 stated here [guess]。
- Data: warehouse.db 的 experiment_daily，筛选 ranker_boost、2026-09-17 至 2026-09-30；数据覆盖至末日，完整入库状态未获独立确认。[measured]
- Reconciled: not done（没有提供仪表盘或独立源数据）。[measured]
- Queries and checks: [查询及结果](/private/tmp/ds-runs/8fa178bacc/analysis/queries.json)、[检查日志](/private/tmp/ds-runs/8fa178bacc/analysis/.ds-checks.log)、[复现脚本](/private/tmp/ds-runs/8fa178bacc/analysis/analysis.py)。[measured]
