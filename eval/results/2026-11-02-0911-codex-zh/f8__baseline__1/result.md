## Answer
Headline: +36.97%（95% 区间：36.68%–37.26%；条件性 Wilson 区间）[measured]
2026-W41 购物垂类共有 107,810 次搜索和 39,857 次点击，点击率为 36.97%。[measured]
- Observed: +36.97%（95% 区间：36.68%–37.26%）[measured]
- Adjusted: not computed（问题是单周点击率，无需调整比较组）[inferred]
- Causal effect: not identified（没有干预或对照；识别因果效应需要随机实验或可信的准实验）[inferred]

## What it means for 商品运营引用
建议引用“2026-W41 购物垂类点击率为 36.97%”，这是水平值，并非增长幅度。[inferred] 区间约为点估计上下 0.29 个百分点；尚未提供会改变决策的最小变化，无法判断这一精度是否足够。[inferred]

## Why we believe it
- Alternatives considered:
  - 直接连接三张表：ruled out，250 个购物查询的分类记录重复，会将点击率抬高至 40.90%，高估 3.93 个百分点。[measured]
  - 对查询点击率取简单平均：ruled out，结果为 36.94%，该口径给予每个查询相同权重，而非每次搜索。[measured]
- Checks run:
  - 查询与周唯一性：pass，无重复事实记录。[measured]
  - 分类映射：pass，无分类冲突、重复类别映射或未映射查询。[measured]
  - 分类重复：flag，已用 EXISTS 筛选，900 个购物查询各计一次。[measured]
  - 计数有效性：pass，无空值、负数、非整数、零搜索或点击数超过搜索数。[measured]
  - 完整周验证：could not run，仅有周标签，缺少每日覆盖和加载完成标记。[measured]

## Caveats, and what would change the answer
- 区间假设每次搜索独立且点击数代表发生点击的搜索次数；汇总表无法验证这两个假设。[guess]
- 若数据覆盖全周，36.97% 是该库的精确描述值；区间仅表示上述模型下的不确定性，不涵盖漏数或口径错误。[inferred]
- 补充指标定义、完整性证明或搜索级数据，可能改变口径或区间。[inferred]

## Provenance
- Metric: SUM(clicks) / SUM(searches) × 100%；购物归属通过 query_category 和 category_vertical 判断，每个查询只计一次；未发现 metrics.json，stated here [guess]
- Data: warehouse.db 的 query_week、query_category、category_vertical；数据仅含 2026-W41，最后完整周期未能验证。[measured]
- Reconciled: not done（未提供仪表盘或独立来源）。[measured]
- Queries and checks: [分析脚本](/private/tmp/ds-runs/78418b95af/analysis/analysis_ctr.py)；[SQL、检查结果及区间](/private/tmp/ds-runs/78418b95af/analysis/ctr_results.json)。[measured]
