## Answer
Headline: 36.97 %(95% 区间 36.18–37.76 %)
2026-W41 购物垂类的点击率(CTR)为 36.97%,即 107,810 次搜索中有 39,857 次点击。

- Observed: 36.97 %(36.18–37.76 %)。按查询聚类的稳健区间,覆盖 900 个查询。[measured]
- Adjusted: not computed(这是单周的描述性指标,没有需要调整的对比)
- Causal effect: not identified(这里没有要估计的干预或对比)

## What it means for Merchandising 引用该数字
这个数字可以直接引用,写成约 37.0%,误差约 ±0.8 个百分点。如果要拿它和其他周或其他垂类比较,只有差异大于约 1 个百分点时才站得住。

## Why we believe it
- Alternatives considered:
  - 直接 join 造成重复计数:query_category 有 250 个查询在 2026-10-09 重新加载,所以同一查询出现两行。直接 join 会得到 56,422 次点击 / 137,945 次搜索 = 40.9%,是虚高的。去重后得到 36.97%。[measured]
  - 同一查询的类别在两次加载间发生变化:已排除。0 个查询出现多个类别,重复行完全一致。[measured]
  - 有查询没有类别映射:已排除。查询缺失数为 0。[measured]
  - 对点击率取各查询点击率的平均值:没有采用。我取的是总点击除以总搜索(加权),这是常规的 CTR 定义。[inferred]
- Checks run:
  - 数据质量:pass。没有空值,也没有 clicks 大于 searches 的行。W41 的 2000 个查询各一行。
  - 去重后的行数:pass。共 900 个购物查询,类别映射是 3 个类别对应 shopping。
  - 区间:pass。按查询聚类的区间是 ±0.79 个百分点,比二项式的 ±0.29 更宽,因为查询之间有差异。
  - 与看板对账:skipped,没有可用的看板。

## Caveats, and what would change the answer
- 数据里只有 W41 一周,所以无法看趋势。
- 点击率按总点击 / 总搜索计算。如果 Merchandising 的口径是各查询点击率的简单平均,数值会不同。
- 购物垂类取自 category_vertical 的 electronics、apparel、home 三个类别。如果映射表有变动,结果也会变。

## Provenance
- Metric: CTR = sum(clicks) / sum(searches),来自 stated here [guess];目录里没有 metrics.json。
- Data: query_week、query_category(按 query_id 和 category 去重)、category_vertical,覆盖 2026-W41。
- Reconciled: not done(没有看板或其他来源可对账)
- Queries and checks: 在本会话中用内联 Python/SQLite 运行,没有保存成文件。