## Answer
Headline: can't tell
实验分流出现样本比例失衡(SRM),两组用户不可比,因此无法确认 treatment 是否真的提升了 CTR;原始差值为 +1.20 pp,但不能当作提升量 [q3, check:srm#1]
- Observed: +1.20 pp (95% CI +1.13 to +1.27),treatment CTR 31.20% vs control 30.00% [q3, q4](measured)
- Adjusted: not computed (表中只有按日汇总的 arm 数据,没有可用来调整的分群维度,且 SRM 的原因未知)
- Causal effect: not identified (需要查明 treatment 组少约 2.4 万用户日的原因 [q3] 并修复分流/日志后重跑,或拿到用户级分配数据做 intent-to-treat 分析)

## What it means for 上线 ranker_boost 的决策
原始区间 +1.13 到 +1.27 pp 看似远高于零,但 SRM 失败(p≈1e-129)说明该区间不能作为因果效应的依据,不应据此做上线决定 [q4, check:srm#1]。

## Why we believe it
- Alternatives considered:
  - 随机分流正常、提升是真实的: ruled out by SRM 失败,实际占比 51.23% / 48.77%,而非 50/50 [check:srm#1] [measured]
  - treatment 组丢失了低点击用户(日志丢失或曝光过滤),使 CTR 虚高: ruled in(未被排除)。两组每用户搜索数完全一致(均为 6.0),缺口是整批用户而非搜索行为差异,与此假设相符,但无法在此数据中证实 [q3] [inferred]
  - 数据不完整: ruled out by 最后一天(2026-09-30)两组均已加载,14 天每天都有 2 行 [check:completeness#1] [measured]
  - 星期效应/季节性: ruled out by 每个 arm 都覆盖同样的 14 天(完整两周),差异不来自窗口不同 [q2, q3] [inferred]
  - mix-shift: could not be tested,表中无平台、国家等分群 [guess]
- Checks run:
  - srm: fail 用户数 499930 vs 475990,chi2 587.26,p 9.86e-130 [check:srm#1]
  - completeness: pass 2026-09-30 为 2 行,等于近期中位数的 100% [check:completeness#1]
  - mix_shift: skipped 没有分群数据
  - fanout: skipped 没有做 join

## Caveats, and what would change the answer
- 先查明 treatment 少约 2.4 万用户日的原因 [q3] (分配、日志、过滤或机器人剔除);修复后重跑,方可读出提升。
- 表只有 arm×日汇总,无法做用户级方差(同一用户重复计入),上述区间按搜索次数独立计算,实际偏窄。
- 数据中没有 metrics.json,CTR 定义是我的假设;若定义为点击用户/用户,结论需重算。

## Provenance
- Metric: CTR = clicks / searches,按 arm 汇总 experiment_daily,2026-09-17 至 2026-09-30,来自 stated here [guess]
- Data: experiment_daily,through 2026-09-30
- Reconciled: not done (无仪表盘或其他来源可对照)
- Queries and checks: .ds-queries.log 与 .ds-checks.log
- Verified: verify_readout: pass (26 numbers on 10 lines; 3 queries, 2 checks, 0 given)