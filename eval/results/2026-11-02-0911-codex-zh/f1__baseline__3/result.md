## Answer
Headline: can't tell
总体 CTR 从 30.421% 降至 28.324%，下降 2.097 个百分点，但无法确定其中多少由 v2 导致。[measured／inferred]
- Observed: −2.097 个百分点（95% 区间：−2.248 至 −1.946）[measured]
- Adjusted: −0.008 个百分点（95% 区间：−0.163 至 +0.148），holding 上线前的平台 × 国家搜索占比 fixed。[measured]
- Causal effect: not identified（需要同期随机分配的 v1/v2 对照实验；现有数据中版本与周次完全重合）。[inferred]

## What it means for 回滚决策
尚未提供触发回滚的最小降幅；调整后的区间仍包含下降 0.163 个百分点，但它不是因果效应区间。[measured／inferred] 现有数据不足以凭此次周环比下降认定应回滚，也不能证明 v2 无害。[inferred]

## Why we believe it
- Alternatives considered:
  - 流量构成变化：ruled in；CTR 较低的移动端占比从 40.11% 升至 55.07%，描述性分解中的构成项为 −2.089 个百分点，接近全部总体降幅。[measured]
  - 同期其他变化：未 ruled out；没有同期对照，也没有足够长的上线前趋势数据。[inferred]
- Checks run:
  - 日期与分组覆盖：pass；14 天、每天四个平台 × 国家组合，共 56 行。[measured]
  - 重复与计数有效性：pass；无重复键、空值或超出合法范围的计数。[measured]
  - 上线记录一致性：pass；前周仅 v1、后周仅 v2，与发布日志一致。[measured]
  - 同星期几配对敏感性：pass；调整变化 −0.007 个百分点，95% 区间 −0.062 至 +0.048。[measured]
  - 因果识别：fail；缺乏同期对照，无法分离版本效应与时间效应。[inferred]

## Caveats, and what would change the answer
- 主区间假设每次搜索为独立二项观测；无法核验重复用户相关性或一次搜索多次点击，区间不包含混杂偏差。[guess／inferred]
- 流量构成也可能受 v2 影响，因此构成调整不能识别总因果效应。[inferred]
- 随机对照数据、正式 CTR 定义及回滚阈值会改变可作出的结论。[inferred]

## Provenance
- Metric: 总 clicks ÷ 总 searches；stated here [guess]，未提供 metrics.json。
- Data: `search_daily`、`release_log`；日期覆盖至 2026-10-04，入库完整性未经独立核验。[measured]
- Reconciled: not done（未提供仪表盘、源数据或完整性水位）。[measured]
- Queries and checks: [SQL 查询](/private/tmp/ds-runs/4d6635dbe1/analysis/analysis_output/queries.sql)、[计算脚本](/private/tmp/ds-runs/4d6635dbe1/analysis/analysis_output/analyze.py)、[结果](/private/tmp/ds-runs/4d6635dbe1/analysis/analysis_output/results.json)、[假设与检查记录](/private/tmp/ds-runs/4d6635dbe1/analysis/analysis_output/notes.md)。[measured]
