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

- A pre-exposure comparison of Successful Search Rate showing the arms were already apart would make the test unreliable.
- Abandonment and CTR by latency bucket that do not worsen as latency rises would rule out the speed story.

## Why it moved

- [inferred] Successful Search Rate did not move (+0.00%) while Latency p95 rose 6.00%. Slower results plausibly offset the ranker's gains.
- [inferred] Abandonment Rate rose 1.60%. That fits slower results, or worse results making users give up; the scorecard cannot separate them.
- [inferred] CTR is down 1.50%, which goes with the abandonment rise.

## Appendix

- Secondary metrics: 54 tested; after a false-discovery correction these moved: CTR (-1.50%). They are exploratory and don't change the call.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

---

# Ranker v7: triage prep

Ready for triage: Ready: every movement triage will ask about has a candidate explanation and none conflict; the explanations are inferred from co-movements, so the cuts below would confirm them.

Scripted call: No effect found. Successful Search Rate reads +0.00% (-0.30% to +0.30%), which rules out the 0.50% change the test was built to find.

## Before any single metric

- What did you change? ranker_model: lambdamart_v6 -> lambdamart_v7; nothing else differs between arms.
- Is the data trustworthy? Yes, as far as the checks reach; not checked: pre period.
- Is the effect real, or chance? Successful Search Rate +0.00% (-0.30% to +0.30%); its interval includes zero. Across the scorecard 4 of 57 metrics moved clearly; about 2.9 would by chance alone.
- Will it last? Probably: effect by days since exposure: first days -0.01%, last days +0.01% (trend +0.002% per day).
- Did the change do what it was built to do? Not shown. If the scorecard or a cut has a coverage metric (the share of queries whose top results changed), register it as feature_metrics.

Metric families used: abandonment = Abandonment Rate, ad_ctr = Ad Click Rate, autocomplete = Autocomplete Acceptance, clicks_per_user = Clicks per User, ctr = CTR, latency = Latency p95 (ms), long_click = Long Click Rate, pagination = Pagination Rate, queries_per_user = Queries per User, reformulation = Reformulation Rate, revenue = Revenue per User, sessions_per_user = Sessions per User, success = Successful Search Rate, time_to_click = Time to First Click (s), zero_result = Zero Result Rate. A wrong pairing here changes every explanation below; fix it in the overlay's metric_families.json.

## Questions triage will ask

1. Successful Search Rate was expected to rise but didn't move. Why? It didn't move clearly (+0.00% (-0.30% to +0.30%)). Status: untested.
   - Likely [inferred]: Slower results cost engagement. The treatment serves results more slowly, and slower pages lose clicks and raise abandonment, which can hide a relevance gain. Speed effects tend to grow over weeks rather than fade.
     Evidence: Latency p95 (ms) rose 6.00% (+5.20% to +6.80%); Abandonment Rate rose 1.60% (+1.20% to +2.00%); CTR fell 1.50% (-1.90% to -1.10%); Successful Search Rate didn't move clearly (+0.00% (-0.30% to +0.30%)).
     To check: cut 1, 3 below.
   - Likely [inferred]: Worse results make users give up. Users leave without clicking because results got worse, not because the answer was on the page.
     Evidence: Abandonment Rate rose 1.60% (+1.20% to +2.00%); Successful Search Rate didn't move clearly (+0.00% (-0.30% to +0.30%)); CTR fell 1.50% (-1.90% to -1.10%).
     To check: cut 2, 4 below.

2. Why did Latency p95 (ms) rise? It rose 6.00% (+5.20% to +6.80%). Status: untested.
   - Likely: Slower results cost engagement, as in question 1.

3. Why did Abandonment Rate rise? It rose 1.60% (+1.20% to +2.00%). Status: untested.
   - Likely: Slower results cost engagement, as in question 1.
   - Likely: Worse results make users give up, as in question 1.

4. Why did CTR fall? It fell 1.50% (-1.90% to -1.10%). Status: untested.
   - Likely: Slower results cost engagement, as in question 1.
   - Likely: Worse results make users give up, as in question 1.

## Ruled out

- Answers on the page reduce clicks: Latency p95 (ms) rose 6.00% (+5.20% to +6.80%).
- Some queries win, others lose: CTR fell 1.50% (-1.90% to -1.10%).

## Cuts to run before triage, in order

1. Abandonment and CTR by latency bucket, per arm (tests: Slower results cost engagement). Supports it: the loss sits in the slow buckets. Against it: the loss is flat across latency buckets. Scored by script once its result is in evidence.json.
2. Abandonment on queries with an answer or rich snippet vs without (tests: Worse results make users give up). Supports it: the rise sits on queries without an answer. Against it: the rise sits on answer-bearing queries. Scored by script once its result is in evidence.json.
3. Latency by page type and load type (cached reloads vs fresh loads), by arm (tests: Slower results cost engagement). Supports it: latency rises on the same page types. Against it: the page mix changed, so latency moved without pages getting slower. Record its outcome in evidence.json under cuts.
4. Config diff of presentation parameters (answers, rich snippets) (tests: Worse results make users give up). Supports it: only ranking differs. Against it: an answer or snippet parameter differs. Record its outcome in evidence.json under cuts.
5. Effect by device and network type (tests: Slower results cost engagement). Supports it: mobile or slow networks carry the loss. Against it: the loss is the same everywhere. Record its outcome in evidence.json under cuts.

Explanations become confirmed only when a cut's result is passed back to explain.py with --evidence; a cut that contradicts a candidate removes it.

## Sources

- Slower results cost engagement: Brutlag, Google, 2009 (400 ms delay: -0.44% searches in weeks 1-3, -0.76% in weeks 4-6, still -0.21% after removal); Dmitriev et al., A Dirty Dozen: Twelve Common Metric Interpretation Pitfalls, KDD 2017 (latency moved by page mix).
- Worse results make users give up: Li, Huffman, Tokuda, SIGIR 2009 (good vs bad abandonment); Song, Shi, Fu, WWW 2013.

---

doc_lint: 0 fail, 0 warn, 248 body words (readout)
cold-read: skim 2/2, full 2/3 - fail

The cold read failed on one takeaway. The reader had trouble reconciling "Could reverse it" with the "Ready" triage status.

Ready for triage: Ready, with open questions

My readiness differs from the script's "Ready". All four explanations are inferred from co-movements and none of the five cuts has been run. The pre-exposure check couldn't run. Whether the ranker changed the top results is also unshown. The engineer should run cuts 1 and 2 before the meeting, because the first question will be why latency, abandonment and CTR all got worse.