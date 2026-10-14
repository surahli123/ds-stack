## Answer
Headline: 0.0 pp (-0.66 到 +0.66 pp) [check:mix_shift#1]
昨天(10-07)原始 CTR 比前 7 天低 2.83 pp,但这是假象:昨天只加载了 0–9 点,按相同小时对比后 CTR 没有变化 [q5, check:mix_shift#1]。
- Observed: -2.83 pp (-3.47 到 -2.20 pp) [q5]
- Adjusted: 0.0 pp (-0.66 到 +0.66 pp),固定每个小时段的构成(0–7 点与 8–9 点,权重相同)不变 [check:mix_shift#1]
- Causal effect: not identified (没有随机实验或可识别的设计;而且在同小时对比下并没有可解释的下降)

## What it means for 是否向领导报告"CTR 下跌"
同小时对比的区间 -0.66 到 +0.66 pp 包含 0,没有证据显示真实下跌;原始的 -2.83 pp 来自昨天只有 10 小时数据、而夜间小时 CTR 低(24%)占比高 [q3, q5, check:mix_shift#1]。建议不要对外报告 -2.83 pp;等 10-07 全天数据落地后再复算。

## Why we believe it
- Alternatives considered:
  - 数据不完整(昨天只有 0–9 点): ruled in by 昨天只有 10 个小时的行,前几天每天 24 小时 [q2] [measured]
  - 构成/小时混合变化(mix-shift): ruled in 为原始差值的原因:同小时对比下各小时 CTR 完全一致(0–7 点为 24%,8–9 点为 31%),0–9 点内前 7 天 CTR 与昨天均为 27.0% [q3, q4, check:mix_shift#1] [measured]
  - 真实的产品/体验变化导致 CTR 下降: ruled out for 已加载的小时,每个小时 CTR 与前 7 天相同 [q3, check:mix_shift#1] [measured];晚些小时(10–23 点)尚无数据,无法判断 [inferred]
  - 星期/季节性: ruled out 部分,前 7 天每日 CTR 稳定在 29.83% 左右 [q2] [measured];同星期对比因历史不足无法做 [guess]
  - 日志/定义变更: not seen,未发现异常,但没有 metrics.json 可核对 [guess]
- Checks run:
  - completeness: fail 10-07 数据不完整(仅 10 小时,基线为 24 小时) [check:completeness#1]
  - mix_shift: pass 同小时对比下变化 +0.00 pp(区间 -0.66 到 +0.66 pp),mix 份额 0% [check:mix_shift#1]
  - mix_shift(整体粒度): could not run 只有 1 个分段,无法分解 [check:mix_shift#2]
  - fanout: skipped 没有做 join
  - srm: skipped 不是实验

## Caveats, and what would change the answer
- 10-07 的 10–23 点尚未加载;全天数据落地后需重算(若晚间 CTR 真有下降则结论会变)。
- 区间假设各搜索独立,实际可能偏窄(mix_shift 已标注 se_assumes_independent_units)。
- 同小时对比的 CTR 在各天几乎完全一致,看起来像合成/聚合数据,建议确认上游数据是否被填充。
- CTR 定义为猜测,需与仪表盘核对。

## Provenance
- Metric: CTR = sum(clicks)/sum(searches),表 search_hourly,按日/小时聚合 stated here [guess]
- Data: search_hourly,截至 2026-10-06(最后完整日);2026-10-07 仅 0–9 点
- Reconciled: not done (没有仪表盘或 metrics.json 可对照)
- Queries and checks: .ds-queries.log, .ds-checks.log
- Verified: verify_readout: pass (56 numbers on 12 lines; 4 queries, 3 checks, 0 given)