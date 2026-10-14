```
## Answer
Headline: -0.00 pp (95% 区间 -0.15 到 +0.15 pp),即在平台×国家内部 CTR 基本没变 [check:mix_shift#1]
整体 CTR 从 30.42% 降到 28.32%,但几乎全部来自流量向移动端(CTR 低)转移,而不是各分群内 CTR 下降;假设 v2 本身没有造成流量结构变化 [check:mix_shift#1]
- Observed: -2.10 pp (-2.25 到 -1.95 pp) [check:mix_shift#1]
- Adjusted: -0.00 pp (-0.15 到 +0.15 pp), holding 平台×国家的流量结构 fixed [check:mix_shift#1]
- Causal effect: not identified (v2 是全量上线,没有对照组;需要 v1/v2 的随机分流实验或保留一部分 v1 流量)

## What it means for 是否回滚 v2
分群内 CTR 变化的区间 (-0.15 到 +0.15 pp) 不包含 -2.1 pp 的整体降幅;mix_shift 的最小关注效应为 0.1 pp,区间略宽于该值,所以不能排除 ±0.15 pp 以内的小影响,但"v2 导致了 2.1 pp 下降"的说法不成立 [check:mix_shift#1]。

## Why we believe it
- Alternatives considered:
  - 流量结构(mix)变化: ruled in,移动端占比从 40.1% 升到 55.1%,桌面 CTR 约 36%、移动约 22%,mix 效应 -2.09 pp,占 100% [check:mix_shift#2] [measured]
  - v2 排序质量下降(PM 的假设): 未被支持,四个平台×国家分群 CTR 变化均在 ±0.02 pp 内 [check:mix_shift#1] [measured]
  - 更粗粒度(仅平台)是否一致: 一致,mix -2.09 pp,分群内 -0.00 pp [check:mix_shift#2] [measured]
  - v2 引起了流量向移动端转移: 未排除,数据中无法区分,但机制上不明显 [inferred]
  - 星期效应/季节性: 两周都是完整的周一到周日,窗口等长同星期构成,日搜索量稳定在 9.6 万到 10.3 万 [q3] [measured]
  - 数据缺失: 两周每天均为 4 行(平台×国家)且无缺口 [q3] [measured]
  - 同期其他变更/日志口径变化: release_log 仅记录 v2 上线一条,无其他记录,但日志可能不完整 [q2] [inferred]
- Checks run:
  - mix_shift(平台×国家,4 分群): flag 整体 -2.10 pp = 分群内 -0.00 pp + mix -2.09 pp [check:mix_shift#1]
  - mix_shift(仅平台,更粗粒度): flag 结论一致 [check:mix_shift#2]
  - completeness: 周粒度按 2 个周期调用 could not run(历史不足 3 个周期,completeness#1);日粒度用我遗漏 10-04 的序列误调用得到 fail(completeness#2,属调用错误);补全后重跑 pass,10-04 为同期中位数的 102% [check:completeness#3]
  - fanout: skipped,没有做 join
  - srm: skipped,这不是随机实验

## Caveats, and what would change the answer
- 没有对照组:v2 是全量上线,"调整后 ≈0"是描述性结果,不是因果效应;随机分流或灰度实验可以确认。
- 若 v2 本身(例如改变了移动端入口)导致移动端流量上升,则 mix 部分也应归因于 v2;需要查移动端流量增长的来源。
- 仅两周数据,区间假设各单元独立,实际可能偏窄。
- 本表只含 searches 与 clicks,点击是否有效(如 CTR 之外的转化)未评估。

## Provenance
- Metric: CTR = sum(clicks) / sum(searches),按 search_daily 汇总,周窗口 09-21~09-27 对比 09-28~10-04 [guess](overlay 中没有 metrics.json)
- Data: search_daily, release_log,截至 2026-10-04
- Reconciled: not done (没有可对照的仪表盘或其他来源)
- Queries and checks: .ds-queries.log 与 .ds-checks.log
- Verified: verify_readout: pass (41 numbers on 12 lines; 2 queries, 3 checks, 0 given)
```