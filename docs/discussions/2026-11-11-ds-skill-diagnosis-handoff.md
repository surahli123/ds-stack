# ds skill 只读诊断与后续交接

> 后续更新 2026 年 11 月 12 日：本地修改与审阅已完成，详见[最新实施与审阅记录](../implementation/2026-11-12-ds-plan-dialogue/review.md)。以下内容保留为历史诊断快照，不代表当前 skill 或实现状态；尚未通过真实模型对比证明讨论效果改善。

> 后续更新 2026 年 11 月 11 日：用户已确认 Claude Code session 停止。本轮已核实最新 main 新增了 ds-plan 和两轮评测；以下旧快照的部分判断已过时。请先阅读[新的诊断与修改提案](../proposals/2026-11-11-ds-plan-dialogue/proposal.md)。原记录保留用于追溯，正式 skill 仍未修改。

记录日期：2026 年 11 月 11 日
状态：候选诊断，未修改 skill，未完成原故障复现

## 当前工作边界

用户要求先交付真实业务讨论稿，再继续诊断 skill。另一个 Claude Code session 正在修改同一套 skill；**本 session 的 skill 修改必须等该 session 结束，再读取最新文件与 diff 后进行。**目前仅新增讨论稿和本笔记，没有改动 skill、README、eval 或全局配置，也没有 stash、切分支、commit 或 push。

真实业务稿独立保存在 [3p 高频用户实验回溯分析讨论稿](2026-11-11-3p-power-user-retro.md)，不包含 skill 诊断、模型审阅或调试过程。

诊断使用本机 Compound Engineering 的 `ce-debug`，本次可读取的版本为 `3.38.1`。原记录中的 `3.38.0` 路径已不存在。原失败会话位于另一台机器，当前没有其完整 transcript 或当时实际加载的 skill 版本。本次案例走查已知原故障，不能称为独立盲测或原故障复现。

## 问题与证据分层

**用户报告的原故障**：原 agent 在讨论 3p power user 的影响时，因 Statsig 过早要求转向 tenant level，偏离用户研究对象，导致后续方向与表达不符合需求。用户已确认原 agent 承接过 SEV 背景，因此“没有理解 SEV 背景”不是已成立诊断。

**本次走查中观察到的问题**：曾从 3p power 扩展到整体 search power；未解释用途就追问跨月数据；因点击稀疏而过早否定频次分组；曾默认相对降幅优先；未及时保持已结束实验的 retro 语境；没有清楚说明 brainstorm 何时完成。这些是本次对话的行为证据，不等于远程 session 的逐字记录。

**本地静态证据**：当前文件对计算、检查与最终 readout 有明确约束，对多轮形成问题及纠偏没有同等明确的流程。静态文本支持设计风险判断，尚不能确认它导致了远程原故障。

## 优先调查的设计缺口

### 1 问题形成阶段容易过早收敛

`skills/ds-mode/SKILL.md:22` 要求用一句话复述问题，随后第 23 行进入指标定义，第 24 至 26 行才规定歧义与可回答性的处理。澄清条件主要是“两种理解产生 materially different numbers”。

`skills/ds-mode/references/plan-critique.md:3` 明确 critique 是 optional，且未接入主流程；第 5 行明确写着：

> One pass, by the analyst, in writing, before the first query. No multi-round Socratic loop, no web search, no subagent orchestration.

**候选因果链**：用户提出尚未定义 power 的业务问题 → agent 很快生成一句合理复述 → 主流程进入指标和计算 → 可选的一次性自审没有与用户逐步校准定义 → 用户真正关心的人群、效应尺度或分析时态被过早锁定。

这是目前最值得优先验证的设计假设。它说明的是流程可能促进过早收敛，不能推出“一次性自审毫无价值”或“每个问题都必须多轮讨论”。

**竞争解释**：模型本身对 Statsig 或实验单位作了无依据的联想，或运行时加载了额外指导；即使补上多轮阶段也可能发生。当前 skill 没有要求 tenant level，因此不能把那次选择直接归因为文件里的明确规则。

### 2 缺少对研究对象与推断单位的持续区分

原故障把实验平台、随机化单位、研究对象混在一起。本次目标是用户影响；实际随机化单位会影响推断，但不能仅凭平台名称替换研究对象。

当前主流程虽要求 metric grain（`skills/ds-mode/SKILL.md:23`），但没有明确要求在 brainstorm 中分别维护研究对象、处理分配单位和结果聚合方式。这是可检验的缺口，不是对原随机化单位的推断。

