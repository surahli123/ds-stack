# Agent runbook: find measurement gaps from search DSAT tickets

You are an agent running this analysis for a data scientist, inside their company environment, on real data. Follow the steps in order. Stop and report at any step whose stop condition is met.

To start it, the person tells you: "Read and follow `docs/dsat-ticket-runbook.md` in the ds-stack repo. The tickets are in `<where>`, the search log is in `<where>`, the month is `<YYYY-MM>`, write outputs to `<directory>`."

## What this is for

The owner's request, verbatim: "假设我要做一个analysis关于search DSAT，目的是根据insights来帮助我们理解现在的measurement有什么gap". An English gloss: suppose I do an analysis of search DSAT; the purpose is to use what it shows to understand what gaps the current measurement has.

A DSAT here is a ticket a user opened about search, with written feedback and the query and results they attached. Each in-scope ticket is a search the user reports as failed. The analysis asks one thing: for those searches, what did our metrics say? A failure the metric scored as a success is a gap in the measurement.

The output is a gap list. It is not a quality trend, not a failure rate, and not a recommendation on what to fund. Add none of those unless the person asks.

## Rules

- **Data stays inside the company environment.** The only place to show ticket content is this session with the person. Don't copy ticket text, queries, document titles, tenant names or user names into any commit, pull request, issue, other chat, web search or outside tool.
- **Models must be approved for this data.** That covers your own model endpoint and any reader or reviewer model a skill calls. If you are not sure, ask before reading a ticket.
- **Work from the output directory.** `cd` into the directory the person named. It must be outside any git repository. Set `DS_QUERIES_LOG` and `DS_CHECKS_LOG` to files in it, and `TMPDIR` to a folder in it. Never `git add` anything produced here. Every output file holds customer text: say so in its first line.
- **Read-only on every data source.** The one exception is `ds-mode`'s own scratch tables under its scratch prefix, and only if the person confirms the warehouse allows them. Change nothing in the ticket system.
- **Read every ticket for the month**, by ticket created time. Don't sample.
- **Use only what a ticket carries and what the log records.**
- **Don't invent a definition.** If `metrics.json` exists in `$DS_OVERLAY_DIR`, it is the definition; if it disagrees with what the person says, stop and ask. Otherwise take each definition from the person and record "confirmed by <person>, <date>" beside it in `analysis_plan.md`.
- **Plan before work.** Show the plan from step 0 and wait for the person's go before step 1. Reading a few tickets and one log lookup to build the plan's examples is allowed before the go.
- **Stop conditions are defaults.** The numbers in them ("about 2,000", "a third", "about 50%") were chosen by this runbook's author, not by the team. When one is met, stop and ask the person whether to continue; they may override it.
- **Failures.** If a step fails, retry once, then stop and report what failed, with the output. Inside `ds-mode`, its own rerun rule applies to its verification step.

## What you need from the person

1. Where the tickets are, and which fields hold the feedback text, the attached query, the attached results, the tenant, the ticket's created time, and the time of the search the user attached.
2. Where the search log is, which fields hold the query id, time, tenant and the per-search metric values, and how the query tool reaches it: `DS_WAREHOUSE`, or a warehouse adapter under `DS_OVERLAY_DIR`. If no adapter exists, stop and ask; the person can run the SQL and paste the result, which `ds-mode` logs with `--pasted`.
3. The definition and grain of each online metric in use. For example: a click-quality score per search, an AI-answer success rule, and any composite built from them. Write down the exact rule, including time windows and thresholds, and whether the metric is per search, per session or per answer.
4. For each metric, what value counts as "the metric scored this search a success". If the team has no cut-off, report results at more than one cut-off and say so.
5. For the timestamp join in step 2: how wide a time window to accept.

If there are more than about 2,000 tickets for the month, stop and ask before reading them.

## Steps

### 0. Write the plan and get a go

Write `analysis_plan.md` in the output directory. Start it with each metric's definition, grain and success cut-off. Then, for each of steps 1 to 4, state: what will be computed, in plain words with numerator and denominator; one worked example using a ticket from this month; which data it depends on; and what it cannot tell us. List anything the request asks that the data cannot answer.

Show it to the person. Their go also confirms the metric definitions. Do not continue without it.

### 1. Read every ticket and give it a failure type

Read all tickets first without labelling. Derive the categories from what users wrote; don't start from a fixed list. Then label every ticket with exactly one category.

- Keep a category for tickets that are not about search quality (a UI request, a login problem) and one for feedback too vague to classify. Don't force these into a failure type. Every other category is in scope.
- Use the attached query and results as evidence, not only the text. Example: the feedback says the first result is the old version, and the attached first result was last modified two years ago. Label: outdated content.
- Write `ticket_labels.csv` (ticket id, category, one-line reason) and `ticket_categories.md` (each category, its definition, its count, and two or three verbatim tickets, no more).
- Ask the person to check about 30 labels picked at random, and report how many they agree with. The labels are one agent's reading, not a reviewed truth; say so wherever they are used.

This step is reading text. `ds-mode` runs aggregate queries only, so do this step outside it, and say in the output that it was done by reading, by which model, and that it has no query log.

Stop if more than about a third of tickets land in "too vague": the categories will not support the rest of the analysis.

### 2. Join each ticket to its search and read what each metric scored

