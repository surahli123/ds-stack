## Answer
Headline: 0.0 个百分点(95% 区间 −0.7 至 +0.7 pp)。我没有发现 CTR 真的下降。

昨天(10-07)的数据只有 0–9 点,不是完整一天。全天口径的 CTR 看起来低 2.8 pp,原因是缺了高 CTR 的下午和晚上时段。按相同小时对比,CTR 完全没变。

- Observed: −2.8 pp(27.0% 对前 7 天的 29.8%;区间约 ±0.7 pp,即 −3.5 至 −2.1),这是直接用已有的 10-07 数据与前 7 天全天数据相比。[measured]
- Adjusted: 0.0 pp(−0.7 至 +0.7),保持小时构成不变(都只看 0–9 点)。前 7 天 0–9 点的 CTR 是 27.0%,10-07 的 0–9 点也是 27.0%。[measured]
- Causal effect: not identified(这只是前后对比,没有对照组。不过调整后差值为 0,也没有需要解释的下降。)

## What it means for 是否对"搜索 CTR 下降"采取行动
如果值得行动的最小下降是 0.5 pp,那么区间上限 −0.7 pp 仍略超出这个门槛,所以样本量能排除大的下降,但排除不了小幅下降。建议不要向领导报"下降 2.8 pp",等 10-07 完整数据落库后再复核。

## Why we believe it
- Alternatives considered:
  - 真实的 CTR 下降:ruled out。相同小时对比,0–9 点的 CTR 逐小时都与前 7 天完全一致(0–7 点 24%,8–9 点 31%)。[measured]
  - 数据不完整(部分日):ruled in。10-07 只有 10 个小时,其他日期都是 24 小时。[measured]
  - 小时构成偏移(夜间 CTR 低、白天高):ruled in。凌晨 0–7 点 CTR 24%,8 点后 31%;缺失的时段是高 CTR 的白天和晚上。[measured]
  - 搜索量异常:ruled out。10-07 每小时的搜索量与基线一致(0–7 点 1400,8–9 点 4200,均在历史范围内)。[measured]
  - 数据重复或缺失小时:ruled out。没有重复的日期加小时,10 个小时都不缺。[measured]
- Checks run:
  - 日期完整性:flag。10-07 只有 0–9 点。
  - 逐小时对比基线:pass。10 个小时的 CTR 与基线全部一致。
  - 重复行:pass。重复行数为 0。
  - 区间:按二项分布的正态近似,把前 7 天按合并比例计算;未考虑日间相关性。

## Caveats, and what would change the answer
- 10-07 在 10 点之后的数据未落库,可能是管道延迟,也可能数据确实缺失。10 点之后若出现真实下降,这个结论会变。[inferred]
- 基线每个小时的 CTR 几乎恒定,数据看起来很规整,可能是合成或已聚合的数据;区间可能偏窄。[guess]
- 没有按渠道、设备、地区拆分的数据,无法排查局部下降。
- 在 10-07 完整数据到位后重跑同一对比,即可确认。

## Provenance
- Metric: CTR = clicks / searches,按合并计数计算(不是各小时 CTR 的平均);来源是 stated here [guess],因为目录里没有 metrics.json。
- Data: search_hourly,覆盖 2026-09-30 至 10-06 的完整天,以及 10-07 的 0–9 点(不完整)。
- Reconciled: not done(没有仪表盘或其他来源可对照)。
- Queries and checks: 查询是在会话中用 Python 的 sqlite3 直接运行的,没有保存到文件;上面列出的每个数字都可以用 search_hourly 按日期和小时汇总重现。