## Answer
Headline: +54.98% (95% interval: 54.58%–55.38%) [measured；区间 inferred]
2026-W40 按当前标签识别的导航类查询，已有数据中的点击率为 54.98%，但尚未确认整周数据加载完整。[measured/inferred]
- Observed: +54.98% (95% interval: 54.58%–55.38%) [measured；区间 inferred]
- Adjusted: not computed（本次计算单周点击率，未进行调整）[measured]
- Causal effect: not identified（识别因果效应需要明确干预、对照及随机实验或可信的准实验设计）[inferred]

## What it means for 营销规划
可将该值作为暂定描述性基准；尚未提供会改变规划决策的最小变化阈值，因此无法判断区间是否足够精确。[inferred] 正式引用前应确认数据完整性。[inferred]

## Why we believe it
- Alternatives considered:
  - 直接关联全部标签：ruled out；历史标签导致重复计数，应筛选 `is_current=1`。[measured]
  - 使用当前标签：ruled in；关联无扩增或丢失，导航类搜索共 59,800 次、点击 32,878 次。[measured]
- Checks run:
  - completeness#1: could not run；缺少历史周期基线，无法验证整周加载完整性。[measured]
  - fanout#1: fail；未过滤历史标签时，关联从 1,000 行扩增至 1,300 行；该方案已弃用。[measured]
  - fanout#2: pass；过滤当前标签后，关联保持 1,000 行且全部匹配。[measured]
  - 计数合法性: pass；未发现空值、负数或点击数超过搜索数。[measured]
  - mix_shift / srm: skipped；未比较周期变化，也未分析实验。[inferred]

## Caveats, and what would change the answer
- 区间采用 Wilson 方法，假设搜索是独立二项试验；重复用户、多次点击及数据缺失的影响不包含在内。[inferred]
- 当前标签未必代表该周当时的标签；历史口径或补录数据可能改变结果。[inferred]
- 正号表示点击率水平，不表示增长。[inferred]

## Provenance
- Metric: 当前标签为 `navigational` 的查询，`SUM(clicks) / SUM(searches) × 100%`；stated here [guess]，未发现 `metrics.json`。
- Data: `warehouse.db` 中的 `query_stats`、`query_labels`；可见周期截至 2026-W40，最后完整周期无法确认。[measured]
- Reconciled: not done（未提供独立仪表盘或来源）。[measured]
- Queries and checks: [查询日志](analysis_output/queries.json)、[检查日志](.ds-checks.log)、[计算脚本](analysis_output/analyze.py)、[结果](analysis_output/results.json)。[measured]
