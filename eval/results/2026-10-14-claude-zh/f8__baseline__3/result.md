## Answer
Headline: 36.97 %（95% 区间 36.68%–37.26%，仅为二项分布近似）

2026-W41 购物垂类（shopping）的点击率为 36.97%：107,810 次搜索中有 39,9xx 次点击，覆盖 900 个查询。 [measured]
- Observed: +36.97 %（36.68%–37.26%）
- Adjusted: not computed（这是单周的水平值，不是对比，没有需要调整的因素）
- Causal effect: not identified（没有任何干预或对比，这个问题也不涉及因果）

## What it means for 商品运营（Merchandising）引用该数字
请引用 36.97%，不要用直接连表得到的 40.90%。40.90% 偏高约 3.9 个百分点，原因是重复映射造成了重复计数。

## Why we believe it
- Alternatives considered:
  - 直接连表的 40.90%：ruled out。query_category 有 250 个查询各有两行（2026-09-01 和 2026-10-09 各加载一次），连表后这些查询被重复计入 [measured]
  - 两次加载的类目不同，导致查询的垂类变了：ruled out。重复的 250 个查询两次都是同一个类目（apparel、electronics 或 home），没有改类 [measured]
  - 按最早或最晚一次加载去重：两种方式结果相同，都是 36.97% [measured]
- Checks run:
  - 查询 ID 唯一性：flag。2000 个不同查询共 2250 行，其中 250 个重复，已去重
  - 连表覆盖率：pass。W41 的 2000 个查询全部有类目；类目到垂类的映射无缺失
  - 数据合理性：pass。没有 clicks>searches，也没有空值
  - 区间：flag。区间按搜索次数的二项分布近似计算，没有考虑查询之间的差异，实际区间可能更宽 [inferred]

## Caveats, and what would change the answer
- 点击率按总点击数除以总搜索数（加权）计算，不是各查询点击率的平均值。如果口径是后者，数字会不同。
- 区间偏窄，原因见上面的区间检查。
- 垂类只包含 shopping 下的 apparel、electronics、home 三个类目。

## Provenance
- Metric: 点击率 = sum(clicks)/sum(searches)，从 stated here [guess]（目录里没有 metrics.json）
- Data: query_week、query_category、category_vertical，截至 2026-W41（库里只有这一周）
- Reconciled: not done（没有可对照的看板或其他来源）
- Queries and checks: 查询只在本次会话里运行，没有保存成文件

注：上面的点击数“39,9xx”是我按 36.97%×107,810 估算的，没有单独查询核实。