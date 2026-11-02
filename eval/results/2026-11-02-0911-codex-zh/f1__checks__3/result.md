## Answer
Headline: can't tell [inferred]

两周总体 CTR 从 30.421% 降至 28.324%，但按平台和国家固定流量构成后差异接近零，无法确定其中多少由 v2 导致。[measured；inferred]
- Observed: −2.097 个百分点（95% 区间：−2.248 至 −1.946）。[measured]
- Adjusted: −0.002 个百分点（95% 区间：−0.153 至 +0.148），holding 平台×国家构成 fixed，权重取两周占比的平均值。[measured]
- Causal effect: not identified（需要同期随机 v1/v2 对照；当前版本与时间完全重合）。[inferred]

## What it means for 回滚决策
尚未提供触发回滚的最小损失阈值；调整后的区间仍包含最多约 0.153 个百分点的下降，但这不是因果效应的界限。[measured；inferred] 不能仅凭此次周环比下降认定应回滚，也不能据此证明 v2 无害。[inferred]

## Why we believe it
- Alternatives considered:
  - 流量构成变化：ruled in；分解得到构成贡献 −2.095 个百分点，几乎解释全部观察下降。[measured]
  - 调整构成后仍存在同样大的下降：ruled out；调整后的差异及区间均接近零。[measured]
  - 同期其他变化或 v2 改变搜索行为：无法 ruled out；缺少同期对照，发布日志不能排除未记录变化。[inferred]
- Checks run:
  - completeness：pass；可检验日期的分组行数及两周期末搜索量未触发缺载警报。[measured]
  - completeness：could not run；9 月 21—23 日缺少足够历史基线；无加载水位，完整性仍未证实。[measured；inferred]
  - mix_shift：flag；构成变化主导总体下降。[measured]
  - 数据有效性与重复键：pass；未发现无效计数或重复分组键。[measured]
  - fanout：skipped；查询没有连接。[measured]
  - srm：skipped；没有随机实验分组或计划分流比例。[measured]

## Caveats, and what would change the answer
- 区间采用搜索独立的二项近似；重复用户、日间相关性可能使区间偏窄，当前聚合数据无法充分校正。[inferred]
- 固定构成可能移除 v2 经搜索行为产生的部分影响，不能视为总因果效应。[inferred]
- 随机对照、明确回滚阈值、指标定义及加载完成记录会改善判断。[inferred]

## Provenance
- Metric: `SUM(clicks) / SUM(searches)`，from stated here [guess]；未找到 metrics.json，点击是否按搜索去重未确认。
- Data: warehouse.db 的 search_daily、release_log；比较指定两周，数据截至 2026-10-04，最后完整期间未经加载记录确认。[measured]
- Reconciled: not done（未提供仪表盘或独立来源）。[measured]
- Queries and checks: [查询与结果](analysis_output/queries.json)、[分析脚本](analysis_output/analyze.py)、[校验结果](analysis_output/check_results.json)、[校验日志](.ds-checks.log)。[measured]
