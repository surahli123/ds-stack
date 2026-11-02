## Answer
Headline: +36.97% (95% CI: 36.68%–37.26%) [q9] [measured]

2026-W41 购物垂类在库内记录的 107,810 次搜索中获得 39,857 次点击，点击率为 36.97%，这是水平值而非增幅。[q9] [measured]

- Observed: +36.97% (95% CI: 36.68%–37.26%) [q9] [measured]
- Adjusted: not computed (问题是单周总体点击率，无需固定流量构成) [inferred]
- Causal effect: not identified (未提供干预或对照；识别因果效应需要随机实验或可信的准实验设计) [inferred]

## What it means for Merchandising 引用

可引用“库内购物垂类点击率为 36.97%”；区间为 36.68%–37.26%，但不涵盖漏数或口径错误。[q9] [inferred]
未提供足以改变决策的最小差异阈值，无法判断该区间是否足够精确；正式作为完整周指标引用前，应确认加载完成及点击定义。[inferred]

## Why we believe it

- Alternatives considered:
  - 重复分类加载导致重复计数：ruled in，分类表有 250 个重复查询标识、无分类冲突；已去重，两层映射均保持行数。[q5] [check:fanout#1] [check:fanout#2] [measured]
  - 映射缺失或多垂类归属：ruled out，去重后所有查询均匹配唯一类别及垂类。[q4, q5, q7, q8] [measured]
  - 流量构成、季节及星期效应：ruled in 为跨期解释的潜在因素；本次仅报告单周水平，无跨期变化可归因。[q2] [inferred]
  - 数据未齐或埋点、口径变化：ruled in 为未排除的限制；仅有目标周，无加载完成标记或埋点变更记录。[q1, q2] [inferred]
- Checks run:
  - completeness: could not run: need at least 3 earlier periods (trailing days (under 3 weeks of same-weekday history)) before 2026-W41, got 0 [check:completeness#1] [measured]
  - fanout: pass — row counts consistent with a many_to_one left join（查询至去重分类）[check:fanout#1] [measured]
  - fanout: pass — row counts consistent with a many_to_one left join（分类至垂类）[check:fanout#2] [measured]
  - 数值及粒度: pass，查询周粒度唯一，计数无空值、负值或点击超过搜索的记录。[q2] [measured]
  - mix_shift: skipped，未比较两个时期。[inferred]
  - srm: skipped，未分析随机实验。[inferred]

## Caveats, and what would change the answer

- 区间采用 Wilson 方法，假设每次搜索是独立的点击/未点击试验；重复用户、查询内相关性或多次点击会使该区间不适用，需要事件或用户数据验证。[guess]
- 若这些记录是完整总体，36.97% 是该总体的精确描述；区间仅表示上述模型下的不确定性。[q9] [inferred]
- 无加载完整性证据；补数、经确认的指标定义或历史分类变更可能改变结果，应向数据负责人核实。[inferred]

## Provenance

- Metric: SUM(clicks) / SUM(searches) × 100；过滤 week='2026-W41'，通过 query_category 与 category_vertical 确认属于 shopping；每个 query_id 的周记录仅计一次，不平均各查询点击率。from stated here [guess]（DS_OVERLAY_DIR 未设置，无可用 metrics.json）。
- Data: query_week、query_category、category_vertical；库内最新周期为 2026-W41，最后完整周期无法确认。[q1, q2] [measured]
- Reconciled: not done (未提供独立看板或权威来源；去重连接与 EXISTS 两种计算一致) [q7, q9] [measured]
- Queries and checks: .ds-queries.log、.ds-checks.log；报告保存在 readout.md。[measured]
- Verified: verify_readout: pass (16 numbers on 6 lines; 7 queries, 3 checks, 0 given)
