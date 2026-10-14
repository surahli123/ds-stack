## Answer
Headline: -1.82 pp (95% 区间 -1.97 至 -1.67) [check:mix_shift#1]
整体 CTR 从 30.44% 降到 28.61%,几乎全部是各细分内部的下降(而非流量结构变化);这个数是"若 v3 上线是同期唯一变化"的假设下归因于 v3 的上限估计 [check:mix_shift#1]
- Observed: -1.83 pp (95% 区间 -1.98 至 -1.68) [check:mix_shift#1]
- Adjusted: -1.82 pp (95% 区间 -1.97 至 -1.67), holding 平台×国家 流量结构 fixed [check:mix_shift#1]
- Causal effect: not identified (v3 全量同日上线,没有同期旧版对照;需要随机 holdout 或分流实验)

## What it means for 是否回滚 v3
下降集中在桌面端(桌面 -1.80 pp,移动端仅 -0.02 pp)[check:mix_shift#2],区间 -1.97 至 -1.67 pp 全部远大于噪声下限 0.15 pp [check:mix_shift#1],所以下降是真实的;但因果未识别,该区间不能直接当作 v3 的效应。回滚与否的最小阈值未给出,建议先做桌面端 holdout。

## Why we believe it
- Alternatives considered:
  - 流量结构变化 (mix-shift): ruled out,混合效应仅 -0.01 pp,占 1%,平台×国家与仅平台两个粒度结论一致 [check:mix_shift#1, check:mix_shift#2] [measured]
  - 数据不完整: ruled out,两周每天均 4 行,最后一天完整 [q2, check:completeness#1] [measured]
  - 星期/季节性: ruled out 部分,两周都是完整的周一至周日,且上线前一周每日 CTR 稳定在 30.1%–30.8%,上线当天即跳到 28.6% [q2] [inferred]
  - 日志/口径变化: 未排除,release_log 只有 v3 一条记录 [q1];下降只出现在桌面端而移动端不变,这种形态既可能是 v3 在桌面端表现差,也可能是桌面端埋点或其它同期改动 [q4] [guess]
  - PM 的说法 (v3 导致下降): ruled in 作为时间上吻合的解释,但无法证明因果,因为 ranker 与时间完全重合(前周全 v2,后周全 v3)[q4] [measured]
- Checks run:
  - completeness: pass 2026-09-13 有 4 行,为基线的 100% [check:completeness#1]
  - mix_shift: pass 整体 -1.83 pp = 内部 -1.82 pp + 结构 -0.01 pp [check:mix_shift#1]
  - mix_shift (粗粒度,平台): pass 与细粒度一致 [check:mix_shift#2]
  - fanout: skipped 没有做 join
  - srm: skipped 不是随机实验

## Caveats, and what would change the answer
- 前后对比无并行对照:同期任何其它改动(桌面端 UI、埋点、广告位)都会混入 -1.82 pp。桌面/移动分化提示要查桌面端同期变更;桌面端对 v3 做小比例 v2 holdout 可定案。
- 区间假设各次搜索独立,实际同一用户的搜索相关,真实区间会更宽。
- 只比较了一周对一周,未做更长的趋势检查。
- 没有给出回滚阈值,需要决策方给出能容忍的最大 CTR 下降。

## Provenance
- Metric: CTR = sum(clicks)/sum(searches),来自 search_daily,按周汇总;stated here [guess](无 metrics.json)
- Data: search_daily, release_log, through 2026-09-13
- Reconciled: not done (没有可对照的仪表盘或其它来源)
- Queries and checks: .ds-queries.log, .ds-checks.log
- Verified: verify_readout: pass (30 numbers on 10 lines; 3 queries, 3 checks, 0 given)