## Answer
Headline: can't tell
treatment 的原始 CTR 比 control 高 1.20 pp,但两组用户数分配比例严重偏离 50/50(treatment 仅占 48.8%),样本比例失衡(SRM)检验失败,两组不可比,因此不能把这个差异当作提升量。 [q2, check:srm#1]
- Observed: +1.20 pp (95% CI +1.13 to +1.27 pp);CTR = clicks/searches,treatment 31.2% vs control 30.0% [q2, q4]
- Adjusted: not computed (数据中没有可用于分层的维度,只有按天、按组的汇总;且 SRM 失败的原因未知,分层也无法修复)
- Causal effect: not identified (需要查明分流不均的原因并修复后重跑,或证明被丢失的用户与结果无关)

## What it means for 上线决策
原始区间 +1.13 到 +1.27 pp 远大于零,但 SRM 失败意味着该区间不可信,不能据此判断是否上线;在找到分流偏差原因之前不应做决定。 [q4, check:srm#1]

## Why we believe it
- Alternatives considered:
  - 分流/日志缺陷导致的选择偏差(treatment 少约 2.4 万用户,占 4.8%):ruled in,SRM 检验 p≈0(用户数份额 0.5123 vs 0.4877) [q2, check:srm#1] [measured]
  - 搜索量份额与用户份额相同(均为 0.5123 / 0.4877),说明每用户搜索量一致,缺失的是整批用户而非部分记录 [check:srm#2] [measured]
  - 数据不完整/某天缺失:ruled out,14 天均有两行,最后一天为完整的 100% [q3, check:completeness#1] [measured]
  - 星期效应/季节性:ruled out(作为差异来源),每一天 treatment CTR 都高于 control,两组日期相同且各覆盖完整 14 天 [q3] [inferred]
  - 提升确由 ranker 改动带来(请求方的假设):not identified,随机化已被 SRM 质疑 [check:srm#1] [inferred]
  - 分段结构变化(mix-shift):skipped,表中无平台/国家等分段 [q1] [measured]
- Checks run:
  - srm(用户数): fail 份额 0.5123 vs 0.4877,p≈1e-130 [check:srm#1]
  - srm(搜索数): fail 份额相同,p≈0 [check:srm#2]
  - completeness: pass 2026-09-30 有 2 行,为近期中位数的 100% [check:completeness#1]
  - mix_shift: skipped 没有分段维度
  - fanout: skipped 未做 join

## Caveats, and what would change the answer
- 未找到 metrics.json,CTR 按 clicks/searches 定义,是猜测;若官方定义是按用户去重点击,数字会不同。
- 只有日汇总,没有用户级数据,无法诊断是谁丢了;需要分流日志和曝光日志。
- 若查明缺失用户是随机的(如日志丢失),可重新评估;若与结果相关(如低意图用户被过滤),真实提升可能更小或为负。
- 区间只考虑搜索级别独立性,未考虑同一用户内的相关性,实际区间会更宽。

## Provenance
- Metric: CTR = sum(clicks)/sum(searches),按 arm,2026-09-17 至 09-30,来自 stated here [guess]
- Data: experiment_daily (experiment='ranker_boost'),through 2026-09-30
- Reconciled: not done (没有仪表盘或其他来源可对照)
- Queries and checks: .ds-queries.log, .ds-checks.log
- Verified: verify_readout: pass (28 numbers on 10 lines; 4 queries, 3 checks, 0 given)