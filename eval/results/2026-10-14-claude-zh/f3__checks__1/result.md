我跑完了 mix_shift 和 completeness 两项检查,下面是结论。

```
## Answer
Headline: can't tell
整体 CTR 周环比下降约 1.83 个百分点,这是实测值。但 v3 是 100% 全量上线,没有同期对照组,所以其中有多少归因于 v3 无法确定。
- Observed: -1.83 pp (95% 区间 -1.98 到 -1.68)。CTR 从 30.44% 降到 28.61%。[measured]
- Adjusted: -1.82 pp (95% 区间 -1.97 到 -1.67),保持平台×国家的流量结构不变。流量结构变化只贡献 -0.01 pp。[measured]
- Causal effect: not identified(需要 v3 的随机对照/灰度实验,或同期仍使用 v2 的 holdout 流量)

## What it means for 是否回滚 v3
这个下降几乎全部来自同一段内的 CTR 变化,不是流量结构变化。但现有数据不能证明 v3 是原因。若 v3 的真实影响小于约 0.15 pp(噪声底)就不足以左右决策;而观测到的 -1.8 pp 远大于这个值,所以建议先做 v3 的小流量 holdout 对照,再决定回滚。

## Why we believe it
- Alternatives considered:
  - 流量结构变化(平台/国家占比):已排除,mix 效应只有 -0.01 pp,占 1%。[measured]
  - 数据缺失或加载不全:基本排除,最后一天 2026-09-13 的行数是近期中位数的 100%,两周每天都是 4 行。[measured]
  - v3 本身导致下降:无法排除。下降只出现在桌面端,US 为 -3.1 pp,other 为 -2.9 pp,而移动端基本没变(US 和 other 都在 ±0.05 pp 以内);时间上与上线吻合。[measured] 这与"v3 主要影响桌面端"一致,但无法证明。[inferred]
  - 同期其他变化(桌面端 UI、埋点、季节性):无法排除。release_log 只有 v3 一条记录,不能证明当周没有其他变更。移动端不变只能说明这个因素若存在也是桌面端特有的。[inferred]
- Checks run:
  - mix_shift: pass,整体 -1.83 pp = 段内 -1.82 pp + 结构 -0.01 pp。
  - completeness: pass,2026-09-13 的行数达到基线的 100%。
  - srm: skipped,这不是随机实验,没有分流比例可查。我用占位数据跑过一次,结果无意义,请勿引用。
  - fanout: skipped,没有做表连接。

## Caveats, and what would change the answer
- 只有前后各一周,所有时间相关因素都与 v3 混在一起。
- 区间只反映抽样噪声,假设各次搜索相互独立,实际用户内部有相关性,真实区间会更宽。
- 如果能拿到 v3 灰度期或 holdout 的数据,或确认桌面端同期没有其他变更,就可以估计因果效应。
- 这里没有 metrics.json,CTR 的定义是我自己设定的。

## Provenance
- Metric: CTR = clicks / searches,汇总后再相除,出处:stated here [guess]
- Data: search_daily(56 行)和 release_log,覆盖 2026-08-31 到 2026-09-13,最后一天完整。
- Reconciled: not done(没有可对照的看板或其他数据源)
- Queries and checks: 检查结果记录在 checks/ 目录下的 .ds-checks.log(mix_shift#1、completeness#1)。查询是内联运行的,没有单独的日志。
```