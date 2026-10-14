```
## Answer
Headline: can't tell
整体 CTR 周环比下降 1.83 个百分点,而且这个下降几乎全部发生在桌面端,但 v3 是否是原因无法从这份数据确定。

- Observed: -1.83 pp (95% 区间 -1.98 ~ -1.68),30.44% → 28.61% [measured]
- Adjusted: -1.82 pp (-1.97 ~ -1.67),固定平台×国家的流量构成不变 [measured]
- Causal effect: not identified(v3 在 9/7 对 100% 流量上线,没有同期的 v2 对照组或随机分流;排序器版本与时间完全重合。需要灰度/A-B 实验、holdout,或排除同日其他变更后再判断)

## What it means for 是否回滚 v3
观察到的下降幅度约 1.7~2.0 pp,远大于日常噪声(约 0.15 pp),所以下降是真实的。但这个区间描述的是"前后变化",不是"v3 的效果",不能单凭它决定回滚。建议做一个小比例 v2 holdout 来直接确认。

## Why we believe it
- Alternatives considered:
  - 流量构成变化(平台/国家占比):已排除。构成效应仅 -0.01 pp,占变化的 1% [measured]
  - v3 本身导致下降:无法排除。下降精确出现在 9/7 当天(9/6 为 30.4%,9/7 为 28.6%),时间吻合,且之后一周稳定在较低水平 [measured];但这与同日其他变化的解释同样一致 [inferred]
  - 同日其他变更/埋点变化:无法排除。release_log 只记录了 v3 一条,不能证明当天没有别的改动 [inferred]
  - 桌面端专属问题(如 v3 在桌面端表现差,或桌面端点击埋点出问题):可能。桌面端美国 -3.11 pp (±0.28)、桌面端其他国家 -2.87 pp (±0.30),移动端几乎无变化(美国 -0.03 pp、其他 -0.04 pp,区间均包含 0)[measured]。如果是排序质量问题,通常不会只影响桌面端,这点值得查 [guess]
  - 季节性/周期:未能检验,只有两周数据,没有往年或更长历史 [guess]
- Checks run:
  - mix_shift: pass 整体 -1.83 pp = 段内 -1.82 pp + 构成 -0.01 pp
  - completeness: could not run 需要至少 3 个更早的周期,只有 2 周数据;但两周每天都是 4 个分段,日搜索量稳定在约 9.6 万~10.3 万,无明显缺失 [measured]
  - srm: skipped 没有实验分流,不适用
  - fanout: skipped 没有做连表

## Caveats, and what would change the answer
- 只有前后各一周,且是单一时间点切换,没有对照,不能把变化归因给 v3。
- 区间假设各次搜索相互独立,实际同一用户的重复搜索会让真实区间更宽。
- 若发现桌面端点击埋点或 UI 在 9/7 有改动,结论会改变;若 v2 holdout 显示 v2 同期 CTR 也下降,则 v3 影响接近 0。
- 建议先查桌面端的 9/7 变更和点击日志,再决定回滚。

## Provenance
- Metric: CTR = clicks / searches,按周汇总,stated here [guess](没有 metrics.json)
- Data: search_daily、release_log,覆盖 2026-08-31 至 2026-09-13(两个完整周)
- Reconciled: not done(没有可对照的仪表盘或其他数据源)
- Queries and checks: 查询为临时内联 Python/SQLite,未单独记录;检查结果记录在 .ds-checks.log(mix_shift#1、completeness#1)
```