# Agentic Search Service Instrumentation Requirements

> From: the MCP search research team. Date: 2026-11-24. Audience: the engineering team.
>
> This version replaces the 2026-11-23 version, which put every field at the MCP server entry point. It specifies logging inside the **agentic search service**. MCP-side data is owned by the MCP team; we only list what we assume it holds (Table 2).
>
> This is a **requirements list, not a gap list**. We do not know which fields the service already records. Please mark each row of Table 1 "exists / partly / does not exist". Thresholds, parameters, field names and enum values are **suggested values**. We say what we need and why, not how to implement it.

## 1. Purpose

The research studies usage and quality of search through the MCP server. It infers latent demand for the agentic tier that launches in January 2027, and looks at what drives adoption and user value. Callers are users' agents, which decide by themselves whether to call a tool and which tier to request. We cannot see query text. The service also serves a CLI entry point; for now we look at MCP traffic only. The future light tier is the current search tool.

| Label | Research question | Mainly depends on |
|---|---|---|
| **R1 Usage** | Who uses the MCP server, and how: by account type (interactive human, human-started long-running task, unattended pipeline), tenant and client. How concentrated usage is, and what the automation accounts behind most calls are doing | Table 2 |
| **R2 Quality** | Where current search falls short, across every tool. Without query text, separate retries after a retrieval failure, caller style and genuine multi-step needs | Table 2. Table 1 adds where agentic requests fail |
| **R3 Latent demand** | How many people and tenants need more complex search, and in which scenarios | Table 2. Table 1 adds realised complexity after launch |
| **R4 Adoption** | Tenant and person funnels (enable MCP → connect account → active → use search → use agentic). Who does not use it, and why | Both: funnel and requested tier in Table 2; executed tier, fallback and failure in Table 1 |
| **R5 Value** | Person-level time spent searching and repeated searches, against a pre-launch baseline | Both: baseline in Table 2; agentic requests in Table 1 |

## 2. Logging boundary

Request path (MCP only; the CLI path is out of scope): `caller agent → MCP server → agentic search service → retrieval backend`

**Rule.** Each field has exactly one system of record: the layer that is the only one able to see the information. Where both layers see it, one is named as the record and the other only passes the join ID through (plus tenant and user identifiers, for joining). Latency and status mean different things at each layer, so each layer has its own field (section 6).

What each layer alone can see (our understanding; please correct it):

| Layer | Only this layer can see | Here |
|---|---|---|
| Caller agent | Why it called, which tier it chose and why, the user's instructions, its model | Not observable |
| MCP server | Caller identity; every tool call, including the current search tool; the sequence of calls on a stream; requested tier; tool description version; latency as the caller experiences it; client cancellation and timeout | Table 2 (MCP team) |
| Agentic search service | Executed tier and fallback reason; each internal step; documents retrieved, read and cited; stop reason; internal latency and failures; cost; versions | Table 1 (the ask) |
| Retrieval backend | Candidates and scores of each retrieval | Through the service's step records |

A "stream" is the sequence of calls from the same (tenant, user, client).

**Assumptions** (questions in section 10): (1) light-tier requests do not pass through the service; they are served by the existing search path and are visible only on the MCP side, which in principle holds all existing search behaviour data (Q1); (2) the service holds the original query text and its embedding at request time (Q7); (3) every agentic request reaches the service, and any fallback is decided and logged there (Q6); (4) the MCP side holds the group 1 items of Table 2.

## 3. Table 1: required from the agentic search service

This is the ask. Log every request whatever its entry surface; we filter to `mcp` in analysis. The prefix `svc_` marks fields whose MCP-side counterpart means something different.

**Priority** (redefined for the new timing, section 7). Nothing here can be backfilled: the trace cannot be rebuilt and no text is stored.

- **A**: Recorded in the internal beta from now on, and complete on launch day. We need beta data to run the acceptance checks and build the offline measures before customer traffic.
- **B**: Complete on launch day. Beta data helps but is not required.
- **C**: Can be added after launch. Analyses that need it start when it lands.

