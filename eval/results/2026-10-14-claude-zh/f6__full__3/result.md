## Answer
Headline: +50.05 pp (95% CI 49.93 至 50.17;这是 CTR 的水平值 50.05%,不是变化量) [q4]
2026-10-05 至 10-11 这一周的搜索 CTR 为 50.05%(外部流量,点击搜索数 321,780 / 有结果搜索数 642,880)。 [q4]
- Observed: +50.05 pp (95% CI 49.93 至 50.17),周水平值,二项近似区间 [q4]
- Adjusted: not computed (数据库只有这一周,没有对比期,无法做 mix_shift)
- Causal effect: not identified (这是描述性水平值,没有变化量,也没有实验设计)

## What it means for 每周业务评审 (WBR)
本周 CTR 为 50.05%,区间半宽约 0.12 pp [q4]。库里没有上周数据,所以无法判断是上升还是下降。请求中也没有给出会改变决策的阈值。

## Why we believe it
- Alternatives considered:
  - 口径错误(用 clicks 而非 searches_with_click): ruled out。若用 clicks 会得到 70.07%,明显偏高;按 metrics.json 取 searches_with_click [q4] [measured]
  - 口径错误(分母用全部 searches): ruled out。那样会得到 46.05%;按 metrics.json 分母为有结果搜索 [q4] [measured]
  - 机器人/内部流量混入: ruled out。已按 traffic_type='external' 排除 [q4] [measured]
  - 数据不完整: ruled out。7 天各 6 行(2 平台 × 3 流量类型),齐全 [q5, check:completeness#1] [measured]
  - 星期/季节性、mix-shift: 无法检验,库内只有一周 [inferred]
- Checks run:
  - completeness: pass 10-11 为 6 行,等于近几天中位数的 100% [check:completeness#1]
  - mix_shift: skipped 没有对比期
  - fanout: skipped 未使用 join
  - srm: skipped 非实验

## Caveats, and what would change the answer
- 只有一周数据,无环比/同比。要说明涨跌,需要 2026-09-28 至 10-04 周的数据。
- 区间按"每次搜索独立"的二项近似,忽略了日内相关性,实际区间可能略宽。
- 未与仪表盘对账。若仪表盘与此相差超过 0.1 pp,应排查口径差异。

## Provenance
- Metric: searches_with_click / searches_with_results,traffic_type='external',来自 metrics.json
- Data: search_daily_v,截至 2026-10-11
- Reconciled: not done (本周仪表盘数字未提供;metrics.json 仅记录 2026-10-01 曾对上 0.1 pp)
- Queries and checks: .ds-queries.log 与 .ds-checks.log
- Verified: verify_readout: pass (24 numbers on 8 lines; 2 queries, 1 checks, 0 given)