- Join by the attached query id. For tickets without a usable id, try tenant plus the time of the attached search (not the ticket's created time), inside the window the person chose, and require the query text to match where the log holds it. Accept a match only when exactly one log row fits.
- Report the join rate for each method and in total, and the join rate per category. If one category's join rate is more than 10 points below the total, say so: its results rest on fewer tickets.
- List the tickets that did not join and why (no id, id not in the log, time outside the log). Exclude them from everything below, and say how many.
- For each category and each metric, report: joined tickets, how many the metric scored a success, and that share with an interval. The share is the miss rate.

How to run it: the labels are in a local file and the log is in the warehouse. Pass each category's ticket ids to the query as an inline id list, and keep every result aggregated to one row per category. The query runner returns at most 200 rows and refuses row-level output, so a per-ticket result will be blocked.

Example of one miss: the user long-clicked the outdated first result and read it, so the click metric gave the search a high score. The user then opened a ticket. The metric said success; the user said failure.

Stop if the total join rate is under about 50%. Report the join problem first; the miss rates would rest on too few tickets.

### 3. Turn each failure type into a log signature and count it in all traffic

For each in-scope category, write the pattern in the log that the failed searches share, using only logged fields. Example: "long click on a document last modified more than a year ago". Then count searches matching it in all traffic for the month, as a count and as a share of all searches.

- Say plainly, next to every count, that it counts searches matching the signature, not confirmed failures. A matching search may have been fine.
- Report two shares side by side for each signature: the share of the category's joined tickets that match it, and the share of all searches that match it. A signature that matches few of its own tickets is not usable. Neither is one that most traffic matches, however many tickets it catches. The signature was written from these same tickets, so this is an in-sample check; say so.
- Look at how each count is spread over days, tenants and source systems. One outage week or one large tenant can supply most of a count. Report it when it does.
- Some categories have no possible signature. A factually wrong AI answer that the user accepted looks the same in the log as a good answer. List these separately. They are the gaps no log-based metric can close.

### 4. Summarise as a gap list

One row per in-scope category. The "not about search quality" and "too vague" categories get a row with their ticket count only.

| Failure type | Tickets | Joined | Scored a success by each metric (n, share, interval) | Searches matching the signature (count, share of all) | Signature usable? |
|---|---|---|---|---|---|

Then, in this order: the categories the metrics miss most; the categories the metrics already catch; the categories with no log signature; and what the analysis cannot tell us. Don't rank a category whose joined tickets are fewer than a floor agreed with the person.

Label every statement as measured, inferred from measured facts, or a guess. A belief with no measurement behind it is a guess, however plausible.

## What this analysis cannot tell us

State these in the output. Don't soften them.

- **The overall failure rate.** We don't know what share of failed searches leads to a ticket. It is likely small, and who files one is not random. Shares among tickets are shares among people who complained.
- **Failures nobody reports.** A user who never notices the failure, or whose results were trimmed by permissions, opens no ticket.
- **Errors in the other direction.** A search the metric scored a failure while the user was satisfied never produces a ticket.
- **Whether quality is getting better or worse.** A change in ticket volume can come from a change in users or in filing habits.
- **How many matching searches really failed.** Step 3 counts matches.

Optional, only if the person asks: tickets per 1,000 searches by tenant tier or source system. This is a ticket rate. It cannot separate how often search fails from how readily people file.

## Using the ds-stack skills

- Step 0: if `ds-plan` is installed, use it to write the plan, then add the worked example per step that this runbook asks for. This runbook's wait-for-go is stricter than `ds-plan`'s own flow; the runbook wins.
- Step 1: outside the skills, as above.
- Steps 2 to 4: use `ds-mode` and follow its `SKILL.md`, within the rules above. Its readout needs one Headline number: use the composite metric's miss rate among joined in-scope tickets, with its interval. Put the gap list as tagged lines under Answer, one tag per number. Note in the output anywhere the format did not fit.
- Check the readout with `ds-verify` if it is installed. It copies the database to a temporary directory, so keep `TMPDIR` inside the output directory, and skip it if the warehouse cannot be copied. Either way, verify by hand at least three numbers in the readout against the logged query results. A tag proves a query ran, not that the number came from it.
- Write-up, if the person wants one: `ds-doc`, then `doc-tighten`. `cold-read` sends the document to a reader model: run it only if the document holds no verbatim ticket text and the person confirms the reader model is approved. Otherwise use its `--prompts-only` path or skip it.
- If the skills are not installed, the four steps still stand. Log every query and its result in a file so each number can be traced.

## What to hand back

In the output directory: `analysis_plan.md`, `ticket_labels.csv`, `ticket_categories.md`, the query log, and the readout with the gap list. Report to the person, in this session: the join rate, the gap list, the label spot-check result, what could not be answered, and anything you did not verify, marked as not verified.

## Later uses of the same tickets

Not part of this run. Do one only when the person asks. Each reuses the labels from step 1.

1. **A check set for metrics.** Each labelled in-scope ticket is a search a user reported as failed. Before adopting a new metric or changing one, ask how many of these it scores correctly.
2. **New signals.** For a category the metrics miss, a signature from step 3 that matches most of its tickets and little of all traffic is a candidate monitor. Test it on a later month's tickets first.
3. **An alarm.** Tickets per 1,000 searches by tenant and source system. It does not measure quality, but an outage shows up in it quickly.
