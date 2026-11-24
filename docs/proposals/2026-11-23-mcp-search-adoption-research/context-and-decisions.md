# Context and decisions so far

This is a summary of the discussion between the project owner (the search data scientist) and the assistant that drafted the documents in this folder. It is here so that an agent picking up the work knows what has already been decided and why, and does not reopen those points with the owner.

It sits in a public repository, so it uses the same placeholders as the other files and gives no internal names or observed numbers. Resolve the placeholders by following `meta-prompt.md`.

## The anchor, in five lines

If you read nothing else, hold on to these.

1. The subject is the inside of the agentic search service: its sub-searches and the logic that connects them. The MCP entry side belongs to the MCP team.
2. The question is which types of task truly need agentic search. Findings are about task types, not tenants or users.
3. The owner does research. The owner does not build the service, write the tool description or evaluate description changes.
4. Need is judged by what later rounds contributed, never by how many steps were run.
5. Do the work and report. Do not reopen what is settled below, and do not redo what has already been answered.

## How to use this file

This file can be used on its own. Paste it at the start of any session on this work, with or without the other documents, and reread it before you deliver anything.

Treat the section "Settled" as decided. Work within it. If evidence in the code or data shows that a settled point is wrong, do not open a discussion about it: finish the work, and state the evidence once in your final report.

Treat the section "Tried and dropped" as closed. Do not propose those ideas again unless the owner asks.

The section "Still open" lists the only questions worth raising. Some are for you to investigate; some are for the owner or other teams and are listed so that you leave them alone.

**Keep a living copy.** This public file was written before any internal investigation and is not updated with internal findings. Keep a localised copy in the internal environment and maintain it as the decision log for this work:

- When an open question has been answered, by you in earlier work or by the owner, move it to "Settled" with the answer, the evidence and the date. Check your earlier output and the report's history before you investigate anything in "Still open"; if it is already answered there, record the answer and do not redo the work.
- When the owner decides something new, add it to "Settled" in one or two lines, with the reason if one was given.
- When an idea is rejected, add it to "Tried and dropped" with the reason.
- Where the living copy and this public file differ, the living copy is right.

## Signs that you are drifting

Each of these has already happened once in this project. If you notice one, stop and return to the anchor.

- You are analysing tool-call health on the MCP side: failure categories, latency percentiles by outcome, traffic by day, client or region breakdowns. That is the MCP data scientist's work. Record what exists, pass it on, and return to the service.
- You are adding a field that serves no named research question.
- You are treating a count of steps, rounds or sources as a sign that a request needed agentic search.
- You are proposing wording for the tool description, an experiment on description versions, or a way to measure the effect of a description change.
- You are drawing conclusions about which tenants or users to target.
- You are asking the owner about something under "Settled", or offering the owner a choice between options that "Settled" or "Tried and dropped" already decides.
- You are investigating a question that your own earlier work has answered.
- You have stopped to discuss when you could have chosen the reading that fits the settled points, noted it in one line, and carried on.
- Your output is mostly caveats, appendix references and statements that things are proposals, and an engineer could not act on it quickly.

## The project in one paragraph

The company has an agentic search service, `<AGENTIC_SERVICE>`, reached through the MCP tool `<AGENTIC_TOOL>`. The callers are users' coding agents, which decide for themselves whether to call a tool and which effort to ask for, guided by the tool description. The service is in internal early access and launches to customers soon. The owner studies usage and quality of search to learn which types of task truly need agentic search, so that adoption grows and the tool is used for the right tasks.

## Settled

**Who the user is.** The user is the person. The person does not choose the tool or the effort; their agent does. The person only experiences whether the task got done and how long it took.

**What this team does and does not do.** The owner's team does research. It does not build the service. It does not write the tool description and does not evaluate the effect of description changes; the agentic search team and product do that, and they are already running their own experiments on how agents choose an effort. The owner's findings feed their changes.

**How the work is split between data scientists.** This took the longest to work out and is the point most likely to drift.

- The MCP team and its data scientist own the entry side for MCP: whether a tool is called, entry-side adoption, and tool-call health (success, failure, latency as the caller sees it).
- A CLI data scientist does the same for the CLI entry. The service also serves the CLI, but only MCP traffic is studied for now.
- The owner owns the inside of the service: the sub-LLM calls, the internal sub-searches and the logic that connects them. This is how the owner's manager described it.

A worked example the owner settled on: for the task "trace how a policy changed over the past year and who was affected" and the task "find one named document", the entry side sees no difference, because both need a search. The inside of the service is where they differ: one needs light effort and the other needs agentic.

**Two kinds of repeated search.** A caller's agent issuing several search calls in a row happens on the MCP side and belongs to the entry side. Several sub-searches inside one agentic request happen inside the service and belong to the owner. The owner's subject is the second kind.

