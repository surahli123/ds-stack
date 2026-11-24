# MCP search usage and latent demand: research plan (2026-11-23)

> Reader: the project owner. This plan rewrites the earlier v1 plan with a narrower scope. The v1 plan and the topic reports are unchanged, so you can go back to them for method detail (internal research notes, not included in this repository). All thresholds are **initial assumptions** and must be calibrated on our own data. External facts marked "unverified" keep the marking from the topic reports.

## 1. Summary in one paragraph

Our team studies usage and quality of the existing MCP search tool. From them we infer the latent demand of people and tenants for more complex search. We want to answer three questions. Who will benefit once the agentic tier launches? What is blocking adoption? How should we measure value at the level of people? The output is insights and recommendations. We do not make decisions for the product team. Today we use the existing logs to segment usage and to profile automation accounts qualitatively. Once session traces are available, we work on episodes that span tools. We separate three things: retries after a retrieval failure, caller calling style, and genuine multi-step dependency. We report the size of demand as intervals, name the first target population and collect the value baseline. After the January launch, we describe who used the agentic tier and who did not, and we read value. With the narrowed scope, this research can answer "where is the demand, and how large is it?" It cannot answer whether the agentic tier can meet that demand. That depends on the product team's evaluation. Nor can it answer whether demand that goes unused is a tool description problem. That depends on their tier-selection experiments. The most urgent deliverable right now is the instrumentation requirements (section 6).

## 2. Scope, division of work and interfaces

### 2.1 What we do and what we do not do

| This team does | This team does not do (owner) |
|---|---|
| Usage: account classification, tenant and client segmentation, usage concentration, qualitative profiling of automation accounts | Build the agentic search and evaluate its quality (product) |
| Quality: where light search is not enough, covering search, fetch and structured queries | Write, finalise and evaluate the effect of the tool description (product) |
| Latent demand: size and distribution, expressed as intervals | Tier-selection experiments: which tier Codex and Claude Code pick under different wordings (product) |
| Adoption, demand side: funnel, features of who benefits, target population, barriers, qualitative research | Architecture, schema compatibility, fallback, kill switch, on-call, guardrails (engineering) |
| Value: definitions at the person and tenant level, baseline, post-launch readings | Go/no-go and tool description revisions (product) |

Removed from v1 entirely, and not kept in a smaller form: v1's WL3 (tool description harness, capture lab, candidate variants); the part of v1's WL4 on the causal effect of the tool description and on exposure inference; the sync-versus-async decision, the tool description freeze date, the V_launch selection rule, the decision mapping from sizing to tool description direction, and the guardrail parameters.

### 2.2 Interfaces

| Direction | Content | Purpose |
|---|---|---|
| From product | Evaluation conclusions on which task classes agentic does better than light on. The task classification must map to the production intent labels | To convert into "addressable demand" |
| From product | Tool description versions and change dates; tier-selection experiment results; call traces with known structure from offline evaluation (if they can be shared) | To split post-launch windows; to explain "demand but no use"; to calibrate Se/Sp |
| From engineering | Instrumentation in the agentic search service (MCP-side data is confirmed with the MCP team; section 6); agentic latency p50/p95, per-call cost or quota rules; launch date and population; backend change log | Barrier analysis; baseline window |
| To product | Target population definition and size; list of quality problems in light search; value metric definitions and baseline; need-stratum labels computed before launch | Need strata use pre-launch features only. Product can therefore use them as a stratification variable, not affected by the tool description, when it analyses tier selection |
| To engineering | Automation profiles (class, C1/C2) and cost risk intervals; instrumentation requirements | Quotas and guardrails are set by engineering |

**Link to the tool description evaluation.** Product answers "on a given task, did the agent choose correctly, and was the result good?" (call and task level). This team answers "over time, which people and tenants use the tool, and do search time and re-searching change?" (person level, longitudinal). We do not estimate the effect of the tool description. We report the windows before and after a change separately and make no attribution.

### 2.3 Reference notes for the product team (benchmark survey, not developed into a design)

1. Atlassian's `search` already has a `mode` parameter (STANDARD by default, ENHANCED, AGENTIC). During the gradual rollout in 2026-10, users hit a 403 "Agentic search is not enabled". The official skill calls the heavier modes "optional extras" and falls back silently on failure. Evidence: the official skill and an official forum reply. The full schema is **unverified**. Implication: the enablement conditions and the runtime errors are themselves adoption barriers.
2. Of 16 composite products, only 3 put light and heavy retrieval behind a parameter of the same tool. More often they split them into separate tools. No product uses the name `effort`. "The industry prefers splitting" is an inference.
3. Client-side tool search retrieves by name and description. Sentry changed only the first sentence and the pointers to sibling tools. Across 56 queries, top-3 misses fell from 7 to 2 (official commit, which describes itself as directional).
4. Each Atlassian `search` call consumes up to 10 Rovo credits and fails if credits run out. A third party says overage billing starts on 2026-12-03 (**unverified**). The cost will pass through to administrators.
5. A public Atlassian ticket says that when a query is longer than 10–15 words, MCP search quality is lower than in-product search. This hints that the light tier may be weak on long requests. We will test this by using query length as a stratification variable for quality.

