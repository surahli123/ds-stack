## Answer
Headline: can't tell
实验两组的用户分配比例严重偏离 50/50,两组不可比,原始 CTR 差异 +1.20 pp 不能当作 ranker_boost 的效果 [check:srm#1, q5]。
- Observed: +1.20 pp (+1.13 到 +1.27 pp;按 q5 的搜索数与点击数用两比例公式算出) [q5]
- Adjusted: not computed (没有分群字段可用,表里只有按天、按组的汇总,且 SRM 失败的原因未知)
- Causal effect: not identified (需要查明 SRM 的原因并修复分流/日志后重跑,或用分流前的用户属性核对两组是否同质)

## What it means for 上线决策
原始区间 +1.13 到 +1.27 pp 虽然全为正,但 SRM 失败(p 约 1e-129)说明分配过程有问题,区间只反映抽样误差,不含分配偏差,因此不能据此决定上线 [check:srm#1, q5]。

## Why we believe it
- Alternatives considered:
  - 分流/日志缺陷(某组有用户被丢弃或被过滤):ruled in,对照组用户 499930、实验组 475990,占比 51.2% 对 48.8% [q2, check:srm#1] [measured]
  - 实验组 CTR 更高是因为用户组成不同(选择偏差):无法排除,因为 SRM 暗示进入两组的用户不是随机的,且没有分群数据可检验 [check:srm#1] [inferred]
  - 星期效应/季节性:基本排除,两组每天都同时观测,每天实验组 CTR 都高于对照组约 1.2 pp [q4] [measured]
  - 数据不完整:ruled out,14 天都有 2 行,最后一天与前几天持平 [check:completeness#1, q3] [measured]
  - 搜索量差异驱动 CTR:ruled out,两组人均搜索数都是 6.0 [q5] [measured]
  - ranker_boost 本身提升了 CTR(提出者的假设):未被证伪但也未被证实,在 SRM 解决前无法判断 [check:srm#1] [inferred]
- Checks run:
  - srm: fail 观测占比 0.512265/0.487735 对期望 0.5/0.5,chi2 587.26 [check:srm#1]
  - completeness: pass 2026-09-30 有 2 行,为近期中位数的 100% [check:completeness#1]
  - mix_shift: skipped 没有分群维度可用,表中只有分组汇总
  - fanout: skipped 没有做任何 join

## Caveats, and what would change the answer
- SRM 原因未明:若能确认缺失的约 2.4 万用户与 CTR 无关(例如纯日志丢失),原始差异才有可能解读为效果。
- CTR 定义是我假设的,若口径是"有点击的用户占比"则数字会不同。
- 只有日汇总,无法做用户级方差或分群分析。

## Provenance
- Metric: CTR = 点击数 / 搜索数,来自 experiment_daily 汇总,stated here [guess](未找到 metrics.json,DS_OVERLAY_DIR 未设置)
- Data: experiment_daily,到 2026-09-30
- Reconciled: not done (没有可对照的看板或其他来源)
- Queries and checks: .ds-queries.log 和 .ds-checks.log
- Verified: verify_readout: pass (25 numbers on 9 lines; 4 queries, 2 checks, 0 given)