| Group | Field | Definition | Type / values | Unlocks | Priority |
|---|---|---|---|---|---|
| Request | `svc_request_id` | The service's own request ID | string | Correlation, deduplication | A |
| | Join ID (name to be confirmed, J1) | The existing ID linking this request to its MCP call | string | Every join with Table 2 | A |
| | `entry_surface` | `mcp` / `cli` / `other` | enum | Isolating MCP traffic | A |
| | `tenant_id`, `user_id` | Passed through unchanged from the MCP call, for joining. The MCP side is the record | string | Joins | A |
| | `svc_ts_start`, `svc_ts_end`, `svc_latency_ms` | Request received; last byte sent; total time in the service | timestamp (ms, UTC), int | R4 (latency barrier), R5 (`W_ud`) | A |
| | `svc_ttfb_ms` | Time to the first byte of the response | int | R4, (d) | B |
| | `svc_status`, `svc_err_code` | `ok` / `error` / `timeout` (own time limit or downstream timeout) / `cancelled` (cancellation received from upstream) / `rejected` (refused before execution); error code, naming the failing component where known | enum, string | R2, R4 (failure as a reason for not using) | A |
| | `effort_executed`, `fallback_reason` | Tier actually run: `agentic` / `light`. Why it fell back to light; null if it did not. Reasons must separate enablement, quota or cost, capacity, time limit and internal error | enum, enum | R4 ("requested, but fell back") | A |
| | `cost_units` | Defined by engineering; comparable with a current search call (M9) | float | R1, R4 (cost barrier), R5 (`equiv_calls_ud`) | B |
| Step (one record per internal step) | `step_idx`, `step_start_ms`, `step_latency_ms`, `step_status` | Order; start offset from `svc_ts_start` (steps may run in parallel); duration; outcome (`svc_status` enum) | int, int, int, enum | (b), (c), (d) | A |
| | `step_type` | `subquery_retrieval` / `doc_read` / `rerank` / `synthesis` / other | enum | (b), (c), (d) | A |
| | `step_n_results`, `step_top_score` | Result count and top score of a retrieval step | int, float | R2 (weak retrieval inside agentic), (c) | A |
| | `step_docs` | Documents retrieved or read: `[(doc_id, rank, source)]`. Internal doc_id, not URL | array | (a), (b); R5 (`refind_xday`) | A, needs approval |
| | `step_acl_filtered_n` | Candidates removed by permission filtering | int | R2 (no content or no permission) | C |
| | `subq_chars`, `subq_toks`, `subq_cos_orig` | For a generated sub-query: length, and embedding cosine to the original query (quantised to 0.01). No text | int, int, float | (b) | C, needs approval |
| Summary (per request) | `n_steps`, `n_subqueries`, `n_iterations` | Steps; generated sub-queries; rounds in which the service decided to search again | int | (b); R3, R5 (`equiv_calls_ud`) | A |
| | `n_sources`, `n_docs_read` | Distinct sources; distinct documents read | int | (b) | A |
| | `stop_reason` | `answered` / `budget_exhausted` / `timeout` / `no_results` / `cancelled` | enum | (c); R2, R4 | A |
| Output | `answer_chars`, `answer_toks` | Answer length. No text | int | R5 | B, needs approval |
| | `n_citations`, `cited_docs` | Citation count; `[(doc_id, source)]` cited | int, array | (a); R5 | A, needs approval |
| | `answer_flag` | `ok` / `low_confidence` / `no_answer` | enum | R2, R5 | B |
| Query features (assumption 2) | `q_chars`, `q_toks` | Characters and tokens in the original query | int | R2, R3 | A, needs approval |
| | `query_hash` | `HMAC(K_tenant, normalize(q))`. Same key and normalisation as on current search calls (M8) | string | R1 (templated calls), R2 (exact repeats across tiers) | B, needs approval |
| | `intent_coarse`, `intent_conf`, `multihop_score`, `intent_ver` | As agreed before: coarse task type (6–9 classes from the research team; type of task, not topic); confidence; probability that the query needs multiple steps; classifier version | enum, float, float, string | R3, R4 | C, needs approval |
| Versions | `svc_version`, `model_version` | Service version; version of the model used inside the service | string | R5 (concurrent changes) | A |
| | `ranker_version`, `index_version` | Ranker and index versions used | string | R5 | A |
| | Service change log | Every change to the service, model, ranking, index, budgets and time limits: time, version, summary | table | R5 | A (start now) |
| Offline (not logged) | (a)–(d) below | Computed by the research team; listed only to show dependencies | — | R3, R4, R5 | — |

