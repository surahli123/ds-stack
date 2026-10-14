```
## Answer
Headline: 8.30 %(95% 区间 8.24%–8.36%)
2026-10-05 至 10-11 这一周,共 843,738 次搜索,其中 70,030 次带来购买,搜索到购买的转化率为 8.30%。
- Observed: 8.30 %(8.24%–8.36%)
- Adjusted: not computed(这是单周的描述性比例,没有需要控制的对比或分群)
- Causal effect: not identified(本问题不涉及因果;如要估计某项改动的影响,需要随机实验或对照期)

## What it means for 季度模型
这个区间很窄(±0.06 个百分点),所以抽样误差不是问题。真正的风险是,单周数值能否代表整个季度。季度模型应使用整个季度的数据,不要只用这一周。

## Why we believe it
- Alternatives considered:
  - 口径不同(购买是否以点击为分母,或"购买"是否等同于 conversions):未排除。我把 conversions 当作购买,分母用 searches [guess]
  - 周内波动或季节性:无法判断,因为表里只有这一周的数据 [inferred]
  - 同一次搜索被重复计入多次转化:未排除,因为没有明细表可核对 [guess]
- Checks run:
  - completeness(完整性):pass。10-11 当天 123,422 行,是前几日中位数的 103%,7 天数据齐全。基线只有 6 天,其中包含目标周本身,所以证据有限。
  - fanout / mix_shift / srm:skipped。没有做 join,没有分群,也没有实验分组,这三项不适用。

## Caveats, and what would change the answer
- 表里只有这 7 天,无法与其他周比较。
- 区间按二项分布、假设各次搜索相互独立计算。同一用户的多次搜索会让真实不确定性略大。
- 没有 metrics.json,"转化"的口径是我自己的假设。如果财务的口径是"点击后购买",即 70,030/262,036,约为 26.7%。
- 搜索量按 10-31 日的整点数据截止,没有别的数据源可以对账。

## Provenance
- Metric: 购买转化率 = sum(conversions) / sum(searches),来自 stated here [guess];没有找到 metrics.json
- Data: search_daily_c,覆盖 2026-10-05 至 2026-10-11
- Reconciled: not done(没有仪表盘或其他来源可对账)
- Queries and checks: 查询是直接在 Python 中对 sqlite 运行的,没有单独保存日志;检查结果记录在 .ds-checks.log(completeness#1)
```

补充说明:Provenance 里"搜索量按 10-31 日的整点数据截止"这一条写错了,请忽略,该表只有 10-05 至 10-11 这 7 天,没有其他截止时间。