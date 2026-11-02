## Answer
Headline: can't tell [inferred]  
治疗组观测 CTR 从对照组的 30.00% 升至 31.20%，高出 1.20 个百分点，但尚不能确认是治疗造成的提升。[measured：数值；inferred：因果判断]
- Observed: +1.200 个百分点（名义 95% 区间：+1.125 至 +1.275）[measured]
- Adjusted: +1.200 个百分点（名义 95% 区间：+1.125 至 +1.275），holding 日期构成 fixed，按两组合并搜索量加权。[measured]
- Causal effect: not identified（需要核验随机分配及入样记录、解释人数失衡，并用随机化单位明细估计区间）。[inferred]

## What it means for 上线决策
未提供会改变上线决定的最小提升门槛；若门槛为 0 个百分点，名义区间完全高于它，若门槛落在 +1.125 至 +1.275 之间，则区间跨越门槛。[measured] 但人数失衡尚未解释，且区间依赖独立搜索假设，当前结果不足以单独支持上线。[inferred]

## Why we believe it
- Alternatives considered:
  - 日期构成差异造成表面提升：ruled out，固定日期构成后差异仍为 +1.200 个百分点，14 天每天均为正。[measured]
  - 分流异常、选择性入样或日志缺失：ruled in 为待排查解释，治疗组每天人数均比对照组少 1,710；现有数据不能区分原因。[measured：人数；inferred：解释]
- Checks run:
  - 日期覆盖与重复：pass，14 天 × 2 组共 28 行，无重复或缺失日期组别。[measured]
  - 数据有效性：pass，数据库完整性检查通过，计数字段无空值、负值或点击数超过搜索数。[measured]
  - 50/50 比例：flag，治疗组每日人数占比约 48.773%；若这些人数是当天独立随机分配用户，单日比例检验 p≈9.4×10⁻¹¹。[measured；假设为 guess]
  - 随机化与用户聚类：could not run，仅有日汇总，无分配记录及用户标识。[measured]

## Caveats, and what would change the answer
- 区间假设每次搜索是独立二元点击试验；重复用户、搜索相关性及一次搜索多次点击均无法核查，因此它们不是已验证的实验效应区间。[guess：假设；inferred：限制]
- 每组每天搜索数恰为人数的 6 倍；需确认字段生成方式。跨日人数合计不能当成去重实验人数。[measured：比例；inferred：限制]
- 补齐指标定义、分配与曝光日志、用户级结果及上线门槛后，可重新判断因果提升和决策意义。[inferred]

## Provenance
- Metric: 暂以 CTR＝总 clicks／总 searches，提升＝治疗组 CTR－对照组 CTR；stated here [guess]，目录中没有 metrics.json。[measured]
- Data: warehouse.db 的 experiment_daily，筛选 ranker_boost，2026-09-17 至 2026-09-30（含首尾）；日期覆盖到 09-30，源数据是否完整入仓无法验证。[measured]
- Reconciled: not done（没有提供仪表盘或独立源数据）。[measured]
- Queries and checks: [计算脚本](/private/tmp/ds-runs/06d11bc29c/analysis/analyze.py)、[SQL、检查及结果日志](/private/tmp/ds-runs/06d11bc29c/analysis/analysis_log.json)。[measured]
