## Answer
Headline: can't tell
正式口径尚未确认；若仅计 external 流量，以有点击的搜索次数除以全部搜索次数，该周 CTR 为 46.05%，这是水平值而非增幅。[measured；口径 guess]
- Observed: +46.05% (95% interval: 45.93%–46.17%)，采用上述暂定口径。[measured]
- Adjusted: not computed（本次询问单周水平，未指定比较期或需固定的构成）。[inferred]
- Causal effect: not identified（需要明确干预及随机实验或可信的准实验设计）。[inferred]

## What it means for 周度业务回顾
目前不宜将暂定结果作为正式周报指标；尚未提供会改变业务决策的最小变化阈值，无法判断区间是否足够窄。[inferred] 指标口径和加载完整性的不确定性不包含在上述区间内。[inferred]

## Why we believe it
- Alternatives considered:
  - external 流量仅以有结果搜索为分母：ruled in，所得 CTR 为 50.05%，缺少定义文件，无法排除此口径。[measured]
  - 全部流量纳入 internal/bot：ruled in，所得 CTR 为 41.41%，缺少正式筛选规则，无法排除。[measured]
- Checks run:
  - completeness: could not run，10-05 至 10-07 缺少足够历史基线。[measured]
  - completeness: pass，10-08 至 10-11 聚合行数与此前基线一致；不能据此证明底层事件完整。[measured；解释 inferred]
  - 唯一键及计数约束: pass，未发现重复日期/平台/流量键或无效计数。[measured]
  - fanout / mix_shift / srm: skipped，无关联查询、跨期变化或实验分析。[inferred]

## Caveats, and what would change the answer
- 区间采用 Wilson 方法，假设搜索事件独立；重复用户造成的相关性可能使区间偏窄。[inferred]
- 确认分子、分母、流量过滤规则及加载完成状态后，才能确定正式答案。[inferred]

## Provenance
- Metric: 周内 `SUM(searches_with_click) / SUM(searches) × 100`，筛选 `traffic_type='external'`，日期含首尾；stated here [guess]，未发现 metrics.json。
- Data: `warehouse.db` 的 `search_daily_v`，数据覆盖至 2026-10-11；最后完整期间未能确认。[measured；完整性 inferred]
- Reconciled: not done（未提供仪表盘或独立来源）。[inferred]
- Queries and checks: [查询及结果](analysis_output/queries.jsonl)、[计算脚本](analysis_output/analyze.py)、[区间结果](analysis_output/results.json)、[检查日志](.ds-checks.log)。
