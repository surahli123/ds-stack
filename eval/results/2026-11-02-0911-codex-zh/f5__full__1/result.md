## Answer
Headline: can't tell [inferred]

实验组观测 CTR 比对照组高 +1.200 pp，但人数比例异常尚未解释，无法确认是 treatment 带来的提升。 [check:mix_shift#1, check:srm#1] [inferred]

- Observed: +1.200 pp (95% CI +1.125 至 +1.275)，搜索独立的二项近似区间。 [check:mix_shift#1] [measured]
- Adjusted: +1.200 pp (95% CI +1.125 至 +1.275), holding 日期搜索权重固定为两组权重的均值；同样假定搜索独立。 [check:mix_shift#1] [measured]
- Causal effect: not identified (需核实随机分配人数、解释样本比例异常，并恢复完整的分配及结果数据)。 [check:srm#1] [inferred]

## What it means for 上线决策
尚未提供会改变上线决定的最小提升阈值；若只要求正向变化，描述性区间完全为正，但它不涵盖分流或选择偏差，不能据此批准上线。 [check:mix_shift#1, check:srm#1] [inferred]
应先解释分流异常，再把有效实验区间与正式上线阈值比较。 [inferred]

## Why we believe it

- Alternatives considered:
  - 日期构成、星期及共同季节性：ruled out 作为主要解释；两组同期覆盖完整日期，按日期和星期调整均不改变结论，日期构成贡献约 +0.000 pp；不能排除组别特有的时间影响。 [q3, check:mix_shift#1, check:mix_shift#2] [inferred]
  - 分流、筛选或漏记异常：ruled in 为待查解释；control 的 users 合计 499,930，treatment 为 475,990，偏离声明的等比分流，但 users 是否为独立分配人数未知。 [q2, check:srm#1] [inferred]
  - 末日明显掉量：ruled out；两组末日搜索量均与此前中位数一致，但持续漏记仍可能存在。 [check:completeness#1, check:completeness#2] [inferred]
  - 平台、国家、来源构成或埋点定义变化：ruled in 为未排除的解释；唯一表没有这些维度及埋点版本。 [q1] [inferred]
  - treatment 真正有效：ruled in 为可能解释；观察差异为正，但无法与上述偏差区分。 [check:mix_shift#1, check:srm#1] [inferred]
- Checks run:
  - srm: fail sample ratio mismatch: observed shares [0.512265, 0.487735] vs expected [0.5, 0.5]: chi2 587.26, p 9.86e-130; arms are not comparable until the cause is found [check:srm#1] [measured]
  - assignment_srm: could not run 缺少去重分配记录；上述检验仅以每日 users 合计作诊断，重复用户会破坏独立性。 [q1] [inferred]
  - completeness: pass 2026-09-30: 214260 rows = 100% of the trailing days (under 3 weeks of same-weekday history) median (214260) [check:completeness#1] [measured]
  - completeness: pass 2026-09-30: 204000 rows = 100% of the trailing days (under 3 weeks of same-weekday history) median (204000) [check:completeness#2] [measured]
  - coverage_and_validity: pass 每组均有 14 天、每天一行，未发现空值、负计数或 clicks 超过 searches；上面 completeness 的 rows 实际输入为搜索量。 [q3] [measured]
  - mix_shift: pass overall change +1.20 pp = within-segment +1.20 pp (95% CI +1.12 to +1.27) + mix +0.00 pp (mix share 0%) [check:mix_shift#1, check:mix_shift#2] [measured]
  - segment_mix: could not run 无平台、国家及来源字段。 [q1] [measured]
  - fanout: skipped 未使用连接。 [q3, q4] [measured]

## Caveats, and what would change the answer

- 区间假定每次搜索是独立的点击与否试验；重复搜索及多次点击可能使其失效。需确认指标口径并提供用户级数据，按随机化单位估计不确定性。 [inferred]
- users 是每日汇总，不能证明全期独立分配人数；需分配日志、过滤规则、埋点审计及装载水位来区分分流异常、活跃差异与漏记。 [inferred]
- 日期齐全和流量稳定不等于确认数据完整；当前无法验证持续性缺失。 [inferred]

## Provenance

- Metric: 实验 ranker_boost、2026-09-17 至 2026-09-30（含首尾），按组 SUM(clicks)/SUM(searches)，实验组减对照组乘以百，单位 pp；源粒度为日期×实验×组。from stated here [guess]（DS_OVERLAY_DIR 未设置，无 metrics.json）。
- Data: warehouse.db 的 experiment_daily，覆盖至 2026-09-30；末日量级检查通过，最后完整装载日期无法独立确认。 [q1, q3] [measured]
- Reconciled: not done (未提供独立仪表盘或可信对账来源)。 [measured]
- Queries and checks: .ds-queries.log、.ds-checks.log；复算脚本 analyze.py，报告 readout.md。 [measured]
- Verified: verify_readout: pass (32 numbers on 10 lines; 4 queries, 5 checks, 0 given)
