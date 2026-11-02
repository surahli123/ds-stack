## Answer

Headline: can't tell [inferred]  
上线后整体 CTR 从 30.441% 降至 28.615%，下降 1.827 个百分点，但现有数据无法确定其中多少由 v3 导致。[measured；归因判断 inferred]

- Observed: −1.827 个百分点（95% 区间：−1.978 至 −1.675）。[measured]
- Adjusted: −1.817 个百分点（95% 区间：−1.966 至 −1.667），holding 平台×国家的搜索流量占比 fixed，权重取两周占比的平均值。[measured]
- Causal effect: not identified；版本与周次完全重合，需要同期随机分配的 v2/v3 对照才能可靠识别。[inferred]

## What it means for 回滚决策

尚未提供会触发回滚的最小 CTR 损失阈值；观察区间虽全部为负，却不是 v3 因果效应的区间，不能据此判定达到回滚门槛。[inferred] 建议明确门槛并开展随机对照，同时优先排查桌面端下降。[inferred]

## Why we believe it

- Alternatives considered:
  - 平台×国家流量构成变化：ruled out 作为主要解释，构成项仅贡献 −0.010 个百分点。[measured]
  - 桌面端特有变化：ruled in；桌面端下降 2.999 个百分点，移动端下降 0.042 个百分点，但两端均切换了版本，移动端不能直接充当未处理对照。[measured；对照判断 inferred]
  - 同期产品、埋点或用户需求变化：ruled in 作为未排除解释；发布表只记录了 v3 上线，不能证明没有其他变化。[inferred]
- Checks run:
  - completeness: pass；9 月 3—13 日分组行数稳定，两周末搜索量检查均通过；这只是完整性的间接证据。[measured；局限 inferred]
  - completeness: could not run；8 月 31 日—9 月 2 日缺少足够历史基线。[measured]
  - mix_shift: pass；下降主要来自分组内 CTR 变化，而非已观测流量构成变化。[measured]
  - 数据合法性与唯一性：pass；无空值或非法计数，无重复日期×平台×国家×版本键。[measured]
  - fanout: skipped；未使用连接。[measured]
  - srm: skipped；没有随机分流实验或预期分配比例。[measured]

## Caveats, and what would change the answer

- 区间采用独立搜索、二项点击假设；缺少用户级数据，无法校正重复用户相关性，区间可能偏窄。[guess；影响 inferred]
- 固定流量构成后的变化仍是前后相关性，不能排除同期混杂。[inferred]
- 随机对照结果、点击口径说明、加载完成记录及回滚阈值会改变判断。[inferred]

## Provenance

- Metric: CTR = SUM(clicks) / SUM(searches)，from stated here [guess]；未发现 metrics.json，未确认 clicks 是否为至少点击一次的搜索数。
- Data: search_daily、release_log；比较 2026-08-31—09-06 与 2026-09-07—09-13，数据截至 09-13；加载完成状态未经权威记录确认。[measured]
- Reconciled: not done（没有独立仪表盘或源数据可供核对）。[measured]
- Queries and checks: [查询与结果](queries.jsonl)、[分析脚本](analyze.py)、[检查日志](.ds-checks.log)、[计算结果](results.json)。[measured]
