# Plan-stage mistakes (2026-11)

Two plan-stage mistakes from real work met the archive rule, so the plan critique became its own skill, `ds-plan`, which loads on planning requests instead of only inside ds-mode.

## 1. A framing disagreement (2026-10-30)

A PM reads customer feedback as "CJK search quality is poor". The analyst's quality metric (keyword and AI search) says otherwise: one CJK language is clearly worse but small and concentrated in a few large accounts, while a larger, dispersed group of European languages sends little feedback. Asked: how should the analyst frame and research the disagreement?

The agent answered with no lookups and no questions. It got the framing right: split measurement, weighting and unit of analysis; account clustering; suppressed demand. It missed four things:
- it never asked what decision was on the table;
- the first test it recommended validated the metric only on complained-about queries, though a later section proposed a stratified sample;
- it assumed tenant data could be replayed and shown to raters;
- it asked seven questions.

The decision actually made matched none of the three outcomes its decision rule offered (Korean-specific work, a platform fix, neither): prioritize the top five languages, split by region.

This isn't an eval task yet. Graded by keyword over the whole plan, the reply passes items it shouldn't: "data access" in a prompt placeholder reads as naming access. It needs closing lines first, as p2 has.

## 2. Tenant level for a user-randomized test (2026-11)

The requester asked for a plan for a user-randomized test whose question was about 3P users. The agent recommended tenant-level analysis for more power, and defined 3P users by a tenant label. The requester pointed out that a "3P power" tenant also has users who never use 3P content. The agent didn't address it.

The rules this added to ds-plan are questions 4 and 5 (unit and segment) and "When the requester objects". The eval task is `eval/plan/tasks/p2`: two turns, graded by script on the closing lines. Calibrate it on plain prompting before trusting a gain.
