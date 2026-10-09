# Doc types

Four types cover almost every doc in the source corpus. Each one has a job, a reader, a skeleton and a word budget. The budget counts the body only; an appendix is outside it. `doc-tighten` enforces the budget.

## Readout (analysis or experiment result)

Job: tell the reader what the data says and what to do about it. Budget: 600 words.

1. Answer: The result in one or two sentences, with the number and its uncertainty.
2. What it means for the decision: The recommendation and who acts on it.
3. Why we believe it: The evidence, one claim per paragraph, each leading with the claim. Alternatives ruled in or out.
4. Caveats: What would change the answer, and how big the blind spot is.
5. Appendix (optional): Method, queries, sources, extra cuts.

How readouts go wrong in the corpus: they open with data sources and method (76 of 119 docs open with method or status), repeat findings in a second "summary" section, and pack reasoning into table cells.

Opening that works:

> ## Answer
> Keep ranker v2. The 2.1 pp CTR drop comes from more mobile traffic, not from the ranker: CTR inside each platform did not move.

## Memo (decision or recommendation)

Job: get a decision made. Budget: 900 words.

1. The ask: The decision needed, from whom, by when.
2. Recommendation: The option you recommend and the one reason that decides it.
3. Options: Two or three real options, each with cost, benefit and risk. Use a table only if cells stay short facts.
4. Risks and what we'd watch.
5. Appendix (optional).
How memos go wrong: the decision sits in the last third, or nowhere. That happened in 11 of 19 plans and designs.

## Plan

Job: let someone execute or approve the work. Budget: 900 words.

1. Goal and done: What will be true when this is finished, stated so it can pass or fail.
2. Decisions needed now: Anything the reader must settle before work starts.
3. Steps: Numbered, each ending in a checkable result.
4. Risks.
5. Out of scope.
How plans go wrong: a changelog or status block opens the doc, open decisions surface hundreds of lines in, and the same rule is restated in several sections. Only 2 of 11 plans in the corpus had a summary.

## Handover

Job: let the next person (or agent) continue without rereading the history. Budget: 500 words.

1. Current state: One or two sentences: what works, what doesn't, what is mid-flight.
2. Next step: The single next action, with the command or file to start from.
3. Blockers and open questions.
4. Where things are: Paths, branches and links: only the ones the next person will open.

How handovers go wrong: they turn into logs, with dated DONE lines, struck-through items and a status line the body contradicts (6 of 30 handovers). They also fill up with undefined ID codes and session artifacts.

## Not on the list

A doc that teaches (a tutorial or how-to) or describes a system for lookup (reference) follows Diátaxis instead. Use the closest skeleton above and name the change you made in your reply.
