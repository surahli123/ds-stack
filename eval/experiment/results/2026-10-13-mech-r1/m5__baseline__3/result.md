**Ready for triage: Not ready**

I read the files directly and recomputed a few p-values and CIs from the Pulse numbers. They are internally consistent. The problems are in what the numbers say together.

## What the scorecard shows

| Metric | Result (95% CI) | Reading |
|---|---|---|
| Successful Search Rate (primary) | 41.20% → 41.48%, +0.28pp, +0.68% relative [+0.28%, +1.08%], p=0.0009 | Real lift, but see the bar problem below |
| Abandonment Rate (guardrail) | +2.1% relative [1.5%, 2.7%], p<0.001 | Significantly worse. Still inside the 4% margin, so the guardrail technically passes |
| Latency p95 (guardrail) | +0.2% [−0.3%, +0.7%] | Fine, well inside the 2% margin |
| CTR | −1.1% [−1.5%, −0.7%], p<0.001 | Down |
| Clicks per User | −1.2% [−1.9%, −0.5%], p=0.0008 | Down |
| Autocomplete Acceptance | −0.69% relative, p=0.025 | Probably noise (see below) |
| Long Click, Reformulation, Queries/Sessions per User, Time to First Click, Revenue, Ads, Zero Result, Pagination | All flat | Nothing to explain |

## Why I can't explain the movement

1. **The lift doesn't show up in any segment.** Successful Search Rate deltas by segment are:
   - Mobile −0.10pp
   - Desktop −0.11pp
   - Head queries +0.02pp
   - Tail queries −0.18pp
   - Navigational −0.11pp
   - Informational +0.01pp

   Mobile and desktop are both negative, so a blend of the two cannot be +0.28pp. A pooled gain that no segment shows is the signature of a mix shift between arms, or of a different metric definition in the segment cuts. CTR has the same problem: overall −0.34pp, but mobile is +0.07pp and desktop is −0.41pp, which doesn't average to −0.34pp. Both mismatches need an explanation before anyone claims the ranker caused the lift.

2. **The story doesn't hang together.** Success is up while CTR, clicks per user and Long Click Rate are flat or down, and abandonment is up. A better ranker would normally raise long clicks. My hypotheses (not established):
   - The success definition counts something other than long clicks, such as answer-style snippets or a changed click-attribution rule.
   - A mix shift, as in point 1.
   - Fewer but better clicks, which would mean abandonment shouldn't rise.

   The engineer should not present any of these as the cause.

3. **The success bar is ambiguous.** The prereg says `bar: 0.005` with no unit.
   - Read as absolute (+0.5pp), the point estimate of +0.28pp misses it.
   - Read as relative (+0.5%), the point estimate of +0.68% clears it, but the CI lower bound of +0.28% does not.

   The guardrail margins (0.02 for latency, 0.04 for abandonment) only make sense as relative, so relative is more likely. The engineer should confirm this with whoever wrote the prereg.

## Deep-dive cuts to run, in this order

1. **Arm composition by platform and query type.**
   - Test vs. control share of mobile/desktop and head/tail users.
   - Confirm the segments partition the population. Head and tail baselines (35% and 30%) both sit below the overall 41%, so there is likely an unreported torso segment.
   - Expect a skew that explains the pooled-versus-segment gap. If the arms are balanced, the metric or segment definitions differ, and that needs fixing.
2. **Success-rate decomposition.**
   - Split success into long clicks, short clicks and other signals.
   - Split abandonment by whether the query had a click.
   - Expect the lift to come from a non-click or short-click path, matching the flat Long Click Rate and the higher abandonment.
3. **Per-query-type CTR and abandonment.** Tail queries are the most likely home of the abandonment increase (+1.07% relative there, though not individually significant).
4. **Time trend.** The daily series is flat at about +0.64–0.72% across 12 of 14 days, so there is no novelty decay. It is also suspiciously regular (a repeating 0.64/0.68/0.72 pattern), so I'd check how it was built before showing it. If real, it supports durability.

## Other points

- **No multiple-comparison control.** The config has `bonferroniCorrection: false`, and there are 56 secondary metrics (about 40 of them segment cuts). Expect a few p<0.05 hits by chance. The desktop CTR, mobile Reformulation and Autocomplete Acceptance results are likely noise. Don't let the engineer explain them as real effects.
- **Sample size.** Each arm has 1.0M units against a planned 900k, which only adds power. Exposures are balanced and the health check passed.
- **Audit log.** It's empty, so there were no mid-test changes. Layer allocation is 20%, split 50/50.
- **Prereg compliance.** Only `ranker_model` was intended to differ between arms, and `snippet_length` is 160 in both. Compliant.

## Before the meeting

Items 1 and 2 above and the bar-unit question can be resolved quickly. If composition is balanced, the segment mismatch is explained, and the bar is relative, I'd upgrade this to "Ready, with open questions". The open question would be the +2.1% abandonment increase, which passes its guardrail but is a clear cost.