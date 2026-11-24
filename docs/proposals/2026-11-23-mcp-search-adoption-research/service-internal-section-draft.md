# Draft section: inside the agentic search service

## Placeholders

This file sits in a public repository, so internal names are replaced by placeholders and observed numbers are left out; facts are stated qualitatively. Resolve the placeholders by following `meta-prompt.md` in the same folder: establish each value from evidence, and leave a placeholder in place rather than guess. Where the existing report holds an observed value for a fact stated here, it can be restored during localisation. Remove this table when pasting the section into the report.

| Placeholder | Stands for | Where its real value is likely to be found |
|---|---|---|
| `<AGENTIC_SERVICE>` | The internal name of the agentic search service | The audience line and summary of the existing report; the service's code repository; the MCP handler code that calls the service |
| `<AGENTIC_TOOL>` | The name of the MCP tool through which callers' agents reach the service | The tool filter in the "Source" line of the existing report; the tool registration in the MCP handler code |
| `<INVOCATION_ID_FIELD>` | The MCP invocation ID: the field the MCP handler sets as its event correlation ID | The MCP handler code; the call-identity row and the join-key question of the existing report |
| `<MCP_EVENT_TABLE>` | The MCP-side event table the existing report audits | The "Source" line of the existing report |
| `<OPT_OUT_FIELD>` | The usage-data opt-out column that the existing report filters on | The "Source" line of the existing report; the schema of `<MCP_EVENT_TABLE>` |
| `<SERVICE_LOG_SOURCE>` | Where the agentic search service writes its request logs and traces | Logging and tracing calls in the service's code; the data catalogue; the service owner. The existing report does not name it |
| `<RUN_BUDGET>` | The service's run budget: the time limit after which a call is ended | The existing report's analysis of failed calls that reach the run budget; the service's configuration |

---

## Inside the agentic search service (`<AGENTIC_SERVICE>`)

This section covers what happens inside the agentic search service after a `<AGENTIC_TOOL>` call reaches it: the tier it runs, each round of sub-queries and retrievals, the documents it reads and cites, and why it stops. It sits apart from the MCP-side tables because only the service can see these steps, so the service is their system of record and the MCP row only needs to share a key with it. The service's logs have not been audited yet, so the evidence column is mostly empty; field names, expected values, acceptance checks and leads in this section are proposals, and engineering may already use different names.

### What we log now and what to log next

The table follows one agentic request through the service, from arrival to stop. "What we log now" uses only what the audit of `<MCP_EVENT_TABLE>` and one read of the MCP handler code established, on a short window of mostly internal traffic. Nothing on the service side has been checked.

| Step in a call | What we log now | What to log next |
|---|---|---|
| Request received and joined to the MCP call | The MCP side sets its event correlation ID to the MCP invocation ID, `<INVOCATION_ID_FIELD>` (code read). Whether the service receives it, or another shared key, is not checked. A client retry gets a new invocation ID, there is no client request ID, and the MCP session ID is documented as unreliable | The shared key on every service request, retries and fallbacks included; the service's own request ID; entry surface; tenant and user passed through; start and end time (question 4a) |
| Tier decided and any fallback | Code read: requested effort, executed effort and fallback reason are written only into the tool response and are not logged. A recovery from agentic to light stays inside one call, and the recovered call shows as a success | Executed effort and fallback reason, logged by the service where the decision is made. Requested effort belongs on the MCP row, a request for the MCP team (question 5a) |
| Each round of sub-queries | Not audited. The MCP row has no step count | Round index on every step, and how each retrieval query was produced: original, rewrite, decomposition or follow-up, with no text (questions 6a, 6d) |
| Each retrieval step and what it returned | Not audited | Step type, timing, status, result count, top score and document IDs with rank. One shadow light retrieval on the original query, on every request or a recorded sample (questions 6b, 6c) |
| Documents read | Not audited | Document IDs read, and distinct documents and sources per request. Document IDs need a privacy decision |
| Synthesis and citations | Not audited | Cited document IDs with source, answer length and an answer flag (`ok`, `low_confidence`, `no_answer`). No answer text |
| Stop | Not audited. The service has a run budget (`<RUN_BUDGET>`); which layer enforces it is not checked | Stop reason, and which cap was hit when a budget ends the request (question 6a) |
| Versions and configuration | Not audited | Service, model, ranker and index versions on every request, and a change log for budgets, caps and time limits |

