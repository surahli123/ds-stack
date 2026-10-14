## Answer
Headline: can't tell

总体 CTR 从 30.421% 降至 28.324%，下降主要对应流量构成变化，但无法确定其中多少由 v2 导致。[measured；inferred]
- Observed: −2.097 个百分点（95% 区间：−2.248 至 −1.946）。[measured]
- Adjusted: −0.008 个百分点（95% 区间：−0.163 至 +0.148），holding 上线前的平台×国家搜索占比 fixed。[measured]
- Causal effect: not identified；需要同期随机分配的 v1/v2 对照实验，才能区分版本影响与时间变化。[inferred]

## What it means for 回滚决策
尚未提供会触发回滚的最小损失阈值；调整后区间包含零及最多约 0.163 个百分点的下降。[measured] 即使阈值大于这个数，该区间也不是因果区间，不能据此证明应回滚或 v2 无害。[inferred]

## Why we believe it
- Alternatives considered:
  - 流量构成变化：ruled in；低 CTR 的移动端搜索占比从 40.11% 升至 55.07%，按上线后各层 CTR 分解，构成项为 −2.089 个百分点。[measured]
  - 各层 CTR 普遍大幅下降：ruled out；四层变化介于 −0.080 至 +0.051 个百分点。[measured]
  - 同期其他变化或 v2 自身改变流量构成：ruled in，仍属可能；数据没有同期对照，也未记录查询意图、获客或埋点变化。[inferred]
- Checks run:
  - 日期与分层覆盖：pass；14 天、每天四层，共 56 行，无重复键、空值或非法计数。[measured]
  - 上线与对照：flag；前周全部 v1，后周全部 v2，版本与周完全重合。[measured]
  - 权重敏感性：pass；改用后周权重，调整差异为 +0.003 个百分点。[measured]
  - 同星期配对：pass；按天等权的调整差异为 −0.007 个百分点，95% 区间为 −0.062 至 +0.048。[measured]

## Caveats, and what would change the answer
- 主区间假设每次搜索是独立的二项结果、权重固定；重复用户、多次点击及时间相关性无法验证。[guess]
- 构成分解是描述性计算；若 v2 改变搜索频次，固定构成可能移除部分真实影响。[inferred]
- 随机对照、明确的点击口径及回滚阈值，会使因果判断与决策更可靠。[inferred]

## Provenance
- Metric: SUM(clicks) / SUM(searches)；未提供 metrics.json，stated here [guess]。
- Data: warehouse.db 的 search_daily、release_log；所比较两周为 2026-09-21–09-27 与 2026-09-28–10-04，日期分层齐全至 10-04，但无入库完成标记。[measured]
- Reconciled: not done（未提供 dashboard 或独立来源）。
- Queries and checks: [查询及原始结果](analysis_output/queries_and_results.json)、[计算结果](analysis_output/results.json)、[复现脚本](analysis_output/analyze.py)、[方法与限制](analysis_output/methods.md)。
