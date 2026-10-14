## Answer
Headline: -0.00 pp (-0.15 至 +0.15 pp) [check:mix_shift#1]
整体 CTR 从 30.42% 降到 28.32%,但下降几乎全部来自流量向移动端偏移(占 100%),各细分内部的 CTR 基本没变,所以 v2 本身对 CTR 的影响约为 0(前提:v2 没有改变流量构成)。 [check:mix_shift#1]
- Observed: -2.10 pp (-2.25 至 -1.95 pp) [q3, check:mix_shift#1]
- Adjusted: -0.00 pp (-0.15 至 +0.15 pp), holding 平台×国家的流量构成 fixed [check:mix_shift#1]
- Causal effect: not identified (v2 与周次完全重合,没有同期 v1 对照;需要按流量随机分配 v2/v1 的 A/B 或 holdback)

## What it means for 是否回滚 v2
区间 -0.15 至 +0.15 pp 内的细分内 CTR 变化很小;用户未给出回滚阈值,这里假设 0.1 pp(mix_shift 的 min_effect)作为会改变决定的最小变化,则区间仍略跨过该阈值,只能说"没有证据表明 v2 降低了 CTR",不能证明其无害。整体 -2.10 pp 的下降不应作为回滚理由。 [check:mix_shift#1]

## Why we believe it
- Alternatives considered:
  - 流量构成偏移(mix-shift): ruled in,桌面端占比由 59.9% 降到 44.9%,移动端由 40.1% 升到 55.1%;移动端 CTR 约 22% 对桌面端约 36% [q6, check:mix_shift#2] [measured]
  - PM 的假设(v2 导致下降): ruled out 作为主因,各平台×国家细分内 v1 与 v2 的 CTR 几乎相同(例如 desktop US 37.07% 对 37.07%) [q5, check:mix_shift#1] [measured]
  - 季节性/星期: ruled out 作为主因,两周都完整覆盖周一至周日,且细分内 CTR 没变化 [q3, q5] [inferred]
  - 数据不完整: ruled out,每天 4 行,完整 [q3, check:completeness#1] [measured]
  - 日志/定义变更: ruled out 在现有证据下,release_log 只有 v2 上线一条记录;但未见移动端流量上升的原因记录 [q2] [inferred]
- Checks run:
  - mix_shift(平台×国家): flag 混合效应 -2.09 pp,细分内 -0.00 pp [check:mix_shift#1]
  - mix_shift(平台,更粗粒度): flag 结果一致,混合效应 -2.09 pp [check:mix_shift#2]
  - completeness: pass 2026-10-04 行数为基线的 100% [check:completeness#1]
  - fanout: skipped 没有做 join
  - srm: skipped 不是随机实验

## Caveats, and what would change the answer
- v2 与周次完全重合,无同期对照,无法识别因果;需要 holdback 或随机分流才能确认。
- 若 v2 本身造成了向移动端的流量偏移(例如改变了桌面端使用),则 mix 部分也应归因于 v2;需查明移动端流量上升的来源(营销、产品发布等)。
- 区间的标准误假设各单元独立,真实区间可能更宽。
- 只有两周数据,每个细分每周仅 7 天。

## Provenance
- Metric: CTR = sum(clicks)/sum(searches),表 search_daily,按周汇总, stated here [guess]
- Data: search_daily, release_log, through 2026-10-04
- Reconciled: not done (没有可对照的看板或 metrics.json)
- Queries and checks: .ds-queries.log, .ds-checks.log
- Verified: verify_readout: pass (30 numbers on 11 lines; 4 queries, 3 checks, 0 given)