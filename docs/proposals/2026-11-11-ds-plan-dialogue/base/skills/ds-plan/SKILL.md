---
name: ds-plan
description: >-
  Use when asked to plan, frame, scope or brainstorm an analysis, a research
  question or a metric, and before any non-routine analysis: a new metric, a
  causal question with no randomized test, a costly decision, a disagreement
  about what the data says, or a request you can't restate in one sentence.
  Checks the decision, the unit of analysis, the data and the scope before
  the first query, and ends with a short plan. Also runs on /ds-plan.
---

# ds-plan

A plan that answers the wrong decision, at the wrong unit, or with data nobody can reach is wrong however rigorous the rest is. Catch that before the first query, in one pass, in writing. No multi-round Socratic loop, no web search, no subagents.

## Before answering

1. If `$DS_OVERLAY_DIR` is set and holds `metrics.json`, read it and name the metric, its grain and its pitfalls in the plan instead of hedging on them. Never search the filesystem for one.
2. If the decision or the metric is still unknown, ask at most two questions. When no one can answer, state the premise, label it `[guess]` and go on.

## Questions

Answer each in a line or two. "Looks fine" doesn't count: most plans have a gap, so name it. A question you can't answer is a finding: settle it before querying, or carry it into the plan's open questions. If an answer changes the plan, change the plan first.

Decision
1. What decision does this feed, who makes it, and what are the options, including scope (which segments, markets or items come first)? What would they do on each plausible answer?
2. What is the smallest change that would alter the decision?
3. Are the metrics the ones the decision-maker tracks? If not, how do they map?

Unit
4. Which unit was randomized or treated, and which unit does the question ask about: user, tenant or account, query, session? Estimate at the unit the question names, never coarser than the randomized one. Rolling a user-randomized test up to tenants doesn't buy power; it leaves fewer units. To use tenants, stratify by them in the user-level analysis, and cluster intervals by tenant only when tenants were treated whole.
5. How is each segment defined? Use the analysis unit's own attribute, measured before the test started. A tenant label put on users (a "power" tenant) also covers users without the trait: say how many, or use each user's own behavior.

Methodology
6. What is the one assumption the plan leans on most, and what result would show it is wrong?
7. What else could explain the result, and which of those can the data separate?
8. Is the metric a valid measure of what the decision cares about, or a proxy (engagement for satisfaction)? If you test that, is the test sample drawn independently of the outcome, or only from known failures?
9. For a causal question: what did the treatment do, how are treated units identified (not from the outcome), and what is the counterfactual?
10. Is the sample large enough for the smallest change that matters, counting the clustering from question 4?
11. Do populations differ enough (new and returning users, platforms) that pooling them could mislead?

Feasibility
12. What is the one input everything depends on? Have you queried it for the period you need, or do you only think it exists?
13. What else does the plan assume: a join key, a label, a baseline period, access to the rows? Can a result be reproduced for another user and date (permissions, personalization, index state)?
14. What is the smallest version that still answers the decision?

## When the requester objects

Answer the objection before anything else: say whether it holds, with evidence or the query that would settle it, and change the plan if it does. Don't restate the earlier argument.

## The plan

Reply with this, short enough to read in two minutes:

```
Decision: <the decision, who makes it, the options>
Unit: <the unit of analysis, and why it matches the decision>
First test: <the one analysis to run first>; it fails if <result>
Questions: <at most three, the ones the decision needs>
Open: <questions above you couldn't answer, and what the answer will say if they stay open>
Premises: <each one labeled measured, given or [guess]>
```

When the plan feeds an analysis, follow the `ds-mode` skill next, if it is installed.
