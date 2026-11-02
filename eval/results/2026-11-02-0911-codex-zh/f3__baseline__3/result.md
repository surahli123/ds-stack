## Answer
Headline: can't tell [inferred]  
上线后整体 CTR 从 30.441% 降至 28.615%，下降 1.827 个百分点，但无法确定其中多少由 v3 导致。[measured；归因判断 inferred]

- Observed: −1.827 个百分点（95% 区间：−1.978 至 −1.675）[measured]
- Adjusted: −1.818 个百分点（95% 区间：−1.967 至 −1.668），holding 上线前的平台 × 国家搜索量占比 fixed [measured]
- Causal effect: not identified（版本与周次完全重合；需要同期随机 v2/v3 对照，或满足可信识别假设的准实验）[inferred]

## What it means for 回滚决策
尚未提供改变决策的最小降幅；若以整体周环比下降 1 个百分点为阈值，观测区间全部超过该阈值，但这只是条件示例。[guess] 若回滚取决于 **v3 导致的损失**，现有数据无法与任何因果阈值比较，也不能据此证明 v3 无害。[inferred]

## Why we believe it
- Alternatives considered:
  - 平台与国家流量构成变化是主要原因：ruled out；按上线前权重分解，构成变化仅贡献 −0.009 个百分点。[measured]
  - 桌面端特有变化：ruled in；桌面 US／其他国家分别下降 3.107／2.872 个百分点，移动端仅下降 0.031／0.043 个百分点；原因仍未知。[measured；原因判断 inferred]
  - 同期其他变化或埋点问题：ruled in（仍可能）；发布日志仅记录 v3 上线，无法排除未记录变化。[inferred]
- Checks run:
  - 数据完整性：pass；14 天每天均有四个平台 × 国家组合，无重复键、空值或计数越界。[measured]
  - 对照组：flag；前周全部 v2、后周全部 v3，移动端同样接受处理，不能直接当未处理对照。[measured；对照判断 inferred]
  - 区间敏感性：pass；按相同星期几配对、重抽样 20,000 次，观测变化区间为 −1.878 至 −1.780，调整后为 −1.859 至 −1.770 个百分点。[measured]

## Caveats, and what would change the answer
- 主区间采用独立伯努利搜索假设及正态近似；缺少用户级数据，无法验证重复用户相关性，区间不包含同期混杂的不确定性。[inferred]
- 调整仅覆盖平台和国家；不能消除查询类型、用户构成或其他时间变化的影响。[inferred]
- 同期随机保留 v2 对照、验证点击埋点，并提供回滚阈值，才能直接支持归因与决策。[inferred]

## Provenance
- Metric: CTR = SUM(clicks) / SUM(searches)，非每日 CTR 的简单平均；from stated here [guess]，未提供 metrics.json，clicks 是否代表发生点击的搜索尚未验证。
- Data: search_daily、release_log；覆盖至 2026-09-13，每日分层齐全，但无入库完成标记。[measured]
- Reconciled: not done（无仪表盘或独立来源；前后周分别为 212,933/699,485、200,094/699,266）。[measured]
- Queries and checks: [查询与检查记录](/private/tmp/ds-runs/eb7a9c2347/analysis/queries_and_checks.json)、[计算脚本](/private/tmp/ds-runs/eb7a9c2347/analysis/analyze.py)、[结果](/private/tmp/ds-runs/eb7a9c2347/analysis/results.json)。[measured]
