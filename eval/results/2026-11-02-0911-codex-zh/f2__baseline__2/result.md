## Answer
Headline: +54.98% (95% interval: 54.58%–55.38%) [measured；区间为 inferred]
2026-W40 按当前标签归类的导航查询共有 59,800 次搜索、32,878 次点击，点击率为 54.98%，这是水平值而非增幅。[measured]
- Observed: +54.98% (95% interval: 54.58%–55.38%) [measured；区间为 inferred]
- Adjusted: not computed（本次统计单周点击率，未指定调整因素）[inferred]
- Causal effect: not identified（需要明确干预及随机实验或可信的准实验设计）[inferred]

## What it means for 营销规划
规划文档可使用 54.98% 作为当前标签口径的点击率。[measured] 条件性区间约为点估计上下 0.40 个百分点；未提供足以改变规划的最小变化阈值，因此无法判断该精度是否满足决策需求。[inferred]

## Why we believe it
- Alternatives considered:
  - 混用历史标签：ruled out；不筛选当前标签会得到 44.99%，混入 200 条过期导航标签。[measured]
  - 对各查询点击率取简单平均：ruled out；结果为 55.01%，不符合本次总点击数除以总搜索数的口径。[measured]
- Checks run:
  - 统计记录唯一性：pass，无重复查询／周记录。[measured]
  - 当前标签覆盖及唯一性：pass，每个查询恰有一个当前标签，且均为最新版本。[measured]
  - 计数有效性：pass，无空值、非正搜索数、负点击数或点击数超过搜索数。[measured]
  - 周完整性：could not run，缺少结算标记及日级记录。[measured]

## Caveats, and what would change the answer
- 区间使用 Wilson 方法，假设搜索独立且点击为二元结果；汇总数据无法验证这些假设。[inferred]
- 当前标签不一定等于 W40 当时的标签；提供标签生效日期可能改变分类结果。[inferred]
- 若数据覆盖完整，本周比例本身是精确汇总值；上述区间描述模型下的不确定性，不涵盖漏数或错标。[inferred]

## Provenance
- Metric: `SUM(clicks) / SUM(searches) × 100%`，筛选 `week='2026-W40'`、`intent='navigational'`、`is_current=1`；from stated here [guess]（未提供 metrics.json）。
- Data: `warehouse.db` 的 `query_stats`、`query_labels`；最新可见周期为 2026-W40，最后完整周期无法确认。[measured]
- Reconciled: not done（未提供仪表盘或独立核对来源）。[measured]
- Queries and checks: [查询与检查日志](/private/tmp/ds-runs/3ea8a89057/analysis/queries_and_checks.json)、[计算脚本](/private/tmp/ds-runs/3ea8a89057/analysis/analysis.py)。[measured]
