## Answer
Headline: +50.05 % (95% 区间 49.93 到 50.18 %) [q5]
2026-10-05 至 10-11 这一周,搜索 CTR(external 流量,有点击的搜索数 / 有结果的搜索数)为 50.05%,即 321,780 / 642,880 [q5]。
- Observed: +50.05 % (95% 区间 49.93 到 50.18 %) [q5]
- Adjusted: not computed (数据库只有这一周,没有对比期,无法做 mix_shift)
- Causal effect: not identified (这是水平值而非变化量;要判断因果需要有对照或随机实验)

## What it means for 每周业务评审
本周 CTR 约 50.05%,区间宽度约 ±0.12pp [q5];因为没有上周数据,无法判断环比涨跌,这个数只能当作本周水平值报告。分平台:桌面 161,597/322,792,移动 160,183/320,088,两者非常接近 [q4]。

## Why we believe it
- Alternatives considered:
  - 把 clicks(总点击数)当分子会高估:ruled out,使用 searches_with_click,符合 metrics.json 的 pitfall [q5] [measured]
  - 包含 internal/bot 流量:ruled out,已过滤 traffic_type='external' [q5] [measured]
  - 数据不完整:ruled out,7 天每天 6 行(2 平台 × 3 流量类型) [q3, check:completeness#1] [measured]
  - 平台构成变化(mix-shift):not assessed,无对比周;本周两平台 CTR 几乎相同,构成影响很小 [q4] [inferred]
  - 季节性/星期效应:could not be assessed,只有一周数据 [q3] [guess]
- Checks run:
  - completeness: pass 2026-10-11 的行数为趋势中位数的 100% [check:completeness#1]
  - mix_shift: skipped,没有对比期
  - fanout: skipped,没有做 join
  - srm: skipped,不是实验

## Caveats, and what would change the answer
- 仓库里只有 2026-10-05 至 10-11 这一周,无法给出环比;需要上周数据才能判断变化。
- 区间是我用二项分布近似手算的(假设搜索相互独立),同一用户的多次搜索会使真实区间更宽。
- 未与周报看板对账;若看板差异超过 0.1pp 需要核查。

## Provenance
- Metric: CTR = searches_with_click / searches_with_results,traffic_type='external',按周汇总,from metrics.json
- Data: search_daily_v,through 2026-10-11
- Reconciled: not done (无法访问周报看板)
- Queries and checks: .ds-queries.log, .ds-checks.log
- Verified: verify_readout: pass (24 numbers on 6 lines; 3 queries, 1 checks, 0 given)