## 3. Research questions and hypotheses

| RQ | Testable hypothesis (initial) | Method | Purpose |
|---|---|---|---|
| RQ1 Usage | H1a: By tool call, usage is highly concentrated (a few automation accounts account for >50%). By person or by episode, it is clearly more spread out | Lorenz curves on three views: tool call, episode, cost | Explains why we weight by person |
| | H1b: At least one of the highest-volume automation accounts is C2 (script with hard-coded parameters) | Constant-parameter ratio, client and authentication fields, CSM reconciliation | Whether a C2 account uses the agentic tier is decided by the customer's developers |
| RQ2 Quality | H2a: Retry chains concentrate on low-confidence results (`top_score` below the tenant P25, or zero results) | Compare the confidence distributions of retry chains and dependent chains | If retries are common, the problem lies in retrieval quality |
| | H2b: Differences in chain rate come mainly from caller style: the variance between client × version accounts for more than 50% | Variance decomposition in a mixed model | If it holds, chain metrics that are not stratified cannot be used as evidence of demand |
| | H2c: There are cross-tool signals that looking at search alone would miss (long search↔fetch chains, switching between search and structured queries) | Cross-tool episodes | Adds to the demand and quality evidence |
| RQ3 Demand | H3a: Dependent episodes concentrate in a few people and tenants, and the share is higher in class B than in class A | Person-level and tenant-level distributions + cluster bootstrap | Target population |
| | H3b: The possibly unmet demand of "complex intent × single tool call × low confidence" is not negligible | 2×2 | Reported separately from demand that is already met |
| RQ4 Adoption | H4a: People in a high need stratum before launch use the agentic tier more often after launch | Pre-registered stratified comparison | Tests the target population definition |
| | H4b: The median episode wall-clock time of existing dependent chains is ≥ the agentic p50. Expected to hold for class B, not necessarily for class A | Baseline `span_s` compared with the latency from engineering | Latency tolerance as a barrier |
| RQ5 Value | H5: For people who use the agentic tier, `W_ud` does not increase and `re_search_30m` decreases | ITS + same-user before/after pairing + negative control | A descriptive reading, not a go/no-go |

## 4. Metric definitions

### 4.1 Units, populations and weighting

- **Units**: tool call; step (tool calls in the same stream that start ≤1 s apart, or whose intervals overlap, count as one step); episode (4.2); user-day (the denominator is people who were active in the baseline period, and it includes days with zero tool calls).
- **Class**: A interactive human; B human-started long-running task; C unattended pipeline, split into C1 (the LLM decides the tool calls) and C2 (script with hard-coded parameters). Class is a soft label at the episode level. An account gets a mixture proportion. We draw a single-class conclusion for an account only if one class reaches ≥90%. Before launch, class C is decided by manual profiling plus CSM reconciliation. The classifier gives probabilities only. We report two versions: borderline accounts all assigned to A, and all assigned to C.
- **Weighting**: episode → within-person average → macro-average across people → tenant weight ∝ min(√active people, cap). Cluster bootstrap at the tenant level.
- **Report layout, three columns**: person-weighted (A+B, with B shown separately), automation separately, and raw total. We add a sensitivity analysis that drops the top-2 accounts of each tenant. Cells with fewer than 10 people are suppressed.

### 4.2 Episodes and call chain types

- The stream key is (tenant, user, client). We allow at most 5 open episodes, to handle interleaving. The session in the trace is used only as a soft hint. **Episodes cover all tools in the server.**
- `T_hard` starts at 10 min. We set it per client category by fitting a GMM to the gaps in the log and taking the valley. The merge condition is `emb_cos_max5 ≥ θ_e`. Once doc_id is available, we can add result overlap or CTAR. We set θ at the P99 of a null built from pairs of the same user on different days (a cross-user null would be too easy). Resends after an error do not count in behavioural metrics.

