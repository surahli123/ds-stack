## Answer

Headline: can't tell [inferred]

比较 2026-08-31—09-06 与 2026-09-07—09-13，总体 CTR 从 30.44% 降至 28.61%，下降 1.83 个百分点，但无法确定其中多少由 v3 导致。[measured；归因判断 inferred]

- Observed: −1.827 个百分点（95% 区间：−1.978 至 −1.675）[measured]
- Adjusted: −1.818 个百分点（95% 区间：−1.967 至 −1.668），holding 上线前的平台 × 国家搜索量占比 fixed。[measured]
- Causal effect: not identified（版本与周次完全重合；需要同期随机分配的 v2/v3 对照实验，或有可信识别假设的准实验）。[inferred]

## What it means for 回滚决策

尚未提供足以触发回滚的最小因果下降阈值，因此不能完成阈值比较。[inferred] 调整后的区间仍全部低于零，但它是周际变化区间，不能据此认定回滚会恢复相应 CTR；建议用随机保留的 v2 对照验证。[inferred]

## Why we believe it

- Alternatives considered:
  - 平台、国家流量构成变化是主要原因：ruled out，构成变化的描述性分解贡献仅 −0.010 个百分点。[measured]
  - 桌面端特有变化：ruled in，桌面 CTR 变化为 −2.999 个百分点（95% 区间：−3.202 至 −2.796），移动端为 −0.042（−0.259 至 +0.175）；下降主要集中在桌面端。[measured]
  - 同期需求、埋点或其他产品变化：ruled in，现有数据无法排除；发布日志不能证明没有其他变化。[inferred]
  - 把移动端当作未处理对照：ruled out，移动端同样切换至 v3，且没有足够历史验证平行趋势。[measured；设计判断 inferred]
- Checks run:
  - completeness: pass，09-03—09-13 日搜索量及两个周末的分组行数通过检查。[measured]
  - completeness: could not run，08-31—09-02 缺少足够前期基线；完整加载仍未获独立确认。[measured]
  - mix_shift: pass，平台及平台 × 国家分解均未发现构成变化主导下降。[measured]
  - 数据有效性、聚合键唯一性: pass，未发现空值、非法计数或重复聚合键。[measured]
  - fanout: skipped，未使用 JOIN。[measured]
  - srm: skipped，没有实验分配记录或计划分流比例。[measured]

## Caveats, and what would change the answer

- 所有区间采用独立搜索的二项近似；若存在重复用户、日间相关性或一次搜索多次点击，区间可能不适用或偏窄。[inferred]
- 调整可见流量构成不能消除时间混杂，也不能证明 v3 无害。[inferred]
- 随机对照、明确的回滚阈值、点击口径及加载完成记录，会使结论更可靠。[inferred]

## Provenance

- Metric: `SUM(clicks) / SUM(searches)`；from stated here [guess]，未找到 `metrics.json`，点击是否按搜索去重未获确认。
- Data: `warehouse.db` 中的 `search_daily`、`release_log`，截至 2026-09-13；末日通过完整性启发式检查，但最后完整期间未获加载水位确认。[measured]
- Reconciled: not done（未提供独立仪表盘或来源总量）。[measured]
- Queries and checks: [查询日志](/private/tmp/ds-runs/75a45791f8/analysis/queries.jsonl)、[检查日志](/private/tmp/ds-runs/75a45791f8/analysis/.ds-checks.log)、[计算脚本](/private/tmp/ds-runs/75a45791f8/analysis/analyze.py)、[方法说明](/private/tmp/ds-runs/75a45791f8/analysis/methodology.md)。[measured]