**Why the step trace matters.** Request totals show that an agentic request happened; the trace shows what it did and whether it was needed. The research team computes, offline and not logged: (a) whether an agentic request was needed: if every cited document already appeared in the first retrieval step, the light tier would probably have been enough; (b) realised complexity: how many steps and sources were used; (c) where failures happen; (d) where latency goes.

## 4. Table 2: assumed to exist on the MCP side (owned by the MCP team)

Dependencies to confirm, not requirements. Existing search behaviour data is, in principle, all held by the MCP team. We assume the following already exist; please confirm each as exists / partly / does not exist. [`mcp-data-checklist.md`](mcp-data-checklist.md) lists the same rows, with what each is for and what we lose without it. Names are those of the previous version.

The plan's pre-launch baseline of current search behaviour depends on this table (section 7). This is a dependency risk, which the research team will raise with the MCP team separately.

| ID | Item (previous field names) | Unlocks | Exists / partly / does not exist |
|---|---|---|---|
| | **Group 1: needed for any pre-launch analysis** | | |
| M1 | Tenant and user (`tenant_id`, `user_id`). The record for both | All | |
| M2 | Every tool call on the server (`request_id`, `tool_name`) | R1, R2 | |
| M3 | Time as the caller experiences it (`ts_start`, `ts_end`, `latency_ms`) | R2, R5 | |
| M4 | Caller identity (`client_name`, `client_version`, `user_agent`, `auth_type`, `credential_id`, `grant_type`) | R1, R2 | |
| M5 | Status with client cancellation and timeout (`status`, `err_code`) | R2, R4 | |
| M6 | Join ID shared with the service (J1) | R4, R5 | |
| | **Group 2: needed for the finer analysis** | | |
| M7 | Stream-level query similarity (`emb_cos_prev`, `emb_cos_max5`, `emb_cos_max5_lag`, `emb_ver`; `ctar` if approved) | R2, R3, R5 | |
| M8 | Query features of current search calls (`q_chars`, `q_toks`, `query_hash`, `intent_*`; as Table 1) | R2, R3, R4 | |
| M9 | Results of current search calls (`n_results`, `top_score`, `cost_units`, backend and ranker version) | R1, R2, R5 | |
| M10 | Funnel events: tenant enablement, account connection, tenant size, agentic enablement | R4 | |
| M11 | Requested tier (`effort_requested`: `light` / `agentic` / null) | R4 | |
| M12 | Returned document identifiers (`result_docs`) | R2, R3, R5 | |
| M13 | Tool description version (`desc_version`; change log kept by product) | R4, R5 | |
| M14 | Session identifier (`session_id`) | R2 | |

`emb_cos_max5` is the highest cosine over the last 5 queries on the same stream; `emb_cos_max5_lag` says how many queries back that match is (1 = the previous query).

**Why M7 is here, not in Table 1.** These features compare a query with earlier queries on the same stream, which spans every tool and both tiers. The service sees only requests sent to it, so it would compare an agentic query only with earlier agentic queries and miss the current search calls in between. Even if light-tier requests pass through the service (Q1), it does not see other tools, nor, as far as we know, the client that defines the stream. So M7 belongs to the layer that sees the whole stream: the MCP side.

## 5. Table 3: join contract

| ID | Item | What we need | Please confirm |
|---|---|---|---|
| J1 | Join ID | The existing ID linking an MCP call to its service request, on both sides, for every request: retries, fallbacks, timeouts, cancellations and errors included | Field name on each side; coverage; whether one MCP call can map to several service requests, and how retries are marked |
| J2 | Tenant and user | The service carries `tenant_id` and `user_id` exactly as on the MCP call, not re-mapped or hashed differently | That values match on joined pairs |
| J3 | Clock alignment | UTC in ms from synchronised clocks, so MCP latency minus service latency is the time outside the service. Suggested skew ≤50 ms | Clock source and expected skew |

