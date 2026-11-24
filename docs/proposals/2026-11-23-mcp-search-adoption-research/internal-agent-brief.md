# Standing brief for revising the agentic search instrumentation report

## Placeholders

This file sits in a public repository, so internal names are replaced by placeholders and no observed numbers are given. Resolve the placeholders by following `meta-prompt.md` in the same folder before you use this brief: establish each value from evidence, and leave a placeholder in place rather than guess. Once they are resolved, your mapping can replace this table.

| Placeholder | Stands for | Where its real value is likely to be found |
|---|---|---|
| `<REPORT_TITLE>` | The title of the existing report this brief governs | The report itself and its revision history |
| `<AGENTIC_SERVICE>` | The internal name of the agentic search service | The audience line and summary of the existing report; the service's code repository; the MCP handler code that calls the service |
| `<AGENTIC_TOOL>` | The name of the MCP tool through which callers' agents reach the service | The tool filter in the "Source" line of the existing report; the tool registration in the MCP handler code |
| `<INVOCATION_ID_FIELD>` | The MCP invocation ID: the field the MCP handler sets as its event correlation ID | The MCP handler code; the call-identity row and the join-key question of the existing report |
| `<MCP_EVENT_TABLE>` | The MCP-side event table the existing report audits | The "Source" line of the existing report |
| `<SERVICE_LOG_SOURCE>` | Where the agentic search service writes its request logs and traces | Logging and tracing calls in the service's code; the data catalogue; the service owner. The existing report does not name it |

---

You maintain the report `<REPORT_TITLE>`. This brief explains what the report is for, so that each revision serves that purpose and you can make good calls in cases it does not cover.

## What the research is for

The agentic search service, `<AGENTIC_SERVICE>`, sits behind the MCP tool `<AGENTIC_TOOL>`, which users' coding agents call. It is in internal early access before its customer launch, and only its MCP traffic is studied for now. The search data scientist who owns this report wants to find which types of task truly need agentic search, so that the agentic search team can change the tool description and the service's internal behaviour. This runs as a loop: analysis, a description change, new calls from callers' agents, new data. Success has two measures: the share of agentic requests that truly needed agentic search goes up, and few requests that needed it are missed. The first comes from the service's own data; the second also needs entry-side data held by the MCP data scientist, because a request that never reached the service is not in its logs.

The readers are the search data scientist, the service's engineers who will add the logging (the report is a joint draft with them, not a list of demands), the MCP team and the MCP data scientist. A good revision shows, field by field, whether the data can answer a research question yet and what would close the gap.

## Where the boundary sits

The subject is the inside of the service: the sub-LLM calls, the internal sub-searches, the logic that connects them, and why a request stops. That is where need shows; the MCP row records that a call happened, not what the service did. MCP-side tool-call health (whether a tool is called, entry-side adoption, call success and failure, latency as the caller sees it) belongs to the MCP team and its data scientist. Record what MCP-side data exists and what this research needs from it, and pass gaps to the MCP team rather than turning them into this team's work.

Each field has one system of record, the layer that alone can see the information: requested effort at the MCP entry, executed effort and fallback reason inside the service. Your own code read shows why this matters: today these are written only into the tool response, and a recovery from agentic to light shows as a success on the MCP row. The two sides meet at the join key. The MCP side sets its correlation ID to the MCP invocation ID (`<INVOCATION_ID_FIELD>`); whether the service receives it, or another shared key, on every request including retries and fallbacks, has not been checked. Until it is, the service's records cannot be tied to a caller.

## What belongs in the report

A field belongs if it serves a named research question, and the report should say which: R1 usage, R2 quality of current search, R3 latent demand (including whether an agentic request was needed), R4 adoption, R5 value. A field that only serves entry-side tool-call health belongs to the MCP side.

## What to keep and what to change

Keep the evidence-first method: each field carries row counts or a "code read" basis and a status label (USABLE NOW, PARTIAL, OPEN, BLOCKED). That is what turned a requirements list into a gap list. Then:

- re-title the existing content as MCP-side data readiness, and stop extending it;
- add the section on the inside of the service, starting from the draft section that came with this brief;
- give every field the research question it serves;
- move the join-key check to the top of the questions and the priorities;
- take MCP-health investigations (long and fast failures by day, latency percentiles by outcome, profiling MCP columns) out of the search data scientist's priorities and offer them to the MCP data scientist.

## What to do first

Audit what the service logs today in `<SERVICE_LOG_SOURCE>`, to the same evidence standard you applied to `<MCP_EVENT_TABLE>`, and fill the "Observed evidence" column of the service section. Where you could not look, write "not yet audited".

## Why a step count is not evidence of need

If the service runs a similar number of rounds for every request, or stops at a budget cap, the count describes the service rather than the request, and empty or permission-filtered retrievals add rounds to requests that are hard rather than needed. Need shows in what the later rounds contributed: whether cited documents first appeared after the first round or came from a sub-query that found different documents, and whether one light retrieval on the original query would have found them. So the round of each step, how each query was produced, cited documents and stop reason matter more than any count.

## Privacy

Query, sub-query and answer text are not stored, and analysts do not read them. Derived features computed at request time (lengths, keyed hashes, a similarity scalar, coarse labels), document identifiers, step types, timings, scores and cited documents are usable subject to a privacy decision. When a field needs that decision, flag it in the table and leave the decision to the privacy review, rather than assuming approval or finding a workaround.

## Stating uncertainty

The current report repeats that things are proposals or unverified in many places and sends readers to appendices. State each uncertainty once, where it applies, in plain words; one line at the top of a section is often enough. Engineers should be able to read a table quickly and act on it.

## Before you deliver a revision

- Does each new or changed field name the research question it serves?
- Is anything here entry-side tool-call health work that belongs to the MCP data scientist?
- Does each row of the service section have evidence, or an explicit "not yet audited"?
- Is the join-key check first, and does it cover retries and fallbacks?
- Does anything read a step or round count as evidence of need?
- Does anything store or read text, or assume a privacy approval not yet given?
- Is each uncertainty stated once, where it applies?
