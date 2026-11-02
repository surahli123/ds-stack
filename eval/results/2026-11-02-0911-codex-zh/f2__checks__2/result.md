## Answer
Headline: +54.98% (95% interval: 54.58%–55.38%) [measured]
按当前意图标签，2026-W40 已入库导航型查询的点击率为 54.98%，即 59,800 次搜索产生 32,878 次点击。[measured]
- Observed: +54.98% (95% interval: 54.58%–55.38%) [measured]
- Adjusted: not computed（仅描述该周点击率，无需调整）[inferred]
- Causal effect: not identified（未定义干预或对照；需随机实验或可信的准实验设计）[inferred]

## What it means for 营销规划
可暂以约 55% 作为已入库数据的规划基准。[inferred] 未提供足以改变决策的最小变化阈值，因此无法判断上述区间是否足够精确；区间也不涵盖数据漏载风险。[inferred]

## Why we believe it
- Alternatives considered:
  - 直接关联全部历史标签：ruled out，关联行数从 1,000 增至 1,300，导致重复计数。[measured]
  - 仅使用当前标签：ruled in，`is_current=1` 后标签键唯一，全部搜索记录均匹配且无行数膨胀。[measured]
- Checks run:
  - completeness#1: could not run，缺少历史周期，无法验证周数据完整性。[measured]
  - fanout#1: fail，未筛选标签版本的关联新增 300 行；最终计算已修正。[measured]
  - fanout#2: pass，当前标签关联前后均为 1,000 行。[measured]
  - 数据有效性: pass，无重复查询记录、空值、负值或点击数大于搜索数的记录。[measured]
  - mix_shift / srm: skipped，未比较跨期变化或实验效果。[inferred]

## Caveats, and what would change the answer
- 使用当前标签；若需要该周当时的分类，须提供标签生效时间。[inferred]
- 区间采用 Wilson 方法，假设搜索独立且点击计数代表是否点击；聚合数据无法验证这些假设。[inferred]
- 若存在漏载、标签修订或不同点击口径，结果需重算。[inferred]

## Provenance
- Metric: `SUM(clicks) / SUM(searches) × 100%`，筛选目标周及当前导航标签；未找到 metrics.json，口径 stated here [guess]。
- Data: `query_stats`、`query_labels`；数据含 2026-W40，最后完整周期无法确认。[measured]
- Reconciled: not done（未提供仪表盘或独立核对源）。[measured]
- Queries and checks: [查询记录](analysis_output/queries.json)、[计算脚本](analysis_output/compute.py)、[结果与检查](analysis_output/result.json)、[检查日志](.ds-checks.log)。