## 6. Fields that are easy to confuse

| Field | Record owner | Reason |
|---|---|---|
| Requested tier | MCP side (M11) | Only the MCP server sees what the agent asked for, including requests that never reach the service |
| Executed tier, `fallback_reason` | Service | Only the service knows what it ran and why it fell back (assumption 3) |
| Latency | Both, different fields | MCP `latency_ms` (M3) is the total the caller experienced. `svc_latency_ms`, `svc_ttfb_ms` and step latencies are the internal breakdown |
| Status | Both, different fields | MCP `status` (M5) records client cancellation and timeout. `svc_status` records internal failure, the service's own time limit and cancellations it received. The status criterion applies to each side for its own meaning |
| `tenant_id`, `user_id` | MCP side (M1) | The MCP server authenticates the caller. The service passes them through (J2) |
| Derived query features | Agentic requests: service. Stream similarity: MCP side (M7). Current search calls: open (M8) | Assumption 2: the service holds the query text and embedding. Open question (Q1, Q7): if light-tier requests skip the service, features of current search calls can only come from the MCP side, and the baseline depends on them |

## 7. Timing

- **Table 1 has no pre-launch baseline.** The service has no customer traffic before launch, so its fields must be complete on launch day: a request not logged with its trace cannot be reconstructed. They should be recorded in the internal beta from now on, to run the acceptance checks, calibrate (a)–(d) and fix problems before customer traffic. Beta readings are labelled internal and not extrapolated to customers. Suggested latest date for priority A: 3 weeks before launch, not counting the year-end holidays.
- **The pre-launch baseline is about current search behaviour (Table 2).** Post-launch readings are compared with at least 3 clean weeks (suggested; excludes the year-end holidays). Derived features of current search calls (M7, M8) can only be computed while the request is handled. **A period not captured cannot be recomputed.** For a mid-January launch, they need to be in place around the first week of December. If they come later or do not exist, the pre-launch demand estimate stays coarse and post-launch value can only be read descriptively.

## 8. Privacy

**Do not store query text, generated sub-query text, answer text, or embeddings of any of them**, in logs, traces, temporary tables or backups. If existing service traces contain such text, the research copy must exclude it.

| Feature | How to compute it without storing the text |
|---|---|
| Lengths (query, sub-query, answer) | Count at request time; store only the integer |
| `query_hash` | Keyed HMAC, one key per tenant, stored apart from the data and not accessible to analysts. Rotate keys (suggested: every quarter). No per-token hashes. Same key and normalisation wherever computed |
| `subq_cos_orig` | Reuse the embeddings retrieval already computes. Store only the quantised cosine |
| `intent_*` | Classify at request time; store only label and confidence. Training does not use production query text |
| `step_docs`, `cited_docs` | Internal doc_id, not URL or title |
| `emb_cos_*`, `ctar` (M7) | As agreed before: last 5 embeddings per stream in memory only (suggested TTL: 60 minutes), store only the quantised cosine; `ctar` caches result terms as term-level HMACs (suggested TTL: 10 minutes), stores only the ratio |

| Risk | Mitigation |
|---|---|
| Unkeyed hashes of low-entropy queries can be reversed by dictionary attack | Keyed HMAC, key stored apart |
| One key across tenants allows cross-tenant linkage | One key per tenant |
| Per-token hashes can be reversed from word statistics | Do not do it |
| Embeddings of query, sub-queries or answer can be inverted | Never write them to disk; store only cosines |
| User ID plus documents retrieved, read and cited over time is personal behaviour data; the trace adds detail | Restrict access and retention. Suppress cells under 10 people in external reports |
| Account-level profiles risk employee monitoring | Research use only; not given to tenant administrators |

