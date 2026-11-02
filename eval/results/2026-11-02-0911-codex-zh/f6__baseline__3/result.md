## Answer
Headline: +50.05% (95% interval: 49.93%–50.18%) [measured；区间依赖 inferred 假设]
2026-10-05 至 2026-10-11，外部流量中有结果的 642,880 次搜索里，321,780 次发生点击，搜索 CTR 为 50.05%，这是水平值而非增幅。[measured]
- Observed: +50.05% (95% interval: 49.93%–50.18%) [measured；区间依赖 inferred 假设]
- Adjusted: not computed（本次报告总体 CTR，没有指定比较基准或需要固定的因素）[inferred]
- Causal effect: not identified（需要明确干预及随机实验或可信的准实验设计）[inferred]

## What it means for 周度业务复盘
该周可报告搜索 CTR 为 50.05%。[measured] 区间约为估计值 ±0.12 个百分点；未提供足以改变决策的最小变化阈值或基准，无法判断是否达到行动标准。[inferred]

## Why we believe it
- Alternatives considered:
  - 用点击总次数作分子：ruled out，该口径得到 70.07%，重复计入一次搜索中的多次点击，不符合指标定义。[measured]
  - 用全部搜索作分母：ruled out，该口径得到 46.05%，包含无结果搜索。[measured]
  - 包含内部及机器人流量：ruled out，该口径得到 44.53%，违反外部流量过滤条件。[measured]
- Checks run:
  - 数据库完整性：pass，SQLite 检查返回 ok。[measured]
  - 日期及维度覆盖：pass，七天每天均有两个平台、三类流量，共 42 行。[measured]
  - 粒度重复：pass，日期×平台×流量类型无重复。[measured]
  - 计数约束：pass，无空值、负数或分子超过分母等异常。[measured]
  - 入库完整性：could not run，没有加载完成标记。[measured]

## Caveats, and what would change the answer
- 95% 区间使用 Wilson 方法，假设搜索相互独立；缺少用户或会话明细，无法校正重复搜索的相关性。[inferred]
- 对已记录的全量搜索，50.05% 是直接计算值；区间不涵盖漏报、迟到数据或埋点误差。[inferred]
- 如有迟到数据或口径修订，应重新计算。[inferred]

## Provenance
- Metric: 外部流量的 `SUM(searches_with_click) / SUM(searches_with_results) × 100%`，from [metrics.json](/private/tmp/ds-runs/7d4a0e67b2/overlay/metrics.json)，按搜索量加权汇总。[measured]
- Data: `warehouse.db` 的 `search_daily_v`，日期覆盖至 2026-10-11；最后完整入库周期无法确认。[measured]
- Reconciled: not done（未提供本周看板值；指标文件记载的历史核对不能验证本周）。[measured]
- Queries and checks: [查询及检查日志](/private/tmp/ds-runs/7d4a0e67b2/analysis/ctr_queries_and_checks.json)、[计算脚本](/private/tmp/ds-runs/7d4a0e67b2/analysis/analyze_ctr.py)。[measured]
