## Answer
Headline: −2.0968 个百分点（观测总 CTR 变化；95% CI：−2.248 至 −1.946），不是 v2 的因果效应。[check:mix_shift#1]
总体 CTR 从 30.4212% 降至 28.3243%；按平台×国家作中点权重分解，流量构成项为 −2.0945 个百分点，组内变化为 −0.0023 个百分点（95% CI：−0.153 至 +0.148）。**可归因于 v2 的百分点无法从这些数据识别，不能答成零，也不能把组内残差当作 v2 效应。** [q4, check:mix_shift#1]

## What it means for 回滚决策
不建议仅凭这次总体下降判定 v2 有害并回滚：构成变化已在算术上解释几乎全部下降，但这不证明 v2 无害，也不说明构成变化与它无关。[q4, check:mix_shift#1]
尚未给出触发回滚的最小损害阈值；组内变化区间跨过零，且并非因果效应区间，不能用它保证满足回滚阈值。应通过同期随机分流的旧版对照估计影响，再按预设阈值决策。[q4, check:mix_shift#1]

## Why we believe it
- Alternatives considered:
  - 流量构成：纳入解释。较低 CTR 的移动端份额由 40.11% 升至 55.07%；仅按平台分解时，构成项为 −2.0932、组内项为 −0.0036 个百分点，与平台×国家结果一致。[check:mix_shift#1, check:mix_shift#3] [measured]
  - v2：不能确认或排除因果影响。前期各组全部为 v1，后期全部为 v2，版本与时间完全重合；发布记录仅确认全量上线，没有同期旧版对照。[q2, q4] [inferred]
  - 星期构成：两期均为完整周一至周日，排除比较窗口星期数量不同；只有两周记录，无法排除跨周需求或季节性变化。[q3] [inferred]
  - 数据不完整：未发现明显缺日或量级异常；共 14 天，每天 4 个分群单元，两期每组均覆盖 7 天，未发现空值、负值或点击大于搜索量的单元。无加载完成标记，不能严格证明数据已全部到齐。[q3, q4] [measured]
  - 埋点或口径变化：无法排除。现有发布表只记载 ranker 上线，没有独立埋点审计、指标定义或可信看板可供核对。[q1, q2] [inferred]
- Checks run:
  - completeness: pass — 2026-09-27: 101828 rows = 102% of the trailing days (under 3 weeks of same-weekday history) median (99521.5) [check:completeness#1]
  - completeness: pass — 2026-10-04: 101900 rows = 102% of the trailing days (under 3 weeks of same-weekday history) median (99762) [check:completeness#2]
  - mix_shift: flag — mix-dominant: overall change -2.10 pp = within-segment -0.00 pp (95% CI -0.15 to +0.15) + mix -2.09 pp (mix share 100%); report the mix shift as part of the answer [check:mix_shift#1]
  - mix_shift（粗粒度复核）: flag — mix-dominant: overall change -2.10 pp = within-segment -0.00 pp (95% CI -0.15 to +0.15) + mix -2.09 pp (mix share 100%); report the mix shift as part of the answer [check:mix_shift#3]
  - 粗粒度检查曾因输入 JSON 格式错误未运行，已修正重跑；原始失败记录保留在日志中。
  - fanout: skipped — 未使用 join。
  - srm: skipped — 无随机实验分配或计划分流比例，未读取实验 lift。

## Caveats, and what would change the answer
- 分解是描述性恒等式。若版本影响重复搜索、用户返回或平台构成，构成项也可能包含版本作用；需要随机对照识别总效应。
- 区间假设搜索之间独立且点击数可视为二项成功数；没有用户级数据，无法处理重复搜索聚类，也不能核实一次搜索是否可能多次计入点击。确认指标定义并取得用户级随机实验汇总后重算。
- 完整性检查以搜索总量衡量日流量，不是原始事件行数；两周历史不足以形成稳定的同星期基线。需加载完成标记与更长历史验证。
- 缺少流量来源维度、同期其他变更与埋点审计。补齐这些信息可以检验替代解释，但单纯前后比较仍不能识别因果效应。

## Provenance
- Metric: stated here [guess]：CTR = SUM(clicks) / SUM(searches)，来源 search_daily；以日期×平台×国家×ranker 汇总行累计分子分母，非日 CTR 简单平均。仅过滤 2026-09-21 至 2026-09-27 和 2026-09-28 至 2026-10-04，无其他过滤；按测试要求未读取 DS_OVERLAY_DIR。
- Data: 仅本地 warehouse.db 中 search_daily 与 release_log；观察覆盖至 2026-10-04，加载完成状态未经独立认证。
- Reconciled: not done（本地没有独立可信看板或指标来源，禁止外部集成）。
- Queries and checks: .ds-queries.log 与 .ds-checks.log；检查摘要保留工具原文，完整输出见日志。
- Verified: verify_readout: pass (36 numbers on 8 lines; 4 queries, 4 checks, 0 given)
