## Answer
Headline: can't tell [inferred]

整体 CTR 从 30.441% 降至 28.615%，下降 1.827 pp，但其中多少可归因于 v3 无法识别。[q7] [measured] [inferred]

- Observed: -1.827 pp (95% CI: -1.978 至 -1.675) [check:mix_shift#1] [measured]
- Adjusted: -1.817 pp (95% CI: -1.966 至 -1.667), holding 平台×国家的两周平均搜索占比 fixed；这是描述性调整，不是版本效果。[check:mix_shift#1] [measured]
- Causal effect: not identified (需要同期随机保留旧版本的对照组，或具有可信反事实和可验证假设的准实验) [inferred]

## What it means for 回滚决策
尚未提供会触发回滚的最小因果损失门槛；调整后下降幅度的区间为 1.667–1.966 pp，若门槛低于下界，描述性下降已超过门槛，若落在区间内则仍有统计不确定性。[check:mix_shift#1] [inferred]

这个区间不是因果区间，因此不能据此断定回滚会恢复多少 CTR；应通过随机旧版保留组或随机回切验证归因。[inferred]

## Why we believe it

- Alternatives considered:
  - 已观测流量构成是主要解释：ruled out，平台×国家构成变化仅对应 -0.0099 pp；仅按平台调整也得到 -1.8173 pp，与细分结果一致。[check:mix_shift#1, check:mix_shift#2] [measured]
  - 星期覆盖不同：ruled out，两周均覆盖完整星期，逐星期配对均下降；更广泛的季节性或同期冲击仍未排除。[q7, q8] [measured] [inferred]
  - 缺日、重复汇总行：ruled out，每天均有完整分组，无重复键或非法计数；源端漏记仍无法排除。[q3, q4, q5] [measured] [inferred]
  - 日志或口径变化：ruled in（仍可能，并非已证实），没有埋点审计或独立来源可核对，发布日志只记录了版本上线。[q1, q2] [inferred]
  - v3 导致下降：ruled in（候选解释，并非因果证据），旧版和新版与前后周完全重合；桌面端明显下滑、移动端相对稳定，但两端都接受新版，移动端不能直接充当未处理对照。[q3, q6] [inferred]
- Checks run:
  - completeness: could not run 首日无更早历史：could not run: need at least 3 earlier periods (trailing days (under 3 weeks of same-weekday history)) before 2026-08-31, got 0 [check:completeness#1] [measured]
  - completeness: pass 2026-09-06: 4 rows = 100% of the trailing days (under 3 weeks of same-weekday history) median (4) [check:completeness#2] [measured]
  - completeness: pass 2026-09-13: 4 rows = 100% of the trailing days (under 3 weeks of same-weekday history) median (4) [check:completeness#3] [measured]
  - mix_shift: pass 平台×国家：overall change -1.83 pp = within-segment -1.82 pp (95% CI -1.97 to -1.67) + mix -0.01 pp (mix share 1%) [check:mix_shift#1] [measured]
  - mix_shift: pass 平台：overall change -1.83 pp = within-segment -1.82 pp (95% CI -1.97 to -1.67) + mix -0.01 pp (mix share 1%) [check:mix_shift#2] [measured]
  - 日期覆盖与键唯一性: pass 两周各 7 天、28 个分组日，重复行 0。[q5, q7] [measured]
  - fanout: skipped 未做表连接。[inferred]
  - srm: skipped 无随机分组或预定分配比例。[q1, q3] [inferred]

## Caveats, and what would change the answer

- 区间假设搜索相互独立且 clicks 表示发生点击的搜索数；用户重复搜索、时间相关性会使区间偏窄，需要事件级定义和用户级数据复核。[inferred]
- 行数齐全不等于源端完整；需加载完成标记、埋点审计和看板对账确认。[inferred]
- 未观测查询意图、渠道等构成，也没有足够的上线前历史验证趋势；更细数据和同期随机对照可能改变归因。[inferred]

## Provenance

- Metric: SUM(clicks) / SUM(searches)，来自 search_daily，按搜索量加权；纳入 2026-08-31 至 2026-09-06 和 2026-09-07 至 2026-09-13 的全部平台、国家及版本，无其他过滤；源粒度为日期×平台×国家×版本，from stated here [guess]（DS_OVERLAY_DIR 未设置，无可用 metrics.json）。
- Data: search_daily、release_log，through 2026-09-13（最后有数据且日分组齐全的日期，源端完成状态未认证）。[q3, q7] [measured]
- Reconciled: not done (无独立看板或可信源汇总可核对)。[q1] [measured]
- Queries and checks: .ds-queries.log、.ds-checks.log；检查重放脚本 analyze.py；报告 readout.md。
- Verified: verify_readout: pass (39 numbers on 11 lines; 8 queries, 5 checks, 0 given)
