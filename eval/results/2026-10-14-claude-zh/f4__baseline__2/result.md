## Answer
Headline: can't tell (昨天的数据只有 0–9 点,不是完整一天)

CTR "下降"是数据不完整造成的假象:2026-10-07 只有 0–9 点共 10 个小时,而且缺的是 CTR 较高的白天时段。按相同的 0–9 点对比,昨天的 CTR 和前 7 天几乎一样。

- Observed: −2.83 个百分点 (27.00% 对 29.83%;约 ±0.7 pp,按二项分布粗估) [measured]。这是错位比较,不能当作真实下降。
- Adjusted: 0.00 个百分点 (约 ±0.7 pp,按二项分布粗估),固定了时段(两边都只取 0–9 点),昨天 27.00%,前 7 天 27.00% [measured]
- Causal effect: not identified(这是观察数据,没有实验或对照设计;而且这里也看不到需要解释的下降)

## What it means for 是否要对 CTR 下滑采取行动
同口径下的区间约为 ±0.7 pp,以零为中心,没有证据显示 CTR 下降。在拿到 10-07 的完整数据之前,我不建议向领导报告"CTR 下降 2.8 pp"。

## Why we believe it
- Alternatives considered:
  - 真实的 CTR 下降: 不成立。0–9 点的 CTR 每天都是 26.99%–27.01%,昨天是 27.00% [measured]
  - 时段构成不同(partial day)造成的假象: 成立。10-07 只有 10 个小时的数据,而其余日期有 24 个小时。每天 0–7 点 CTR 约 24%,8–22 点约 31%,全天约 29.83%;缺了高 CTR 的白天时段,全天数字自然偏低 [measured]
  - 周内效应(星期几): 这里没有排除,但 7 天内每天的全天 CTR 都在 29.83% 左右,看不出星期几的差异 [inferred]
  - 昨天的 8、9 点是否正常: 正常。这两个小时的 CTR 是 31.0%,和其他日期一致 [measured]
- Checks run:
  - 日期完整性(每天的小时数): flag。10-07 只有 10 小时,其余日期各 24 小时,共 178 行,没有重复的日期加小时 [measured]
  - 同时段对比(0–9 点): pass。昨天 27.00% 对前 7 天 27.00% [measured]
  - 区间: 粗估。没有按小时聚类,也没有做过度离散检验,实际区间可能更宽 [guess]

## Caveats, and what would change the answer
- 10-07 的 10–23 点还没有入库。如果这些小时 CTR 出现下降,全天结果会变,所以要等数据补全后重算。
- 数据管道可能延迟或中断,需要确认 10-07 为什么只有 10 小时(这是 10-14 查看的结果,按理早该入库完整)。
- 我没有找到 metrics.json,CTR 的定义是我假设的。
- 我没有拿看板数字对账。

## Provenance
- Metric: CTR = sum(clicks) / sum(searches),按总量计算,不是小时 CTR 的平均值;来自 stated here [guess]
- Data: search_hourly,2026-09-30 到 2026-10-06 是完整日;2026-10-07 只到 9 点
- Reconciled: not done (没有看板或 metrics.json 可对照)
- Queries and checks: 查询在本次会话的命令行里直接运行,没有保存成文件