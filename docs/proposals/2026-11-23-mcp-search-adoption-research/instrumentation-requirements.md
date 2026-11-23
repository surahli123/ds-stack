# MCP Server Instrumentation Requirements

> From: the MCP search research team. Date: 2026-11-23. Audience: the engineering team.
>
> This is a **requirements list, not a gap list**. We do not currently know which fields the existing logs have, so many fields in the tables below may already exist. Please go through the tables row by row and mark each one "Exists / Partial / Missing" (question 1 in section 5). We will then work out the gap list together.
>
> The thresholds and parameters in this document (number of cache entries, TTLs, coverage rates, error tolerances) are **suggested values**. You can adjust them to fit the implementation. We only say what we need and why. We do not prescribe how to implement it.

## 1. What this instrumentation is for, and why there is a timing requirement

The research team is answering five questions. The "Unlocks" column in the tables below uses these labels.

- **R1 Usage**: Who uses the MCP server, and how. Segment by account type (interactive human, human-started long-running task, unattended pipeline), tenant and client, and look at how concentrated usage is. Find out what the automation accounts that make more than half of all tool calls are doing.
- **R2 Quality**: Where the current search falls short. We cannot see query text, so we need to tell apart three things: retries after a retrieval failure, the caller's own calling style, and genuine multi-step needs. This covers every tool on the server (search, fetch, structured query and so on).
- **R3 Latent demand**: How many people and tenants need more complex search, and in which scenarios.
- **R4 Adoption**: Funnels at tenant level and person level (enable MCP → connect account → active → use search → use the agentic tier after the January launch). Also, who is not using it, and why not.
- **R5 Value**: Person-level metrics such as time spent searching and repeated searches. We build a baseline before launch and compare against it after launch.

**Timing requirement**: Post-launch readings will be compared with the pre-launch baseline. The baseline needs at least 3 clean weeks (suggested value; excludes the year-end holidays). Derived query features can only be computed from the query text while the request is being handled. The text is not stored. So **any period we fail to capture cannot be recomputed later**. Assuming a launch in mid-January, priority A fields need to be in production around the first week of December. Once the launch date is fixed, we will give you the exact latest date. If the fields go live later than that, the post-launch value analysis can only be descriptive.

**Priority**

- **A**: Must be in place before launch. The sooner the better, because it affects the baseline.
- **B**: Must be in place at launch (related to the agentic tier; there are no values before launch; the fields can be created in advance).
- **C**: Can be added later.

## 2. Requirements tables

Meaning of "Produced at": **Entry** = the MCP request entry point; **Backend** = the retrieval backend; **Auth** = the handshake or authentication layer; **Admin** = the admin console or account system; **Offline** = derived offline on the research side. A "stream" is the sequence of calls from the same (tenant, user, client).

### 2.1 This team's requirements

