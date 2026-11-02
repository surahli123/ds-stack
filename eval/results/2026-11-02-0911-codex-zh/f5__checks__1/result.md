## Answer
Headline: can't tell [inferred]  
处理组观测 CTR 为 31.20%，对照组为 30.00%，相差 +1.20 个百分点，但样本比例异常使其不能直接解释为因果提升。[measured / inferred]

- Observed: +1.200 个百分点（名义 95% 区间：+1.125 至 +1.275；假设搜索相互独立）[measured]
- Adjusted: +1.200 个百分点（名义 95% 区间：+1.125 至 +1.275），holding 两组平均的日期搜索占比 fixed。[measured]
- Causal effect: not identified（需核验原始随机分配记录，解释样本失衡，并取得完整用户级结果）。[inferred]

## What it means for 上线决策
尚未提供足以改变上线决定的最小提升；暂以零个百分点为参考。[guess] 观测区间虽全为正，但不包含选择偏差的不确定性，不能据此认定满足上线门槛。[inferred]

## Why we believe it
- Alternatives considered:
  - 日期流量构成造成表面提升：ruled out 作为主要解释；日期调整前后差异均为 +1.200 个百分点。[measured]
  - 分流、入样或埋点异常：ruled in 为待查解释；每日用户数均偏离计划比例，但汇总表无法区分具体原因。[inferred]
- Checks run:
  - srm：fail；按用户数汇总，对照/处理占比为 51.23%/48.77%；每日检查也全部失败，每日 p < 10⁻¹⁰。用户数未证实为分配人数。[measured]
  - completeness：pass；末日两组行数、用户数及搜索量均与近期中位数一致；仅为数据量检查。[measured]
  - mix_shift：pass；日期构成贡献四舍五入为 0.0000 个百分点。[measured]
  - 数据有效性：pass；日期与组别组合齐全且无重复，未发现空值、负数或点击数超过搜索数。[measured]
  - fanout：skipped；未使用关联查询。[measured]

## Caveats, and what would change the answer
- 区间假设每次搜索为独立二元事件；重复用户与多次点击可能使该假设不成立，现有数据无法计算用户聚类区间。[inferred]
- 日用户数相加可能重复计人；每日比例异常仍存在，但可能反映活跃度变化而非分配故障。[inferred]
- 取得分配日志、用户级数据、正式指标定义及上线门槛后重新评估；若无法排除选择偏差，应修复后重跑实验。[inferred]

## Provenance
- Metric: CTR = SUM(clicks) / SUM(searches)，from stated here；未提供 metrics.json。[guess]
- Data: warehouse.db 的 experiment_daily，实验窗口为 2026-09-17 至 2026-09-30；末日通过数据量检查，实际加载完整性未经水位记录确认。[measured / inferred]
- Reconciled: not done（未提供独立看板或源日志）。[measured]
- Queries and checks: [查询记录](/private/tmp/ds-runs/64585578dd/analysis/queries.jsonl)、[检查日志](/private/tmp/ds-runs/64585578dd/analysis/.ds-checks.log)、[复现脚本](/private/tmp/ds-runs/64585578dd/analysis/analyze.py)、[方法与假设](/private/tmp/ds-runs/64585578dd/analysis/methodology.md)。[measured]