**Needs privacy approval**: reading the query, sub-queries and answer in memory to compute features (lengths are lowest risk and can be approved first, alone); writing `query_hash`; `intent_*`; `subq_cos_orig`; writing `step_docs` and `cited_docs`; M7 and M8 wherever computed, including the embedding cache and `ctar` reading result text; profiling automation accounts.

## 9. Acceptance criteria for Table 1 fields needed at launch

Covers priority A and B. Done once met for 7 consecutive days in the internal beta; join rate and cost reconciliation are rechecked in the first week after launch. All values are suggested.

| Field | Acceptance criteria |
|---|---|
| `svc_request_id` | Unique; duplicate rate 0 |
| Join ID | Non-null on 100% of `mcp` requests, including retries, fallbacks, timeouts, cancellations and errors. ≥99% join to an MCP call; unjoined requests are counted and reported |
| `entry_surface` | Non-null 100%. Test requests via MCP and via the CLI are labelled correctly |
| `tenant_id`, `user_id` | Non-null 100%. Equal to MCP-side values on all joined pairs |
| Timings | `svc_ts_end ≥ svc_ts_start`; `svc_latency_ms` matches the difference (≤50 ms); `svc_ttfb_ms ≤ svc_latency_ms`; UTC. On joined pairs the service interval lies inside the MCP interval, within J3 |
| `svc_status`, `svc_err_code` | `svc_status` non-null on every request; values only from the defined enum. A test request that hits the service's time limit is logged as `timeout`, and one the client cancels as `cancelled`; neither as `error`, neither dropped. `svc_err_code` non-null when status is not `ok`. The same criterion applies to MCP-side `status` (M5), raised with the MCP team |
| `effort_executed`, `fallback_reason` | `effort_executed` non-null. `fallback_reason` non-null exactly when agentic was requested and light was run. Each fallback cause, forced in a test, gets its own reason |
| `cost_units` | Daily per-tenant totals reconcile with billing or resource usage (≤1%). Ratio to a current search call stated |
| Step records | ≥1 per executed request; `n_steps` equals their count; `step_idx` unique per request; each step inside the request interval; enum values valid |
| `step_n_results`, `step_top_score`, `step_docs` | Non-null for retrieval steps; score null when `step_n_results = 0`; `step_docs` has `step_n_results` entries; doc_id joins to the index and is stable across days. State whether scores compare across requests |
| Summary fields | Match values recomputed from steps. `stop_reason` non-null; forced tests (budget, timeout, no results, cancel) each get the matching value |
| Output fields | `n_citations` = length of `cited_docs`; every cited doc_id appears in some `step_docs`; a no-answer test gets `no_answer`; `answer_chars` non-null when `svc_status = ok` |
| `q_chars`, `q_toks`, `query_hash` | Non-null 100%. On a test set, normalised-identical queries share a hash within a tenant, differ across tenants, and match current search calls if M8 exists. Analysts cannot get the key |
| Versions, change log | Non-null; version switches match the change log |

## 10. Questions for engineering

1. **Light tier.** Do light-tier requests pass through the agentic search service at all, or only through the existing search path, visible in MCP-side or existing search logs? We assume the latter. This decides where M7–M9 and M12 come from.
2. **Join ID.** What is its field name on each side? Is it on every request on both sides, retries and fallbacks included? Can one MCP call map to several service requests?
3. **Table 2.** Which rows exist today, and for how long are they kept? If you cannot say, who can? (The checklist goes to the MCP team as well.)
4. **Entry surface.** Can the service tell CLI from MCP requests today, and from which field?
5. **Step trace.** Is the internal step trace already recorded in any form (tracing, debug logs)? Which Table 1 fields does it cover, how long is it kept, and does it hold text that must be excluded?
6. **Fallback.** Is every fallback decided inside the service, or can the MCP server reject or fall back first (for example for a tenant not enabled)?
7. **Query text.** Does the service receive the query text and embed it at request time? Does it embed sub-queries?
8. **Cost.** How are `cost_units` defined, relative to a current search call?
9. **Ownership.** Who owns Table 1 logging, and on what schedule? Who keeps the service change log? Who submits the privacy approval?
