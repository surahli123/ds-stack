## Answer
Headline: can't tell（v2 的因果效应无法识别；按平台×国家调整后，v2 前后的变化约为 −0.00 个百分点）
整体 CTR 从 30.42% 降到 28.32%，周环比 −2.10 个百分点。几乎全部来自流量结构变化：移动端占比上升，而移动端 CTR 本来就低。各细分内部的 CTR 基本没动。

- Observed: −2.10 pp (−2.25 到 −1.95) [measured]
- Adjusted: −0.00 pp (−0.15 到 +0.15)，固定平台×国家的流量结构 [measured]。区间由 mix_shift 检查给出，假设各行相互独立。
- Causal effect: not identified。v2 在 100% 流量上线，没有对照组或保留组。上线当天移动端占比也同步跳升，两件事无法分开。要识别效应，需要 v2 与 v1 的并行实验或保留组，或能解释移动端流量跳升的原因。

## What it means for 回滚决策
按细分调整后，v2 的区间是 ±0.15 pp，排除了「v2 让 CTR 下降约 2 pp」。能改变决策的最小变化，mix_shift 检查默认取 0.1 pp。区间比这个阈值宽，所以 v2 带来 0.1 到 0.15 pp 以内的小幅下降，现在无法排除。没有证据支持因为这 2.1 pp 的下降而回滚。但这是前后对比，不是因果结论。

## Why we believe it
- Alternatives considered:
  - v2 降低了点击质量：在各细分内基本排除。四个细分的 CTR 前后差都在 ±0.02 pp 以内 [measured]。
  - 流量结构变化（移动端占比）：成立，解释约 99.9% 的降幅。移动端搜索占比从 40.1% 升到 55.1% [measured]。
  - 移动端流量跳升本身由 v2 引起：无法排除，数据里没有原因 [guess]。
  - 数据缺失或未加载完整造成的假象：已排除，两周每天都是 4 行，且 10-04 数据完整 [measured]。
  - 上线当天的其他改动：release_log 只有一条记录，无法排除未记录的改动 [guess]。
- Checks run:
  - mix_shift: flag。混合效应 −2.09 pp，细分内效应 −0.00 pp，混合占比 100% [check:mix_shift#1]。
  - completeness: pass。10-04 有 4 行，是近期日均行数的 100% [check:completeness#1]。
  - srm: skipped，这不是随机实验，没有分流比例可查。
  - fanout: skipped，没有做表连接。

## Caveats, and what would change the answer
- 只有两个一周的窗口，没有更长的基线，也没有排除周内波动之外的季节性。
- 调整只覆盖平台×国家。更细的维度（查询类型、用户群）如果也有结构变化，没有被控制。
- 如果移动端占比上升是 v2 导致的（例如 v2 改了移动端的入口），那么整体下降仍可能与 v2 有关。需要问清楚这一周移动端流量为什么增加。
- 数据在聚合层，没有会话级数据，区间假设各行独立，实际可能偏窄。

## Provenance
- Metric: CTR = clicks / searches，来自 stated here [guess]。目录里没有 metrics.json。
- Data: search_daily（按平台、国家、ranker 的日汇总）、release_log，截至 2026-10-04。
- Reconciled: not done（没有可对照的仪表盘或其他数据源）。
- Queries and checks: 检查结果记录在 .ds-checks.log（mix_shift#1、completeness#1）。聚合查询是在命令行里直接运行的，没有单独记录查询编号。