## Answer
Headline: can't tell(没有对照组,无法把 -1.83 个百分点的下降单独归因于 v3)
整体 CTR 从 30.44% 降到 28.61%,周环比下降 1.83 个百分点。下降全部来自桌面端,移动端几乎没变。v3 在同一天对 100% 流量上线,所以数据里没有同期的 v2 对照。
- Observed: -1.83 pp (95% 区间 -1.98 ~ -1.68)。这个区间只反映抽样噪声。[measured]
- Adjusted: -1.82 pp (95% 区间 -1.97 ~ -1.67),固定平台×国家的流量结构不变。结构变化只贡献 -0.01 pp。[measured]
- Causal effect: not identified(需要保留一部分 v2 流量的 holdout 或 A/B 实验,或者按平台灰度上线)

## What it means for 是否回滚 v3
会改变决策的最小变化大约是 0.1 pp(`mix_shift` 检查的默认阈值,不是业务给定的数)。-1.8 pp 远超这个值,所以这次下降是真实的。但它能不能算作 v3 的效果,现有数据回答不了。我倾向于先查桌面端的埋点和同期变化;如果有条件,先对一小部分桌面端流量做 v2 holdout,再决定回滚。[inferred]

## Why we believe it
- Alternatives considered:
  - 流量结构变化(平台/国家占比):排除。结构效应仅 -0.01 pp,占 1%。[measured]
  - 数据未加载完整:排除。14 天每天都是 4 行,最后一天与前几天持平。[measured]
  - 桌面端的其他同期变化(埋点、UI、季节性):未排除。下降全在桌面端(美国 -3.1 pp,其他国家 -2.9 pp),移动端 ±0.05 pp。v3 是全平台同时上线的,如果 v3 是原因,为什么只影响桌面端?这一点需要解释。[inferred]
  - 自然周波动:基本排除。上线前一周每日 CTR 在 30.1%~30.8% 之间,上线后每日 28.3%~28.9%,两段没有重叠,且下降从 9 月 7 日当天开始。但这只说明变化发生在上线当天,不能证明原因是 v3。[measured]
  - 同一天发生的其他变化:`release_log` 只有 v3 一条记录,不代表没有别的变化。[guess]
- Checks run:
  - mix_shift: pass,结构效应 -0.01 pp,组内效应 -1.82 pp。
  - completeness: pass,2026-09-13 的 4 行是近期中位数的 100%。
  - srm: skipped,这不是随机实验,没有分流比例可检验。
  - fanout: skipped,没有做 join。

## Caveats, and what would change the answer
- 前后各只有一周,没有往年同期数据,也没排除周度季节性。
- 区间假设各次搜索相互独立,同一用户的重复搜索会让真实区间更宽。
- 若发现桌面端 9 月 7 日也有其他发布或埋点改动,v3 的归因要重算。
- 若 holdout 显示桌面端 v3 比 v2 低,则回滚;若 v2 holdout 同样下降,则不是 v3 的问题。

## Provenance
- Metric: CTR = clicks / searches,汇总所有行(stated here [guess],目录里没有 metrics.json)
- Data: `search_daily`、`release_log`,到 2026-09-13(完整)
- Reconciled: not done(没有可对账的仪表盘或其他数据源)
- Queries and checks: 检查结果记录在工作目录的 `.ds-checks.log`(`mix_shift#1`、`completeness#1`)。查询是临时执行的,没有单独记录。