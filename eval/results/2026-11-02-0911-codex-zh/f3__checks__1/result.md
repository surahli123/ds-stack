## Answer
Headline: can't tell

整体 CTR 从前一周的 30.441% 降至后一周的 28.615%，下降 1.827 个百分点，但无法确定其中多少由 v3 导致。[measured；因果判断 inferred]

- Observed: −1.827 个百分点（95% 区间：−1.978 至 −1.675）。[measured]
- Adjusted: −1.817 个百分点（95% 区间：−1.966 至 −1.667），holding 平台×国家的搜索量占比 fixed，权重取两周占比的平均值。[measured]
- Causal effect: not identified；需要同期随机分配的 v2/v3 对照，或具有可信识别假设的未受影响对照组。[inferred]

## What it means for 回滚决策

尚未提供足以触发回滚的最小损失阈值；若阈值小于 1.667 个百分点，调整后的**周际降幅**区间整体超过该阈值。[inferred] 但这不是 v3 的因果区间，不能据此断言回滚能恢复这些点击；建议用随机保留的 v2 对照验证。[inferred]

## Why we believe it

- Alternatives considered:
  - 平台×国家流量结构变化：ruled out 作为主要解释，分解贡献仅 −0.010 个百分点。[measured]
  - 桌面端特有问题：ruled in 为待查方向；桌面端下降约 2.999 个百分点，移动端下降约 0.042 个百分点。[measured]
  - 同期需求、界面或埋点变化：ruled in 为未排除解释，数据库缺少相应记录。[inferred]
  - 用移动端作未处理对照：ruled out；移动端同样切换到 v3，不能直接识别整体因果效应。[measured；识别判断 inferred]
- Checks run:
  - completeness: pass，9 月 3—13 日每日分组行数稳定；could not run，8 月 31 日—9 月 2 日缺少足够历史基线。[measured]
  - mix_shift: pass，下降主要来自分组内部 CTR 变化。[measured]
  - 数据有效性与重复检查：pass，未发现非法计数、空值或重复分组键。[measured]
  - fanout: skipped，未使用 JOIN。[measured]
  - srm: skipped，没有随机实验分配及预期比例。[measured]

## Caveats, and what would change the answer

- 区间采用独立搜索、二项分布近似；重复用户、时间相关性或每次搜索多次点击可能使其不适用，且区间不包含混杂偏差。[inferred]
- 行数稳定不能证明点击事件完整入库；缺少加载完成标记。[inferred]
- 随机对照、用户级数据、埋点核验及明确回滚阈值会改变判断。[inferred]

## Provenance

- Metric: `SUM(clicks) / SUM(searches)`，按周汇总；未提供 metrics.json，口径 stated here [guess]。
- Data: `search_daily`、`release_log`，数据覆盖至 2026-09-13；最后完整期间未获加载记录确认。[measured]
- Reconciled: not done，未提供仪表盘或独立源数据。[measured]
- Queries and checks: [SQL 与结果](analysis_output/queries.json)、[可复现脚本](analysis_output/analyze.py)、[检查与计算日志](analysis_output/run.log)、[检查原始记录](.ds-checks.log)。[measured]