| Type | Rule (initial values) | Counted toward |
|---|---|---|
| retry | Adjacent `emb_cos ≥0.9` or exact repeat, and the result is low-confidence or has overlap ≥0.6 | Quality problem list. **Not counted as demand** |
| refine | θ_e ≤ `emb_cos` <0.9, and the result is not low-confidence | Not counted |
| dependent | ≥3 sequential steps, adjacent `emb_cos` < θ_e, gaps on the order of seconds. With CTAR, require ≥ θ_c. Without CTAR, report an interval | **Main body of agentic demand** |
| search↔fetch | search and fetch alternate, reading several different documents | Counted as multi-step demand. We stratify by client first, to rule out style effects |
| search↔structured | A search followed by a switch to a structured query, or the reverse | Reported separately. Attribution is still open (insufficient retrieval, or a need for structured queries) |
| fanout / batch | `step_width ≥3` and sibling `emb_cos ≤0.6` / class C patterns | Reported separately / excluded from the people denominators |

- Call chains arise from three sources. **Only dependent chains and confirmed cross-tool multi-step chains count as agentic demand.** Result-reactivity identifies only rewrite loops. It does not identify dependent chains, because after a successful call the next hop is not similar to the previous hop to begin with.
- Sources for Se/Sp: internal employees opt in to label their own call sequences (200–300 items, needs approval); traces from the product team's offline evaluation (if they can be shared). If we have neither, we report only the interval between the wide and narrow thresholds.

### 4.3 Latent demand

| Metric | Definition |
|---|---|
| `dep_rate_H` | Share of human episodes that are dependent (including confirmed cross-tool multi-step), stratified by client × version |
| `need_people` / `need_tenants` | Number of people with dependent episodes on ≥2 different days, and the number of tenants they cover |
| `retrieval_fail_rate_H` | Retry-type share, aggregated by intent × data source into the quality problem list |
| `complex_single_unmet` | Share with `multihop_score ≥τ`, a single tool call and a low-confidence result (possibly unmet) |
| `style_share` | Share of the variance in chain rate that lies between clients |
| Addressable demand | Number of dependent episodes × the share, taken from the product evaluation, of "agentic does better on this intent class". Not reported until the product conclusions are available |
| `calls_saveable_C` | Σ(n_calls−1) over C1 dependent chains. Used only as an upper bound on automation cost |

Demand that is already met (dependent, fanout, cross-tool) and possibly unmet demand are reported separately and are not added. We report intervals under both the wide and narrow thresholds. Rogan-Gladen is used only to give bounds. Every table states its confounders: caller style, the user's AGENTS.md or CLAUDE.md instructions, the current tool description, and the caller's model and effort, which we cannot observe. `need_score`, query length and the intent distribution are all affected by the tool description. **After launch we no longer use them for demand estimation.** We use only their pre-launch values, for sizing and stratification.

### 4.4 Adoption funnel

| Stage | Definition | Denominator |
|---|---|---|
| T1 | Tenant has MCP enabled | All customer tenants |
| T2 | Account has completed MCP authorisation | Valid accounts in the tenant |
| T3 | At least 1 tool call of any tool in the week | T2 |
| T4 | At least 1 search episode in the week | T3 |
| T5 (after launch) | At least 1 actual agentic execution in the week | T4 |
| T6 | Used again within 14 days of the first agentic use | T5 |

We report by class, tenant and client. We report T5 and T6 additionally by pre-launch need stratum. "Did not use" is decomposed into these cases: the agent never requested agentic; it requested agentic, but the request fell back to light, timed out or was cancelled; the tenant is not enabled; the client cannot see the new parameter. The last two rely on information from product and engineering. Conclusions from internal beta-testing employees are labelled separately and are **not extrapolated to customers**.

### 4.5 Value

| Metric | Definition | What it measures |
|---|---|---|
| `W_ud` | Σ episode span per user-day (including agentic latency) | The part of waiting time that belongs to search |
| `equiv_calls_ud` | Σ (a light call counts as 1; an agentic call counts as its number of internal sub-retrievals) | Tool-side cost |
| `re_search_30m` | Share of episodes after which, within 30 min of the end, a new episode appears whose first query has `emb_cos_max5 ≥0.7` with it | Proxy for unmet need |
| `refind_xday` | Share of returned documents that were already seen in the past 7 days (needs doc_id) | Picking up work across days |
| `terminal_conf` | `top_score` of the last tool call, and whether it returned zero results | Coarse proxy for convergence |
| Subjective rating | Interviews and a short questionnaire | The only measure that comes close to whether people accept the outcome |

**"Shorter chains" is not used as a value metric.** The tool description may itself ask for fewer rewrites, so shorter chains only show that the agent complies. Retention is described only. We cannot measure whether the agent's task was completed or whether people accepted the outcome. A direct comparison between people who use the agentic tier and people who do not is self-selected, so we do not report it as causal. Atlassian's self-reported "adopters' ARR growth is about 2 times that of non-adopters" is this kind of comparison.

