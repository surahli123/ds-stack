## Answer
Headline: -1.82 pp (95% CI -1.97 至 -1.67) [check:mix_shift#1]
总体 CTR 从 30.44% 降到 28.61%,几乎全部是组内下降(构成变化仅 -0.01 pp),且集中在 desktop(-1.80 pp);该数字假设 v3 上线时流量构成未变,且同期没有其他因素 [check:mix_shift#1, check:mix_shift#2]
- Observed: -1.83 pp (95% CI -1.98 至 -1.68) [check:mix_shift#1]
- Adjusted: -1.82 pp (95% CI -1.97 至 -1.67), holding platform × country 构成固定 [check:mix_shift#1]
- Causal effect: not identified (v3 是全量上线,没有同期对照组;需要随机分流的旧版 holdout,或排查 desktop 同期其他变化)

## What it means for 是否回滚 v3
区间整体在 -1.97 到 -1.67 pp,远低于 mix_shift 的最小有意义变化 0.1 pp [check:mix_shift#1],所以下降是真实的,不是噪声;但因果无法识别,是否回滚取决于 desktop 的下降是否确由 v3 引起,建议先对 desktop 做小比例 v2 holdout。 [check:mix_shift#2]

## Why we believe it
- Alternatives considered:
  - 构成变化(platform/country): ruled out,platform 粒度与 platform×country 粒度结果一致,构成效应仅 -0.01 pp,占 1% [check:mix_shift#1, check:mix_shift#2] [measured]
  - 星期/季节性: ruled out(部分),两周都是完整周一到周日,每天口径相同;逐日数据显示 09-07 起每天都低于前一周,但只有两周数据,无法排除周级季节性 [q3] [inferred]
  - 数据不完整: ruled out,每天 4 行,最后一天 100% 达到基线 [check:completeness#1] [measured]
  - 日志/口径变更: not ruled out,release_log 只有 v3 上线一条记录,未见埋点变更记录,但无法证实 [q2] [guess]
  - PM 的说法(v3 导致下降): ruled in 为相关,不能确认为因果;下降发生在 v3 上线当天,且只出现在 desktop(desktop 36.04%→33.04%,mobile 22.02%→21.98%),与 v3 同时发生 [q4] [inferred]
- Checks run:
  - completeness: pass 2026-09-13 有 4 行,为基线的 100% [check:completeness#1]
  - mix_shift: pass 总变化 -1.83 pp = 组内 -1.82 pp + 构成 -0.01 pp(platform × country) [check:mix_shift#1]
  - mix_shift: pass 粗粒度(platform)结果一致,-1.83 pp = 组内 -1.82 pp + 构成 -0.01 pp [check:mix_shift#2]
  - fanout: skipped 没有使用 join
  - srm: skipped 不是随机实验,没有分流计数

## Caveats, and what would change the answer
- 没有同时运行的对照组,不能把 -1.82 pp 全部算作 v3 的效果;一个 desktop 的 v2 holdout 或同期 desktop 变更清单可以确认。
- 只有两周数据,周级季节性无法排除;更长的历史基线可以检验。
- 区间假设各单位独立(se_assumes_independent_units),实际同一用户多次搜索会让区间偏窄。
- CTR 是代理指标;如果 v3 在 desktop 上改变了结果展示方式(如更少需要点击),点击下降未必意味着体验变差。

## Provenance
- Metric: CTR = sum(clicks) / sum(searches),表 search_daily,按周汇总,来自 stated here [guess]
- Data: search_daily, release_log, through 2026-09-13
- Reconciled: not done (没有可对照的看板或其他来源)
- Queries and checks: .ds-queries.log, .ds-checks.log
- Verified: verify_readout: pass (34 numbers on 12 lines; 3 queries, 3 checks, 0 given)