Today none of these steps can be counted. The MCP row shows that a `<AGENTIC_TOOL>` call happened and how long the caller waited. It does not show which effort was requested or run, whether the service fell back, how many rounds it ran, or what each round found.

### Field requirements

Research question: R1 usage, R2 quality of current search, R3 latent demand, including whether an agentic request was needed, R4 adoption, R5 value. A field that serves none of them does not belong in this section. Nothing here can be backfilled: a request logged without its trace cannot be rebuilt, and no text is kept to replay.

| Analysis need | Research question | Field in `<SERVICE_LOG_SOURCE>` | Expected value (proposed) | Observed evidence | Acceptance check (proposed) |
|---|---|---|---|---|---|
| Join: MCP call | R1–R5 | `<INVOCATION_ID_FIELD>`, or another shared key | Same value as on the MCP row, on every request including retries and fallbacks | **OPEN**: the MCP side sets its correlation ID to the invocation ID (code read); service side not yet audited | Non-null on every MCP request; at least 99% join to an MCP row; unjoined requests counted |
| Join: service request | R1–R5 | `svc_request_id` | One ID per service request | **OPEN**: not yet audited | Unique; state whether one MCP call can map to several service requests |
| Scope: entry surface | R1–R5 | `entry_surface` | `mcp`, `cli` or `other` | **OPEN**: not yet audited | Test requests through MCP and the CLI are labelled correctly |
| Join: tenant and user | R1, R3, R4 | `tenant_id`, `user_id` | Passed through unchanged; the MCP row is the record | **OPEN**: not yet audited | Equal to the MCP values on all joined pairs |
| Internal time | R4, R5 | `svc_ts_start`, `svc_ts_end`, `svc_latency_ms`, `svc_ttfb_ms` | Received to last byte, and to first byte; ms, UTC | **OPEN**: not yet audited | End after start; on joined pairs, inside the MCP interval within the agreed clock skew |
| Internal outcome | R2, R4 | `svc_status`, `svc_err_code` | `ok`, `error`, `timeout`, `cancelled` or `rejected`; error code naming the failing component | **OPEN**: not yet audited. A call that recovered from agentic to light shows as a success on the MCP row (code read) | A forced time-limit test is logged as `timeout` and a forced cancel as `cancelled`; neither as `error`, neither dropped |
| Tier and fallback | R3, R4 | `effort_executed`, `fallback_reason` | `agentic` or `light`; the reason separates enablement, quota or cost, capacity, time limit and internal error; null when there was no fallback | **OPEN**: code read, both are written only into the tool response, not to the MCP row; service logs not yet audited | `fallback_reason` is set exactly when agentic was requested and light ran; each fallback cause, forced in a test, gets its own reason |
| Cost | R1, R4, R5 | `cost_units` | Defined by engineering; comparable with one light search call | **OPEN**: not yet audited | Daily per-tenant totals reconcile with billing or resource use within 1% |
| Steps | R2, R3, R4 | `step_idx`, `step_type`, `step_start_ms`, `step_latency_ms`, `step_status` | One record per internal step; type `subquery_retrieval`, `doc_read`, `rerank`, `synthesis` or other | **OPEN**: not yet audited. The MCP row has no step count | At least one step per executed request; `step_idx` unique per request; each step inside the request interval |
| Round of each step | R3 | `iteration_idx` | The round the step belongs to; steps in one round may run in parallel | **OPEN**: not yet audited | Non-null; `n_iterations` equals the number of distinct values |
| How each query was produced | R3 | `query_origin` | `original`, `rewrite`, `decomposition` or `followup`, for each retrieval step; no text | **OPEN**: not yet audited | Non-null on every retrieval step |
| Retrieval result | R2, R3 | `step_n_results`, `step_top_score`, `step_acl_filtered_n` | Result count, top score, and candidates removed by permission filtering, per retrieval step | **OPEN**: not yet audited | Non-null on retrieval steps; score null when there are no results; state whether scores compare across requests |
| Documents retrieved and read | R3, R5 | `step_docs` | `[(doc_id, rank, source)]`, internal doc ID, not URL. Needs a privacy decision | **OPEN**: not yet audited | Entries match `step_n_results`; doc IDs join to the index and are stable across days |
| Sub-query shape | R3 | `subq_chars`, `subq_toks`, `subq_cos_orig` | Length, and embedding cosine to the original query rounded to 0.01; no text. Needs a privacy decision | **OPEN**: not yet audited | Non-null for each generated sub-query; no text or embedding written |
| Request summary | R3, R5 | `n_steps`, `n_subqueries`, `n_iterations`, `n_sources`, `n_docs_read` | Counts per request. They describe the work done, not whether it was needed | **OPEN**: not yet audited. The MCP row has no step count | Match values recomputed from the step records |
| Stop | R2, R3, R4 | `stop_reason` | `answered`, `budget_exhausted`, `timeout`, `no_results` or `cancelled`; for a budget stop, which cap was hit | **OPEN**: not yet audited. A run budget exists (`<RUN_BUDGET>`); the enforcing layer is not checked | Forced budget, timeout, no-results and cancel tests each get the matching value |
| Citations | R3, R5 | `n_citations`, `cited_docs` | Citation count; `[(doc_id, source)]` cited. Needs a privacy decision | **OPEN**: not yet audited | `n_citations` equals the length of `cited_docs`; every cited doc ID appears in some `step_docs` |
| Answer | R2, R5 | `answer_chars`, `answer_toks`, `answer_flag` | Answer length with no text (needs a privacy decision); `ok`, `low_confidence` or `no_answer` | **OPEN**: not yet audited | A no-answer test gets `no_answer`; length non-null when status is `ok` |
| Light retrieval for comparison | R3 | `light_shadow_docs`, `light_shadow_k`, `light_shadow_ver` | One light retrieval on the original query while the request is served: top-k `[(doc_id, rank)]`, the k used, configuration version; every request or a recorded sample. Needs a privacy decision | **OPEN**: not yet discussed with engineering | At most k entries; doc IDs join to the index; version matches the light configuration; sampling rate stated |
| Query features | R1, R2, R3 | `q_chars`, `q_toks`, `query_hash` | Length of the original query; keyed per-tenant hash, with the same key and normalisation as on current search calls. Needs a privacy decision | **OPEN**: not yet audited | Identical normalised queries share a hash within a tenant and differ across tenants; analysts cannot get the key |
| Task type | R3, R4 | `intent_coarse`, `intent_conf`, `multihop_score`, `intent_ver` | Coarse task type (6–9 classes, type of task rather than topic), confidence, probability of needing several steps, classifier version. Needs a privacy decision | **OPEN**: not yet audited | Labels only from the agreed classes; version non-null; checked against a labelled sample |
| Versions | R3, R5 | `svc_version`, `model_version`, `ranker_version`, `index_version`; service change log | Versions on every request; a change log of service, model, ranking, index, budgets and time limits | **OPEN**: not yet audited | Non-null; version switches match the change log |

