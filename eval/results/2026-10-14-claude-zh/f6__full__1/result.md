## Answer
Headline: +50.05 % (95% CI 49.93 to 50.17) [q6]
2026-10-05 至 2026-10-11 这一周的搜索 CTR 为 50.05%(321,780 次带点击的搜索 / 642,880 次有结果的搜索)。 [q5, q6]
- Observed: +50.05 % (95% CI 49.93 to 50.17) [q6]
- Adjusted: not computed (只有这一周的数据,没有对比期,无变化可分解)
- Causal effect: not identified (这是单周水平值,不是变化量;没有干预可识别)

## What it means for 每周业务回顾 (WBR)
这是一个水平值而不是变化量,库里没有上周数据,所以无法判断涨跌;若要说"变化",需要上周同口径数值。 [q2]

## Why we believe it
- Alternatives considered:
  - 用 clicks 作分子(会重复计算多次点击): ruled out,按 metrics.json 用 searches_with_click;若误用会得到 70.07% [q6] [measured]
  - 分母用全部 searches(含无结果搜索): ruled out,metrics.json 规定分母为 searches_with_results;误用会得到 46.05% [q6] [measured]
  - 混入 bot/internal 流量: ruled out,只取 traffic_type='external' [q3, q5] [measured]
  - 平台(desktop/mobile)构成: ruled out 为影响因素,两平台 CTR 几乎相同(desktop 50.06%,mobile 50.04%) [q5] [measured]
  - 星期效应: 单周数据无法检验,只能在 caveats 说明 [q4] [inferred]
- Checks run:
  - completeness: pass 2026-10-11 行数为同周日前几天中位数的 102% [check:completeness#1]
  - mix_shift: skipped 没有对比期,无法分解
  - fanout: skipped 没有做 join
  - srm: skipped 不是实验

## Caveats, and what would change the answer
- 区间是把搜索当作独立样本的二项近似(±0.12 pp),没有考虑按天聚类,实际可能略宽。
- 表中只有这一周(7 天),无法做周环比或星期效应检验;补上上周数据后才能说涨跌。
- completeness 的基线只是同一周内的前几天,不是历史同星期数据,力度有限。
- 未与 WBR 看板当期数字对账;metrics.json 记录 2026-10-01 时与看板一致(0.1 pp 内)。

## Provenance
- Metric: CTR = searches_with_click / searches_with_results,traffic_type='external',按搜索粒度,表 search_daily_v,from metrics.json
- Data: search_daily_v,through 2026-10-11
- Reconciled: not done (没有本周看板数字可对照)
- Queries and checks: .ds-queries.log, .ds-checks.log
- Verified: verify_readout: pass (14 numbers on 7 lines; 5 queries, 1 checks, 0 given)