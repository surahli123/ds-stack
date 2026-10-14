## Answer
Headline: -0.00 pp (-0.15 至 +0.15 pp) [check:mix_shift#1]
整体 CTR 从 30.42% 降到 28.32%,但下降几乎全部来自流量向 mobile(CTR 约 22%)倾斜,而不是 v2 让各平台内的 CTR 变差;前提是 v2 本身没有改变流量构成。 [check:mix_shift#1]
- Observed: -2.10 pp (-2.25 至 -1.95 pp) [check:mix_shift#1]
- Adjusted: -0.00 pp (-0.15 至 +0.15 pp), holding 平台构成(desktop/mobile)fixed [check:mix_shift#1]
- Causal effect: not identified (v2 是全量一次性上线,没有对照组;需要 v1/v2 随机分流的 A/B,或确认 mobile 占比上升与 v2 无关)

## What it means for 是否回滚 v2
构成效应为 -2.09 pp,组内效应为 -0.00 pp,区间 ±0.15 pp 内未见 v2 使各平台 CTR 下降的证据;若回滚的门槛是组内 CTR 下降超过 0.3 pp,则区间不触及该门槛。 [check:mix_shift#1] 该 0.3 pp 门槛是 mix_shift 检查的默认阈值,不是用户给出的数字。 [check:mix_shift#1]

## Why we believe it
- Alternatives considered:
  - 构成变化(mix-shift):ruled in,desktop 占比从 59.9% 降到 44.9%,mobile 相应上升,构成效应 -2.09 pp,占 100% [check:mix_shift#1] [measured]
  - 更细粒度(平台×国家)是否一致:ruled in(结论一致),组内 -0.00 pp (-0.15 至 +0.15),构成 -2.09 pp [check:mix_shift#2] [measured]
  - v2 导致 CTR 下降(PM 的假设):ruled out 作为平台内的效应,desktop 36.05% vs 36.05%,mobile 22.06% vs 22.02%,几乎不变 [q4, check:mix_shift#1] [measured]
  - v2 导致流量向 mobile 倾斜:not ruled out,数据无法区分;该推断没有机制证据 [guess]
  - 季节性/星期:ruled out 作为主因,两周都是完整的周一到周日,各 28 行 [q3] [inferred]
  - 同期其他发布或日志变更:ruled out,release_log 中只有 v2 上线一条记录 [q2] [measured]
  - 数据缺失:ruled out,两周每天都有 4 个分段 [q3] [measured]
- Checks run:
  - completeness: could not run 历史周期不足 3 个,无法对比 [check:completeness#1]
  - mix_shift(平台): flag 构成占 100%,组内 -0.00 pp [check:mix_shift#1]
  - mix_shift(平台×国家): flag 与平台粒度一致 [check:mix_shift#2]
  - fanout: skipped 没有做 join
  - srm: skipped 不是随机实验

## Caveats, and what would change the answer
- 没有对照组,v2 是否间接导致流量向 mobile 倾斜无法判断;需要查 mobile 占比上升的原因(如获客渠道、app 发布)。
- 只有两周数据,没有更长历史,不能排除每周波动;补充更多周数据可确认。
- 区间假设各搜索相互独立,实际可能偏窄。
- 指标定义是我自己设定的,未与仪表盘核对。

## Provenance
- Metric: CTR = sum(clicks) / sum(searches),search_daily,按周汇总,from stated here [guess]
- Data: search_daily, release_log, through 2026-10-04
- Reconciled: not done (没有仪表盘数字,也没有 metrics.json)
- Queries and checks: .ds-queries.log, .ds-checks.log
- Verified: verify_readout: pass (34 numbers on 12 lines; 3 queries, 3 checks, 0 given)