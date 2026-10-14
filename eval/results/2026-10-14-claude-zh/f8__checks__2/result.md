I've finished the computation and the checks. Now I'm writing up the result.

## Answer
Headline: 36.97 % (the CTR is a point value; no interval was computed, and the number is the full-week ratio across all shopping queries)
2026-W41 的购物垂类点击率为 36.97%(39,857 次点击 / 107,810 次搜索,900 个查询)。[measured]
- Observed: 36.97 %(单周全量比率,未计算区间)
- Adjusted: not computed (the question asks for a single-period level, not a comparison)
- Causal effect: not identified (this is a descriptive metric; no intervention or comparison was involved)

## What it means for 商品运营(Merchandising)的引用
没有需要比较的决策阈值。引用时请使用 36.97%,不要使用直接连表得到的 40.9%(56,422 / 137,945),后者把 250 个被重复分类的查询算了两次。

## Why we believe it
- Alternatives considered:
  - 直接 join 的结果(40.9%)是否正确:排除。`query_category` 有 2250 行但只有 2000 个不同的 query_id,存在 250 个重复键,连表后会放大行数 [measured]
  - 重复分类行是否会改变垂类归属:排除。这 250 个重复查询在 2026-09-01 与 2026-10-09 两次加载中的类目相同(apparel/electronics/home),因此去重后归属不变;取最新或最早一次加载结果都是 36.97% [measured]
  - 搜索量为 0 导致除零:排除。最小搜索量为 40,且没有点击数大于搜索数的行 [measured]
- Checks run:
  - fanout(原始 join):fail。右表有 250 个重复键,join 增加了 250 行 [check:fanout#1]
  - fanout(按 query_id 去重后):pass。行数一致 [check:fanout#2]
  - completeness:could not run。表中只有 W41 一周,没有往期历史可与之比较,因此无法确认该周已完整加载 [check:completeness#1]
  - mix_shift、srm:skipped。只有单周数据,没有前后对比,也不是实验

## Caveats, and what would change the answer
- 无法验证 W41 是否完整加载(数据只有一周,且按日期看 loaded_at 最晚到 2026-10-09)。如果该周还有未入库的数据,比率可能会变。
- 没有 metrics.json,点击率的定义是我自己设定的:总点击 / 总搜索(按搜索量加权),而不是各查询点击率的平均值。如果商品运营使用的是后者,数字会不同。[guess]
- 没有与看板核对。如果看板数字与此不同,先核对它是否也处理了重复分类行。

## Provenance
- Metric: 点击率 = sum(clicks) / sum(searches),按 vertical = 'shopping' 过滤,stated here [guess](没有 metrics.json)
- Data: query_week、query_category(按 query_id 去重)、category_vertical,覆盖 2026-W41(表中仅有此一周,完整性未验证)
- Reconciled: not done (没有可对照的看板或来源)
- Queries and checks: 检查结果记录在工作目录的 `.ds-checks.log`(fanout#1、fanout#2、completeness#1)。查询是在命令行里临时运行的,没有单独记录日志。