## 5. Workstreams

**WL1 Usage and qualitative profiling of automation accounts**
- What we do: Lorenz curves on the three views, and segmentation. An automation sampling frame (top 20 by tool calls, top 10 by cost, 10 random from the tail, at most 3 accounts per tenant). One page of profile per account (template in the automation research notes, §4.2 (internal, not in this repo)). Evidence is graded. Strong evidence is only client-credentials authorisation or a service account. A clientInfo of `mcp/0.1.0`, or a workflow-type name, is moderate. An old `auth_time` or a static header is weak. A gap above 60 s does not mean a human is in the loop. The "Claude Code 60 s timeout spike" cannot be used as a fingerprint (corrected in v1, Appendix B (internal, not in this repo)). We do not build our own capture lab. We calibrate the gap thresholds with employee accounts and CSM-confirmed accounts as seeds. CSM reconciliation and 3–5 customer interviews (automation research notes, §4.3–4.4 (internal, not in this repo)). Convert C1 dependent chains into the tool call volume and cost interval "if they used the agentic tier instead".
- Outputs: current state of usage; automation profiles and class labels (two versions); cost risk notes.
- Dependencies: logs; authentication and client fields; CSM; agentic per-call cost.

**WL2 Quality and latent demand**
- What we do: Implement and calibrate 4.2, and test H2 and H3. Report the 4.3 intervals by person, tenant, client and class. Summarise retry chains and low-confidence results for long queries into a quality problem list. Run internal interviews with 5–8 people plus a questionnaire, asking "what did you not ask the agent to search for, because you thought it could not be found?" Once the product evaluation is available, convert to addressable demand.
- Outputs: a specification document (the metric registry states the population and weighting); sizing v1 (behavioural level); sizing v2 (addressable); quality problem list.
- Dependencies: trace; derived query features and their approval; WL1 classes; product evaluation.

**WL3 Adoption**
- What we do: Current state of T1–T4. Define the first target population using pre-launch features only (high need stratum, many class B long tasks, tenant already enabled), give an interval for its size, and pre-register H4a. Barrier analysis: latency tolerance (H4b plus interviews), cost or quota, the administrator enablement threshold, and awareness (questionnaire). Schedule the qualitative research together with WL1, and reconcile what people say with telemetry. After launch, report T5, T6 and the "did not use" decomposition.
- Outputs: funnel baseline; target population list and size; barrier list (with strength of evidence); post-launch adoption report.
- Dependencies: tenant enablement and connection data; latency and billing information; the product team's tier-selection experiment results.

**WL4 Value**
- What we do: Define the 4.5 metrics and hand them to product. Build a baseline of at least 3 clean weeks. Split users randomly into two halves for an A/A test, to estimate the noise floor and the detectable effect. Back-fill the existing coarse-grained series as far as possible, to serve as the long pre-period series for ITS. After launch: ITS plus same-user before/after pairing, stratified by client. The negative control is the latency, errors and tool call volume of light tool calls from C2 accounts. Client upgrades and backend changes enter as covariates. Windows before and after a tool description change are analysed separately. Write down the reading rules before launch, to avoid choosing metrics after the fact.
- Outputs: baseline dashboard; first read at +4 weeks; report at +8 weeks (including limitations).
- Dependencies: derived query features; trace; agentic sub-retrieval counts; change log.

## 6. Instrumentation requirements (summary)

The full version is in [`instrumentation-requirements.md`](instrumentation-requirements.md) (revised 2026-11-24). It targets logging inside the **agentic search service**, not the MCP server. The request path is caller agent → MCP server → agentic search service → retrieval backend. Each field has one system of record: the layer that is the only one able to see it. The document has three tables.

- **Table 1, the ask, to the engineering team for the agentic search service.** Request-level fields: service request ID, the existing join ID to the MCP call, entry surface (so that MCP traffic can be separated from CLI traffic), tenant and user identifiers passed through, timings, the service's own status, executed tier and `fallback_reason`, cost units. One record per internal step: type, latency, results, top score, document IDs, sub-query length and similarity without text. A per-request summary with stop reason; answer length, citations and a no-answer flag; derived features of the original query; versions and a change log. From the step trace we compute offline whether an agentic request was needed, its realised complexity, and where failures and latency occur. It is a requirements list, not a gap list.
- **Table 2, a dependency owned by the MCP team.** MCP-side data we assume exists: tenant and user, tool calls for every tool, caller-experienced time and status, caller identity, the join ID; and, for finer analysis, query similarity and query features of current search calls, result fields, funnel events, requested tier, document IDs, tool description version and session ID. We ask only for confirmation and raise gaps with the MCP team separately. R1–R3 and the pre-launch baseline depend mainly on this table. Pre-launch analysis depends on this MCP-side data, to be confirmed with the MCP team using [`mcp-data-checklist.md`](mcp-data-checklist.md); if the finer items are missing, the pre-launch latent demand estimate stays at a coarse level.
- **Table 3, the join contract.** The existing join ID (field name and coverage to be confirmed), tenant and user identifiers, and clock alignment.

