## Answer
Headline: can't tell [inferred]

整体 CTR 从 30.4212% 降至 28.3243%，下降中的 −2.0945 pp 对应流量结构变化、−0.0023 pp 对应组内变化，但可归因于 v2 的幅度无法识别。[check:mix_shift#2] [measured] [inferred]

- Observed: −2.0968 pp (95% CI: −2.248 至 −1.946) [check:mix_shift#2] [measured]
- Adjusted: −0.0023 pp (95% CI: −0.153 至 +0.148), holding 平台×国家的权重固定为两周占比的均值；这是描述性分解。[check:mix_shift#2] [measured]
- Causal effect: not identified（版本与周次完全重合；需要同期随机分配的 v1/v2 对照实验，或有可信反事实的准实验）。[q5] [inferred]

## What it means for 是否回滚

尚未提供最小回滚阈值；调整后区间仍容许约 0.15 pp 的下降，若这个幅度足以触发回滚，当前结果不能排除它。[check:mix_shift#2] [inferred]
不建议仅凭原始下降认定 v2 有害并回滚；描述性区间也不能证明 v2 无害，应以随机对照和预设门槛作决定。[q5] [inferred]

## Why we believe it

- Alternatives considered:
  - 流量结构变化：ruled in，低 CTR 的移动端搜索占比从 40.1085% 升至 55.0721%；分解中的结构项几乎覆盖全部下降，但其来源未知。[check:mix_shift#3] [measured]
  - 星期构成不同：ruled out，两周都完整覆盖周一至周日；季节性或同期需求变化仍 ruled in 为未排除的解释，缺少更长历史及同期对照。[q4] [inferred]
  - 缺天、缺分组或重复：ruled out，每天都有相同分组覆盖且键无重复；组内事件漏报仍未排除。[q4, q5, q6] [measured] [inferred]
  - 埋点或口径变化：ruled in 为未排除的解释；发布表只记载 ranker 上线，不能替代埋点审计。[q3] [inferred]
  - v2 的影响：ruled in 为未排除的解释；没有同期旧版本对照，且 v2 可能改变重复搜索和流量构成，不能将结构项自动认定为外因。[q5] [inferred]
- Checks run:
  - completeness: pass 2026-09-27: 4 rows = 100% of the trailing days (under 3 weeks of same-weekday history) median (4) [check:completeness#3] [measured]
  - completeness: pass 2026-10-04: 4 rows = 100% of the trailing days (under 3 weeks of same-weekday history) median (4) [check:completeness#4] [measured]
  - mix_shift: flag mix-dominant: overall change -2.10 pp = within-segment -0.00 pp (95% CI -0.15 to +0.15) + mix -2.09 pp (mix share 100%); report the mix shift as part of the answer [check:mix_shift#2] [measured]
  - mix_shift: flag mix-dominant: overall change -2.10 pp = within-segment -0.00 pp (95% CI -0.15 to +0.15) + mix -2.09 pp (mix share 100%); report the mix shift as part of the answer [check:mix_shift#3] [measured]
  - 分层敏感性: pass 平台×国家与仅平台的结论一致；仅平台调整值为 −0.0036 pp（95% CI: −0.154 至 +0.147）。[check:mix_shift#2, check:mix_shift#3] [measured]
  - 数据有效性: pass 无空计数、负计数或 clicks 大于 searches，无重复日期×平台×国家×版本键。[q2, q6] [measured]
  - fanout: skipped 未进行连接。[inferred]
  - srm: skipped 无随机分配记录，不能检验实验分流。[q1, q5] [inferred]

## Caveats, and what would change the answer

- 区间采用独立搜索的二项近似，假定 clicks 表示发生点击的搜索数；重复用户、日间相关性及多次点击可能使区间失真，需要事件口径和用户级数据验证。[inferred]
- 完整性检查仅验证汇总覆盖和行数，无法证明事件全部入库；需要加载水位、埋点审计和可信仪表盘对账。[inferred]
- 固定流量构成可能去掉 v2 的真实间接影响；同期随机实验应同时追踪 CTR、搜索量和流量构成，并预设回滚阈值。[inferred]

## Provenance

- Metric: SUM(clicks)/SUM(searches)，来自 search_daily，日×平台×国家×ranker 粒度；分别筛选 2026-09-21—2026-09-27 与 2026-09-28—2026-10-04，无其他筛选；from stated here [guess]（没有可用的 metrics.json）。
- Data: search_daily、release_log，through 2026-10-04；日期和分组覆盖完整，事件入库完整性未独立确认。[q2, q4, q5] [measured] [inferred]
- Reconciled: not done（未提供仪表盘或独立可信来源）。[inferred]
- Queries and checks: .ds-queries.log、.ds-checks.log；复算脚本 analysis_checks.py，报告 readout.md。
- Verified: verify_readout: pass (36 numbers on 10 lines; 6 queries, 4 checks, 0 given)
