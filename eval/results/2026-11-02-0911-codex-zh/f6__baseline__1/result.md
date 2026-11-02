## Answer
Headline: +50.05% (95% interval: 49.93%–50.18%) [measured；区间模型 inferred]
2026-10-05 至 2026-10-11，外部流量中有结果的 642,880 次搜索里，321,780 次产生点击，CTR 为 50.05%，这是当周水平而非增幅。[measured]
- Observed: +50.05% (95% interval: 49.93%–50.18%) [measured；区间模型 inferred]
- Adjusted: not computed（报告当周总体水平，未指定调整目标）。[inferred]
- Causal effect: not identified（需要随机实验或可信的准实验设计）。[inferred]

## What it means for 周度业务回顾
周报可填写搜索 CTR **50.05%**。[measured] 区间半宽约 0.12 个百分点；未提供决策所需的最小变化阈值或对比期，无法判断是否达到应改变决策的幅度。[inferred]

## Why we believe it
- Alternatives considered:
  - 用全部搜索作分母：ruled out，结果为 46.05%，不符合指标定义。[measured]
  - 用点击总次数作分子：ruled out，结果为 70.07%，会重复计入同一次搜索的多次点击。[measured]
  - 纳入内部或机器人流量：ruled out，metrics.json 明确只纳入 external。[measured]
- Checks run:
  - 日期覆盖：pass，7 天均存在，每天包含 2 个平台、3 类流量。[measured]
  - 重复及数值约束：pass，分组键无重复，空值、负值及计数关系异常均为 0。[measured]
  - 分平台核对：pass，外部流量的平台分项加总与周总量一致。[measured]
  - 数据入库完成状态：could not run，无完成水位记录。[measured]

## Caveats, and what would change the answer
- 95% 区间采用 Wilson 二项模型，假定搜索相互独立；重复用户导致的相关性无法从日汇总数据估计。[inferred]
- 若这些记录是完整总体，50.05% 就是该周实际比例；区间描述模型下的波动，不涵盖漏报或口径错误。[inferred]
- 补录数据、时区边界或指标定义变更可能改变结果。[inferred]

## Provenance
- Metric: `SUM(searches_with_click) / SUM(searches_with_results) × 100%`，仅 `traffic_type='external'`，来自 [metrics.json](/private/tmp/ds-runs/0ec6ceaca5/overlay/metrics.json)。[measured]
- Data: `warehouse.db` → `search_daily_v`，日期覆盖至 2026-10-11；入库完整性未确认。[measured]
- Reconciled: not done（无本周仪表盘数值；指标文件中的历史核对记录不能代替本周核对）。[measured]
- Queries and checks: [查询脚本](/private/tmp/ds-runs/0ec6ceaca5/analysis/analyze_ctr.py)、[检查结果](/private/tmp/ds-runs/0ec6ceaca5/analysis/ctr_checks.json)。[measured]
