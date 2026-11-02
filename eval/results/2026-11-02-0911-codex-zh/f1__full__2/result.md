## Answer
Headline: can't tell [inferred]

总体 CTR 从 30.4212% 降至 28.3243%，其中 -2.0945 pp 对应流量构成变化，固定构成后的变化为 -0.0023 pp，但无法确定多少由 v2 导致。[check:mix_shift#1] [measured] [inferred]

- Observed: -2.0968 pp (95% CI: -2.248 至 -1.946) [check:mix_shift#1] [measured]
- Adjusted: -0.0023 pp (95% CI: -0.153 至 +0.148), holding 平台×国家的搜索占比固定为两周占比的平均值 [check:mix_shift#1] [measured]
- Causal effect: not identified (需要同期随机分配的旧版对照组；当前版本与时间完全重合，调整值不等于因果效应) [q4] [inferred]

## What it means for 回滚决策

不应仅凭总体下降就认定需要回滚；业务尚未给出触发回滚的最小损失，若该阈值落在调整区间 -0.153 至 +0.148 pp 内，连固定构成后的变化也无法明确判定是否跨过阈值。[check:mix_shift#1] [inferred]

该区间不是因果效应区间，无法据此证明保留或回滚更好；应预先确定损失阈值并开展随机对照比较。[inferred]

## Why we believe it

- Alternatives considered:
  - 流量构成变化: ruled in，低 CTR 的移动端占比从 40.1085% 增至 55.0721%，分解所得构成项为 -2.0945 pp。[check:mix_shift#1, check:mix_shift#2] [measured]
  - 星期覆盖不同: ruled out，两周均覆盖周一至周日；其他季节性或同期事件仍不能排除，现有数据只有这两周。[q3] [inferred]
  - 缺日期或缺分组: ruled out，每日均有完整的平台×国家组合；但汇总行存在不代表底层事件已全部入库。[q3, q4] [measured] [inferred]
  - 埋点或定义变化: ruled in（仍属未排除的可能），发布日志只记录版本上线，没有埋点审计或指标字典可核实。[q1, q2] [inferred]
  - v2 导致下降: ruled in（仍属未识别的可能），没有同期旧版流量；组内变化接近零既不能证明无影响，也不能排除版本通过流量构成影响总体 CTR。[q4, check:mix_shift#1] [inferred]
- Checks run:
  - mix_shift: flag 平台×国家分解与仅按平台分解一致；后者调整值为 -0.0036 pp (95% CI: -0.154 至 +0.147)。[check:mix_shift#1, check:mix_shift#2] [measured]
  - completeness: pass 2026-09-24 至 2026-10-04 每日分组行数与此前中位数一致；仅验证行覆盖，不证明事件入库完整。[q3, check:completeness#4, check:completeness#5, check:completeness#6, check:completeness#7, check:completeness#8, check:completeness#9, check:completeness#10, check:completeness#11, check:completeness#12, check:completeness#13, check:completeness#14] [measured]
  - completeness: could not run 2026-09-21 至 2026-09-23 缺足够早期基线。[check:completeness#1, check:completeness#2, check:completeness#3] [measured]
  - 数据有效性与唯一性: pass 无无效计数、空分组或重复日期×平台×国家×版本键。[q5, q6] [measured]
  - fanout: skipped 未使用连接。[inferred]
  - srm: skipped 无随机分组或预设分流比例。[q1, q4] [inferred]

## Caveats, and what would change the answer

- 调整仅是描述性分解；若版本改变了搜索频率或流量构成，固定构成会移除部分真实影响。随机对照应同时测量总体 CTR 和流量构成。[inferred]
- 区间采用独立搜索、二项点击及固定权重假设；同一用户的搜索相关性或每次搜索多次点击可能使区间失准，需要用户级搜索与点击明细核实。[inferred]
- 缺流量来源、查询意图、更长历史及入库水位；补齐这些信息可能改变调整结果和完整性判断。[inferred]

## Provenance

- Metric: CTR = SUM(clicks) / SUM(searches)，不额外过滤；来源为 search_daily 的日期×平台×国家×版本汇总，分别汇总 2026-09-21—2026-09-27 与 2026-09-28—2026-10-04；假定 clicks 表示发生点击的搜索数。from stated here [guess]；DS_OVERLAY_DIR 未设置，无可用 metrics.json。
- Data: search_daily、release_log；日期覆盖至 2026-10-04，分组覆盖完整，最后完整入库日期未经水位确认。[measured]
- Reconciled: not done (库内无独立仪表盘或可信总量来源) [measured]
- Queries and checks: `.ds-queries.log`、`.ds-checks.log`；复跑检查脚本 `run_checks.py`，报告 `readout.md`。
- Verified: verify_readout: pass (18 numbers on 6 lines; 6 queries, 16 checks, 0 given)
