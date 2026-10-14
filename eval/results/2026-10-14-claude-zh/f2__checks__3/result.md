```
## Answer
Headline: 55.0 % (95% 区间 54.6%–55.4%)
2026-W40 的导航类查询点击率约为 55.0%(32,878 次点击 / 59,800 次搜索,按当前标签 is_current=1 统计,共 400 个查询)。[measured]
- Observed: +55.0 %(54.6%–55.4%,二项近似,按搜索次数计)
- Adjusted: not computed(这是单周的水平值,不是对比,没有需要调整的混杂因素)
- Causal effect: not identified(这是描述性指标,不涉及干预)

## What it means for 营销规划文档
规划文档可以直接引用约 55%。区间只有 ±0.4 个百分点,所以统计误差不会改变规划;真正会改变数字的是标签口径。若把已失效的旧标签一并计入,结果会变成 45.0%。

## Why we believe it
- Alternatives considered:
  - 把 query_labels 全表直接连接(含历史标签):ruled out。同一查询有多条标签会使行数膨胀,得到 45.0%(600 行/400 个查询,旧标签行的点击率仅 25.0%)。只取 is_current=1 后每个查询恰好一条标签。[measured]
  - 标签版本 v1 与 v2 口径不同:ruled out。当前标签下 v1 为 54.98%,v2 为 54.99%,几乎一致。[measured]
  - 对每个查询的点击率取简单平均:未采用。按搜索次数加权(总点击/总搜索)才是通常的点击率定义。[inferred]
- Checks run:
  - fanout(当前标签连接):pass。1000 行连接后仍为 1000 行,每个查询恰好匹配一条当前标签。
  - completeness:could not run。库里只有 W40 一周,缺少历史周来比较。该周是否已完整加载无法验证。
  - 数据完整性:pass。没有空值,也没有 clicks>searches 的行。[measured]
  - mix_shift、srm:skipped。没有跨期对比,也不是实验。

## Caveats, and what would change the answer
- 只有 W40 一周的数据,无法确认它已完整加载。如果它是部分加载的,数字可能偏移。
- 口径取决于“当前标签”。若营销想用别的标签版本,数字会变。
- 区间用的是二项近似,没有考虑查询之间的聚集效应,实际区间可能略宽。

## Provenance
- Metric: 点击率 = sum(clicks)/sum(searches),限于 intent='navigational' 且 is_current=1 的查询,metrics.json 不存在,此定义为 stated here [guess]
- Data: query_stats、query_labels,覆盖 2026-W40(库中唯一的一周,完整性未验证)
- Reconciled: not done(没有仪表盘或其他来源可对照)
- Queries and checks: 查询为临时的内联 SQL,未单独保存。检查结果记录在 .ds-checks.log(fanout#1、completeness#1)
```