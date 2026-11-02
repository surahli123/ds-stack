## Answer
Headline: +36.97% (95% 区间：36.68%–37.26%) [measured]
已入库数据中，2026-W41 购物垂类的点击率为 36.97%，但整周加载完整性尚未确认。[measured]
- Observed: +36.97% (95% 区间：36.68%–37.26%) [measured]
- Adjusted: not computed（仅计算当周点击率，无比较或调整目标）[inferred]
- Causal effect: not identified（需明确干预及随机实验或可信的准实验设计）[inferred]

## What it means for 营销引用
可引用为“当前已入库数据的购物垂类点击率”，完整周口径须待加载确认。[inferred] 未提供足以改变决策的最小变化阈值，无法判断该区间是否满足决策精度要求。[inferred]

## Why we believe it
- Alternatives considered:
  - 直接连接原始类别表：ruled out，重复映射导致连接增加 250 行，重复计权；最终按查询与类别去重。[measured]
  - 类别冲突：ruled out，重复记录的类别一致。[measured]
- Checks run:
  - completeness#1: could not run 缺少历史周期，无法检验加载完整性。[measured]
  - fanout#1: fail 原始连接存在重复计入。[measured]
  - fanout#2、fanout#3: pass 去重后的类别连接及垂类连接均无增行或漏配。[measured]
  - 数据有效性：pass 无缺失或非法点击计数，无重复查询周记录。[measured]
  - mix_shift、srm: skipped 未分析变化或实验效应。[inferred]

## Caveats, and what would change the answer
- 区间采用 Wilson 方法，假设每次搜索对应独立的二元点击结果；聚合数据无法验证此假设，区间不包含漏数风险。[inferred]
- 完整加载证明、点击口径确认或补录数据可能改变可引用结论。[inferred]

## Provenance
- Metric: 点击数合计 ÷ 搜索数合计 × 100；按搜索量加权。来自 stated here [guess]，未提供 metrics.json。
- Data: query_week、query_category、category_vertical；可见周期截至 2026-W41，最后完整周期无法确认。[measured]
- Reconciled: not done（未提供独立仪表盘或来源）。
- Queries and checks: [查询日志](analysis_output/queries.json)、[计算脚本](analysis_output/calculate.py)、[计算结果](analysis_output/result.json)、[校验日志](.ds-checks.log)。
