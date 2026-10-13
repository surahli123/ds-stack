# Ranker v7: Escalate

Decision: Escalate. Successful Search Rate rose 0.68% (+0.28% to +1.08%), but Abandonment Rate rose 2.10% (+1.50% to +2.70%), the wrong way, though inside its 4.00% margin.

Ask: Decide the trade-off at triage.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: secondary metric CTR got worse after correction.

Triage: Ready: every movement triage will ask about has a candidate explanation and none conflict; the explanations are inferred from co-movements, so the cuts below would confirm them.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Abandonment Rate | guardrail | +2.10% (+1.50% to +2.70%) | at most 4.00% higher | worse, within margin |
| Successful Search Rate | primary | +0.68% (+0.28% to +1.08%) | estimate at least 0.50% higher | better |
| 1 other guardrail | guardrail | | | within margin |

Checks: passed: scorecard, sample split, config params, config edits, novelty; not run: pre period.

## What would change the call

- If abandonment sits on queries with no answer or rich snippet, or users re-search soon after leaving, the rise is harm and the abandonment trade-off tips against the change.
- If success rises only on queries where the ranking changed, the win is real and larger there; if it is flat there, the overall rise is not from ranking.
- A pre-exposure comparison that shows the arms already differed would make the test unreliable.

## Why it moved

- [inferred] Successful Search Rate rose 0.68% while abandonment went up and CTR fell 1.10%: this fits users getting answers on the page and leaving without a click. No cut has tested it.
- [inferred] Clicks per User fell 1.20% while Queries per User didn't move clearly, which fits fewer clicks per search and no extra searching. It does not show whether those searches were satisfied.
- [guess] The mobile and desktop success rates are both slightly down though overall success is up, so the overall rise is not yet traced to any slice.

## Appendix

- Secondary metrics: 54 tested; after a false-discovery correction these moved: CTR (-1.10%), Clicks per User (-1.20%). They are exploratory and don't change the call.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms).
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

---

# Ranker v7: triage prep

Ready for triage: Ready: every movement triage will ask about has a candidate explanation and none conflict; the explanations are inferred from co-movements, so the cuts below would confirm them.

Scripted call: Escalate. Successful Search Rate rose 0.68% (+0.28% to +1.08%), but Abandonment Rate rose 2.10% (+1.50% to +2.70%), the wrong way, though inside its 4.00% margin.

## Before any single metric

- What did you change? ranker_model: lambdamart_v6 -> lambdamart_v7; nothing else differs between arms.
- Is the data trustworthy? Yes, as far as the checks reach; not checked: pre period.
- Is the effect real, or chance? Abandonment Rate +2.10% (+1.50% to +2.70%); its interval excludes zero. Across the scorecard 7 of 57 metrics moved clearly; about 2.9 would by chance alone.
- Will it last? Probably: effect by days since exposure: first days +0.67%, last days +0.69% (trend +0.002% per day).
- Did the change do what it was built to do? Not shown. If the scorecard or a cut has a coverage metric (the share of queries whose top results changed), register it as feature_metrics.

Metric families used: abandonment = Abandonment Rate, ad_ctr = Ad Click Rate, autocomplete = Autocomplete Acceptance, clicks_per_user = Clicks per User, ctr = CTR, latency = Latency p95 (ms), long_click = Long Click Rate, pagination = Pagination Rate, queries_per_user = Queries per User, reformulation = Reformulation Rate, revenue = Revenue per User, sessions_per_user = Sessions per User, success = Successful Search Rate, time_to_click = Time to First Click (s), zero_result = Zero Result Rate. A wrong pairing here changes every explanation below; fix it in the overlay's metric_families.json.

## Questions triage will ask

1. Why did Abandonment Rate rise? It rose 2.10% (+1.50% to +2.70%). Status: untested.
   - Likely [inferred]: Answers on the page reduce clicks. More users get their answer from the results page itself (answers, richer snippets), so they leave without clicking and don't retry.
     Evidence: Abandonment Rate rose 2.10% (+1.50% to +2.70%); Successful Search Rate rose 0.68% (+0.28% to +1.08%); CTR fell 1.10% (-1.50% to -0.70%); Queries per User didn't move clearly (-0.07% (-0.97% to +0.83%)).
     To check: cut 1, 4 below.

