## Answer
Headline: 46.0%(95% 区间 45.9% 至 46.2%),口径为外部真实用户、有点击的搜索数 ÷ 搜索数。[measured,口径选择为 guess]
2026-10-05 至 10-11 这一周,外部真实流量的搜索 CTR 为 46.0%。如果把机器人和内部流量都算进去,则是 41.4%。

- Observed: 全部流量 +41.4%(41.3% 至 41.5%);仅外部流量 46.0%(45.9% 至 46.2%)。这是水平值,不是变化量。[measured]
- Adjusted: not computed(这是单周水平值,没有对比期,没有需要调整的变化)
- Causal effect: not identified(这是描述性指标,不涉及干预)

## What it means for 周度业务回顾
这个数字只能作为本周的基准值,不能据此判断涨跌。区间只有约 ±0.1 个百分点,所以统计误差不是问题。真正影响数字的是口径:机器人流量占 12.5%,把外部口径拉低了约 4.6 个百分点。口径选错比抽样误差大得多。

## Why we believe it
- Alternatives considered:
  - 机器人流量拉低 CTR:纳入后总体 CTR 为 41.4%,机器人自身仅 约2.0%(2074/105117),所以在外部口径中排除了机器人。[measured]
  - 内部流量抬高 CTR:内部 CTR 为 67.2%,占比 4.2%。如果只排除机器人、保留内部,结果为 47.1%。我选择外部口径是为了代表真实用户。[measured]
  - CTR 应按点击数 ÷ 搜索数计算:这样外部为 64.5%,这是人均点击次数,不是比例,可能超过 100%,因此不采用。[inferred]
  - 本周数据不完整:ruled out,见下方 completeness 检查。[measured]
- Checks run:
  - completeness:pass。10-11 当天有 6 行,是前几天中位数的 100%,7 天都完整,每天各 6 行(2 个平台 × 3 种流量类型)。
  - mix_shift:skipped(实际无意义)。表里只有这一周,没有对比期,我传入的是前后相同的数,结果恒为 0,不能说明任何问题。
  - fanout、srm:skipped。没有做表连接,也没有实验分组。

## Caveats, and what would change the answer
- metrics.json 不存在,CTR 的官方定义没有找到。我用的是"有点击的搜索 ÷ 搜索",并且排除了机器人和内部流量,这是我的假设 [guess]。如果周报沿用含全部流量的口径,应报 41.4%。
- 区间假设每次搜索相互独立,实际用户有重复搜索,真实区间会更宽一些。
- 仓库数据从 10-05 才开始,所以无法与上周比较,也无法与已有看板核对。

## Provenance
- Metric: 有点击的搜索数 ÷ 搜索数,仅 traffic_type='external',出处是 stated here [guess]
- Data: search_daily_v,到 2026-10-11(最后一个完整周期)
- Reconciled: not done(没有看板或 metrics.json 可对照)
- Queries and checks: 检查结果记录在工作目录下的 .ds-checks.log(completeness#1、mix_shift#1)。查询是交互式 Python 执行的,没有单独保存脚本。