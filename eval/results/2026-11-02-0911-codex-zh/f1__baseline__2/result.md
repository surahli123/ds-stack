## Answer
Headline: can't tell [inferred]
整体 CTR 从 30.421% 降至 28.324%，下降 2.097 个百分点，但无法确定其中多少由 v2 导致。[measured / inferred]
- Observed: -2.097 个百分点（95% 区间：-2.248 至 -1.946）[measured]
- Adjusted: -0.008 个百分点（95% 区间：-0.163 至 +0.148），holding 上线前的平台 × 国家搜索量占比 fixed [measured]
- Causal effect: not identified（需要同期随机分配的 v1/v2 对照实验；现有数据中版本与周次完全重合）[inferred]

## What it means for 回滚决策
尚未提供触发回滚的最小损失阈值；调整后区间仍包含下降 0.163 个百分点，因此也不能证明没有有意义的损失。[measured / inferred] 现有证据不足以把整体下降归因于 v2 并据此回滚，且该区间不是因果效应区间。[inferred]

## Why we believe it
- Alternatives considered:
  - 流量构成变化：ruled in，移动端搜索占比从 40.108% 升至 55.072%；以上线后各组 CTR 分解，构成变化项为 -2.089 个百分点。[measured]
  - 四组 CTR 普遍大幅下降：ruled out，各平台 × 国家组变化仅在 -0.080 至 +0.051 个百分点之间。[measured]
  - 同期其他变化或 v2 改变搜索流量构成：无法 ruled in/out，缺少同期对照和流量来源数据。[inferred]
- Checks run:
  - 日期与分组覆盖：pass，两周共 14 天，每天均有四组记录。[measured]
  - 重复键、空值及计数边界：pass，未发现异常。[measured]
  - 上线核对：pass，第一周仅 v1，第二周仅 v2，与发布记录一致。[measured]
  - 因果识别：fail，没有同期版本重叠或对照组。[measured]
  - 点击去重与用户相关性：could not run，仅有聚合计数。[measured]

## Caveats, and what would change the answer
- 区间假设每次搜索独立、点击数代表发生点击的搜索数；这些假设无法由聚合表验证。[guess]
- 标准化固定已观察到的前周权重，仅调整平台与国家；不能消除时间混杂，且可能去除 v2 经流量构成产生的影响。[inferred]
- 随机对照数据、明确的指标口径及回滚阈值会改变可作出的判断。[inferred]

## Provenance
- Metric: CTR = SUM(clicks) / SUM(searches)，按搜索量加权；from stated here [guess]，未找到 metrics.json。
- Data: search_daily、release_log；覆盖至 2026-10-04，两周日期与分组齐全，无法独立确认入库完整性。[measured]
- Reconciled: not done（未提供独立仪表盘或源数据）。
- Queries and checks: [查询与检查日志](/private/tmp/ds-runs/7d11186d9c/analysis/queries_and_checks.json)、[计算脚本](/private/tmp/ds-runs/7d11186d9c/analysis/analysis.py)、[计算结果](/private/tmp/ds-runs/7d11186d9c/analysis/results.json)。
