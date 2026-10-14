## Answer
Headline: 46.05%(95% 区间 45.93%–46.17%)
2026-10-05 至 10-11 这一周,外部真实用户的搜索 CTR 为 46.05%,即约每两次搜索中有近一次产生点击。[measured]
- Observed: 46.05%(95% 区间 45.93%–46.17%),口径为外部流量中"有点击的搜索数 / 搜索数" = 321,780 / 698,782。区间是按二项分布对每次搜索独立计算的,所以只反映抽样波动,不含口径选择带来的差异。[measured]
- Adjusted: not computed(只报告单周水平,没有对比对象需要调整)
- Causal effect: not identified(这是描述性指标,没有对照或干预设计)

## What it means for 每周业务回顾
这是单周水平值,没有环比或同比,所以数据本身不支持"上升"或"下降"的判断。因为口径选择会让数值在 41.4% 到 46.1% 之间变动,所以采用的口径比抽样误差(±0.12 个百分点)重要得多。

## Why we believe it
- Alternatives considered:
  - 全部流量(含 bot 和内部):41.41%(347,425 / 838,961)。ruled out,因为 bot(CTR 约 1.97%)和内部流量(67.2%)会扭曲真实用户的行为。[measured]
  - 点击数 / 搜索数:外部为 64.5%,内部超过 100%。ruled out,因为一次搜索可以有多次点击,所以这个比值不是 0–100% 的比率。[measured]
  - 分母改用有结果的搜索:没有计算,因为没有给出指标定义。[guess]
  - 桌面端与移动端的差异:外部流量中桌面端 46.06%、移动端 46.04%,基本无差异,所以平台不影响汇总口径。[measured]
- Checks run:
  - 日期完整性:pass,7 天每天都有 6 行(2 个平台 × 3 种流量类型)。[measured]
  - 周内日度波动:pass,各日搜索量在 11.7 万到 12.3 万之间,无异常日。[measured]
  - 与外部看板或 metrics.json 核对:could not run,环境中没有这两样东西。

## Caveats, and what would change the answer
- 没有 metrics.json,CTR 定义是我的假设:排除 bot 和内部流量,取有点击的搜索占比。如果业务回顾使用全流量口径,数值是 41.4%,需要先和看板的口径对齐。[guess]
- 数据只有这一周,没有历史可比较,也没有做趋势或异常判断。
- 把 bot 流量从分母中剔除,依赖 traffic_type 标注准确。[inferred]

## Provenance
- Metric: CTR = 外部流量中 searches_with_click / searches,来源 stated here [guess]
- Data: search_daily_v,覆盖 2026-10-05 至 2026-10-11(整周完整)
- Reconciled: not done(没有可对照的看板或来源)
- Queries and checks: 查询是直接用 Python 对 warehouse.db 运行的,没有保存为文件,结果都在上面的对话记录中。