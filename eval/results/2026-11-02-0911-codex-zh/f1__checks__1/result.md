## Answer
Headline: can't tell [inferred]

上线后整体 CTR 下降了 2.097 个百分点，但按平台和国家分层后，变化接近零；现有数据无法确定其中多少由 v2 导致。[measured/inferred]

- Observed: −2.097 个百分点（95% 区间：−2.248 至 −1.946）。[measured]
- Adjusted: −0.002 个百分点（95% 区间：−0.153 至 +0.148），holding 平台×国家的流量占比固定为两周占比的平均值。[measured]
- Causal effect: not identified（版本与时间完全重合；需要同期随机 v1 对照组，或具备可信识别假设的对照设计）。[inferred]

## What it means for 回滚决策

尚未提供触发回滚的最小损失阈值；调整后区间仍包含最多约 0.153 个百分点的下降，也包含改善，且它不是因果效应区间。[measured/inferred] 因此，不宜仅凭整体下降就认定应回滚，也不能据此认定 v2 无害；应按业务阈值设计随机对照验证。[inferred]

## Why we believe it

- Alternatives considered:
  - 流量结构变化：ruled in；移动端搜索占比从 40.11% 升至 55.07%，其 CTR 较低，结构分解项为 −2.095 个百分点，几乎解释全部观察下降。[measured]
  - 平台×国家组内 CTR 普遍大幅下降：ruled out；固定分组权重后的变化接近零，区间为 −0.153 至 +0.148 个百分点。[measured]
  - 同期需求、用户构成或埋点变化：ruled in（仍无法排除）；数据库没有可用于检验这些解释的对照或明细。[inferred]
  - v2 自身改变搜索频次及流量结构：ruled in（仍无法排除）；结构分解不能证明结构变化独立于上线。[inferred]
- Checks run:
  - mix_shift#1: flag，下降主要来自平台×国家的流量结构变化。[measured]
  - completeness#4–#14: pass，09-24 至 10-04 每日分组行数稳定；检查因历史不足而使用滚动日期基准。[measured]
  - completeness#1–#3: could not run，09-21 至 09-23 缺少足够历史基准。[measured]
  - 日期与分组覆盖、重复键、计数有效性：pass，日期和分组齐全，未发现重复键、空值或非法计数。[measured]
  - fanout: skipped，计算未使用连接。[measured]
  - srm: skipped，没有随机实验分流及预期分配比例。[measured]

## Caveats, and what would change the answer

- 区间使用独立搜索的二项分布近似，并固定观察到的分组权重；重复用户、日期相关性及单次搜索多次点击可能使区间不可靠。[guess/inferred]
- 分组行数齐全不证明底层事件全部入库；缺少加载完成标记。[inferred]
- 随机对照、用户级数据、明确的 CTR 口径和回滚阈值，会使归因及决策更可信。[inferred]

## Provenance

- Metric: `SUM(clicks) / SUM(searches)`，按周汇总后相减；from stated here [guess]，未提供 `metrics.json`。
- Data: `warehouse.db` 中的 `search_daily`、`release_log`；比较 2026-09-21—09-27 与 2026-09-28—10-04，数据覆盖至 10-04，最后完整加载日期无法确认。[measured/inferred]
- Reconciled: not done（未提供仪表盘或独立源数据）。[measured]
- Queries and checks: [查询及结果](analysis_output/queries.json)、[分析脚本](analysis_output/analyze.py)、[计算结果](analysis_output/results.json)、[检查日志](.ds-checks.log)。[measured]