**The shadow light retrieval** is the most direct evidence of whether light search would have found what the service cited, and it cannot be produced later because no query text is kept to replay. It costs one extra retrieval per agentic request, so engineering should weigh it; a sample is enough if the sampling rate is logged. Without it, the fallback is to check whether all cited documents appeared in the first round, which overstates how often light was enough if the first round is stronger than a light retrieval (question 6b).

### Was this agentic request needed?

These fields let us judge need from document identifiers, rounds and citations, without any text. Requests that failed, fell back, timed out or ended with no answer are set aside, and those that hit a budget are reported separately because their need is cut off. For the rest, if every cited document is in the shadow light retrieval, light search would probably have been enough. If not, we look at what the later rounds contributed: the round in which each cited document first appeared, and whether the sub-query that found it retrieved different documents from the original query (a decomposition) or mostly the same ones (a rewrite). Broken down by task type, the share of requests that needed agentic search tells the team which tasks need it; the second measure, needed requests that were missed, also needs MCP-side data, because requests that never reached the service are not in its logs. A step or round count cannot do this on its own. If the service runs a similar number of rounds for every request, or stops at a cap, the count describes the service and not the request, and empty or permission-filtered retrievals add rounds to requests that are hard rather than ones that need more search. Counts stay in the table as a denominator and for diagnosis. One case needs a definition from the team before it is counted either way: evidence that one light retrieval finds, but which the service combines across several documents.

