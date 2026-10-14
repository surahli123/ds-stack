```
## Answer
Headline: can't tell
10-07 的数据只加载到 0–9 点(10/24 小时),原始 CTR 27.0% 比前 7 天的 29.83% 低 2.83 pp,但这是残缺日的时段构成造成的假象;按相同小时对比,变化为 0.00 pp [q2, q5, check:completeness#1, check:mix_shift#1]
- Observed: -2.83 pp (-3.47 到 -2.20)(10-07 的 0–9 点 vs 前 7 天全天;区间为按两比例手算的 95% 区间,未计入时段相关性) [q2, q5]
- Adjusted: +0.00 pp (-0.66 到 +0.66),holding 小时段构成(0–7 点 / 8–9 点)fixed [check:mix_shift#1]
- Causal effect: not identified (需要随机实验或明确的变更/上线记录;这里没有)

## What it means for 是否需要向领导通报 CTR 下跌并启动调查
同小时对比的区间 (-0.66, +0.66) pp 包含 0,没有证据显示真实下跌;全天数据落地后才能下结论,需重新用完整的 10-07 对比 [check:mix_shift#1, q4]。

## Why we believe it
- Alternatives considered:
  - 时段构成变化(mix-shift):ruled in。10-07 只含夜间低 CTR 小时(0–7 点 24%),前 7 天全天含白天高 CTR 小时;同小时对比 27.0% vs 27.0%,mix 贡献解释了全部表观下跌 [q3, q4, check:mix_shift#1] [measured]
  - 数据不完整:ruled in。10-07 仅有 10 行,为基线中位数 24 行的 42% [q2, check:completeness#1] [measured]
  - 星期效应/季节性:not ruled out。前 7 天每日 CTR 稳定在约 29.83%,波动极小,但只有一周数据,无法看周几差异 [q2] [inferred]
  - 日志或指标定义变化:not ruled out。没有变更记录可查,且每个小时的 CTR 与前 7 天完全一致,不像定义变化 [q3] [inferred]
  - 真实的产品/排序变化(提问者暗含的原因):ruled out as 当前证据所支持的解释,因为同小时 CTR 无变化 [q4, check:mix_shift#1] [inferred]
- Checks run:
  - completeness: fail 10-07 仅 10 行,为基线的 42%,这是数据缺口,所以 Headline 是 can't tell [check:completeness#1]
  - mix_shift: pass 按小时段拆分,整体变化 +0.00 pp = 段内 +0.00 pp (95% CI -0.66 到 +0.66) + 构成 +0.00 pp [check:mix_shift#1]
  - fanout: skipped 没有 join
  - srm: skipped 不是实验

## Caveats, and what would change the answer
- 10-07 的 10–23 点尚未落地;完整数据到位后用完整日重算即可定论(若白天 CTR 也与前 7 天一致,则无下跌)。
- 同小时对比只覆盖 0–9 点,不能说明下午和晚间没有问题。
- 区间假设各次搜索独立,实际可能偏窄。
- 无 metrics.json,CTR 定义为猜测。

## Provenance
- Metric: CTR = sum(clicks)/sum(searches),按 search_hourly 小时粒度汇总到日,来源 stated here [guess]
- Data: search_hourly,截至 2026-10-06(最后一个完整日);2026-10-07 只含 0–9 点
- Reconciled: not done (没有可对照的看板或其它来源)
- Queries and checks: .ds-queries.log, .ds-checks.log
- Verified: verify_readout: pass (57 numbers on 10 lines; 4 queries, 2 checks, 0 given)
```