**What the owner hands over.** Conclusions about types of task, not about tenants or users. A tool description is one fixed text read by every customer's agent, so a finding about which tenants need agentic search cannot be written into it.

**The loop.** The owner analyses the data. The agentic search team changes the description and the service's behaviour. Callers' agents call the tool. New data comes back to the owner.

**What success looks like.** Two measures, and both are needed.

1. The share of agentic requests that truly needed agentic search goes up. The owner can compute this from the service's own data.
2. Few requests that needed agentic search are missed. This also needs entry-side data from the MCP data scientist, because a request that never reached the service is not in its logs.

The first measure alone can be gamed: a very conservative description sends only the most obvious requests to agentic, the share rises, and many needed requests are missed.

**How the two data scientists depend on each other.** The MCP data scientist has the requests that did not use agentic search. The owner has the internal trace that shows what a request that truly needed agentic search looks like. Neither can answer "who needed it and did not get it" alone.

**How to judge whether a request needed agentic search.** By what the later rounds contributed, not by how much work was done. A count of steps or rounds describes the service when the number of rounds is fixed or capped. Better evidence: the round in which each cited document first appeared; whether sub-queries found different documents (a decomposition) or mostly the same ones (a rewrite); whether one light retrieval on the original query would already have found the cited documents. Requests that failed, timed out, gave no answer or hit a cap are set aside first, because they show neither need nor its absence.

**Working with engineering.** Instrumentation is a joint draft with engineering, who are also designing it. It is not a list of demands. The owner's part is what must be computable and why; engineering's part is what can be logged and at what cost.

**One system of record per field.** Each field is recorded by the layer that alone can see the information. Where both layers see something, one is named as the record. Latency and status are recorded on both sides because they mean different things on each: what the caller experienced, and what happened inside.

**Privacy.** Query text, sub-query text and answer text are not stored and analysts do not read them. Features derived at request time are acceptable subject to a privacy decision. Anything that needs that decision is flagged, not assumed and not worked around.

**Automation accounts.** A small number of accounts produce a large share of search calls. This does not block any decision, but metrics are weighted by person and automation is reported separately.

**The existing report.** Its evidence-first method stays: row counts or a code read behind each field, and the status labels. Its current content is MCP-side data readiness. What it lacks is the inside of the service and the link from each field to a research question.

**Wording.** Say "fallback", not "downgrade", and use `fallback_reason`. The status field must be non-null with defined values, and a forced timeout and a forced client cancel must each be logged as such.

**Public and internal copies.** The files in this public folder are anonymised. Localised versions with internal names and data stay in the internal environment.

## Tried and dropped

- **Requirements aimed at the MCP entry point.** The first template asked for everything to be logged at the MCP server. That was a misreading; the existing report inherited it. The subject is the inside of the service.
- **An evaluation harness for tool descriptions, and candidate description texts.** Out of scope; the agentic search team does this.
- **Routing accuracy as the owner's adoption metric.** It measures the effect of the description, which is not the owner's to evaluate. The owner's measures are the two under "What success looks like".
- **Online experiments that switch description versions.** Only one version can be served at a time during early access.
- **"Call chains got shorter" as a measure of value.** A description that tells agents not to rephrase lowers it mechanically.
- **Reading several search calls in a row as demand for agentic search.** Such chains have three sources: retries after a weak retrieval, the calling agent's habits, and real multi-step need. Only the third counts.
- **Step or round counts, and the number of sources merged, as evidence of need.** See above.
- **Query complexity alone as evidence of need.** Useful as a prior and for stratifying, not as a judgement.
- **Targeting by tenant or user through the description.** See "What the owner hands over".
- **Reorganising the instrumentation document by measure.** The internal report already follows the template's structure; a second structure would make the two diverge.

## Still open

For you to investigate from code and data (details in `meta-prompt.md`):

1. Where executed effort and the fallback reason should be recorded.
2. Whether light-effort requests pass through the service.
3. Which side should lead the service-side check of the join key.
4. Whether the service receives `<INVOCATION_ID_FIELD>`, or another shared key, on every request, including retries and fallbacks.
5. Whether the number of rounds is fixed, decided by the model or mixed, and what the caps and stop conditions are.
6. What the service logs today about its internal steps, and whether any of it holds text.

For the owner or other teams. Note what you find that bears on them, and leave the decision alone:

- Confirming the split of work with the MCP data scientist in person.
- Privacy decisions on derived features and document identifiers.
- Whether findings about tenants or users have any other use. The owner set this aside without deciding.
- Whether a shadow light retrieval is worth its cost. Engineering weighs this.

## Working with the owner

The owner gives short answers and expects the work to move. Do the work and report; do not turn a step into a discussion. When something is unclear, choose the reading that fits the settled points above, say in one line which reading you chose, and carry on. Collect questions and raise them together at the end. Stop early only when nothing useful can be done without an answer, for example if you cannot read the service's logs at all.
