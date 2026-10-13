# Plan critique

Optional, and not wired into ds-mode's method. Use it only for a non-routine analysis: a new metric, a causal question with no randomized test, a decision that is costly to reverse, or a request you can't restate in one sentence. It gets wired into the method only if the work log shows plan-stage mistakes twice.

One pass, by the analyst, in writing, before the first query. No multi-round Socratic loop, no web search, no subagent orchestration.

Answer each question in a line or two. An answer of "looks fine" doesn't count: most plans have at least one gap, so name it. A question you can't answer is a finding. Either settle it before querying, or carry it into the readout's caveats. If an answer changes the plan, change the plan first.

## Methodology: is the plan sound?

1. What is the one assumption the plan leans on most, and what result would show it is wrong?
2. What could explain the result other than your hypothesis, and which of those can the data separate?
3. Is the metric a valid measure of what the decision cares about, or a proxy (engagement for satisfaction)?
4. For a causal question: what did the treatment do, how are treated units identified (not from the outcome), and what is the counterfactual?
5. Is the sample large enough for the smallest effect that matters?
6. Do different populations (new and returning users, platforms) behave differently enough that pooling them could mislead?

## Decision: will it change what someone does?

1. What decision does this feed, who makes it, and what would they do differently on each plausible answer?
2. What is the smallest change that would alter the decision? The interval gets compared with this number.
3. Are the metrics the ones the decision-maker tracks? If not, how do they map?
4. Can you write "therefore we should..." now? If not, the question isn't ready.

## Feasibility: can it be done with what exists?

1. What is the one input everything depends on? Have you queried it for the period you need, or do you only think it exists?
2. What else does the plan assume exists: a join key, a label, a baseline period, access?
3. What is the smallest version that still answers the question?
4. Does the plan ask more than three questions? Cut it to the one the decision needs.

## Afterwards

Write three to five lines in the work log: what changed in the plan, which questions are still open, and what the Answer will say if they stay open. Then follow the method in `SKILL.md`.
