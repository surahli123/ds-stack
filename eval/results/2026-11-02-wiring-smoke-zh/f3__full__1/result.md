## Answer
Headline: -1.82 pp (95% CI -1.97 to -1.67) [check:mix_shift#1]
整体 CTR 从 30.44% 降到 28.61%,几乎全部是各分群内部的下降(集中在桌面端),流量结构变化可忽略;若同期没有其他因素,这就是 v3 对应的下降幅度。 [check:mix_shift#1]
- Observed: -1.83 pp (95% CI -1.98 to -1.68) [check:mix_shift#1]
- Adjusted: -1.82 pp (95% CI -1.97 to -1.67), holding platform×country mix fixed [check:mix_shift#1]
- Causal effect: not identified (v3 全量上线,没有同时期的旧版本对照组;需要保留旧版本流量的 holdout / A/B 才能识别)

## What it means for 是否回滚 ranker v3
请求中没有给出回滚阈值;但整个区间(-1.97 到 -1.67 pp)都明显低于 0,不是噪声。下降集中在桌面端(-1.80 pp),移动端基本没变(-0.02 pp),且在 9/7 当天呈阶梯式下降,因此 v3 是首要嫌疑,但这只是时间上的吻合,不是因果证明。 [check:mix_shift#2, q7]

## Why we believe it
- Alternatives considered:
  - Mix-shift(平台/国家结构变化): ruled out by 结构效应仅 -0.01 pp,占 1%,细粒度(平台×国家)与粗粒度(平台)结论一致 [check:mix_shift#1, check:mix_shift#2] [measured]
  - 星期/季节性: ruled out by 两周都是完整的周一至周日;9/7 前 7 天桌面端 CTR 稳定在 0.356–0.364,9/7 起整体跳到 0.327–0.333,是阶梯而非渐变 [q7] [measured]
  - 数据完整性/日志变化: ruled out by 两周每天都有数据,搜索量基本持平(每日约 9.6–10.3 万) [q3] [measured]
  - v3 导致下降(PM 的假设): not ruled out; 时间与幅度吻合且集中在桌面端,但所有流量同日切换,无对照;需要 v2 holdout 或桌面端 A/B [q6, q7] [inferred]
  - 同日其他变更(桌面端专属的前端/埋点改动): not ruled out; release_log 只有一条记录,但这不能证明没有其他改动,需向桌面端团队确认 [q2] [inferred]
- Checks run:
  - mix_shift(平台×国家): pass 结构效应 -0.01 pp,分群内 -1.82 pp [check:mix_shift#1]
  - mix_shift(平台): pass 与细粒度一致 [check:mix_shift#2]
  - completeness: could not run 只有两个周期,不足 3 个历史周期 [check:completeness#2]
  - srm: skipped 不是随机实验
  - fanout: skipped 没有做 join

## Caveats, and what would change the answer
- 前后对比只有一周对一周,没有对照;若桌面端同日有其他改动,归因给 v3 会偏大。向桌面端团队确认并看 v3 的 holdout 数据即可判定。
- 区间假设各次搜索相互独立,同一用户的重复搜索会使真实区间更宽。
- 只有 CTR 一个指标;v3 对下游(转化、留存)的影响未评估。
- 下降几乎全在桌面端而移动端为零,这一点也值得排查是否是 v3 在桌面端的特定问题或桌面端埋点问题。

## Provenance
- Metric: CTR = sum(clicks)/sum(searches),表 search_daily,按日汇总后按周合并,来自 stated here [guess](未找到 metrics.json)
- Data: search_daily, release_log, through 2026-09-13
- Reconciled: not done (没有可对照的看板或其他来源)
- Queries and checks: .ds-queries.log, .ds-checks.log
- Verified: verify_readout: pass (33 numbers on 10 lines; 4 queries, 3 checks, 0 given)
- Verified: ds-verify: pass (0 fail, 0 could not verify, 0 warn, 19 pass)