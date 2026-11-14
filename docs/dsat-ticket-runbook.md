# Agent runbook: find measurement gaps from search DSAT tickets

You are an agent running this analysis for a data scientist, inside their company environment, on real data. Follow the steps in order. Stop and report at any step whose stop condition is met.

To start it, the person tells you: "Read and follow `docs/dsat-ticket-runbook.md` in the ds-stack repo. The tickets are in `<where>`, the search log is in `<where>`, the month is `<YYYY-MM>`."

## What this is for

The owner's request, in their words: "假设我要做一个analysis关于search DSAT，目的是根据insights来帮助我们理解现在的measurement有什么gap". In English: analyse search DSAT, and use what it shows to understand what gaps the current measurement has.

A DSAT here is a ticket a user opened about search, with written feedback and the query and results they attached. Each ticket is a search the user says failed. The analysis asks one thing: for those searches, what did our metrics say? A failure the metric scored as a success is a gap in the measurement.

The output is a gap list. It is not a quality trend, not a failure rate, and not a recommendation on what to fund. Add none of those unless the person asks.

## Rules

- Everything stays inside the company environment. Don't copy ticket text, queries, document titles, tenant names or user names into any commit, pull request, issue, chat, web search or outside tool. Write outputs only to a local working directory the person names.
- Read-only on every data source. Run no statement that writes, and change nothing in the ticket system.
- Read every ticket for the month. Don't sample. A few hundred is the expected size; if there are more than about 2,000, stop and ask.
- Use only what a ticket carries and what the log records. Don't look up customer content the person cannot view themselves.
- Don't invent a definition. Take each metric's definition from the person or from the team's metric documentation, write it at the top of the output, and get the person's confirmation before step 2.
- Before running anything, show the person the plan in step 0 and wait for their go.
- Retry a failed step at most once. If it fails again, stop and report what failed, with the output.

## What you need from the person

1. Where the tickets are, and which fields hold the feedback text, the attached query, the attached results, the tenant and the created time.
2. Where the search log is, and which fields hold the query id, time, tenant and the per-search metric values.
3. The definition of each online metric in use. For example: a click-quality score, an AI-answer success rule, and any composite built from them. Write down the exact rule, including time windows and thresholds.
4. For each metric, what value counts as "the metric scored this search a success". If the team has no cut-off, report results at more than one cut-off and say so.
5. A local directory for outputs.

## Steps

### 0. Write the plan and get a go

Write `analysis_plan.md` in the output directory. For each of steps 1 to 4 state: what will be computed, in plain words with numerator and denominator; one worked example using a ticket from this month; which data it depends on; and what it cannot tell us. List anything the request asks that the data cannot answer.

Show it to the person. Do not continue until they say go.

### 1. Read every ticket and give it a failure type

Read all tickets first without labelling. Derive the categories from what users wrote; don't start from a fixed list. Then label every ticket with exactly one category.

- Keep a category for tickets that are not about search quality (a UI request, a login problem) and one for feedback too vague to classify. Don't force these into a failure type.
- Use the attached query and results as evidence, not only the text. Example: the feedback says the first result is the old version, and the attached first result was last modified two years ago. Label: outdated content.
- Write `ticket_labels.csv` (ticket id, category, one-line reason) and `ticket_categories.md` (each category, its definition, its count, and two or three verbatim tickets).

This step is reading text. `ds-mode` runs aggregate queries only, so do this step outside it, and say in the output that it was done by reading, by whom or what, and that it has no query log.

Stop if more than about a third of tickets land in "too vague": the categories will not support the rest of the analysis. Report that instead.

### 2. Join each ticket to its search and read what each metric scored

- Join by the attached query id. For tickets without a usable id, try tenant plus timestamp, and accept a match only when exactly one log row fits.
- Report the join rate for each method and in total, and the join rate per category. If one category joins much worse than the others, say so: its results rest on fewer tickets.
- List the tickets that did not join and why (no id, id not in the log, time outside the log). Exclude them from everything below, and say how many.
- For each joined ticket, read each metric's value for that search. Per category and per metric, report: joined tickets, and how many the metric scored a success. That share is the miss rate.

