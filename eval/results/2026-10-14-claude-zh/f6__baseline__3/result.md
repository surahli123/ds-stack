## Answer
Headline: 46.0 %（95% 区间 45.97%–46.13%）
2026-10-05 至 10-11 这一周,真人(external)流量的搜索点击率(CTR)为 46.0%。如果把机器人和内部流量也算进去,则是 41.4%。

- Observed: +46.05 %(95% 区间 45.97%–46.13%),口径为 external 流量中带点击的搜索数 ÷ 搜索数。区间用 7 个日值的标准误估计 [measured]。
- Adjusted: not computed(这是单周的水平值,没有对比基准可供调整)
- Causal effect: not identified(这只是描述性指标,没有干预或对照)

## What it means for 周度业务回顾(WBR)
这个数是一个水平值,没有上周或目标值可比,所以无法判断它是变好还是变坏。真正影响结论的是口径:是否剔除机器人流量会让数字差出约 4.6 个百分点,远大于 ±0.1 个百分点的抽样误差。

## Why we believe it
- Alternatives considered:
  - 口径 A,全部流量,点击搜索 ÷ 搜索:41.4%。机器人占约 11.3% 的搜索量,点击率仅 2.0%,会明显拉低整体数字,所以排除 [measured]
  - 口径 B,点击数 ÷ 搜索数:external 为 64.5%,但会受单次搜索多次点击的影响,不是"点击率"的常规口径,所以排除 [inferred]
  - 口径 C,分母只用有结果的搜索:external 另算,全流量为 44.5%。未采用,因为没有依据说明 WBR 用这个口径 [inferred]
  - 内部流量(67.2%)是否应剔除:已剔除,因为它不代表用户行为 [inferred]
  - 桌面端与移动端差异:ruled out,两者分别为 46.06% 和 46.04% [measured]
- Checks run:
  - 日期覆盖:pass,7 个完整日期,没有缺失
  - 数据一致性:pass,没有"带点击的搜索数大于有结果的搜索数"或"有结果的搜索数大于搜索数"的行
  - 日间稳定性:pass,日值在 45.9%–46.2% 之间
  - 与看板对账:could not run,没有可用的看板

## Caveats, and what would change the answer
- 没有 metrics.json,CTR 的定义是我自己假设的。如果 WBR 使用别的口径(例如含机器人、按点击数计),数字会变。
- "剔除机器人和内部流量"是我的判断,需要确认这是否是 WBR 的惯例。
- 区间只反映日间波动。如果同一用户的搜索彼此相关,真实不确定性会更大。
- 没有历史数据,无法给出环比。

## Provenance
- Metric: CTR = 带点击的搜索数 ÷ 搜索数,仅 traffic_type = external,来源:stated here [guess]
- Data: search_daily_v,2026-10-05 至 10-11(完整 7 天)
- Reconciled: not done(没有看板或其他参照来源)
- Queries and checks: 查询是在对话中用 Python/sqlite3 直接运行的,没有保存成文件。