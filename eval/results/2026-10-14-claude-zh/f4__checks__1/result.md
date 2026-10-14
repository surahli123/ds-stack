## Answer
Headline: can't tell(昨日数据只加载了 0–9 点,不是完整的一天)

表面上的"下降"约 −2.83 个百分点,但这是数据不完整造成的假象。在已有的 0–9 点上做同时段对比,CTR 与前 7 天相同。

- Observed: −2.83 个百分点 (27.00% vs 29.83%),但这是不同时段的对比,不能当作真实下降 [measured]。在同样的 0–9 点上对比:0.00 个百分点 (−0.66 到 +0.66) [measured]。
- Adjusted: 0.00 个百分点 (−0.66 到 +0.66),固定为同一时段(0–9 点)且小时结构相同 [measured]。区间假设各次搜索相互独立,实际可能偏窄。
- Causal effect: not identified(没有实验或对照设计;而且 10/07 的数据尚未完整)

## What it means for 是否向领导汇报"搜索 CTR 下降"
目前没有证据显示 CTR 下降:同时段的变化是 0.00 个百分点,区间为 ±0.66。这个区间只能排除大于 0.7 个百分点的下降,排除不了更小的下降。要等 10/07 全天数据加载完整后再下结论。

## Why we believe it
- Alternatives considered:
  - 真实的 CTR 下降: 在 0–9 点上基本排除。各小时 CTR 与前 7 天完全一致,0–7 点为 24%,8–9 点为 31% [measured]。
  - 数据不完整(只有 10 个小时): 成立。10/07 只有 0–9 点共 10 行,正常是 24 行 [measured]。
  - 白天高 CTR 的小时缺失,拉低了整日 CTR: 成立,这是 −2.83 个百分点的来源。完整的一天里 10–23 点占了大部分搜索量,而且这些小时 CTR 偏高 [inferred]。
  - 小时构成变化(mix shift): 排除。两个时段的权重与前 7 天相同,mix 效应为 0 [measured]。
  - 10–23 点的真实表现: 无法判断,没有数据 [guess]。
- Checks run:
  - completeness: fail。10/07 只有 10 行,是前 7 天中位数 24 行的 42%(completeness#1)。
  - mix_shift: pass。同时段变化为 +0.00 个百分点,95% 区间 −0.66 到 +0.66,mix 占比 0%(mix_shift#1)。
  - fanout: skipped,没有做连接。
  - srm: skipped,不是实验。

## Caveats, and what would change the answer
- 10/07 的 10–23 点数据到位后需要重算。如果那时 CTR 仍与前 7 天持平,就没有下降。
- 数据管道是否延迟,需要找数据工程团队确认。
- 前 7 天内部很稳定,每天都在 29.83% 附近 [measured]。
- 小时数据看起来很规整(各小时数几乎相同),可能是模拟或聚合数据,我没有核实 [guess]。

## Provenance
- Metric: CTR = clicks / searches(按总数加权),来源是 stated here [guess]。目录里没有 metrics.json。
- Data: search_hourly,完整日期到 2026-10-06;2026-10-07 只有 0–9 点。
- Reconciled: not done(没有仪表盘或其他数据源可比对)
- Queries and checks: 检查结果记录在 `.ds-checks.log`(completeness#1、mix_shift#1)。查询是内联 Python 执行的,没有单独保存。