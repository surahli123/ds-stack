Decision: Ship

This is the scripted call, and I disagree with it. My call would be Escalate.

**Ask:** Approve the launch to all traffic, but only after the review has weighed the dissent below.

**Why the script says Ship:** Queries per User (the pre-registered primary) rose +2.40% (+1.50% to +3.30%). That clears the 1.00% bar. The one registered guardrail, Latency p95 (ms), held at +0.20% (-0.30% to +0.70%), inside its 2.00% margin.

**Status:** Day 14 of 14, with 1,000,000 users per arm against 900,000 planned. The sample split, config and mid-flight-edit checks passed. The pre-period and novelty checks could not run.

| Metric | Role | Change (95% interval) | Bar | Verdict |
|---|---|---|---|---|
| Queries per User | primary | +2.40% (+1.50% to +3.30%) | at least 1.00% | better |
| Latency p95 (ms) | guardrail | +0.20% (-0.30% to +0.70%) | within 2.00% | within margin |

## Analyst's view: Escalate
The primary rose with reformulations, which is a plausible bad reason. Successful Search Rate, the metric in the experiment's own hypothesis, did not improve. The gain may be a worse experience.

## Why it moved
- [inferred] Reformulation Rate rose +5.10% (+4.30% to +5.90%) alongside Queries per User, so users may be re-searching because first results miss.
- [measured] Successful Search Rate moved -0.35% (-0.75% to +0.05%). Time to First Click rose +1.28%.
- [guess] Ad Click Rate fell -1.98% (-3.18% to -0.78%). The cause is unknown.

## What would change the call
- A pre-registered primary of Successful Search Rate, with an interval that rules out a loss.
- Reformulation Rate staying flat in a rerun, or a split showing the extra queries are new searches rather than retries. Either would support Ship.
- The owner confirming Queries per User as the primary. The pre-registration file has no owner sign-off, and the experiment config names Successful Search Rate as primary.

## Appendix
- Of 55 secondary metrics, two moved after a false-discovery correction: Reformulation Rate (+5.10%) and Ad Click Rate (-1.98%). They are exploratory and don't change the call.
- Settings: 95% intervals, variance reduction off, no multiple-comparison correction. The scorecard doesn't record whether sequential testing was used.
- The full metric table is in `all_metrics.md`.

Lint: 0 fail, 0 warn, 248 body words (readout)

Cold read: skim 2/2, full 2/3 - fail. The reader missed the pre-period caveat and found the Ship headline and the Escalate analyst view in conflict.

I replaced the rendered title line with the required `Decision:` first line. I also wrote the guardrail row out in full, because the render left its "Bar" cell blank. The lint and cold-read results above are for the rendered file, not this edited text.