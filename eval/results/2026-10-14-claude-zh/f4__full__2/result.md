## Answer
Headline: +0.0 pp (-0.66 到 +0.66 pp) [check:mix_shift#1]
10-07 的数据只加载了 0–9 点(10 小时),表面上的 -2.8 pp 是不完整一天造成的假象;按相同的 0–9 点对比,CTR 与前 7 天一致,没有可测出的下降 [q3, check:mix_shift#1, check:completeness#1]
- Observed: -2.83 pp (-3.49 到 -2.18 pp),即 27.00% 对 29.83%,但 10-07 只有 10/24 小时,不可比 [q4]
- Adjusted: +0.0 pp (-0.66 到 +0.66 pp),holding 小时构成(0–9 点同一批小时)fixed [check:mix_shift#1]
- Causal effect: not identified (未做随机实验;且在同小时口径下并无变化可解释)

## What it means for 是否向领导报告“搜索 CTR 下降”
不应报告下降。同小时口径的区间 -0.66 到 +0.66 pp 不含 -2.8 pp 的表观降幅 [check:mix_shift#1, q4];但请求中没有给出“值得行动的最小变化”,所以无法判断 ±0.66 pp 以内的小变动是否重要。待 10-07 全天数据落库后再复核。

## Why we believe it
- Alternatives considered:
  - 数据不完整/部分日(夜间小时 CTR 本来就低): ruled in,是表观下降的原因。10-07 只有 hour 0–9,夜间 0–7 点 CTR 为 24%,拉低了合计 [q2, q3, check:completeness#1] [measured]
  - 小时构成偏移(mix-shift): 与完整日对比时 ruled in;同小时对比后构成效应为 0 [check:mix_shift#1] [measured]
  - 星期效应/季节性: ruled out 的证据有限,前 7 天每日 CTR 稳定在 29.83% 左右,无明显星期波动;但没有更早的同星期数据 [q2] [inferred]
  - 日志/口径变化: 未发现,逐小时 CTR 与前 7 天逐小时完全一致,但无法排除上游 ETL 延迟 [q3] [inferred]
  - 真实的产品/排序原因导致下降: ruled out,同小时 CTR 没有变化 [check:mix_shift#1] [measured]
- Checks run:
  - completeness: fail 10-07 仅 10 行,为基线中位数 24 的 42% [check:completeness#1]
  - mix_shift: pass 同小时口径总变化 +0.00 pp,构成 0%,区间 -0.66 到 +0.66 pp [check:mix_shift#1]
  - fanout: skipped 未做 join
  - srm: skipped 非实验

## Caveats, and what would change the answer
- 10-07 的 10-23 点数据尚未加载;全天 CTR 要等数据补齐后才能得出,若下午/晚间 CTR 真有变化,此处看不到。
- 对比只覆盖 0–9 点,只是一天的一部分;区间假设各小时独立,实际可能偏窄。
- 表里没有平台/国家等分段,无法检查其他构成偏移。
- 没有 metrics.json,CTR 定义为猜测。

## Provenance
- Metric: 搜索 CTR = sum(clicks)/sum(searches),按日聚合自小时表 [guess]
- Data: search_hourly,截至 2026-10-06(最后一个完整日);2026-10-07 仅 0–9 点
- Reconciled: not done (无仪表盘或其他数据源可对账)
- Queries and checks: .ds-queries.log, .ds-checks.log
- Verified: verify_readout: pass (52 numbers on 11 lines; 3 queries, 2 checks, 0 given)