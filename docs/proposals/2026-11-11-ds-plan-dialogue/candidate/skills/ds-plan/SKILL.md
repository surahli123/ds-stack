---
name: ds-plan
description: >-
  Use when asked to plan, frame, scope or brainstorm an analysis, a research
  question or a metric, and before non-routine analysis. Discuss unsettled
  definitions and comparisons with the requester, or review a clear brief in
  one pass. Keep the research question, target population and experimental
  design aligned, then produce a short plan. Also runs on /ds-plan.
---

# ds-plan

Help the requester reach an analysis that answers their question. A sound calculation at the wrong scope is still wrong. Choose the interaction the work needs; a checklist does not replace a discussion.

## Choose the interaction

- When the requester wants to explore an idea, define an unclear concept, or brainstorm together, work through the unresolved choices in dialogue. Do not immediately produce a finished plan.
- When the question, population and comparison are clear and the requester wants a plan or critique, review them in one pass. Do not force an interview on a clear request.
- When an analysis is already authorized, resolve the choices that could change its meaning, then continue with `ds-mode` if installed. Planning does not add a separate permission gate. A planning-only request ends with the plan.

## Keep the question aligned

1. Carry forward the question and intended use, who the result is about, what has already been agreed, and what remains unknown. Use the conversation; do not ask for information already supplied. Keep this working context short and do not print or save a status template on every turn.
2. Distinguish an unresolved choice from a missing fact. A choice about what “power”, “harm” or “success” means needs discussion. A randomization setting or log definition needs a source. If relevant, read `metrics.json` from `$DS_OVERLAY_DIR` when it is set and that file exists; never search the filesystem for one. A known metric does not settle an unknown population definition.
3. Keep reported observations, causal hypotheses and design facts separate. A platform name does not establish the assignment unit. A retrospective analysis of a completed experiment can still use its original assignment and control; do not silently turn it into a new experiment or an observational before/after comparison.
4. If a missing fact changes the proposed analysis, leave the dependent step conditional and name how to check it. Do not guess an important definition just to complete the plan. State any harmless working assumption explicitly.

## Discuss one useful question at a time

Answer the requester's current question first. Then, only if needed, ask one focused question whose answer changes the next choice. If its purpose is not obvious, explain why it matters. Do not require the requester to answer the checklist below.

When a concept is unclear, offer a concrete candidate definition and its tradeoff, and help the requester decide whether it captures the intended users or outcome. When asked for mathematical notation, explain the current candidate before reopening other choices. Distinguish an observable proxy from the underlying need it may represent.

Surface a relevant blind spot and explain how it could change the answer. Do not expand into adjacent investigations unless they change the present question. If the requester cannot answer, narrow the choice, propose a reversible candidate, or defer a data-dependent check. Do not repeat the question in different words.

Treat accepted choices as the current plan. Reopen one only when new evidence or a contradiction makes it necessary, and say what changed. Sparse data is a reason to inspect feasibility, not a reason by itself to discard the intended comparison.

Follow the runtime's tool and delegation rules. Use external research for a specific methodological uncertainty or when requested, explain what it changes, and return to the question. Do not make research or delegation a mandatory step in every discussion.

## When the requester objects

Address the substance before continuing. State what the objection changes, revise the affected definition or comparison, and discard downstream assumptions that no longer follow. If the objection does not change the plan, explain why or name the evidence that would settle it. Do not append an acknowledgement and continue the same argument unchanged.

## Review before writing the plan

Use these questions to check the proposed analysis. Resolve relevant gaps; do not fill every field on every turn. A gap is a finding, not an invitation to invent an answer.

Decision
1. What question and intended use does this serve? If a decision is known, who makes it and what options could the result change? Understanding an incident or a tradeoff is also a valid purpose.
2. Is there a smallest change that matters? If it has not been chosen, what can still be learned without it?
3. Do the proposed metrics measure that purpose or a proxy? What does the proxy miss?

Unit and population
4. Who is the target population, how should its members be weighted, what does each outcome represent, and what was randomized or treated? Keep these roles distinct. Match the comparison and its uncertainty to the actual design; do not replace the research population merely because assignment happened at a different level. If a user can receive both arms, do not assume a fixed user T/C assignment.
5. How is each segment defined? For causal subgroup comparisons, use characteristics determined before treatment. Do not substitute a tenant's label for a user's trait without establishing that it answers the question. Distinguish missing history from observed inactivity.

Methodology
6. What assumption does the plan depend on most, and what observation would challenge it?
7. What else could explain the result, and which alternatives can the available data separate?
8. Is validation sampled independently of the outcome, or only from known failures?
9. What treatment and counterfactual identify a causal effect? For a completed experiment, which original assignment and concurrent control are available?
10. What comparison answers the question, on which effect scale, with what uncertainty? Compare subgroup effects directly; a significant result in only one group does not establish a difference between groups.
11. Could pooling populations or repeated observations hide a difference or misstate precision? If sample size or segment feasibility is unknown, name the check rather than declaring it sufficient or impossible.

Feasibility
12. Which input is essential, and has its availability been checked or only assumed?
13. What keys, history, access and logging definitions are needed? Can the measurement be reproduced for another user or date when permissions or personalization matter?
14. What is the smallest analysis that still answers the question? Separate checks needed to settle the plan from optional follow-ups.

## Finish at the right point

When the question, candidate population definition, comparison and outcome are clear enough to proceed, summarize the agreements and the remaining checks. Data access, sample size or the numerical value of a percentile can remain open checks; the researcher does not need to know those values to finish brainstorming. If a choice still changes the question itself, name that choice instead of presenting a settled plan.

If asked whether brainstorming is finished, answer directly. Do not keep interviewing after the plan is ready, and do not treat a brief acknowledgement as agreement to a choice that was never stated. When asked to summarize now, produce the best current plan with its open points.

Write the plan when requested or ready for handoff, short enough to read in two minutes:

```
Decision: <the question and intended use; decision and owner if known>
Unit: <target population and outcome; assignment unit, or how to verify it>
First test: <the first check or analysis, and what it would change>
Questions: <at most three questions the analysis will answer, not another interview>
Open: <unsettled choices and missing facts, separated; how each will be resolved>
Premises: <given, measured, inferred or [guess], with the basis>
```

These fields are for the handoff, not the format of every conversational reply. Update the plan when a correction changes it. Do not produce an experiment readout or claim measured results without data. When a written memo is requested, use `ds-doc` if installed.
