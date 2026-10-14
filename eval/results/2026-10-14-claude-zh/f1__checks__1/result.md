## Answer
Headline: can't tell(v2 的因果效应无法识别;但整体 CTR 的下降几乎全部来自流量结构变化)

整体 CTR 从 30.42% 降到 28.32%,周环比 −2.10 个百分点;在每个平台×国家分群内部,CTR 基本没变,下降来自流量向低 CTR 的移动端转移。

- Observed: −2.10 pp (95% 区间 −2.25 至 −1.95) [measured]
- Adjusted: −0.002 pp (95% 区间 −0.15 至 +0.15),固定平台×国家的流量结构不变(分群内变化) [measured]
- Causal effect: not identified(v2 是 100% 全量上线,没有同期对照组或灰度分流;要识别需要 v1/v2 的随机 holdout,或上线前后都有未受影响的对照分群)

## What it means for 是否回滚 v2
分群内的 v2 相关变化区间(−0.15 到 +0.15 pp)很窄,没有证据显示 v2 拉低了 CTR。这个区间只是观测前后比较,不是因果估计。我没有定义"足以回滚的最小变化",所以只能说:如果团队认为 0.15 pp 以上的下降就值得回滚,这些数据没有显示达到那个量级。当前数据不支持以"CTR 下降"为由回滚。

## Why we believe it
- Alternatives considered:
  - 流量结构变化(移动端占比上升):ruled in。移动端搜索占比从 40.1% 升到 55.1%,而移动端 CTR(约 21–23%)远低于桌面端(约 35–37%);结构效应 −2.09 pp,占总变化的 99.9% [measured]
  - 移动端占比上升的原因:未查明。可能是 v2 改变了入口或流量分配,也可能是自然的周变化或活动 [guess]
  - v2 真的降低了 CTR:无法排除也无法证实。分群内变化约为 0,但 v2 也可能通过改变流量结构间接影响整体 CTR [inferred]
  - 数据未加载完整:ruled out。每天 4 行,最后一天 10-04 完整 [measured]
  - 同期其他变更:release_log 里只有 v2 一条记录,但日志可能不完整 [inferred]
- Checks run:
  - mix_shift:flag。结构效应 −2.09 pp,分群内 −0.002 pp,结构占比约 100%
  - completeness:pass。10-04 的行数为基线的 100%
  - srm:skipped。这不是随机实验,v1/v2 是按周切换的,50/50 的分配假设不适用。表面上的 p=0.52 没有意义
  - fanout:skipped。没有做 join

## Caveats, and what would change the answer
- 只有两周数据,v2 与"第几周"完全重合,无法区分 v2 和周效应。
- 区间的标准误假设各单元独立,实际日度数据可能有相关性,真实区间可能更宽。
- 只按平台×国家分群;更细的分群(查询类型、用户群)里可能仍有 v2 的影响。
- 要得到因果结论,需要 v1 的随机 holdout,或用 v2 的历史灰度数据。
- 需要查明移动端占比上升的原因。如果它由 v2 引起(例如 v2 改变了入口或展示),结论会变。

## Provenance
- Metric: CTR = sum(clicks)/sum(searches),在 stated here 中定义 [guess](没有 metrics.json)
- Data: search_daily、release_log,覆盖 2026-09-21 至 2026-10-04(完整)
- Reconciled: not done(没有可对照的仪表盘或其他数据源)
- Queries and checks: 检查结果记录在工作目录的 .ds-checks.log(mix_shift#1、completeness#1、srm#1);查询是直接用 Python 对 sqlite 做的聚合,没有单独记录日志