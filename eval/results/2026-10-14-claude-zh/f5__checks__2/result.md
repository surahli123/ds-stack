## Answer
Headline: can't tell
处理组的 CTR 在原始数据上高出 1.20 个百分点,但分流比例严重偏离 50/50(SRM 检验失败),所以这个差异不能当作因果提升。
- Observed: +1.20 个百分点 (95% 区间 +1.13 到 +1.27);对照组 30.00%,处理组 31.20%。区间是对 clicks/searches 做两比例 z 检验得到的,把每次搜索当作独立样本,所以偏窄。[measured]
- Adjusted: not computed (没有用户层或分群数据,无法在分流失衡的前提下做调整)
- Causal effect: not identified (需要先查清处理组少约 2.4 万用户的原因,修复后重跑,或拿到分配日志做用户层分析)

## What it means for the launch decision
我们没有给出可用的提升数字,所以不应拿 +1.2 个百分点去判断是否上线。我也不知道最小可接受的提升是多少,要等分流问题查清、因果估计出来之后,才能拿区间跟这个门槛比较。

## Why we believe it
- Alternatives considered:
  - 真实的排序器效果:没有被排除。分流失衡之外,数据本身与它一致。[inferred]
  - 处理组流失或被过滤掉的用户本来点击率偏低,留下来的是更爱点击的人:不能排除,而且方向恰好会抬高处理组 CTR。[inferred]
  - 每用户搜索量不同导致的差异:排除。两组都是 6.0 次搜索/用户。[measured]
  - 某几天的异常:基本排除。28 行日数据里,处理组每天都比对照组高约 1.1 到 1.3 个百分点。[measured]
- Checks run:
  - srm:fail。用户数 对照 499,930 / 处理 475,990,占比 51.23% 对 48.77%,chi2 587.3,p≈1e-130。(第一次我误输入了错误的数字,结果 srm#1 作废,以 srm#2 为准。)
  - completeness:could not run。表里只有 2 个臂 × 14 天,没有足够的往期同星期历史。日期 09-17 到 09-30 每天都有两个臂的行,但无法做更严格的验证。
  - mix_shift:skipped。表里没有分群维度。
  - fanout:skipped。没有做任何 join。

## Caveats, and what would change the answer
- 处理组每天都少约 1,700 用户,且几乎恒定,像是系统性原因(例如分配、日志或曝光上报问题),不像随机波动。[inferred]
- 如果能确认缺失的用户是随机丢失、与点击行为无关,+1.2 个百分点才可信。
- CTR 的定义是我的假设:clicks/searches。
- 区间没有处理同一用户多次搜索的相关性,真实区间会更宽。

## Provenance
- Metric: CTR = clicks / searches,汇总整个实验期,来源 stated here [guess];没有找到 metrics.json
- Data: experiment_daily,2026-09-17 到 2026-09-30(14 天,每天 2 个臂)
- Reconciled: not done (没有可对照的仪表盘或其他数据源)
- Queries and checks: 查询是在命令行里直接执行的,没有单独的日志文件。检查结果记录在 `.ds-checks.log`(srm#1 作废、srm#2、completeness#1)。