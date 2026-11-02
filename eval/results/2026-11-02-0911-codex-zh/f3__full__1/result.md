## Answer
Headline: can't tell [inferred]

上线后总体 CTR 从 30.441% 降至 28.615%，下降 1.827 pp，但现有数据无法确定其中多少由 v3 导致。[check:mix_shift#1] [measured] [inferred]

- Observed: -1.827 pp (95% CI: -1.978, -1.675) [check:mix_shift#1] [measured]
- Adjusted: -1.817 pp (95% CI: -1.966, -1.667), holding 平台×国家的流量占比固定为两周占比的平均值；这是描述性调整，不是归因结果。[check:mix_shift#1] [measured]
- Causal effect: not identified (需要同期随机保留的旧版本对照，或具有可信反事实的准实验；当前版本与周次完全重合)。[q4] [inferred]

## What it means for 回滚决策

尚未提供触发回滚的最小降幅，无法直接对照决策阈值；调整后区间对应下降 1.667–1.966 pp，但不是因果效应区间。[check:mix_shift#1] [measured] [inferred]

这支持立即调查桌面端退化并开展随机版本对照，不能仅凭前后差值认定回滚会恢复同等幅度的 CTR。[q4, q7] [inferred]

## Why we believe it

- Alternatives considered:
  - 平台及国家构成变化作为主要解释：ruled out，构成项仅 -0.010 pp；组内变化为 -1.817 pp，按平台粗分也得到 -1.817 pp。[check:mix_shift#1, check:mix_shift#2] [measured]
  - 星期覆盖不同：ruled out，两周均完整覆盖周一至周日；其他季节性或同期需求变化：ruled in，仍可能存在，只有前后两周无法排除。[q3] [measured] [inferred]
  - 缺日或重复汇总：ruled out，每天均有平台×国家四个单元，键无重复；单元内部漏报：ruled in，尚无独立加载完成凭据。[q3, q5] [measured] [inferred]
  - 埋点或定义变化：ruled in，仍待排查；发布日志只记录 ranker 上线，无法证明其他变化不存在。[q1, q2] [inferred]
  - v3 造成退化：ruled in，属于可能解释而非已证实原因；桌面端下降 2.999 pp、移动端下降 0.042 pp，但两端均被处理，移动端不能自动作为未处理对照。[q4, q7] [measured] [inferred]
- Checks run:
  - completeness: pass 2026-09-06: 4 rows = 100% of the trailing days (under 3 weeks of same-weekday history) median (4) [check:completeness#7] [measured]
  - completeness: pass 2026-09-13: 4 rows = 100% of the trailing days (under 3 weeks of same-weekday history) median (4) [check:completeness#14] [measured]
  - completeness: could not run 最初三天缺少足够的更早历史；其余日期均通过行数检查，但行数检查不验证搜索事件是否全部入库。[check:completeness#1, check:completeness#2, check:completeness#3] [measured] [inferred]
  - mix_shift: pass overall change -1.83 pp = within-segment -1.82 pp (95% CI -1.97 to -1.67) + mix -0.01 pp (mix share 1%) [check:mix_shift#1] [measured]
  - mix_shift: pass 粗粒度平台复核与平台×国家结果一致。[check:mix_shift#2] [measured]
  - 数据有效性: pass 无空值、非法计数或重复粒度键。[q5] [measured]
  - fanout: skipped 未使用连接。[measured]
  - srm: skipped 无随机分组或实验分配数据。[q1, q4] [measured]

## Caveats, and what would change the answer

- 区间采用独立搜索、二项分布假设；重复用户、日间相关性或一次搜索多次点击会使区间不适用或偏窄，需要事件定义及用户级数据复核。[inferred]
- 调整仅覆盖平台和国家，未覆盖流量来源、查询意图等；如这些构成变化，调整结果可能改变。[inferred]
- 需要标准 CTR 定义、独立看板和入库水位确认口径及完整性；需要随机对照与预设回滚阈值才能回答因果决策。[inferred]

## Provenance

- Metric: CTR = SUM(clicks) / SUM(searches)，分别汇总 2026-08-31 至 2026-09-06、2026-09-07 至 2026-09-13，包含所有平台、国家及版本；源粒度为日期×平台×国家×ranker，from stated here [guess]；DS_OVERLAY_DIR 未设置，无 metrics.json。
- Data: warehouse.db 的 search_daily、release_log；可见数据截至 2026-09-13，日期及汇总单元齐全，实际加载完成状态未独立证实。[measured]
- Reconciled: not done (未提供独立看板或可信对账源)。[measured]
- Queries and checks: .ds-queries.log、.ds-checks.log；复核脚本 run_analysis.py。[measured]
- Verified: verify_readout: pass (30 numbers on 9 lines; 6 queries, 7 checks, 0 given)
