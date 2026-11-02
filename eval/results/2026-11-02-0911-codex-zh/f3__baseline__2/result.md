## Answer
Headline: can't tell [inferred]

后一周总体 CTR 从 30.441% 降至 28.615%，下降 1.827 个百分点，但无法确定其中多少由 v3 导致。[measured：变化；inferred：归因限制]

- Observed: -1.827 个百分点（95% 区间：-1.978 至 -1.675）[measured]
- Adjusted: -1.818 个百分点（95% 区间：-1.967 至 -1.668），holding 平台×国家的搜索量占比固定为前一周构成。[measured]
- Causal effect: not identified；需要同期随机分配的 v2/v3 对照，或满足可信识别假设的准实验。[inferred]

## What it means for 是否回滚
调整后的区间完全低于零，但它衡量的是周际变化，不能当作 v3 的因果损失区间。[inferred] 未提供足以触发回滚的最小损失阈值，因此无法完成阈值比较，也不能仅凭这些数据断言回滚会挽回多少 CTR。[inferred]

## Why we believe it
- Alternatives considered:
  - 平台和国家构成变化解释主要下降：ruled out；按前期权重分解，构成变化仅贡献 -0.009 个百分点。[measured]
  - 桌面端特有的问题或 v3 在桌面端的差异化影响：ruled in（仍可能）；桌面端下降 2.999 个百分点，移动端下降 0.042 个百分点，不能据此区分具体原因。[measured：变化；inferred：解释]
  - 同期需求、其他产品变化或埋点变化：ruled in（未排除）；发布日志仅记录 v3 上线，无法证明不存在其他变化。[inferred]
- Checks run:
  - 覆盖与完整性：pass 两周共 14 天，每天均有四个平台×国家组合；实际数据入库完整性未获外部确认。[measured]
  - 重复与计数合法性：pass 无重复键、缺失字段或越界计数。[measured]
  - 对照与版本重叠：fail 前期全部 v2、后期全部 v3，版本与时期完全重合。[measured]
  - 移动端作为对照：flag 移动端也升级了，不能直接假设其不受处理影响。[inferred]
  - 分解核对：pass 调整后变化与构成贡献之和等于总体变化。[measured]

## Caveats, and what would change the answer
- 区间使用独立二项近似，假设每次搜索对应一次是否点击；聚合数据无法验证重复用户相关性或多次点击，区间可能低估不确定性。这些不是因果区间。[inferred]
- 仅有两周，无法检验长期趋势；固定平台和国家也不能消除其他同期混杂。[inferred]
- 随机保留或恢复同期 v2 对照、核验点击埋点，并明确回滚阈值，可让归因与决策更可靠。[inferred]

## Provenance
- Metric: `SUM(clicks) / SUM(searches)`，按搜索量加权；未找到 metrics.json，定义 stated here [guess]。
- Data: `warehouse.db` 中的 `search_daily`、`release_log`；记录覆盖至 2026-09-13，两周日期及分组齐全，尚未外部确认最后完整周期。[measured]
- Reconciled: not done（没有仪表盘或独立来源可供核对）。
- Queries and checks: [SQL 查询](/private/tmp/ds-runs/aa0f213d24/analysis/queries.sql)、[计算与检查脚本](/private/tmp/ds-runs/aa0f213d24/analysis/analyze.py)、[完整结果](/private/tmp/ds-runs/aa0f213d24/analysis/results.json)。
