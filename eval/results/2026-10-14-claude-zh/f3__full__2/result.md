## Answer
Headline: -1.82 pp (95% 区间 -1.97 到 -1.67) [check:mix_shift#1]
整体 CTR 从 30.44% 降到 28.61%,几乎全部下降(-1.80 pp)来自桌面端,移动端基本持平(-0.02 pp);若 v3 上线时没有改变流量构成、也没有其他同期变化,则这是与 v3 同时出现的下降幅度 [check:mix_shift#1, check:mix_shift#2]
- Observed: -1.83 pp (95% 区间 -1.98 到 -1.68) [check:mix_shift#1]
- Adjusted: -1.82 pp (95% 区间 -1.97 到 -1.67), holding 平台×国家构成固定 [check:mix_shift#1]
- Causal effect: not identified (v3 同时全量上线,没有对照组;需要保留一部分 v2 流量的 holdout/AB,或桌面端日志与追踪的核查)

## What it means for 是否回滚 v3
构成变化(mix)仅解释 -0.01 pp,区间下限 -1.67 pp 远大于噪声下限 0.15 pp,所以这不是流量构成或随机波动造成的 [check:mix_shift#1]。请求中没有给出回滚阈值;区间整体为负,若可接受的最大损失小于 1.67 pp 则下降已超过该水平,但因果尚未识别,建议先做桌面端的 v2 对照再决定 [check:mix_shift#1]。

## Why we believe it
- Alternatives considered:
  - 平台/国家构成变化 (mix-shift): ruled out by 构成效应仅 -0.01 pp,占比 1%,平台粒度与平台×国家粒度结论一致 [check:mix_shift#1, check:mix_shift#2] [measured]
  - 数据不完整: ruled out by 14 天每天都有 4 行(2×2 的平台×国家),最后一天与前 7 天中位数相比达 100% [check:completeness#1, q3] [measured]
  - 星期效应/季节性: ruled out by 两周均为完整的周一至周日,窗口长度相同 [q3] [inferred]
  - 同期的其他发布: ruled out by release_log 只有 v3 一条记录,但日志可能不完整 [q2] [inferred]
  - v3 导致下降 (PM 的说法): 与数据一致但未被证明;下降集中在桌面端(-3.0 pp:36.04% 到 33.04%),移动端 22.02% 到 21.98%,说明要么 v3 只在桌面端有害,要么桌面端同时发生了追踪/日志变化 [q6, check:mix_shift#2] [inferred]
  - 日志或指标定义变化: not ruled out,只有两周的数据,无法核实桌面端的埋点 [guess]
- Checks run:
  - mix_shift: pass 平台×国家粒度,整体 -1.83 pp = 组内 -1.82 pp + 构成 -0.01 pp [check:mix_shift#1]
  - mix_shift: pass 平台粒度(较粗),与上一结果一致 [check:mix_shift#2]
  - completeness: pass 最后一天 4 行,为基线的 100% [check:completeness#1]
  - fanout: skipped 没有做 join
  - srm: skipped 不是随机实验

## Caveats, and what would change the answer
- 上线前后完全重合 (v2 全在第一周,v3 全在第二周),v3 与"那一周"无法分开;一个桌面端 v2 holdout 即可识别
- 下降只出现在桌面端,需确认桌面端点击埋点或客户端版本没有同期变化
- 区间假设单位独立 (se_assumes_independent_units),同一用户的重复搜索会使真实区间更宽
- 只有 2 周数据,无更早的基线来估计周间自然波动

## Provenance
- Metric: CTR = sum(clicks)/sum(searches),按周汇总,来源 search_daily;没有 metrics.json (DS_OVERLAY_DIR 未设置),定义为 stated here [guess]
- Data: search_daily, release_log, through 2026-09-13
- Reconciled: not done (没有可对照的看板或其他来源)
- Queries and checks: .ds-queries.log, .ds-checks.log
- Verified: verify_readout: pass (38 numbers on 10 lines; 3 queries, 3 checks, 0 given)