## Answer
Headline: 46.05 %(95% 区间 45.93–46.17 %)
2026-10-05 至 10-11 这一周,外部真实用户的搜索点击率(CTR)为 46.05 %。这是一个水平值,没有与上周比较。

- Observed: 46.05 %(45.93–46.17 %),按"有点击的搜索数 ÷ 搜索数"、仅外部流量计算 [measured]。区间是对 698,782 次搜索按二项分布算的,没有考虑按天聚集的相关性。
- Adjusted: not computed(没有可比较的对象,也没有需要调整的混杂因素)
- Causal effect: not identified(这只是描述性指标,没有实验或对照设计)

## What it means for 周度业务回顾
CTR 的口径不同,数字差别很大:全部流量为 41.41 %,外部加内部(去掉机器人)为 47.06 %,外部为 46.05 %。口径之间的差距(最大约 5.6 个百分点)远大于抽样误差(±0.12 个百分点)。所以口径比抽样误差更影响决策,汇报时必须写明口径。

## Why we believe it
- Alternatives considered:
  - 机器人流量拉低了整体 CTR:成立。机器人占搜索量约 12.5 %,CTR 只有约 1.97 %,所以全部流量口径的 41.41 % 偏低 [measured]
  - 内部流量抬高了 CTR:成立。内部流量 CTR 约 67 %,占比约 4 %,会把去掉机器人后的数字从 46.05 % 抬到 47.06 % [measured]
  - 把"点击数 ÷ 搜索数"当作 CTR:未采用。外部口径下为 64.5 %,内部甚至超过 100 %,不是比例意义上的点击率 [measured]
  - 桌面端和移动端的差异:排除。外部流量中两者分别为 46.06 % 和 46.04 %,几乎一样 [measured]
- Checks run:
  - completeness: pass。10-11 当天有 6 行,是前几天中位数的 100 %,整周 7 天 × 6 个分组共 42 行,无缺失。
  - mix_shift: skipped。只有一周数据,没有可比的前后期。
  - fanout: skipped。没有做连接,只对单表做聚合。
  - srm: skipped。这不是实验。

## Caveats, and what would change the answer
- 没有 metrics.json,CTR 口径是我自己定的,属于猜测 [guess]。如果你们的看板口径是全部流量(41.41 %),或是"点击数 ÷ 搜索数",数字会完全不同。
- 仓库里只有这一周的数据,无法给出周环比,也无法对账。
- 视图名为 `search_daily_v`,我没有查它的底层定义,不能确认机器人和内部流量的标记是否准确 [inferred]。

## Provenance
- Metric: 有点击的搜索数 ÷ 搜索数,仅 traffic_type=external,出处是 stated here [guess]
- Data: `search_daily_v`,覆盖 2026-10-05 至 10-11,最后一个完整日是 10-11
- Reconciled: not done(没有看板或其他来源可对照)
- Queries and checks: 查询是在终端里直接运行的,没有记录文件。completeness 检查的结果记录为 completeness#1,写在工作目录的 `.ds-checks.log`。