## Answer
Headline: can't tell [inferred]  
两周总体 CTR 从 30.421% 降至 28.324%，下降几乎全部对应平台与国家流量构成变化，但无法确定其中多少由 v2 导致。[measured；归因限制 inferred]

- Observed: −2.097 个百分点（95% 区间：−2.248 至 −1.946）[measured]
- Adjusted: −0.002 个百分点（95% 区间：−0.153 至 +0.148），holding 平台×国家构成固定，权重取两周搜索占比的平均值。[measured]
- Causal effect: not identified（需要同期随机分配的 v1/v2 对照实验，或有可信反事实的准实验）。[inferred]

## What it means for 回滚决策
尚未提供触发回滚的最小降幅；调整后区间仍包含约 0.15 个百分点的下降，但它不是因果区间，不能据此排除 v2 的损害。[measured；inferred] 现有证据不足以支持“v2 导致此次总体下降，因此回滚”的判断，也不足以证明 v2 无害。[inferred]

## Why we believe it
- Alternatives considered:
  - 流量构成变化：ruled in；分解得到构成项 −2.095 个百分点，组内变化项 −0.002 个百分点。[measured]
  - v2 或同期其他变化：无法 ruled in/out；前周全部为 v1，后周全部为 v2，版本与时间完全重合。[measured；inferred]
- Checks run:
  - completeness：pass；09-24 至 10-04 每日聚合行数稳定。[measured]
  - completeness：could not run；09-21 至 09-23 缺少足够历史基线。[measured]
  - mix_shift：flag；总体变化由构成项主导。[measured]
  - 覆盖、计数与重复键检查：pass；日期及平台×国家分组齐全，无非法计数或重复键。[measured]
  - fanout：skipped；未使用 JOIN。[measured]
  - srm：skipped；没有随机实验分配及预设比例。[measured]

## Caveats, and what would change the answer
- 区间采用独立搜索、二元点击的二项近似；无法验证重复用户、日间相关性及多次点击，区间可能偏窄。[inferred]
- 流量构成也可能受 v2 影响；固定构成不能识别 v2 的总因果效应。[inferred]
- 随机对照结果、明确回滚阈值和埋点口径验证会改变决策依据。[inferred]

## Provenance
- Metric: `SUM(clicks) / SUM(searches)`，from stated here [guess]；未提供 `metrics.json`。
- Data: `search_daily`、`release_log`，覆盖至 2026-10-04；聚合行覆盖完整，事件加载完整性未获确认。[measured；inferred]
- Reconciled: not done（未提供 dashboard、独立源或加载水位）。[measured]
- Queries and checks: [查询与结果](analysis_output/queries.json)、[检查日志](.ds-checks.log)、[补充检查](analysis_output/additional_checks.json)、[方法与区间假设](analysis_output/methods.md)。[measured]