| Group | Field | Definition | Type / values | Produced at | Unlocks | Priority |
|---|---|---|---|---|---|---|
| Call | `request_id` | Unique ID of each tool call | string | Entry | Correlation, deduplication | A |
| | `tool_name` | Name of the tool that was called. **Log every tool on the server** (search, fetch, structured query and so on), not only search | string | Entry | R1, R2 (cross-tool call chains) | A |
| | `session_id` | Session identifier from the session trace | string | Entry (trace) | R2 (supporting signal for task segmentation) | A (ships with the trace) |
| Identity and segmentation | `tenant_id`, `user_id` | The tenant; a stable user identifier | string | Auth | All | A |
| | `auth_type` | Authentication method: OAuth user authorisation / API key or PAT / service account / client credentials / other | enum | Auth | R1 (identifying unattended-pipeline accounts) | A |
| | `credential_id` | Identifier of the credential or OAuth client used for this tool call. Used to tell apart different agents or scripts under the same user | string (may be hashed) | Auth | R1 | A |
| | `grant_type` | Grant type of the access token | enum | Auth | R1 (strongest evidence for an unattended pipeline) | A; lowered to C if it needs changes to the auth service |
| | `client_name`, `client_version` | Name and version that the MCP client reports about itself in clientInfo. With the older protocol they are sent at handshake and must be attached to every tool call. With the newer protocol they are in `_meta` on every request | string | Auth (handshake) | R1, R2 (stratifying by caller) | A |
| | `user_agent` | HTTP User-Agent | string | Entry | R1 | A |
| Time and status | `ts_start`, `ts_end`, `latency_ms` | The time the request was received; the time the last byte was sent; server-side processing time | timestamp (ms, UTC), int | Entry | R2 (segmentation), R5 (time spent searching) | A |
| | `status` | ok / error / timeout / cancelled (cancelled by the client, or client disconnected) | enum | Entry | R2 (resends after an error are not counted as behaviour), R4 | A |
| | `err_code` | Error code | string | Entry | R2, R4 | A |
| Results | `n_results` | Number of results returned | int | Backend | R2 (zero results), R5 | A |
| | `top_score` | Relevance score of the top-ranked result | float | Backend | R2 (separating retrieval failure from multi-step need), R5 (convergence) | A |
| | `result_docs` | Stable internal identifiers of the returned documents: `[(doc_id, rank, source)]` | array | Backend | R2, R3 (result overlap between adjacent calls), R5 (revisits across days) | A (if the backend can supply it now); otherwise added later, once the trace includes URLs |
| | `acl_filtered_n` | Number of candidates filtered out because of permissions | int | Backend | R2 (separating no content, no permission and weak retrieval) | C |
| Derived query features (computed at write time, see section 3) | `q_chars`, `q_toks` | Number of characters and number of tokens in the query | int | Entry | R2, R3 | A |
| | `query_hash` | `HMAC(K_tenant, normalize(q))` | string | Entry | R1 (templated calls), R2 (exact repeats) | A, needs approval |
| | `emb_cos_prev`, `emb_cos_max5`, `emb_ver` | Embedding cosine similarity between this query and the previous query on the same stream, and between this query and the last 5 queries, quantised to 0.01; the embedding model version. Only computed for tools that take a query parameter | float, string | Entry | R2, R3 (retry or new need) | A, needs approval |
| | `intent_coarse`, `intent_conf`, `multihop_score`, `intent_ver` | Coarse task type (6–9 classes; the research team provides the class list, which describes the type of task, not the topic); confidence; probability that the query needs multiple steps; classifier version | enum, float, string | Entry | R3 (complex intent), R4 | A, needs approval |
| | `ctar` | Of the words in this query that are new, the share that appear in the titles or snippets of the results returned by the previous call on the same stream | float | Entry + Backend | R3 (direct evidence of multi-step dependency) | A, needs approval; if it is not approved, it is not built |
| Tier and cost | `internal_steps`, `parent_call_id` | Number of sub-searches inside an agentic tool call; the top-level tool call that a sub-search belongs to | int, string | Backend | R5 (convert to equivalent call counts so that before and after are comparable) | B |
| | `cost_units` | Cost units of each tool call. Engineering defines how it is measured. It must be comparable between the light tier and the agentic tier | float | Backend | R1 (concentration by cost), R4 (cost barriers) | A |
| Versions | `backend_version`, `ranker_version` | Retrieval backend version and ranker version used for each tool call | string | Backend | R5 (ruling out changes made at the same time) | A |
| | Backend change log | Every change to the retrieval backend, ranking, index and timeout configuration: time, version, summary | table | Maintained by engineering | R5 | A (start recording now) |
| Funnel | Tenant enablement events | The time a tenant enables or disables MCP | event | Admin | R4 | A |
| | Account connection events | The time an account completes or revokes MCP authorisation, with the client and `auth_type` | event | Auth | R4 | A |
| | First call | The time of an account's first call to any tool and of its first call to search | timestamp | Offline; must be persisted if the log retention period is too short | R4 | A |
| | Tenant size snapshot | Number of valid accounts or seats per tenant, weekly | table | Admin | R4 (funnel denominator) | A |
| | Agentic enablement status | Whether the tenant has the agentic tier enabled (if it needs to be enabled separately), and when | event | Admin | R4 | B |
| Offline derived | `zero_res`, `rep_lag`, step, episode, call chain type | The research side computes these from the fields above. They need no instrumentation. They are listed only to show the dependencies | — | Offline | R2, R3 | — |

### 2.2 Items to be provided by, or shared with, the product team

The items below mainly serve the product team's evaluation of the tool description and tier selection. This team uses them only to interpret changes in usage (splitting the data into windows before and after a change, and breaking down why people are not using the tool). We do not evaluate the description itself.

| Field | Definition | Type / values | Produced at | How this team uses it | Priority |
|---|---|---|---|---|---|
| Description change log | Identifier of each version, the time it took effect, summary of the change | table | Maintained by the product team | Split readings into windows before and after each change. No attribution | A (start recording now) |
| `desc_version` | Version of the tool description the client had at the time of the tool call (the client may have cached an older version) | string | Entry | Same as above | B |
| `effort_requested` | Tier passed in by the caller; empty if none was passed | light / agentic / null | Entry | R4: whether the agent ever requested agentic | B |
| `effort_executed`, `fallback_reason` | Tier actually executed; reason for falling back to the light tier | enum, string | Backend | R4: why a request did not take effect | B |

**Out of scope**: tools/list delivery and exposure records, schema compatibility fingerprints, IP/ASN/TLS fingerprints, parameters self-reported by the caller, shadow comparison queries, and citation click-throughs. If the product team needs any of these for its own evaluation, please align with them directly.

## 3. Privacy

**Do not store query text or embeddings.** Do not write them to logs, temporary tables or backups. How each derived feature is computed:

| Feature | How to compute it without storing the text |
|---|---|
| Length | Count at request time and store only the integer |
| `query_hash` | A keyed HMAC. Each tenant has its own key, stored apart from the data and not accessible to analysts. Rotate the keys regularly (suggested: every quarter). Do not hash per token |
| `emb_cos_*` | Reuse the query embedding that retrieval has already computed. For each stream, keep only the last 5 in memory (suggested TTL: 60 minutes). Store only the quantised cosine |
| `intent_*` | Classify at request time. Store only the label and the confidence. Classifier training does not use production query text |
| `ctar` | Briefly cache the set of words from the titles and snippets of the previous results (store them as term-level HMACs; suggested TTL: 10 minutes). Store only the ratio |
| `result_docs` | Store the internal doc_id, not the URL (URL paths often contain titles). If URLs are needed, manage them as a controlled field |

