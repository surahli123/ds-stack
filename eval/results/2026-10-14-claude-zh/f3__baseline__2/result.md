## Answer
Headline: can't tell(整体 CTR 的下降是真实的,但没有对照组,无法把它单独归因给 v3)

整体 CTR 从 30.44% 降到 28.61%,下降约 1.8 个百分点。下降全部来自桌面端,移动端几乎没变;这个降幅与 v3 上线同一天出现,但数据里没有同期未使用 v3 的对照。

- Observed: -1.83 pp (95% CI -1.98 ~ -1.68),[measured]
- Adjusted: -1.82 pp (-1.97 ~ -1.67),固定 platform×country 的流量构成不变,[measured]
- Causal effect: not identified(需要保留一部分流量继续用 v2 的 A/B 或 holdout,或在桌面端同期没有其他改动的证据)

## What it means for 是否回滚 v3
这个下降不是流量构成变化造成的,v3 是最主要的嫌疑对象,但"全部归因于 v3"在设计上无法确认。桌面端降 2.9~3.1 pp、置信区间都远离 0,若这些差值有哪怕一半是 v3 导致的(约 0.9 pp),就已经足以影响回滚决定;所以建议先对桌面端做 v2 holdout(小比例流量切回 v2)再定回滚,而不是直接依据这个对比。

## Why we believe it
- Alternatives considered:
  - 流量构成变化(桌面/移动、US/其他占比): 排除,两周占比几乎相同,调整后结果与原始差值一致 [measured]
  - 日常波动/趋势: 基本排除,上线前 7 天稳定在 30.0%~30.8%,上线当天起稳定在 28.3%~28.9%,呈阶跃 [measured]
  - 同期其他改动(如桌面端界面、埋点变化): 无法排除,release_log 仅有 v3 一条记录,但无法证明没有其他改动 [guess]
  - v3 只在桌面端有害: 与数据相符(桌面 US -3.11 pp、其他 -2.87 pp;移动 -0.03、-0.04 pp),但 v3 同时 100% 上线,移动端无变化也可能说明桌面端另有原因 [inferred]
- Checks run:
  - 前后周对比及 CI(双比例正态近似): pass,见上
  - 按 platform×country 分层: flag,效果高度集中在桌面端
  - 逐日走势: pass,上线日出现阶跃,无预先趋势
  - 对照组/并行 v2 流量: could not run,v3 全量上线,数据中 ranker 与周完全重合
  - 点击埋点/日志口径是否变化: could not run,无相关数据

## Caveats, and what would change the answer
- 只有两周数据,ranker 与时间完全混淆,只能做前后对比。
- 区间只反映抽样误差,不包含"同期其他改动"的不确定性。
- 若有桌面端 v2 holdout 或查明同期无其他桌面端改动,即可给出因果估计;若发现桌面端点击埋点同日变更,结论会改变。
- 可能值得看的指标:v3 是否带来下游收益(转化、搜索放弃率),因为 CTR 下降不一定意味着结果变差。

## Provenance
- Metric: CTR = sum(clicks)/sum(searches),按 stated here 定义 [guess](目录中没有 metrics.json)
- Data: search_daily(56 行)、release_log(1 行),2026-08-31 至 2026-09-13,两周均完整
- Reconciled: not done(没有仪表盘或其他来源可对账)
- Queries and checks: 在本次会话中用 Python/sqlite3 内联执行,未保存为文件