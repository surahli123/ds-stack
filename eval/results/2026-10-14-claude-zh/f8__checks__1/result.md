## Answer
Headline: 36.97 %(95% 区间 36.68%–37.26%)
2026-W41 购物垂类的点击率(CTR)为 36.97%,即 107,810 次搜索中有 39,857 次点击,覆盖 900 个查询。
- Observed: 36.97 %(36.68%–37.26%)。这是点击总数除以搜索总数。区间用二项近似算出,没有考虑查询之间的聚类,所以实际可能略宽。[measured]
- Adjusted: not computed(这只是单周的描述性比率,没有要控制的对比)
- Causal effect: not identified(这里没有做任何干预,也不是在估计效应)

## What it means for Merchandising 引用该数字
这个数字可以引用,但必须用去重后的口径(36.97%)。如果不先去重就直接 join,得到的是 40.89%,高估约 3.9 个百分点。这个偏差远大于 ±0.3 个百分点的区间。

## Why we believe it
- Alternatives considered:
  - 直接 join 的 40.89%(1150 行,137,945 次搜索,56,422 次点击):已排除。`query_category` 里有 250 个 query_id 重复(2250 行对应 2000 个 id),join 后购物查询被重复计算 [measured]
  - 重复的 query_id 对应不同类别:已排除。没有任何 query_id 对应多个类别,重复行只是重复加载的拷贝 [measured]
  - 比率口径(每个查询 CTR 的平均值,而不是总点击除以总搜索):未采用。我按"总点击/总搜索"计算,这是 CTR 的常规定义 [inferred]
- Checks run:
  - fanout(原始 join):fail。右表 2250 行对应 2000 个键,有 250 个重复键行,已按 query_id 去重 [measured]
  - fanout(去重后):pass。行数保持 2000 行,未丢失也未增加 [measured]
  - completeness:could not run。库里只有 W41 一周,没有更早的历史可对比。`loaded_at` 最晚为 2026-10-09,W41 本应在 10-11 结束,所以最后一两天可能没加载完 [inferred]
  - 数据合理性:pass。没有 clicks>searches 或 searches≤0 的行,所有 query_id 都有类别,5 个类别都映射到了垂类 [measured]
  - mix_shift、srm:skipped。只有单周数据,也没有实验,不适用

## Caveats, and what would change the answer
- 如果 W41 末尾几天数据未加载完,CTR 可能有偏。请确认该周已完整加载。
- 没有 metrics.json,CTR 的定义是我自己假设的,请跟 Merchandising 确认。
- 没有与看板核对;如果看板用的是未去重的 join,会显示约 40.9%。
- 区间没有考虑查询聚类。

## Provenance
- Metric: CTR = sum(clicks)/sum(searches),定义为 stated here [guess]
- Data: query_week、query_category(按 query_id 去重)、category_vertical,涵盖 2026-W41(完整性无法验证)
- Reconciled: not done(没有看板或其他来源可对照)
- Queries and checks: 检查日志在 `.ds-checks.log`(fanout#1、fanout#2、completeness#1);查询是在会话中即席运行的,没有另存为文件