```
## Answer
Headline: 约 0 个百分点(−0.00 pp,95% 区间 −0.15 至 +0.15)——但这是"调整后"的数字,不是因果结论
CTR 周环比从 30.42% 降到 28.32%,下降 2.10 个百分点,几乎全部来自流量结构向移动端倾斜(移动端 CTR 本来就低);各细分内部的 CTR 基本没变。
- Observed: −2.10 pp (−2.25 至 −1.95) [measured]
- Adjusted: −0.00 pp (−0.15 至 +0.15),固定平台×国家四个细分的流量结构不变 [measured]。结构效应 −2.09 pp,占 99.9%。
- Causal effect: not identified(v2 在 9/28 同时 100% 上线,没有同期 v1 对照组或 A/B 分流;需要一个保留 v1 的 holdout,或能解释移动端占比上升原因的独立证据)

## What it means for 是否回滚 v2
调整后的 v2 效应区间(±0.15 pp)远小于观测到的 2.10 pp 下降,在这些细分内部看不到 v2 拖累 CTR 的证据。这不能证明 v2 无害,但"CTR 下降 2.1 pp"本身不构成回滚理由。检查工具设定的最小有意义变化为 0.1 pp,区间上限略超出该值,所以小幅(约 0.1–0.15 pp)的影响仍无法排除。

## Why we believe it
- Alternatives considered:
  - 流量结构变化(桌面→移动)解释下降:支持。mix_shift 显示结构效应 −2.09 pp,桌面占比从约 60% 降到约 45% [measured]
  - v2 降低了细分内 CTR:基本排除。四个细分的 CTR 变化均在 ±0.02 pp 以内 [measured]
  - 移动端占比上升是 v2 造成的:无法判断。这需要流量来源数据,表里没有 [guess]
  - 数据不完整造成假象:排除。见下方 completeness 检查 [measured]
- Checks run:
  - mix_shift: flag,结构主导(占 100%),整体 −2.10 pp = 细分内 −0.00 pp + 结构 −2.09 pp
  - completeness: pass,10/04 有 4 行,为近几日中位数的 100%
  - srm: skipped,没有实验分流,v2 是全量上线
  - fanout: skipped,没有做表连接

## Caveats, and what would change the answer
- 只有两周的汇总数据,前后对比与上线时间完全重合,其他同期变化(营销投放、移动端版本、季节性)无法分离。
- 平台×国家以内可能还有未观察到的结构变化(如查询类型)。
- 区间假设各单元独立,实际可能偏窄。
- 若 v2 本身改变了平台构成(如移动端体验改善导致移动搜索增多),则调整会掩盖这一间接效应。

## Provenance
- Metric: CTR = clicks / searches,按周汇总,来源为 stated here [guess](目录中没有 metrics.json)
- Data: search_daily(56 行,4 个细分×14 天)、release_log,截至 2026-10-04(完整)
- Reconciled: not done(没有仪表盘或其他来源可对照)
- Queries and checks: 查询为本次会话内联运行;检查记录在工作目录的 .ds-checks.log
```