## Answer
Headline: +54.98% (95% 区间：54.58%–55.38%) [measured；区间假设：guess]
按当前意图标签，2026-W40 导航类查询的点击率为 54.98%，即 59,800 次搜索产生 32,878 次点击。[measured]
- Observed: +54.98% (95% 区间：54.58%–55.38%) [measured；区间假设：guess]
- Adjusted: not computed（本次仅计算单周点击率，无调整目标）[inferred]
- Causal effect: not identified（没有干预或对照；需随机实验或可信的准实验设计）[inferred]

## What it means for 营销规划
规划文档可引用该观测值，并注明按当前标签统计、整周加载完整性尚未确认。[inferred] 未提供会改变决策的最小变化阈值，因此无法判断该区间是否足够精确。[inferred]

## Why we believe it
- Alternatives considered:
  - 使用全部历史标签：ruled out，标签连接会重复计数。[measured]
  - 对各查询点击率取简单平均：ruled out，本次指标按搜索量加权。[inferred]
- Checks run:
  - completeness: could not run，缺少此前周期，无法验证完整性。[measured]
  - fanout（全部标签）: fail，连接将 1,000 行扩为 1,300 行；已弃用。[measured]
  - fanout（当前标签）: pass，连接前后均为 1,000 行，全部匹配。[measured]
  - 数据有效性及查询—周唯一性: pass，无空值、负值、点击超过搜索量或重复查询—周记录。[measured]
  - mix_shift / srm: skipped，无跨期变化或实验比较。[inferred]

## Caveats, and what would change the answer
- Wilson 区间假设每次搜索独立且最多计一次点击；汇总数据无法验证这些假设。[guess]
- 当前标签不一定等于该周当时的标签；历史标签生效时间、补录数据或不同点击定义可能改变答案。[inferred]

## Provenance
- Metric: `100 × SUM(clicks) / SUM(searches)`，筛选 `week='2026-W40'`、`intent='navigational'`、`is_current=1`；from stated here [guess]，未提供 metrics.json。
- Data: `query_stats`、`query_labels`；可见周期截至 2026-W40，最后完整周期未确认。[measured]
- Reconciled: not done（未提供独立仪表盘或对账来源）。[measured]
- Queries and checks: [查询日志](analysis_output/queries.json)、[计算脚本](analysis_output/calculate.py)、[结果及检查](analysis_output/results.json)、[检查日志](.ds-checks.log)。
