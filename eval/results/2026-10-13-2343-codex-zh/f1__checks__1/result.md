## Answer
Headline: can't tell [inferred]  
整体 CTR 从 30.421% 降至 28.324%，下降 2.097 个百分点，但无法确定其中多少由 v2 引起。[measured；归因判断 inferred]

- Observed: −2.097 个百分点（95% 区间：−2.248 至 −1.946）[measured]
- Adjusted: −0.002 个百分点（95% 区间：−0.153 至 +0.148），holding 平台 × 国家占比固定为两周占比的平均值。[measured]
- Causal effect: not identified；需要同期随机分配的 v1/v2 对照，才能区分版本效果与时间变化。[inferred]

## What it means for 回滚决策
尚未提供触发回滚的最小下降阈值；调整后区间仍容许约 0.15 个百分点的下降，但它不是因果区间，不能用于确认 v2 安全。[inferred] 目前证据不足以仅凭这次周环比下降决定回滚，建议通过随机对照验证。[inferred]

## Why we believe it
- Alternatives considered:
  - 流量结构变化：ruled in；移动端搜索占比从 40.108% 升至 55.072%，平台 × 国家构成变化的描述性贡献为 −2.0945 个百分点。[measured]
  - 各细分人群 CTR 普遍恶化：ruled out 作为整体下降的主要描述性解释；固定占比后变化接近零。[inferred]
  - 同期需求变化或 v2 引发的流量结构变化：无法 ruled in/out；版本与周次完全重合，没有同期对照。[inferred]
- Checks run:
  - completeness：pass；两周末的行数与搜索量检查通过；无加载水位，不能保证源数据完整。[measured；限制 inferred]
  - completeness：could not run；最早几个日期缺少足够历史基线。[measured]
  - mix_shift：flag；下降主要来自流量构成变化。[measured]
  - 数据有效性与键唯一性：pass；未发现非法计数或重复键。[measured]
  - fanout：skipped；未使用关联查询。[measured]
  - srm：skipped；无实验分配记录或预定分流比例。[measured]

## Caveats, and what would change the answer
- 区间假设每次搜索是独立的二元点击事件；汇总数据无法验证该假设或处理用户内相关性，实际不确定性可能更大。[inferred]
- 流量结构也可能受 v2 影响；调整可能移除其部分效果，不能把结构贡献直接认定为非 v2 原因。[inferred]
- 随机对照数据、明确的回滚阈值及点击口径，会改变可支持的决策。[inferred]

## Provenance
- Metric: `SUM(clicks) / SUM(searches)`；from stated here [guess]，未提供 metrics.json。
- Data: `warehouse.db` 的 `search_daily`、`release_log`；截至 2026-10-04，完整性仅通过计数检查，未获加载水位确认。[measured]
- Reconciled: not done（未提供仪表盘或独立来源）。[measured]
- Queries and checks: [查询与数据](analysis_output/queries.json)、[计算结果](analysis_output/results.json)、[检查日志](.ds-checks.log)、[方法与复现](analysis_output/methodology.md)。[measured]