Timing: the agentic search service has no customer traffic before launch, so Table 1 fields must be complete on launch day and should be recorded in the internal beta from now on. The pre-launch baseline of at least 3 clean weeks applies to current search behaviour (Table 2), whose derived query features cannot be backfilled. Whether light-tier requests pass through the agentic search service at all is still open. Priorities: A is recorded in the internal beta now and complete at launch; B is complete at launch; C can be added after launch. Fields in v1 that served the tool description evaluation or guardrails are no longer required.

## 7. Phased timeline

| Phase | What we do | Outputs |
|---|---|---|
| Now (existing logs only) | Send the instrumentation requirements and submit them for approval. WL1 segmentation and automation profiles. Current state of T1–T4. A coarse split by time only, to give an upper bound on multi-call episodes (it cannot separate the three sources). Start CSM reconciliation and interviews. Back-fill the ITS series | Instrumentation requirements; usage current state; automation profile v0 |
| After trace is available (before launch) | Calibrate episodes and chain types. Sizing v1. Target population. Baseline and A/A. Once doc_id or URL is available, add the document-level metrics | Sizing v1; target population; baseline |
| After the January launch | T5, T6 and the "did not use" decomposition. Value readings. Observe automation volume and cost. Sizing v2 | Adoption and value reports |

Only two constraints have a basis. Launch is in January 2027. And the baseline needs at least 3 clean weeks before launch (an initial assumption; the year-end holidays do not count, and v1 assumed they run 12/21–1/3). If launch is in mid-January, the derived query features of current search calls and the trace (MCP-side data; section 6) need to be in place around the first week of December. Otherwise value can only be analysed descriptively. We will schedule the other milestones once the launch and trace dates are fixed.

## 8. Risks and questions we cannot answer

**Risks**: Instrumentation or approval delays leave too little baseline. Classification errors for automation accounts change the denominator for people (the two versions give bounds). Without CTAR, the dependent interval may be too wide to rank populations. Demand comes from customer logs, but early agentic usage comes from internal beta-testing employees. With small traffic, absolute metrics cannot support causal conclusions about subgroups (Radlinski et al. 2008). Concurrent shocks such as holidays, client upgrades and ranking changes.

**What the narrowed plan cannot answer**
- Whether agentic can actually meet the demand we identify: this depends on the product evaluation. Without it, sizing stays at the behavioural level and acts as an upper bound.
- How much of "demand but no use" is a tool description or tier-selection problem: this depends on the product team's tier-selection experiments. This research can only separate it from causes such as enablement, latency and failure.
- The causal effect of the tool description wording; the causal effect of agentic on value (there is no randomisation, only a quasi-experimental reading of the overall launch effect).
- Whether the agent's task was completed and whether people accepted the outcome; demand that was never raised because people thought it could not be found (interviews can fill in only part of this); the value of C2 script accounts (only possible through customer communication); product trade-offs (merging tools, default tier, pricing).

## 9. Questions for the project owner to confirm

1. **Data and privacy**: Who approves the derived query features (adjacent similarity, intent labels, `query_hash` computed with a tenant key, CTAR), and when will we have a decision? When will trace and URL be available? Can the retrieval backend write doc_id today?
2. **Launch form**: The exact date in January. Whether launch covers all customer tenants and automation accounts. Whether agentic needs separate enablement by an administrator. Whether it is billed by usage or has a quota.
3. **Product interface**: Can their evaluation and tier-selection experiments give conclusions by a task classification that maps to the production intent labels, and can they share them? When? Who maintains the tool description change log?
4. **Qualitative channels**: Can we reach the owners of the top automation accounts through CSMs, and run 3–5 customer interviews? Are internal interviews and opt-in self-labelling feasible?
5. **Purpose of value**: Is it for description and recommendations only, or does it need to support a decision (such as wider rollout)? If the latter, who sets the decision criterion (such as the non-inferiority margin for `W_ud`)?
6. **Delivery order**: After instrumentation, do we deliver the automation profiles first (for engineering) or the first target population (for product)?