### Questions for engineering

These three questions decide whether the service's data can say which requests needed agentic search: question 4 is whether one request can be traced into the service, question 5 is where effort is decided, and question 6 is how the service decides how much to search. They continue the numbering of the existing questions. This section asks them and does not settle them.

| Question | What we know today | Why it matters |
|---|---|---|
| 4a. Does the service receive the MCP invocation ID, or another key shared with the MCP row, on every request, including client retries and fallbacks from agentic to light? This widens the existing question on whether the service receives the invocation ID | The MCP side sets its event correlation ID to `<INVOCATION_ID_FIELD>` (code read). A client retry gets a new invocation ID, and there is no client request ID. The service side is not checked | Ties every service step to one MCP call. Without it, the service's data cannot be split by caller or requested effort, and missed need cannot be measured |
| 4b. What does the service log today about its internal steps, where and for how long, and does any of it hold query, sub-query or answer text? | Not audited. The MCP row has no step count | Decides which fields above are a gap and which are a build. Any text has to be excluded from a research copy |
| 4c. Does the service's record carry, or join to, the user's usage-data opt-out? | The MCP-side analysis uses only rows not opted out (`<OPT_OUT_FIELD>`). The service side is not checked | The service trace has to follow the same rule before anyone analyses it |
| 5a. Where is the fallback decision made, and can the service log executed effort and fallback reason there? | Code read: requested effort, executed effort and fallback reason are written only into the tool response. A recovery to light stays inside one call and shows as a success | Without it, a request that fell back counts as an agentic success, and the share of needed requests has the wrong denominator |
| 5b. Do `<AGENTIC_TOOL>` calls that request light effort pass through the service? | Not checked | Decides whether the service's logs hold light requests at all, and so where light and agentic can be compared |
| 6a. Is the number of rounds fixed, decided by the model, or a mix? What are the caps on rounds, sub-queries, tokens and time, what are the stop conditions, and are changes to them recorded? | Not audited. A run budget exists (`<RUN_BUDGET>`); which layer enforces it is not checked | If rounds are fixed or mostly capped, a round count describes the service and not the request |
| 6b. Does the first retrieval step use the original query, with the same backend, ranker and k as light search? | Not checked | If it does, first-round coverage of cited documents is a usable stand-in for the shadow retrieval. If not, it overstates how often light was enough |
| 6c. Can the service run a shadow light retrieval on the original query, on every request or a logged sample, and at what latency and retrieval cost? | Not yet discussed with engineering | The most direct evidence of whether light would have found the cited documents, and it cannot be produced later |
| 6d. Does the service have an explicit round, and can each step carry its round and how its query was produced? | Not audited | Steps in one round may run in parallel, so step order alone cannot group them. Without both, later-round contribution can only be estimated from timing |

### Priorities for this section

1. Check the join key on the service side first (question 4a). Send test `<AGENTIC_TOOL>` calls, including a forced client retry and a forced fallback to light, and find each one in `<SERVICE_LOG_SOURCE>` by the invocation ID or the shared key. Until this passes, no field above can be tied to a caller. Suggested lead: the service owner, with the MCP team.
2. Audit what the service logs today (questions 4b and 4c) to the standard used for `<MCP_EVENT_TABLE>`: for each field, row counts or a code read, and a status label. Fill the "Observed evidence" column above. Suggested lead: the search data scientist, with the service owner.
3. Answer how the service decides tier, rounds and stops (questions 5a, 5b, 6a, 6b, 6d), and decide whether and how to sample the shadow light retrieval (6c). Suggested lead: the service owner.
4. Agree which missing fields to add during early access and the test for each, starting with the shared key, executed effort and fallback reason, round index, query origin, stop reason and cited documents. Suggested leads: the search data scientist and the service's engineers, jointly.
5. Submit the privacy decision for document IDs, query and sub-query features, answer length and the shadow light retrieval. Suggested lead: the search data scientist, with the service owner.

Timing: the service has no customer traffic before launch, and nothing here can be backfilled, so these fields need to pass their checks during early access. A suggested latest date is three weeks before launch, not counting the year-end holidays.

Dependencies held by the MCP data scientist, not work for this section: entry-side data on requests that never reached the service, which the missed-need measure needs; requested effort; and the tool description version, which marks each turn of the description loop.