**Known risks and mitigations**

| Risk | Mitigation |
|---|---|
| An unkeyed hash can be reversed by a dictionary attack on low-entropy queries | Use a keyed HMAC, with the key stored apart from the data |
| Using the same key across tenants allows cross-tenant linkage | One key per tenant |
| Per-token hashes can be reversed using word-frequency and co-occurrence statistics | Do not do it |
| Embeddings can be inverted to recover the original text | Do not write them to disk. Store only the scalar cosine |
| A stable user ID plus doc_id plus a time series is still personal behaviour data, and there is a risk of re-identification | Restrict access and retention. In external reports, suppress cells with fewer than 10 people |
| Account-level behaviour profiles carry a risk of employee monitoring | Use them only within the research. Do not provide them to tenant administrators |

**Items that need privacy approval**: reading the query in memory during the request to compute derived features (length is the lowest risk and can be approved first, on its own); writing `query_hash` to disk; the short-lived embedding cache; `ctar` reading result text; writing `result_docs` and URLs to disk; account-level profiling of automation accounts.

## 4. Acceptance criteria for priority A fields

A field counts as done once it meets the criteria below for 7 consecutive days in production. All values are suggested and open to discussion.

| Field | Acceptance criteria |
|---|---|
| `request_id` | Unique. Duplicate rate is 0 |
| `tool_name` | Covers 100% of tool calls. Values match the server's current tool list. Every tool that has traffic appears |
| `session_id` | Non-null on all tool calls once the trace is live. Tool calls in the same session belong to the same user |
| `tenant_id`, `user_id` | Non-null rate 100%. Join rate with the account system ≥99% |
| `auth_type`, `credential_id`, `grant_type` | Non-null rate ≥99%. The same `credential_id` does not appear in more than one tenant. The `auth_type` distribution matches the statistics of the auth system |
| `client_name`, `client_version`, `user_agent` | Non-null whenever the client sent clientInfo. Null values are counted separately and their share is reported. Spot-check 100 tool calls against the user agent and find no contradictions |
| `ts_start`, `ts_end`, `latency_ms` | `ts_end ≥ ts_start`. `latency_ms` matches the difference between the two (error ≤50 ms). All times in UTC |
| `status`, `err_code` | Full enum coverage. The daily error rate and timeout rate match the existing monitoring (difference ≤1pp) |
| `n_results`, `top_score` | Non-null rate 100% for search-type tools. `top_score` is null when `n_results=0`. State whether scores are comparable between queries |
| `result_docs` | The doc_id can be joined to the index. The same document keeps the same ID across days. The number of entries equals `n_results` |
| `q_chars`, `q_toks` | Non-null rate 100% for tools that take a query parameter |
| `query_hash` | On a test set: queries that are identical after normalisation have the same hash within a tenant and different hashes across tenants. The analysis side cannot get the key |
| `emb_cos_*` | On test sequences: repeated queries score ≥0.99, and unrelated queries score clearly lower. After the cache expires the value is null, not 0. `emb_ver` is non-null |
| `intent_*` | Non-null rate ≥99%. On the synthetic test set provided by the research team, agreement with the annotated labels reaches a value that both teams agree on |
| `ctar` | On test sequences: greater than 0 when the next query uses words from the previous results, and close to 0 when it is unrelated |
| `cost_units` | Daily per-tenant totals reconcile with the billing or resource-usage figures (error ≤1%) |
| Version fields and backend change log | The times at which the version fields switch match the change log |
| Funnel events and snapshots | The number of enabled tenants and connected accounts matches the current state in the admin console. State the earliest date the data can be traced back to |
| Description change log (product) | Every change has an effective time. After launch, it matches the time `desc_version` switches |

## 5. Questions for the engineering team

1. Which fields do the existing logs have, and how long are they retained? Please mark each row of the tables in 2.1 and 2.2 as "Exists / Partial / Missing".
2. Which fields can be backfilled? For fields that can be recomputed from the existing logs (for example tool name, time, identity, client), how far back can you go? Derived query features cannot be backfilled, because the text was not stored. Please confirm this.
3. Can the retrieval backend now write `doc_id`, rank, source and `top_score` to the log of every tool call? Are scores comparable between queries?
4. What can the auth layer provide? Which authentication methods exist today? Can the tool call log carry `auth_type`, `credential_id` and `grant_type`? Are clientInfo and the user agent already recorded?
5. When will the session trace be available? Who generates the session, and when is a session cut off? When will URLs of returned documents be added?
6. Are tenant MCP enablement and account connections already recorded as events? Can they be traced back? Does the agentic tier need to be enabled separately for each tenant?
7. Who owns this instrumentation, and what is the schedule? Who submits the privacy approval?
