# MCP-Side Data Checklist

> From: the MCP search research team. Date: 2026-11-24. Audience: the MCP team.
>
> This is a **confirmation request, not a requirements document**. We are asking what already exists and how to read it. We are not asking the MCP team to build anything.

**Context.** The research team studies how search through the MCP server is used today, and how well it works, to estimate latent demand for the agentic search tier that launches in January 2027 and to learn what drives adoption and value. The agentic tier has no customer traffic before launch, so current search behaviour is our only evidence until then. It is the baseline that post-launch readings are compared with, and it shows who uses search today and how. We cannot see query text and do not ask for it.

**How to answer.** For each row, mark exists / partly / does not exist, and give the field name and any notes on how to read it. Rows are ordered by how much the research depends on them.

- **Group 1** is needed for any pre-launch analysis.
- **Group 2** is needed for the finer analysis. We expect some of these not to exist. Where one does not, the plan falls back to a coarser pre-launch estimate, and the finer evidence comes from the agentic search service's own trace after launch.

R labels: R1 usage, R2 quality, R3 latent demand, R4 adoption, R5 value. A stream is the sequence of calls from the same tenant, user and client.

| Item | What we need it for | Exists / partly / does not exist | Your field name and notes | What we lose if it does not exist |
|---|---|---|---|---|
| **Group 1: needed for any pre-launch analysis** | | | | |
| M1 Tenant and user identifiers on every call | Counting people and tenants, not just calls (all R) | | | Almost everything: the research is at person and tenant level |
| M2 A record of every tool call, with tool name, for every tool on the server | Seeing usage of each tool and how search combines with other tools (R1, R2) | | | Cross-tool behaviour; usage outside search |
| M3 Start time, end time and latency as the caller experiences it | Grouping calls into episodes; time spent searching (R2, R5) | | | Episodes and the value baseline |
| M4 Caller identity: client name and version, user agent, authentication method, credential and grant type | Telling automation accounts from people; comparing callers (R1, R2) | | | Usage figures dominated by a few pipelines; no adjustment for caller style |
| M5 Status and error code, with client cancellation and timeout recorded as such | Excluding resends after errors; separating failure from non-use (R2, R4) | | | Errors counted as behaviour; a weaker non-use breakdown |
| M6 The join ID shared with the agentic search service | Linking each MCP call to what the service did, from launch (R4, R5) | | | Any link between who asked and what the agentic tier did |
| **Group 2: needed for the finer analysis** | | | | |
| M7 Similarity of each query to recent queries on the same stream (no text) | Telling retries, rewrites and genuine multi-step needs apart (R2, R3, R5) | | | Demand stays a coarse, time-based upper bound |
| M8 Query length, keyed hash and coarse intent label of each search call (no text) | Need strata before launch; exact repeats; complex requests answered in one call (R2, R3, R4) | | | Target population by behaviour only; no exact-repeat detection |
| M9 Result count, top score, cost, and backend and ranker version of each search call | Linking retries to weak results; cost concentration; ruling out backend changes (R1, R2, R5) | | | Retries not linked to result quality; no cost view |
| M10 Funnel events: tenant enablement, account connection, tenant size, agentic enablement | The adoption funnel and its denominators (R4) | | | The funnel starts at "active"; no enablement or connection stage |
| M11 Requested tier | Whether the agent ever asked for agentic, after launch (R4) | | | Cannot separate "never asked" from "asked but fell back" |
| M12 Identifiers of returned documents | Result overlap between calls; re-finding across days (R2, R3, R5) | | | Weaker retry detection; no cross-day measure |
| M13 Tool description version per call | Splitting readings before and after a description change (R4, R5) | | | Changes cannot be separated in time |
| M14 Session identifier | A soft hint for episode boundaries (R2) | | | Episodes rely on time gaps only |

**Closing questions**

1. How far back does each item go, and how long is it kept?
2. How does the research team get read access, and who approves it?
3. Are automation or service accounts flagged in any way?
4. What is the name of the join ID field shared with the agentic search service? Is it on every call that reaches the service, including retries and fallbacks?
5. Is there a schema or data dictionary we can read, and whom should we ask about what a field means?
