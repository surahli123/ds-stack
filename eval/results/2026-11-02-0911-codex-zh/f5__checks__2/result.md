## Answer
Headline: can't tell [inferred]  
治疗组观测 CTR 高出约 1.200 个百分点，但分流检查失败，尚不能认定这是治疗造成的改善。[measured / inferred]

- Observed: +1.200 个百分点（95% 区间：+1.125 至 +1.275；搜索独立假设下）[measured]
- Adjusted: +1.200 个百分点（95% 区间：+1.125 至 +1.275；搜索独立假设下），holding 日期构成 fixed，采用两组日期权重的均值。[measured]
- Causal effect: not identified（需要去重的随机分配记录、完整曝光与点击日志，查明分流偏差后重新估计）。[inferred]

## What it means for 上线决策
尚未提供能改变上线决定的最小收益门槛；若仅以正收益为门槛，上述观测区间完全高于零，但它不是可信的因果区间。[measured / inferred] 建议先查明分流异常，再据此决定是否上线。[inferred]

## Why we believe it
- Alternatives considered:
  - 日期构成变化：ruled out，按日期调整后差值仍为 +1.200 个百分点。[measured]
  - 分流或观测样本选择异常：ruled in，记录中的用户比例偏离预定分流；具体原因尚未确定。[measured / inferred]
- Checks run:
  - srm：fail，首日 control/treatment 用户数为 35,700/33,990，p=9.32×10⁻¹¹；全期日用户数合计检查也失败，但可能重复计人，不能替代分配用户检查。[measured]
  - completeness：pass，末日记录数和搜索量均与近期中位数一致；仅为完整性代理检查。[measured / inferred]
  - mix_shift：pass，日期构成贡献约为 0.000 个百分点。[measured]
  - 数据有效性：pass，未发现重复日期组别键、负计数或点击数超过搜索数。[measured]
  - fanout：skipped，未使用数据库连接。[measured]

## Caveats, and what would change the answer
- 区间假设搜索相互独立且点击符合二项口径；重复用户的相关性可能使区间过窄，现有汇总表无法估计用户聚类误差。[inferred]
- `users` 是否代表随机分配用户未说明；异常也可能来自活跃度或日志覆盖差异，不能直接断言随机化失效。[inferred]
- 日期调整不能修复样本选择偏差；补齐分配日志、指标定义和上线门槛后，应重新评估。[inferred]

## Provenance
- Metric: CTR = SUM(clicks) / SUM(searches)，差值为 treatment − control；from stated here [guess]，未提供 metrics.json。
- Data: `warehouse.db` 的 `experiment_daily`，筛选 `ranker_boost`、2026-09-17 至 2026-09-30；末日通过完整性代理检查，但无加载水位确认最后完整日期。[measured / inferred]
- Reconciled: not done（未提供仪表盘或独立来源）。[measured]
- Queries and checks: [查询与结果](analysis_output/queries.json)、[检查结果](analysis_output/checks_results.json)、[复现脚本](analysis_output/analyze.py)；检查原始日志为 `.ds-checks.log`。[measured]
