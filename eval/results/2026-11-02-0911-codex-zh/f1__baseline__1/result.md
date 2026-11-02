## Answer
Headline: can't tell  
整体 CTR 从 30.421% 降至 28.324%，下降 2.097 个百分点，但无法确定其中多少由 v2 导致。[measured/inferred]

- Observed: −2.097 个百分点（95% 区间：−2.248 至 −1.946）[measured]
- Adjusted: −0.008 个百分点（95% 区间：−0.163 至 +0.148），holding 上线前的平台 × 国家搜索量占比 fixed [measured]
- Causal effect: not identified（需要同期随机分配的 v1/v2 对照实验；当前版本与周次完全重合）[inferred]

## What it means for 回滚决策
尚未提供足以改变回滚决策的最小降幅，因此无法按业务阈值判断；调整后区间仍包含下降 0.163 个百分点，但它不是因果效应区间。[measured/inferred] 现有数据不足以支持“v2 导致下降所以应回滚”，也不能证明 v2 无害。[inferred]

## Why we believe it
- Alternatives considered:
  - 流量结构变化：ruled in；移动端占比从 40.108% 升至 55.072%，其 CTR 较低，按上线后各层 CTR 分解，结构变化项为 −2.089 个百分点。[measured]
  - 同期需求、用户构成或埋点变化：未能 ruled out；没有同期对照或相关记录。[inferred]
  - v2 本身影响：未能 ruled in 或 ruled out；调整后的前后差异不能分离版本与时间影响。[inferred]
- Checks run:
  - 日期与分层覆盖：pass；14 天每天均有四个平台 × 国家组合。[measured]
  - 重复与计数合法性：pass；无重复键、空值、负计数或 clicks 超过 searches。[measured]
  - 版本切换：pass；前周全部 v1、后周全部 v2，与发布日志一致。[measured]
  - 同星期配对敏感性：pass；等权日配对调整差为 −0.007 个百分点，95% 区间 −0.062 至 +0.048。[measured]
  - 因果识别：fail；缺少同期未处理组，无法分离周次与版本效应。[inferred]

## Caveats, and what would change the answer
- 区间假设每次搜索是独立的二元点击结果；无法核验重复用户相关性或 clicks 是否为点击事件数。[guess]
- 流量结构变化也可能受 v2 影响，固定结构可能移除部分总效应。[inferred]
- 随机对照实验、正式指标定义和预设回滚阈值会改变可作出的判断。[inferred]

## Provenance
- Metric: SUM(clicks) / SUM(searches)，from stated here [guess]；未找到 metrics.json。
- Data: search_daily、release_log，覆盖至 2026-10-04；日期齐全，但无数据加载完成标记。[measured]
- Reconciled: not done（未提供仪表盘或独立源数据）。
- Queries and checks: [查询与结果](/private/tmp/ds-runs/507311ba9e/analysis/queries_and_checks.json)、[可复运行脚本](/private/tmp/ds-runs/507311ba9e/analysis/analysis.py)、[方法与假设](/private/tmp/ds-runs/507311ba9e/analysis/methodology.md)。
