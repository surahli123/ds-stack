## Answer
Headline: can't tell [inferred]

总体 CTR 从 30.4212% 降至 28.3243%，下降 2.0968 pp；构成分解中流量占比变化项为 −2.0945 pp，但无法确定其中多少由 v2 导致。[check:mix_shift#2] [measured] [inferred]

- Observed: −2.0968 pp (95% CI: −2.248 至 −1.946) [check:mix_shift#2] [measured]
- Adjusted: −0.0023 pp (95% CI: −0.153 至 +0.148), holding 平台×国家构成固定为两周占比的平均值；这是描述性调整值。[check:mix_shift#2] [measured]
- Causal effect: not identified (需要同期随机分配的旧版对照，或具有可信识别假设的准实验；版本与时间完全重合，调整值不能当作因果效应)。[q2, q4] [inferred]

## What it means for 回滚决策
不应仅凭这次总体下降认定需要回滚；尚未提供最小回滚损失阈值，若其小于 0.153 pp，调整区间仍不能排除达到阈值的下降。[check:mix_shift#2] [inferred]

即使阈值更大，这个区间也只描述固定构成后的变化，不能证明 v2 安全；应通过保留旧版的随机对照检验回滚阈值。[q2, q4] [inferred]

## Why we believe it
- Alternatives considered:
  - 流量构成变化：ruled in，低 CTR 的移动端占比由 40.1085% 升至 55.0721%；平台×国家分解的构成项占下降约 99.89%。[check:mix_shift#2, check:mix_shift#3] [measured]
  - 星期构成不一致：ruled out，两周均完整覆盖周一至周日；更广泛的季节性与同期事件仍无法排除。[q2] [measured] [inferred]
  - 明显缺日或重复汇总：ruled out，可见数据覆盖 14 天、每天 4 个单元，56 个汇总键均唯一；但没有入库完成水位可核实迟到数据。[q2, q5] [measured] [inferred]
  - 埋点或口径变化：ruled in 为尚未排除的解释，发布日志仅记载版本发布，没有独立埋点审计证据。[q1, q3] [inferred]
  - v2 导致下降：ruled in 为未识别的可能性；前周全是旧版、后周全是新版，既无同期对照，也不能排除版本影响流量构成。[q2, q4] [inferred]
- Checks run:
  - completeness: pass — 2026-09-27: 101828 rows = 102% of the trailing days (under 3 weeks of same-weekday history) median (99521.5) [check:completeness#1] [measured]
  - completeness: pass — 2026-10-04: 101900 rows = 102% of the trailing days (under 3 weeks of same-weekday history) median (99762) [check:completeness#2] [measured]
  - mix_shift: flag — mix-dominant: overall change -2.10 pp = within-segment -0.00 pp (95% CI -0.15 to +0.15) + mix -2.09 pp (mix share 100%); report the mix shift as part of the answer [check:mix_shift#2] [measured]
  - mix_shift: flag — 粗化到平台后的调整值为 −0.0036 pp (95% CI: −0.154 至 +0.147)，与细分结论一致。[check:mix_shift#3] [measured]
  - 数据有效性: pass，未见空计数、非正搜索量、负点击量或点击量超过搜索量。[q5] [measured]
  - fanout: skipped，未进行表连接。[measured]
  - srm: skipped，无随机分配记录，不能检查实验分流。[q1, q4] [measured]

## Caveats, and what would change the answer
- 区间按独立搜索、二项点击计算；现有日汇总无法核实每次搜索是否最多计一次点击，也无法处理用户内相关性。需要事件或用户级数据验证口径并计算聚类区间。[inferred]
- 固定构成可能去掉版本经由流量构成产生的影响；还缺少流量来源、查询意图等变量。随机对照及发布前更长历史可能改变归因结论。[inferred]
- completeness 使用搜索量代理加载量，仅检查两周末日相对前期是否异常；每日覆盖检查不等于确认入库完成，需要加载水位与埋点审计。[inferred]

## Provenance
- Metric: SUM(clicks) / SUM(searches)，分别汇总 2026-09-21 至 2026-09-27、2026-09-28 至 2026-10-04，包含全部平台、国家和版本；源粒度为日期×平台×国家×版本。from stated here [guess]：DS_OVERLAY_DIR 未设置，无可用 metrics.json。
- Data: warehouse.db 的 search_daily、release_log；可见覆盖至 2026-10-04，完整性代理检查通过，未获独立加载完成证明。[measured] [inferred]
- Reconciled: not done (没有提供仪表盘或独立可信 CTR 来源)。[measured]
- Queries and checks: .ds-queries.log、.ds-checks.log；复现检查脚本 analysis_artifacts/run_checks.py；报告 readout.md。[measured]
- Verified: verify_readout: pass (34 numbers on 10 lines; 5 queries, 4 checks, 0 given)
