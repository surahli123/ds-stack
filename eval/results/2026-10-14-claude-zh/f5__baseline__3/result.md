## Answer
Headline: can't tell

两组 CTR 相差 +1.20 个百分点,但实验分流有严重的样本比例失衡(SRM),所以不能把这个差值当作 ranker_boost 的效果。

- Observed: +1.20 pp (95% 区间 +1.13 至 +1.27 pp)。对照组 30.00%,实验组 31.20%。区间按"搜索次数"做二项近似算出,没考虑同一用户的多次搜索相关,实际区间会更宽。[measured]
- Adjusted: not computed (表里只有按日、按组汇总的数据,没有用户级或分群字段,没法控制任何协变量)
- Causal effect: not identified (需要先查清并修好分流失衡的原因,再用用户级数据重新分析或重跑实验)

## What it means for 上线决策
我们没有设定最小可上线提升幅度,所以只能说:+1.13 至 +1.27 pp 的区间虽然完全高于 0,但它没算入分流偏差,不能据此上线。先查明 SRM,在此之前建议暂缓决策。[inferred]

## Why we believe it
- Alternatives considered:
  - 分流或曝光记录有偏,导致实验组少了约 2.4 万用户,而且丢掉的可能是特定类型的用户:无法排除,是最可能的解释。实验组 475,990 用户,对照组 499,930,比例为 48.8% 比 51.2%,与 50/50 的偏差约为 24 个标准差(z≈24)。[measured]
  - 实验组用户流失是由新排序造成的(例如出错、加载失败):无法排除,需要查日志。[guess]
  - 单纯的随机波动:已排除,因为 z≈24 不可能由随机性产生。[measured]
  - 日期或星期效应:基本排除。每天的两组差距稳定在约 1.1 至 1.3 pp,每个用户每天都是恰好 6 次搜索。[measured]
- Checks run:
  - 样本比例(SRM):fail,见上。
  - 逐日一致性:pass,28 行数据中每天实验组 CTR 都高于对照组。
  - 数据完整性:flag,每天每组的 searches/users 恰好等于 6.0,而且数值高度规整,不像真实的原始日志,需要确认数据口径。
  - 用户级聚类标准误、新奇效应、分群分析:could not run,表中只有按日汇总。

## Caveats, and what would change the answer
- 如果 SRM 的原因查清,并且丢失的用户与结果无关,那么 +1.2 pp 可能基本成立。
- 如果丢失的用户集中在低点击人群,真实提升可能小于 1.2 pp,甚至是零。
- 需要用户级的分流日志才能算出带聚类的区间,并检查分流是否独立于用户特征。
- 实验期间有 14 天,没有 metrics.json 来确认 CTR 的官方定义。

## Provenance
- Metric: CTR = clicks / searches,按两组实验期总量汇总,来自 stated here [guess]。没有找到 metrics.json。
- Data: experiment_daily(28 行,2026-09-17 至 2026-09-30,全部完整)
- Reconciled: not done (没有可对照的看板或其他数据源)
- Queries and checks: 查询是直接在命令行用 Python 内联运行的,没有保存成脚本或日志文件。