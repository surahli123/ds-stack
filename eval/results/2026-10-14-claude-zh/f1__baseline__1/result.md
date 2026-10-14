## Answer
Headline: 在固定平台×国家构成后,v2 的影响约为 -0.01 个百分点(-0.16 到 +0.15 pp),与零无法区分。
整体 CTR 从 30.42% 降到 28.32%(-2.10 pp),但这几乎全部是流量结构变化造成的:移动端占比从 40% 升到 55%,而移动端 CTR 本来就低。每个细分内部的 CTR 基本没动。
- Observed: -2.10 pp (95% 区间 -2.25 到 -1.95)(measured)
- Adjusted: -0.01 pp (95% 区间 -0.16 到 +0.15),holding 平台×国家的流量构成固定在上周水平(measured)
- Causal effect: not identified(v2 是 100% 全量上线,没有同期对照组;需要 v1/v2 的 A/B 流量,或能解释移动端占比跳升的信息)

## What it means for 是否回滚 v2
排名质量方面,没有证据表明 v2 降低了 CTR;调整后的区间上限是 +0.15 pp,下限是 -0.16 pp。因此"整体 CTR 下降 2.1 pp"不应作为回滚理由。需要先弄清移动端流量为什么在同一天暴增。

## Why we believe it
- Alternatives considered:
  - v2 降低了点击质量:基本排除,四个细分的 CTR 变化都在 ±0.1 pp 以内(桌面美国 37.07%→37.07%,移动美国 22.66%→22.71%,等等)[measured]
  - 流量构成变化(辛普森式结构效应):成立,移动端份额 40.1%→54.9%,解释了约 -2.09 pp [measured]
  - 移动端流量增长本身由 v2 引起(例如新入口或改变了搜索行为):无法排除,没有对照组 [guess]
  - 同期的其他发布或季节性因素:发布日志只有 v2 一条;只有两周数据,无法检验季节性 [inferred]
- Checks run:
  - 日度趋势:pass,9/28 当天出现阶梯式下降,上周内部稳定(30.1%-30.8%),本周稳定(28.1%-28.6%)
  - 细分内 CTR 对比:pass,四个细分均无变化
  - 标准化分解及二项分布置信区间:pass,见上
  - 对照组/A-B:could not run,v2 同日全量上线,没有 v1 流量
  - 搜索量总数:pass,两周约 70 万次,几乎相等,说明总量没变,变的是平台构成

## Caveats, and what would change the answer
- 只有两周数据,区间只反映抽样噪声,不反映周间差异。
- 前后对比无法把 v2 与同日发生的其他变化分开。
- 如果移动端流量的增长是 v2 带来的(例如召回了更多低意图搜索),那么 v2 间接影响整体 CTR,这需要进一步调查。
- 区间只能排除各细分内 CTR 变化大于约 0.16 pp 的情况。

## Provenance
- Metric: CTR = clicks / searches,汇总后相除 [stated here, guess],未找到 metrics.json
- Data: search_daily、release_log,覆盖 2026-09-21 至 2026-10-04(两周均完整)
- Reconciled: not done(没有仪表盘或其他来源可比对)
- Queries and checks: 在本次会话中用 python3 + sqlite3 内联运行,未保存为文件