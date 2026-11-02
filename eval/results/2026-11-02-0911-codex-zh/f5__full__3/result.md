## Answer
Headline: can't tell [inferred]

治疗组观测 CTR 为 31.20%，对照组为 30.00%，差异约 +1.20 个百分点，但分组异常尚未解释，无法确认治疗改善了 CTR。[q5] [measured] [inferred]

- Observed: +1.200 pp (95% CI +1.125 至 +1.275)，搜索独立假设下的两比例区间。[check:mix_shift#1] [measured]
- Adjusted: +1.200 pp (95% CI +1.125 至 +1.275), holding 日期的搜索量权重固定为两组平均，仍使用搜索独立假设。[check:mix_shift#1] [measured]
- Causal effect: not identified (需去重随机分配记录，查清分组偏差与缺失原因，并按随机化单位重算)。[q1, check:srm#1] [inferred]

## What it means for 上线决策
尚未提供最小有意义提升；若暂以超过零为门槛，描述性区间完全为正，但不能据此上线，因为该区间不包含分组选择偏差。[check:mix_shift#1, check:srm#1] [inferred]
应先解释分组异常，再将有效的因果区间与实际业务门槛比较。[inferred]

## Why we believe it

- Alternatives considered:
  - 日期构成及共同星期效应: ruled out 作为主要解释；按日与按实验周分解均得到约 +1.200 pp，日期构成贡献约 +0.000 pp。[check:mix_shift#1, check:mix_shift#2] [inferred]
  - 样本选择或分流异常: ruled in 为待查解释；累计 users 为对照 499,930、治疗 475,990，治疗占 48.77%；它们不一定是去重分配人数。[q2, check:srm#1] [measured] [inferred]
  - 平台、国家或来源构成差异: ruled in 为未排除解释，表内没有这些维度。[q1] [inferred]
  - 数据缺失、埋点或定义变化: ruled in 为未排除解释；日期齐全和量级稳定不能证明无持续漏报，且无加载水位或埋点版本表。[q1, q3] [inferred]
  - 治疗真实改善 CTR: ruled in 为可能解释，但现有汇总不能将其与选择偏差区分。[q5, check:srm#1] [inferred]
- Checks run:
  - srm: fail 将累计 users 暂作独立分配数时，p=9.86e-130；实际分配层面的检验仍需去重记录，该 p 值不能视为已验证的随机化检验。[check:srm#1] [measured] [inferred]
  - completeness: pass 两组 2026-09-20 至 2026-09-30 的逐日搜索量均通过历史量级检查；不能排除持续漏报。[check:completeness#4, check:completeness#14, check:completeness#18, check:completeness#28] [measured] [inferred]
  - completeness: could not run 两组 2026-09-17 至 2026-09-19 缺少足够早期基线；全期每日均有两组记录。[q3, check:completeness#1, check:completeness#2, check:completeness#3, check:completeness#15, check:completeness#16, check:completeness#17] [measured]
  - mix_shift: pass 按日及按实验周结果一致；平台、国家、来源无法检查。[check:mix_shift#1, check:mix_shift#2, q1] [measured]
  - fanout: skipped 未做连接。[inferred]
  - 数据合法性: pass 日期与组别无重复汇总行，计数无空值、负值或 clicks 超过 searches。[q4] [measured]

## Caveats, and what would change the answer

- 区间假设每次搜索是独立二项试验；同一用户重复搜索可能使区间过窄。需要用户级分配与搜索、点击汇总计算聚类区间。[inferred]
- 需要确认 clicks 是否为发生点击的搜索数、users 是否为分配人数，以及实际上线门槛；日期调整无法修复未知选择偏差。[inferred]

## Provenance

- Metric: SUM(clicks)/SUM(searches)，筛选 ranker_boost、2026-09-17 至 2026-09-30（含首尾），按组汇总日表；from stated here [guess]。DS_OVERLAY_DIR 未设置，无可用 metrics.json。
- Data: warehouse.db 的 experiment_daily；数据覆盖至 2026-09-30，最后完整期间无法通过加载水位确认。[q1, q3] [measured]
- Reconciled: not done (数据库无独立仪表盘或可信对账来源)。[q1] [measured]
- Queries and checks: .ds-queries.log、.ds-checks.log；复算脚本 analyze.py，报告 readout.md。
- Verified: verify_readout: pass (16 numbers on 6 lines; 5 queries, 13 checks, 0 given)
