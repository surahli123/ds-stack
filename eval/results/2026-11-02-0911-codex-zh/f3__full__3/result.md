## Answer
Headline: can't tell [inferred]

整体 CTR 从 30.441% 降至 28.615%，下降集中在桌面端，但现有数据无法确定其中多少由 v3 导致。[q6] [measured] [inferred]

- Observed: -1.827 pp (95% CI: -1.978, -1.675)。[q6] [measured]
- Adjusted: -1.817 pp (95% CI: -1.967, -1.667), holding 平台×国家×星期的搜索份额固定为两周份额的平均值；这是描述性变化。[check:mix_shift#3] [measured]
- Causal effect: not identified（需要同期随机分配的旧版留存组，或具备可信反事实的其他设计）。[q2] [inferred]

## What it means for 回滚决策

尚未提供最小回滚门槛；若暂以下降 1 pp 为门槛，调整后区间完全超过该损失门槛，但不能证明回滚能恢复这些点击。[check:mix_shift#3] [guess] [inferred]
建议优先对桌面端做随机对照回滚验证；当前证据不足以仅凭 PM 的归因判定全面回滚收益。[q6] [inferred]

## Why we believe it

- Alternatives considered:
  - 已观测流量构成是主要解释：ruled out；构成项仅 -0.010 pp，分组内变化 -1.817 pp，合计原始变化 -1.827 pp。[check:mix_shift#3] [measured]
  - 星期构成差异：ruled out；两周覆盖相同星期，按星期进一步分层结果一致；其他季节性或同期冲击仍不能排除。[q2] [check:mix_shift#1, check:mix_shift#3] [measured] [inferred]
  - 缺日或缺分组：ruled out；每日平台×国家组合齐全且无重复，但没有入库水位证明事件全部到齐。[q2, q5] [measured] [inferred]
  - 埋点或口径改变：ruled in（仍可能）；发布日志没有埋点审计信息，不能排除漏记点击。[q1, q3] [inferred]
  - v3 导致下降：ruled in（候选解释，未证实）；版本与前后周完全重合，没有同期旧版对照。[q2, q3] [inferred]
  - 桌面端特有问题：ruled in；桌面端下降 -2.999 pp，移动端变化 -0.042 pp；移动端也接受新版，不能直接充当未处理对照。[q2, q6] [measured] [inferred]
- Checks run:
  - completeness: pass 2026-09-06: 4 rows = 100% of the trailing days (under 3 weeks of same-weekday history) median (4) [check:completeness#1] [measured]
  - completeness: pass 2026-09-13: 4 rows = 100% of the trailing days (under 3 weeks of same-weekday history) median (4) [check:completeness#2] [measured]
  - mix_shift: pass overall change -1.83 pp = within-segment -1.82 pp (95% CI -1.97 to -1.67) + mix -0.01 pp (mix share 1%) [check:mix_shift#3] [measured]
  - 分层敏感性: pass 平台×国家、仅平台两种较粗粒度均得到约 -1.82 pp 的调整后变化。[check:mix_shift#1, check:mix_shift#2] [measured]
  - 数据有效性: pass 未发现空计数、非正搜索数、负点击数或点击数超过搜索数。[q5] [measured]
  - fanout: skipped 未进行表连接。[inferred]
  - srm: skipped 没有随机分配记录或同期实验分组。[q1, q2] [inferred]

## Caveats, and what would change the answer

- 区间假设搜索相互独立且点击为搜索级二项结果；缺少用户级数据和点击去重定义验证。区间不包含因果混杂的不确定性。[inferred]
- 查询意图、流量来源变化无法检查；只有两周数据，不能验证长期趋势。补齐这些信息可能改变归因。[inferred]
- 只有假定不存在其他同期影响、分组内构成和埋点不变，且流量构成不是版本影响途径，才能把调整后变化解释为版本效应；这些假设尚未验证。[inferred]
- 需确认指标口径、入库水位及实际回滚门槛；随机保留旧版流量可检验回滚收益。[inferred]

## Provenance

- Metric: SUM(clicks) / SUM(searches)，按搜索加权，来源粒度为日期×平台×国家×ranker；筛选指定两周，纳入所有记录。from stated here [guess]；DS_OVERLAY_DIR 未设置，没有可用的 metrics.json。
- Data: warehouse.db 的 search_daily、release_log；比较 2026-08-31—2026-09-06 与 2026-09-07—2026-09-13，日分组覆盖截至 2026-09-13，事件最终入库完整性未独立确认。[measured]
- Reconciled: not done（没有独立仪表盘或可信汇总来源）。[measured]
- Queries and checks: `.ds-queries.log`、`.ds-checks.log`；派生计算与检查脚本为 `analyze.py`，报告为 `readout.md`。
- Verified: verify_readout: pass (29 numbers on 10 lines; 5 queries, 5 checks, 0 given)
