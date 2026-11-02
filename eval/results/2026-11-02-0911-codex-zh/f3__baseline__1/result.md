## Answer
Headline: can't tell  
[measured] 2026-08-31—09-06 至 2026-09-07—09-13，整体 CTR 从 30.441% 降至 28.615%，下降 1.827 个百分点；其中可归因于 v3 的部分无法识别 [inferred]。
- Observed: -1.827 个百分点（95% 区间：-1.878 至 -1.780）[measured]
- Adjusted: -1.818 个百分点（95% 区间：-1.859 至 -1.770），holding 上周平台 × 国家联合流量占比 fixed [measured]
- Causal effect: not identified（需要同期随机分配的 v2/v3 对照实验）[inferred]

## What it means for 回滚决策
尚未提供足以触发回滚的最小损失阈值，因此无法完成阈值比较；上述区间描述周间变化，不是 v3 的因果效应区间。[inferred] 数据支持优先调查桌面端并开展随机对照验证，不能据此断言回滚会恢复 1.827 个百分点。[inferred]

## Why we believe it
- Alternatives considered:
  - 平台、国家流量构成变化是主要原因：ruled out；固定构成后仍下降 1.818 个百分点，构成差异仅对应 -0.009 个百分点。[measured]
  - 桌面端特有问题：ruled in，作为待查解释；美国、其他国家桌面端分别下降 3.107、2.872 个百分点，移动端仅下降 0.031、0.043 个百分点。[measured]
  - 同期需求变化、其他改动或埋点异常：ruled in，仍无法排除；发布日志仅记录 v3 上线，缺乏独立验证材料。[inferred]
- Checks run:
  - 日期和分层覆盖：pass；14 天每天均有四个平台 × 国家组合，共 56 行。[measured]
  - 重复与计数有效性：pass；无重复分层键、空计数、非正搜索量或越界点击数。[measured]
  - 版本对照：flag；前周全部 v2、后周全部 v3，版本与周次完全重合。[measured]
  - 移动端作为对照：fail；移动端同样升级 v3，不能直接视为未处理对照。[inferred]
  - 区间计算：pass；按相同星期几配对，进行 30,000 次日期块 bootstrap。[measured]

## Caveats, and what would change the answer
- 只有七对日期；区间依赖日期对可重采样的假设，不覆盖混杂偏差，也无法处理未观测的跨日用户相关性。[inferred]
- 固定平台和国家构成不能控制查询意图、用户组成或同期产品变化。[inferred]
- 随机对照结果、独立埋点核验及明确的回滚阈值会改变决策依据。[inferred]

## Provenance
- Metric: CTR = SUM(clicks) / SUM(searches)；未提供 metrics.json，将 clicks 解释为有点击的搜索次数，stated here [guess]。
- Data: warehouse.db 中 search_daily、release_log；日期及分层覆盖完整至 2026-09-13，但无法独立确认入库最终完整性。[measured]
- Reconciled: not done（未提供仪表盘或独立来源）。
- Queries and checks: [查询](queries.sql)、[计算与检查脚本](analysis.py)、[完整结果](results.json)。