Example of one miss: the user long-clicked the outdated first result and read it, so the click metric gave the search a high score. The user then opened a ticket. The metric said success; the user said failure.

Stop if the total join rate is under about 50%. Report the join problem first; the miss rates would rest on too few tickets.

### 3. Turn each failure type into a log signature and count it in all traffic

For each category, write the pattern in the log that the failed searches share, using only logged fields. Example: "long click on a document last modified more than a year ago". Then count searches matching it in all traffic for the month.

- Say plainly, next to every count, that it counts searches matching the signature, not confirmed failures. A matching search may have been fine.
- Check each signature against the tickets: of the joined tickets in that category, how many match the signature? A signature that matches few of its own tickets is not usable; say so.
- Look at how each count is spread over days, tenants and connectors. One outage week or one large tenant can supply most of a count. Report it when it does.
- Some categories have no possible signature. A factually wrong AI answer that the user accepted looks the same in the log as a good answer. List these separately. They are the gaps no log-based metric can close.

### 4. Summarise as a gap list

One row per category:

| Failure type | Tickets | Joined | Scored a success by each metric | Searches matching the signature in all traffic | Signature usable? |
|---|---|---|---|---|---|

Then, in this order: the categories the metrics miss most; the categories the metrics already catch; the categories with no log signature; and what the analysis cannot tell us.

## What this analysis cannot tell us

State these in the output. Don't soften them.

- **The overall failure rate.** Few failed searches lead to a ticket, and who files one is not random. Shares among tickets are shares among people who complained.
- **Errors in the other direction.** A search the metric scored a failure while the user was satisfied never produces a ticket. Tickets cannot show this gap.
- **Whether quality is getting better or worse.** A change in ticket volume can come from a change in users or in filing habits.
- **How many matching searches really failed.** Step 3 counts matches.

Check how uneven filing is where the data allows it: tickets per 1,000 searches by tenant tier, and by any other dimension the team uses. Report it next to the gap list.

## Using the ds-stack skills

- Step 0: if `ds-plan` is installed, use it to write the plan, then add the worked example per step that this runbook asks for.
- Step 1: outside the skills, as above.
- Steps 2 to 4: use `ds-mode` and follow its `SKILL.md` as written, including its query tool, its checks and its readout. The question here has several findings, not one number that moved; put the gap list where the skill's readout format allows, and note in the output anywhere the format did not fit.
- Check the readout with `ds-verify` if it is installed. Either way, verify by hand at least three numbers in the readout against the logged query results. A tag proves a query ran, not that the number came from it.
- Write-up, if the person wants one: `ds-doc`, then `doc-tighten`, then `cold-read` with a reader model the person's rules allow.
- If the skills are not installed, the four steps still stand. Log every query and its result in a file so each number can be traced.

## What to hand back

In the output directory: `analysis_plan.md`, `ticket_labels.csv`, `ticket_categories.md`, the query log, the readout with the gap list, and a short note of where the skills helped, blocked or misled. Report to the person: the join rate, the gap list, what could not be answered, and anything you did not verify, marked as not verified.

## Later uses of the same tickets

Do these only when asked. Each one reuses the labels from step 1.

1. **A check set for metrics.** Each labelled ticket is a search a user confirmed as failed. Before adopting a new metric or changing one, ask how many of these it scores correctly.
2. **New signals.** For each category the metrics miss, a signature from step 3 that matches most of its tickets is a candidate monitor.
3. **An alarm.** Tickets per 1,000 searches by tenant and connector. It does not measure quality, but an outage shows up in it quickly.

## Where this came from

A trial on synthetic data on 2026-11-11 ran these four steps and compared the result with what had been built into the data. It recovered the join rate and the per-type miss rates. It also showed three ways the analysis goes wrong, which the steps above now guard against: skipping the timestamp join, not looking at how a signature count is spread over time (a one-week connector outage supplied nearly a third of one count), and labelling an unsupported belief as an inference. The synthetic tickets came from templates, so labelling was far easier there than it will be on real tickets.
