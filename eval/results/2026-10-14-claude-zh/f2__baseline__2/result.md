## Answer
Headline: 55.0 %(95% 区间 54.9%–55.0%)

2026-W40 导航类查询的点击率(CTR)为 55.0%,即 59,800 次搜索中有 32,878 次点击。

- Observed: 55.0 %(54.9%–55.0%)[measured]
- Adjusted: not computed(这是单周的描述性指标,没有需要控制的比较或混杂因素)
- Causal effect: not identified(这是描述性数字,不涉及因果问题)

## What it means for 营销规划文档
规划文档可直接引用约 55%。区间只有约 ±0.05 个百分点,不会改变任何规划决策。但必须说明口径是"当前标签版本",因为换用旧标签会得到约 43%。

## Why we believe it
- Alternatives considered:
  - 标签版本混用(旧版 v1 加新版 v2)导致重复计数或口径错误:已排除。只取 `is_current=1`,每个 query_id 恰好一条当前标签。若包含非当前标签,导航类会多出 200 个旧标签查询 [measured]。
  - 使用旧标签 v1 会得到不同数字:这个差异是真实存在的。v1 标签下的导航类 CTR 为 43.0%,当前标签(含 v2 重标的查询)为 55.0%。原因是 100 个查询被重标为 v2,而 v1 标签下的"导航"类里混入了点击率较低的查询 [measured]。
  - 宏平均(各查询 CTR 取平均)与总点击/总搜索的汇总口径不同:影响很小,宏平均为 55.0%,与汇总值一致 [measured]。
- Checks run:
  - 当周每个查询只有一行:pass,1000 行、1000 个不同 query_id。
  - 数据质量:pass,没有空值,没有 clicks 大于 searches 的行。
  - 当前标签唯一性:pass,没有查询有多条当前标签。
  - 区间:pass,按查询做自助法重抽样(bootstrap,2000 次)得出区间。
  - 与外部看板对账:could not run,没有可用的看板。

## Caveats, and what would change the answer
- 数据里只有 W40 一周,无法与其他周比较或看趋势。
- 数字取决于"当前"意图标签。如果营销部门使用旧标签口径,答案是 43%。需要确认他们用的口径。
- 区间很窄,是因为样本量大(400 个查询、59,800 次搜索)。它只反映抽样波动,不包含标签错误的影响。
- 我没有看到 CTR 的正式定义(没有 metrics.json),这里按 点击数 ÷ 搜索数 计算 [guess]。

## Provenance
- Metric: CTR = 点击数之和 ÷ 搜索数之和,限定 intent='navigational' 且 is_current=1,来自 stated here [guess]
- Data: query_stats、query_labels,截至 2026-W40(库中仅有这一周)
- Reconciled: not done(没有看板或其他来源可对账)
- Queries and checks: 在本次会话中以内联 Python/SQLite 运行,没有保存到文件。