### 3 对题检查存在但偏后置

`skills/ds-mode/SKILL.md:14` 已明确指出回答错误问题也算错，不能说现有 skill 完全不关心对题。

但 `skills/ds-mode/references/review-checklist.md:20` 才进入“Is it the question that was asked?”。主流程仍以计算、机械检查和最终固定 readout 为中心（`skills/ds-mode/SKILL.md:27` 至第 32 行；第 61 行及以后）。

**待验证的风险**：最终审阅发现跑偏时，分析与 token 已经花出去了。需要调查能否在进入计算前及用户纠正后，用简短状态确认更早发现方向变化。

### 4 当前已查看的评测入口未证明能覆盖多轮纠偏

`eval/run_arms.py:98` 构建固定任务 prompt，第 130 行使用 `claude -p`，第 208 行将构建好的 prompt 交给该调用。所查看的这个入口以固定任务完成为单位。

这不足以证明整个项目完全没有多轮覆盖；目前只能说，不能用此入口的通过结果证明“用户纠正研究对象后，agent 能连续多轮保持方向”。后续应结合 Claude Code 已完成的评测变更再判断缺口。

## 后续验证方案

等待 Claude Code 完成后，先读取其变更范围、最终 skill、相关引用文件和已有 eval，判断上述缺口是否仍存在。不要根据本笔记的旧快照直接覆盖文件。

若仍需改动，先设计短小的多轮行为场景，再决定最小修改。候选场景包括：

| 场景 | 应观察的行为 | 该场景不能证明什么 |
| --- | --- | --- |
| 仅给出 Statsig 和 power user 问题 | 保持用户研究对象；明确哪些实验信息未知 | 不能证明实际随机化或数据正确 |
| 用户纠正为只研究 3p power | 下一轮保持该范围；后续问题能解释其用途 | 不能证明最终分组有业务效度 |
| 说明多数用户只有一次点击 | 先查看频次尾部与并列问题，再判断 P80 是否可用 | 不能证明实际存在非空高频与轻度组 |
| 用户说明实验已结束 | 保持 retro 语境，优先利用原实验记录 | 不能证明原随机设计有效 |
| 用户接受 P80 后问是否 brainstorm 完成 | 区分已定选择、待数据核实项和真正待决策项，清楚交接到下一阶段 | 不能证明后续 SQL 与统计推断正确 |

优先复用已有评测负责行为的入口；是否需要新建多轮 runner，要在检查另一 session 的变更后再定。当前不创建回归测试、不运行修复实验，也不宣称根因已被验证。

## 诊断摘要

- **Problem**：用户期望循序讨论并发现盲区，现有行为却过早选定分析方向，且用户纠正后仍有漂移。
- **Root Cause**：尚未确认。优先假设是缺少明确的问题形成与持续纠偏阶段；竞争解释为模型误判、额外运行时指导或实际加载版本不同。
- **Recommended Tests**：在已有评测基础上验证上述多轮行为，覆盖方向保持与阶段交接；不以文本格式检查代替行为验证。
- **Fix**：diagnosis only；没有 skill 修改。等待另一个 Claude Code session 结束是用户明确要求。
- **Prevention**：待验证后决定是否增加前置问题校准、用户纠正后的范围维护与多轮评测。
- **Confidence**：对本地文本中的流程缺口为中等；对原远程故障的具体因果链为低。

## 本次读取快照

读取时的 repo HEAD：`6437623fc68447b674b42390b0c4c21eb34ab238`。HEAD 不代表另一 session 已结束，也不保证工作区静止。

| 文件 | SHA256 |
| --- | --- |
| `skills/ds-mode/SKILL.md` | `8145c164ffff226b16520e30b785a28a91f0d4008bce52e263a80c50302b214b` |
| `skills/ds-mode/references/plan-critique.md` | `b4639728cfe0265c9d8775ed7db733ff8ce7531e819bb1ced579fda1980b30a8` |
| `skills/ds-mode/references/review-checklist.md` | `e05cb01ac7b5bf50fa064a4be64e9e0d3505a5e9886124cd14746a29ade742e1` |

初始已有改动：`README.md`，以及未跟踪的 `eval/results/2026-10-14-codex-en/`、`eval/results/2026-10-14-codex-zh/`。这些内容不属于本 session 的修改范围。
