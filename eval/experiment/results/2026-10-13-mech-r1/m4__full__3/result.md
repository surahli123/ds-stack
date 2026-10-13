# Ranker v7: No effect found

Decision: No effect found. Successful Search Rate reads -0.10% (-0.40% to +0.20%), which rules out the 0.50% change the test was built to find.

Ask: Agree to stop the test without launching.

Status: day 14 of 14, 1,000,000 users per arm, above the planned 900,000, whole weeks.

Could reverse it: secondary metric CTR got worse after correction.

Triage: Ready: every movement triage will ask about has a candidate explanation and none conflict; the explanations are inferred from co-movements, so the cuts below would confirm them.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Successful Search Rate | primary | -0.10% (-0.40% to +0.20%) | estimate at least 0.50% higher | unclear |
| 2 other guardrails | guardrail | | | all within margin |

Checks: passed: scorecard, sample split, config params, config edits, novelty; not run: pre period.

## What would change the call

- A cut showing the CTR drop is concentrated in queries that had zero results in control would explain the CTR fall, though not reverse the call.
- A pre-period comparison of Successful Search Rate would let the one check that could not run be completed.
- A longer run would only matter if the owner re-registers a smaller bar than 0.50%.

## Why it moved

- [measured] Successful Search Rate read -0.10% against a 0.50% bar, so the new ranker did not raise the share of searches that end in a successful click.
- [inferred] Zero Result Rate fell 12.00% while CTR fell 1.80%, which fits queries that used to return nothing now returning weak results.
- [guess] If CTR already counted zero-result queries in its denominator, that mechanism cannot lower CTR, so the CTR drop may have another cause. No cut has been run on either.

## Appendix

- Secondary metrics: 54 tested; after a false-discovery correction these moved: CTR (-1.80%), Zero Result Rate (-12.00%). They are exploratory and don't change the call.
- Settings: 95% intervals; variance reduction off; harm inside a margin goes to escalate.
- Guardrails within margin: Latency p95 (ms), Revenue per User.
- Every metric, with means and p-values: all_metrics.md.
- Calls: Can't tell means the test is broken. Keep running means not enough data yet. No effect found means enough data and nothing as big as the bar. Escalate means a trade-off for triage.

# Ranker v7: triage prep

Scripted call: No effect found. Successful Search Rate reads -0.10% (-0.40% to +0.20%), which rules out the 0.50% change the test was built to find.

## Before any single metric

- What did you change? ranker_model: lambdamart_v6 -> lambdamart_v7; nothing else differs between arms.
- Is the data trustworthy? Yes, as far as the checks reach; not checked: pre period.
- Is the effect real, or chance? Successful Search Rate -0.10% (-0.40% to +0.20%); its interval includes zero. Across the scorecard 5 of 57 metrics moved clearly; about 2.9 would by chance alone.
- Will it last? Probably: effect by days since exposure: first days -0.11%, last days -0.09% (trend +0.002% per day).
- Did the change do what it was built to do? Not shown. If the scorecard or a cut has a coverage metric (the share of queries whose top results changed), register it as feature_metrics.

## Questions triage will ask

1. Successful Search Rate was expected to rise but didn't move. Why? It didn't move clearly (-0.10% (-0.40% to +0.20%)). Status: answered by the call: the interval rules out the bar.

2. Why did CTR fall? It fell 1.80% (-2.30% to -1.30%). Status: untested.
   - Likely [inferred]: More results for hard queries, lower precision. The change returns results for queries that used to get none, but those results are weak, so averages over all queries fall.
     Evidence: Zero Result Rate fell 12.00% (-14.00% to -10.00%); CTR fell 1.80% (-2.30% to -1.30%).
     To check: cut 1, 2 below.

3. Why did Zero Result Rate fall? It fell 12.00% (-14.00% to -10.00%). Status: untested.
   - Likely: More results for hard queries, lower precision, as in question 2.

## Cuts to run before triage, in order

1. Success and CTR on queries that had zero results in control (tests: More results for hard queries, lower precision). Supports it: these queries now get results but low success. Against it: they succeed at the normal rate. Record its outcome in evidence.json under cuts.
2. The same metrics excluding those queries (tests: More results for hard queries, lower precision). Supports it: the rest of the traffic is flat. Against it: the drop is broad. Record its outcome in evidence.json under cuts.

Explanations become confirmed only when a cut's result is passed back to explain.py with --evidence; a cut that contradicts a candidate removes it.

## Sources

- More results for hard queries, lower precision: Dmitriev et al., A Dirty Dozen: Twelve Common Metric Interpretation Pitfalls, KDD 2017 (ratio metrics move with their denominator); reasoned, no published case of this exact signature.

0 fail, 0 warn, 268 body words (readout)
cold-read: skim 2/2, full 3/3 - pass

The cold reader flagged some confusion. The "Could reverse it" line sits oddly beside the note that a CTR cut would not reverse the call. The "Ready" triage label also sits oddly beside unconfirmed explanations.

**Where I differ from the tool's triage label.** The tool printed "Ready". I removed its `Ready for triage:` line from the prep sheet so there is only one such line. Here is my own:

Ready for triage: Ready, with open questions

Reasons:
- **The two moved metrics are untested.** Only CTR (-1.80%) and Zero Result Rate (-12.00%) moved after correction. The "queries that used to return nothing now return weak results" story is inferred from those two numbers. No cut has been run on it.
- **The story may not fit CTR.** If CTR's denominator already counted zero-result queries, they had zero clicks before, so giving them results can't lower CTR. Zero-result queries are also only about 3.1% of traffic. By my rough arithmetic, a 12% drop in that share could explain well under half of a 1.8% CTR fall. Ask how CTR is defined before triage.
- **One check couldn't run.** There is no pre-period comparison. The checks that did run all passed: sample split, config and novelty.

**Things triage may bring up:**
- **The primary is flat, not negative.** The call is "No effect found" because the interval rules out the 0.5% bar. Don't present -0.10% as harm. Both guardrails are within margin.
- **The other 3 flagged cells are noise.** About 2.9 of 57 metrics would move by chance. The other three are a segment cell for CTR (Navigational), one for Abandonment Rate (Head Queries) and one for Clicks per User (Informational). None survives correction, so don't explain them.
- **The Long Click Rate pointer is stale.** An earlier run's files were left in `/tmp/out`. They show a +0.81% primary lift and a Long Click Rate primary, and none of that is in this scorecard or your pre-registration. I did not use them, and the outputs above are in a clean directory, `out_ranker_v7`. Don't quote that +0.81%.
- **Your pre-registration differs from the team defaults.** Its guardrail is Revenue per User where the defaults use Abandonment Rate, and I used yours as written.

**Next steps:** run the two cuts in order, then bring the results back to `explain.py --evidence`. The first is success and CTR on queries that had zero results in control. The second is the same metrics excluding those queries.