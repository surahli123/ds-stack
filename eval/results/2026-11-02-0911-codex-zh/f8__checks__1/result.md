## Answer
Headline: +36.97%（95% 区间：36.68%–37.26%）[measured；区间 inferred]
2026-W41 已加载数据中，购物垂类的 107,810 次搜索产生 39,857 次点击，点击率为 36.97%。[measured]
- Observed: +36.97%（95% 区间：36.68%–37.26%）[measured；区间 inferred]
- Adjusted: not computed（仅描述该周点击率，无比较基准或调整目标）[inferred]
- Causal effect: not identified（需要随机实验或可信的准实验设计）[inferred]

## What it means for 商业团队引用
可引用为“已加载数据中的购物垂类点击率”，但尚不能确认整周数据完整。[inferred] 未提供足以改变决策的最小变化阈值，因此无法判断该区间是否满足决策要求。[inferred]

## Why we believe it
- Alternatives considered:
  - 直接连接原始分类表：ruled out，重复映射会增加 250 行，造成重复计数。[measured]
  - 去重分类映射后筛选购物垂类：ruled in，分类无冲突，连接未增减行且全部匹配。[measured]
- Checks run:
  - completeness#1: could not run 缺少历史周期，无法验证加载完整性。
  - fanout#1: fail 原始分类连接存在重复计数。
  - fanout#2、fanout#3: pass 去重后的分类连接及垂类连接均通过。
  - 数据有效性: pass 未发现空值、负计数、点击数超过搜索数或重复查询周记录。[measured]
  - mix_shift、srm: skipped 未分析跨期变化或实验效果。

## Caveats, and what would change the answer
- 区间采用 Wilson 方法，假设每次搜索是独立的二项试验；重复用户及多次点击可能使该假设不成立。[inferred]
- 区间不覆盖漏加载和指标定义错误；确认完整加载或取得正式指标口径后，答案可能改变。[inferred]

## Provenance
- Metric: 点击率＝购物垂类总点击数 ÷ 总搜索数 × 100%；采用搜索量加权，from stated here [guess]，未提供 metrics.json。
- Data: query_week、query_category、category_vertical；数据包含至 2026-W41，最后完整周期无法确认。[measured；完整性 inferred]
- Reconciled: not done（未提供独立仪表盘或对账来源）。
- Queries and checks: [查询日志](analysis_output/queries.json)、[检查结果](analysis_output/checks.txt)、[计算脚本](analysis_output/calculate.py)。
