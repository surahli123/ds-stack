## Answer
Headline: 36.97 %(95% 区间 36.68–37.26 %)
2026-W41 购物垂直领域的点击率为 36.97%(39,857 次点击 / 107,810 次搜索,共 900 个查询)。

- Observed: 36.97 %(95% 区间 36.68–37.26 %)
- Adjusted: not computed(这是单周的水平值,不是比较,没有需要控制的因素)
- Causal effect: not identified(这是描述性指标,没有干预,也不涉及因果问题)

## What it means for 商品运营(Merchandising)引用该数字
可以引用 36.97%。要注意的是,直接联表会得到 40.9%,这个数字是错的。要让结论改变,点击率需要偏移约 0.3 个百分点以上,而只要有一次重复联表,偏差就有约 4 个百分点。

## Why we believe it
- Alternatives considered:
  - query_category 有重复行(2250 行对应 2000 个查询,其中 250 个查询在 2026-10-09 被重新加载),直接联表会重复计算:已排除。我按 query_id 去重,计数为 900 个查询,而不是更多。重复前后的分类完全一致,所以用哪次加载都不影响结果 [measured]
  - 指标定义不同(各查询点击率的简单平均):已排除。简单平均为 36.94%,与加权结果几乎相同 [measured]
  - 有查询缺少分类:已排除。W41 的 2000 个查询全部有分类 [measured]
- Checks run:
  - 去重的唯一性:pass。无任何 query_id 的分类在重复加载之间发生变化
  - 最新加载与最早加载对比:pass。两者结果相同(36.9697%)
  - 朴素联表:flag。重复行使搜索量虚增到 137,945,得到 40.90%,不可用
  - 区间:二项分布正态近似,标准误约 0.147 个百分点 [inferred]。忽略了查询之间的聚集效应,实际区间可能略宽

## Caveats, and what would change the answer
- 购物垂直领域 = electronics、apparel、home(取自 category_vertical,表中另有 news 和 weather 属于 info)。
- 表中只有 W41 一周的数据,所以无法与其他周对比或看趋势。
- 点击率口径为 clicks / searches 的加权汇总(inferred)。如果运营想要的是其他口径(例如有点击的搜索占比),数字会变。
- 区间忽略了查询层面的聚集,实际略宽。

## Provenance
- Metric: 点击率 = sum(clicks) / sum(searches),按去重后的查询汇总,from stated here [guess](没有 metrics.json)
- Data: query_week、query_category(按 query_id 去重)、category_vertical,through 2026-W41(库里唯一的一周)
- Reconciled: not done(没有可对照的看板或其他来源)
- Queries and checks: 在本次会话中用 Python/sqlite3 临时执行,没有保存为文件