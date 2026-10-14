## Answer
Headline: can't tell

处理组的 CTR 看起来高了约 1.2 个百分点,但分流比例严重偏离 50/50(SRM 检验未通过),所以这个差异不能当作 ranker_boost 的因果效应。

- Observed: +1.20 个百分点 (95% 区间 +1.13 ~ +1.27),对照组 30.0%,处理组 31.2%。[measured] 区间按搜索次数独立计算,没有考虑同一用户的聚类,实际会偏窄。
- Adjusted: not computed(表里只有按日、按组的汇总,没有用户或分群维度,无法在 SRM 的成因上做调整)
- Causal effect: not identified(需要查明分流不均的原因,并拿到用户级数据,或在分流修复后重跑实验)

## What it means for 上线决策
观察到的 +1.2 个百分点区间很窄,但 SRM 说明两组用户不具可比性,偏差可能比这个区间大得多。在查明原因前,这个数不应作为上线依据。

## Why we believe it
- Alternatives considered:
  - 真实的排序提升效应:无法排除,也无法确认,因为 SRM 失败,两组不可比 [measured]
  - 随机分流本身有偏(处理组流失了约 4.8% 的用户):可能。用户数为 499,930 对 475,990,处理组占比 48.77%,而计划是 50% [measured]。可能与日志丢失、触发条件或机器人过滤有关,但成因是 [guess]。
  - 人均搜索量差异造成假象:排除。两组每用户每天都是 6.0 次搜索 [measured]
  - 某几天的异常造成假象:基本排除。14 天每天两组都有数据,每天的趋势一致 [measured]
- Checks run:
  - srm: fail。chi2=587.3,p≈1e-130,观察占比 51.2% 对 48.8% [check:srm#1]
  - completeness: could not run。该检查要求至少 3 个更早的同期数据,我只传了 2 天。人工核对:9/17~9/30 每天两组各有 1 行,没有缺失日 [measured]
  - fanout: skipped。没有做任何 join
  - mix_shift: skipped。表里没有分群维度

## Caveats, and what would change the answer
- 如果能查明处理组少掉的用户是随机丢失(例如日志问题),并与结果无关,+1.2 个百分点才可能被采信。
- "users" 是按日汇总值,不是去重用户数。
- 没有用户级数据,无法做聚类标准误。
- 没有 metrics.json,CTR 的定义是我假设的。

## Provenance
- Metric: CTR = clicks / searches,stated here [guess]
- Data: experiment_daily,2026-09-17 至 2026-09-30,14 天完整
- Reconciled: not done(没有可对照的看板或其他数据源)
- Queries and checks: 检查记录在 .ds-checks.log(srm#1、completeness#1);查询在会话中直接运行,没有单独保存