2. Why did Successful Search Rate rise? It rose 0.68% (+0.28% to +1.08%). Status: untested.
   - Likely: Answers on the page reduce clicks, as in question 1.
   - Likely [inferred]: Better results, more satisfied clicks. The ranking puts better results where users look, so more searches end in a satisfying click.
     Evidence: Successful Search Rate rose 0.68% (+0.28% to +1.08%); Reformulation Rate didn't move clearly (-0.10% (-0.90% to +0.70%)); Time to First Click (s) didn't move clearly (-0.63% (-1.63% to +0.37%)).
     To check: cut 2, 5 below.

3. Why did CTR fall? It fell 1.10% (-1.50% to -0.70%). Status: untested.
   - Likely: Answers on the page reduce clicks, as in question 1.

4. Why did Clicks per User fall? It fell 1.20% (-1.90% to -0.50%). Status: untested.
   - Likely: Answers on the page reduce clicks, as in question 1.

## Cuts already run

- Config diff of presentation parameters (answers, rich snippets): inconclusive 'Answers on the page reduce clicks'. config differs in ranker_model (lambdamart_v6 -> lambdamart_v7).
- Abandonment by device: inconclusive 'Answers on the page reduce clicks'. Abandonment Rate by device: Mobile +0.21%; Desktop +0.60%.

## Ruled out

- Some queries win, others lose: CTR fell 1.10% (-1.50% to -0.70%).

## Cuts to run before triage, in order

1. Abandonment on queries with an answer or rich snippet vs without (tests: Answers on the page reduce clicks). Supports it: the rise sits on answer-bearing queries. Against it: the rise sits on queries without an answer. Scored by script once its result is in evidence.json.
2. Success on triggered queries only (where the ranking actually changed) vs untriggered (tests: Better results, more satisfied clicks). Supports it: a larger effect on triggered queries, diluted overall. Against it: the same effect on untouched queries, pointing to something other than ranking. Scored by script once its result is in evidence.json.
3. Successful Search Rate on triggered queries (where the ranking changed) vs untriggered (tests: The registered hypothesis). Supports it: a larger effect where the ranking changed. Against it: the same effect on untouched queries. Record its outcome in evidence.json under cuts.
4. A similar query issued again within 5 minutes after an abandoned query (tests: Answers on the page reduce clicks). Supports it: abandoned users don't come back to retry. Against it: abandoned users retry. Scored by script once its result is in evidence.json.
5. Success by query class and device (tests: Better results, more satisfied clicks). Supports it: the gain is largest where the change acts (for example tail queries for a recall change). Against it: the gain is uniform, which a ranking change rarely produces. Record its outcome in evidence.json under cuts.

Explanations become confirmed only when a cut's result is passed back to explain.py with --evidence; a cut that contradicts a candidate removes it.

## Sources

- Answers on the page reduce clicks: Li, Huffman, Tokuda, SIGIR 2009 (good abandonment, higher on mobile); Pew Research 2025 (clicks 8% vs 15% with AI summaries).
- Better results, more satisfied clicks: Kohavi, Tang, Xu 2020, ch. 20 (triggered analysis needs counterfactual logging, and the untriggered complement must look like an A/A).

---

0 fail, 0 warn, 306 body words (readout)
cold-read: skim 2/2, full 3/3 - pass

My view differs from the script's "Ready" verdict, as a separate line:
- Every explanation is still untested, and none of the five cuts has been run.
- The registered abandonment margin is 4.00%, four times the team standard of 1.00%. At 1.00%, a 2.10% rise would be past the margin. The engineer should expect that question.
- Overall success is up, but the mobile (-0.26%) and desktop (-0.25%) rates are both slightly down. The cold read flagged this too, and it needs an answer.
- The pre-period check did not run.

Ready for triage: Ready, with open questions