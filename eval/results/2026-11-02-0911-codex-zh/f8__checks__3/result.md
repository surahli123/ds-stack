## Answer
Headline: +36.97%（95% 区间：36.68%–37.26%）[measured；区间 inferred]
2026-W41 购物垂类的已入库数据中，107,810 次搜索产生 39,857 次点击，点击率为 36.97%。[measured]
- Observed: +36.97%（95% 区间：36.68%–37.26%）[measured；区间 inferred]
- Adjusted: not computed（本题未要求跨期比较或控制变量；分类重复已消除）
- Causal effect: not identified（本题是描述性统计；因果效应需要明确干预和有效对照设计）[inferred]

## What it means for 商品运营引用
可引用“已入库数据的购物垂类点击率为 36.97%”，但整周完整性尚未确认。[measured；完整性 inferred] 未提供会改变决策的最小变化阈值，无法判断该区间是否足以支持具体决策。[inferred]

## Why we believe it
- Alternatives considered:
  - 直接连接原始分类表：ruled out；重复分类会重复加权，得到 40.90%，因此采用存在性筛选，确保每条搜索记录只计一次。[measured]
- Checks run:
  - completeness: could not run；缺少历史周期，且没有加载完成标记。[measured]
  - fanout#1: fail；原始分类连接将 2,000 行扩增为 2,250 行。[measured]
  - fanout#2: pass；分类去重后保持 2,000 行，全部匹配。[measured]
  - fanout#3: pass；类别到垂类映射唯一，全部匹配。[measured]
  - 数据有效性：pass；未发现重复查询周、冲突分类或无效点击／搜索计数。[measured]
  - mix_shift、srm: skipped；没有变化比较或实验分析。[inferred]

## Caveats, and what would change the answer
- 区间采用 Wilson 方法，假设搜索独立且每次搜索是否点击为二元事件；这些假设未获数据定义确认。[guess]
- 区间不涵盖漏载、分类错误或重复用户造成的不确定性；完整性确认或后续补数可能改变结果。[inferred]

## Provenance
- Metric: 购物垂类总点击数 ÷ 总搜索数 × 100%；按搜索量加权，from stated here [guess]；未发现 metrics.json。
- Data: query_week、query_category、category_vertical；覆盖 2026-W41，最后完整周期无法确认。[measured]
- Reconciled: not done（未提供独立报表或源系统对账数据）。
- Queries and checks: [查询及结果](queries.json)、[计算脚本](analysis.py)、[检查日志](.ds-checks.log)、[指标结果](results.json)。
