## Answer
Headline: -0.00 pp (-0.15 to +0.15) [check:mix_shift#1]
整体 CTR 下降了 2.10 pp,但几乎全部来自移动端流量占比上升;各平台内部的 CTR 基本没变,因此在"v2 不改变流量构成"的假设下,没有证据表明 v2 拉低了 CTR。 [check:mix_shift#1]
- Observed: -2.10 pp (-2.25 to -1.95) [check:mix_shift#1]
- Adjusted: -0.00 pp (-0.15 to +0.15), holding 平台构成(桌面/移动)fixed [check:mix_shift#1]
- Causal effect: not identified (v2 已全量上线,没有同期对照组;需要 v1 与 v2 的随机分流或保留部分 v1 流量)

## What it means for 是否回滚 v2
可归因于 v2 的变化区间为 -0.15 到 +0.15 pp,远小于整体 2.10 pp 的下降,不支持"回滚能恢复 CTR"的判断;但这是描述性结论,不是因果结论。 [check:mix_shift#1]

## Why we believe it
- Alternatives considered:
  - 流量构成变化(mix-shift): ruled in by 移动端占比从 40.1% 升到 55.1%,移动 CTR 22.0% 远低于桌面 36.0%,构成效应 -2.09 pp,占 100% [check:mix_shift#1] [measured]
  - 更细粒度(平台×国家)结论是否一致: ruled in by 四个分段的分解给出相同结果,构成效应 -2.09 pp,分段内 -0.00 pp [check:mix_shift#2] [measured]
  - 数据不完整: ruled out by 最后一天行数为趋势基线的 102% [check:completeness#1] [measured]
  - 星期效应/季节性: ruled out by 两周都是完整的周一至周日,各 7 天 [q3] [inferred]
  - v2 导致流量转向移动端(v2 引起构成变化): not ruled out; 需要 v2 上线前后移动端占比的长期趋势,或 v1/v2 并行的随机实验 [guess]
  - 日志或指标口径变化: not ruled out; release_log 只有 v2 上线一条记录,无法确认埋点是否变化 [q2] [inferred]
- Checks run:
  - mix_shift(平台): flag 构成效应 -2.09 pp,分段内 -0.00 pp [check:mix_shift#1]
  - mix_shift(平台×国家): flag 与粗粒度一致 [check:mix_shift#2]
  - completeness: pass 2026-10-04 行数为基线的 102% [check:completeness#1]
  - fanout: skipped 未做任何 join
  - srm: skipped 不是随机实验

## Caveats, and what would change the answer
- 移动端占比上升的原因未知:若是 v2 造成(例如改变了入口或查询量),则 v2 间接导致了下降;需要上线前更长的占比趋势来判断。
- 区间的标准误假设单位独立,实际可能偏窄。
- 仅有两周数据,且 v2 与周期同时切换,无同期对照。

## Provenance
- Metric: CTR = sum(clicks)/sum(searches),表 search_daily,按日汇总 [guess]
- Data: search_daily, release_log, through 2026-10-04
- Reconciled: not done (没有可对照的看板或 metrics.json)
- Queries and checks: .ds-queries.log, .ds-checks.log
- Verified: verify_readout: pass (26 numbers on 11 lines; 2 queries, 3 checks, 0 given); ds-verify: pass (0 fail, 0 could not verify, 0 warn, 19 pass)