## Answer
Headline: can't tell [inferred]  
整体 CTR 从 30.421% 降至 28.324%，下降 2.097 个百分点，但无法确定其中多少由 v2 导致。[measured；归因判断 inferred]

- Observed: -2.097 个百分点（95% 区间：-2.248 至 -1.946）[measured]
- Adjusted: -0.008 个百分点（95% 区间：-0.163 至 +0.148），holding 前一周的平台 × 国家搜索占比 fixed [measured]
- Causal effect: not identified（版本与周次完全重合；需要同期随机分配的 v1/v2 对照实验识别）[inferred]

## What it means for 回滚决策
尚未提供改变回滚决策的最小降幅；调整后区间仍包含下降 0.163 个百分点，但它不是因果区间，不能据此排除 v2 的损害。[inferred] 当前证据不足以把整体下降归责于 v2 并据此回滚，也不足以证明 v2 无害。[inferred]

## Why we believe it
- Alternatives considered:
  - 流量构成变化：ruled in；移动端搜索占比从 40.108% 升至 55.072%，其 CTR 较低；按后一周各层 CTR 分解，构成项为 -2.089 个百分点，占整体降幅的 99.63%，这是算术分解而非因果归因。[measured]
  - 星期构成变化：ruled out 为主要解释；额外固定星期后，调整变化仍为 -0.007 个百分点。[measured]
  - 同期需求、埋点或其他产品变化：未排除；只有两周汇总数据，发布日志仅记录 v2 上线，不能证明不存在其他变化。[inferred]
- Checks run:
  - 数据完整性：pass；14 天、每天 4 个平台 × 国家组合，无重复键、空值或非法计数。[measured]
  - 上线记录：pass；前周全部 v1，后周全部 v2，与日志一致。[measured]
  - 分解核验：pass；构成项加调整项等于整体变化，误差小于 0.000001 个百分点。[measured]
  - 因果识别：fail；没有同期版本重叠、对照组或随机分配记录。[measured]
  - 入库完整性与用户聚类：could not run；缺少水位及用户、会话级数据。[measured]

## Caveats, and what would change the answer
- 区间采用独立搜索的二项近似，并固定观测权重；每次搜索是否最多计一次点击无法验证，重复用户相关性可能使区间偏窄。[guess]
- 若 v2 本身改变搜索频次或流量构成，固定构成会移除部分影响；调整结果不能当作 v2 总效应。[inferred]
- 明确回滚阈值、核实指标口径并开展同期随机对照实验，才能形成可靠的因果决策依据。[inferred]

## Provenance
- Metric: `SUM(clicks) / SUM(searches)`，from stated here [guess]；目录中无 `metrics.json`。[measured]
- Data: `search_daily`、`release_log`；比较 2026-09-21—09-27 与 2026-09-28—10-04，记录覆盖至 2026-10-04，但无入库完成证明。[measured]
- Reconciled: not done（未提供仪表盘或独立源）；前周 212,828 / 699,605，后周 198,374 / 700,366。[measured]
- Queries and checks: [查询与检查日志](queries_and_checks.json)、[计算脚本](analyze.py)、[完整结果](results.json)。[measured]
