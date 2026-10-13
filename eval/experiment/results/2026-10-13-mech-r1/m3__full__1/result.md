Ready for triage: Ready

This is the script's verdict. I disagree with it, so read the last two lines below before triage. The readout and prep sheet follow as rendered.

# Ranker v7: No effect found

Decision: No effect found. Successful Search Rate reads +0.00% (-0.30% to +0.30%), which rules out the 0.50% change the test was built to find.

Ask: Agree to stop the test without launching.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: Latency p95 (ms) rose 6.00% (+5.20% to +6.80%), the wrong way, inside its margin.

Triage: Ready: every movement triage will ask about has a candidate explanation and none conflict; the explanations are inferred from co-movements, so the cuts below would confirm them.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | +0.00% (-0.30% to +0.30%) | estimate at least 0.50% higher | unclear |
| Latency p95 (ms) | guardrail | +6.00% (+5.20% to +6.80%) | at most 10.00% higher | worse, within margin |
| Abandonment Rate | guardrail | +1.60% (+1.20% to +2.00%) | at most 3.00% higher | worse, within margin |

Checks: passed: scorecard, sample split, config params, config edits, novelty; not run: pre period.

## What would change the call

- Latency and abandonment by latency bucket showing the loss only in slow buckets, with relevance up where latency is unchanged, would turn this into a speed fix and rerun.
- A pre-period check on Successful Search Rate, which could not run, showing a baseline gap between arms.
- Tighter guardrail margins than the registered 10% latency and 3% abandonment, as in the team standards of 2% and 1%, would put both guardrails past their margin.

## Why it moved

- [inferred] Latency p95 rose 6.00% and Abandonment Rate rose 1.60%: slower results costing clicks is the leading candidate, and CTR dropping is the same story; no cut has been run yet.
- [guess] Successful Search Rate is flat (+0.00%), consistent with a relevance gain offset by the slowdown, or with no relevance gain; the data cannot separate these.
- [guess] Abandonment could also be users giving up on worse results rather than on slow pages; the answer-and-snippet split tells these apart.

## Appendix

- Secondary metrics: 54 tested; after a false-discovery correction these moved: CTR (-1.50%). They are exploratory and don't change the call.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

# Ranker v7: triage prep

Scripted call: No effect found. Successful Search Rate reads +0.00% (-0.30% to +0.30%), which rules out the 0.50% change the test was built to find.

## Before any single metric

- What did you change? ranker_model: lambdamart_v6 -> lambdamart_v7; nothing else differs between arms.
- Is the data trustworthy? Yes, as far as the checks reach; not checked: pre period.
- Is the effect real, or chance? Successful Search Rate +0.00% (-0.30% to +0.30%); its interval includes zero. Across the scorecard 4 of 57 metrics moved clearly; about 2.9 would by chance alone.
- Will it last? Probably: effect by days since exposure: first days -0.01%, last days +0.01% (trend +0.002% per day).
- Did the change do what it was built to do? Not shown. If the scorecard or a cut has a coverage metric (the share of queries whose top results changed), register it as feature_metrics.

## Questions triage will ask

1. Successful Search Rate was expected to rise but didn't move. Why? Status: untested.
   - Likely [inferred]: Slower results cost engagement. Latency p95 rose 6.00%, Abandonment Rate rose 1.60%, CTR fell 1.50%. To check: cuts 1 and 3.
   - Likely [inferred]: Worse results make users give up. To check: cuts 2 and 4.
2. Why did Latency p95 (ms) rise? Likely slower results (question 1). Untested.
3. Why did Abandonment Rate rise? Likely slower results or worse results (question 1). Untested.
4. Why did CTR fall? It fell 1.50% (-1.90% to -1.10%). Likely slower results or worse results (question 1). Untested.

## Ruled out

- Answers on the page reduce clicks: Latency p95 (ms) rose 6.00% (+5.20% to +6.80%).
- Some queries win, others lose: CTR fell 1.50% (-1.90% to -1.10%).

## Cuts to run before triage, in order

1. Abandonment and CTR by latency bucket, per arm. Supports slower results: the loss sits in the slow buckets. Against: the loss is flat across buckets.
2. Abandonment on queries with an answer or rich snippet vs without. Supports worse results: the rise sits on queries without an answer. Against: it sits on answer-bearing queries.
3. Latency by page type and load type (cached vs fresh), by arm. Supports slower results: latency rises on the same page types. Against: the page mix changed.
4. Config diff of presentation parameters (answers, rich snippets). Supports worse results: only ranking differs. Against: an answer or snippet parameter differs.
5. Effect by device and network type. Supports slower results: mobile or slow networks carry the loss. Against: the loss is the same everywhere.

doc_lint: 0 fail, 0 warn, 311 body words (readout)
cold-read: skim 2/2, full 2/3 - fail

The cold read failed: a fresh reader was unsure whether "Could reverse it" and the triage status settle anything.

My view, separate from the script's: I'd call this "Ready, with open questions".
- None of the five cuts has been run, because I have no data access. Every explanation is inferred.
- The pre-period check couldn't run.
- The team's registered margins are 10% for latency and 3% for abandonment. The team standards are 2% and 1%. Latency (+6.00%) and abandonment (+1.60%) both clear the standards' limits, so the engineer should expect that question.

I shortened the prep sheet from the rendered file, so check it against `triage_prep.md` in the work directory.