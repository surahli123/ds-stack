## Answer
Headline: can't tell [inferred]

治疗组观察 CTR 比对照组高约 +1.200 pp，但用户计数偏离预设分流且原因未明，无法确认这是治疗效果。[q5, check:srm#1] [inferred]

- Observed: +1.200 pp (95% CI +1.125 至 +1.275；搜索独立假设下的名义区间) [check:mix_shift#1] [measured]
- Adjusted: +1.200 pp (95% CI +1.125 至 +1.275；同一假设), holding 两组平均日期流量权重 fixed [check:mix_shift#1] [measured]
- Causal effect: not identified (需核实原始随机分配、跨日用户去重及漏报情况，解释分流偏差后重算，或修复后重跑实验) [q1, check:srm#1] [inferred]

## What it means for 上线决策

尚未提供最小上线收益门槛；即使暂以 +0 pp 为门槛，观察区间虽完全高于它，也不能克服分流偏差，建议暂缓依据本实验上线。[check:mix_shift#1, check:srm#1] [inferred]
实际门槛若落在上述区间内，名义统计结果也无法明确达标；需补充业务门槛并恢复可信的实验估计。[check:mix_shift#1] [inferred]

## Why we believe it

- Alternatives considered:
  - 分流或样本选择异常：ruled in 为待排查解释；累计日用户数为对照 499,930、治疗 475,990，占比约 51.23% / 48.77%，但不能确认这些是互斥、去重的分配人数。[q2, check:srm#1] [inferred]
  - 日期构成、星期及共同季节变化：ruled out 为观察差异的主要解释；同期比较，按日及按周分解均显示日期混合贡献约 +0.000 pp。[q4, check:mix_shift#1, check:mix_shift#2] [inferred]
  - 平台、国家、渠道构成变化：ruled in 为未排除解释；表中没有这些维度。[q1] [inferred]
  - 数据不完整、埋点或定义变化：ruled in 为未排除解释；每天都有数据、末日量正常，但缺少加载水位、原始事件及埋点变更记录。[q1, q3] [inferred]
  - 治疗真实提高 CTR：ruled in 为可能解释；观察差异为正，但异常尚未解释，不能据此归因。[q5, check:srm#1] [inferred]
- Checks run:
  - srm: fail sample ratio mismatch: observed shares [0.512265, 0.487735] vs expected [0.5, 0.5]: chi2 587.26, p 9.86e-130; arms are not comparable until the cause is found [check:srm#1] [measured]
  - completeness: pass 2026-09-30: 214260 rows = 100% of the trailing days (under 3 weeks of same-weekday history) median (214260) [check:completeness#1] [measured]
  - completeness: pass 2026-09-30: 204000 rows = 100% of the trailing days (under 3 weeks of same-weekday history) median (204000) [check:completeness#2] [measured]
  - mix_shift: pass overall change +1.20 pp = within-segment +1.20 pp (95% CI +1.12 to +1.27) + mix +0.00 pp (mix share 0%) [check:mix_shift#1, check:mix_shift#2] [measured]
  - fanout: skipped 未执行连接。[q4, q5] [measured]
  - 字段和日期检查: pass 两组各有 14 天、每天各一行；关键计数无空值、负数或 clicks 大于 searches。[q2, q3, q5] [measured]

## Caveats, and what would change the answer

- 区间按两比例正态近似计算，假设每次搜索是独立二项试验；同一用户重复搜索可能使区间偏窄。需用户级数据及点击口径确认后重算。[inferred]
- SRM 使用累计日用户计数作为代理；若用户跨日重复或 users 指活跃用户，其检验概率不能直接解释为随机分配检验。需要原始分配表确认，不能靠日期调整消除异常。[inferred]
- completeness 输出中的 rows 实际输入为搜索量；它只检查末日相对历史的量级，不能证明整个实验无系统性漏报。需加载完成标志及独立事件源核对。[inferred]

## Provenance

- Metric: CTR = SUM(clicks) / SUM(searches)，治疗减对照乘以 100 得 pp；筛选 ranker_boost、2026-09-17 至 2026-09-30（含首尾），源粒度为日期×实验×组；from stated here [guess]（DS_OVERLAY_DIR 未设置，无可用 metrics.json）。
- Data: warehouse.db 的 experiment_daily；数据覆盖至 2026-09-30，末日量检查通过，最后完整期尚无加载水位确认。[q1, q3] [measured]
- Reconciled: not done (未提供独立 dashboard 或原始事件源)。[measured]
- Queries and checks: .ds-queries.log、.ds-checks.log；复算脚本 analysis_checks.py，报告 readout.md。[measured]
- Verified: verify_readout: pass (35 numbers on 11 lines; 5 queries, 5 checks, 0 given)
