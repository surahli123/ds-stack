Decision: Escalate

# Ranker v7 – launch readout

**Bottom line.** The pre-registered ship rule is met, but the win looks like a symptom of worse results, not better ones. The primary rose while reformulations and ad clicks got worse, and the experiment's own hypothesis metric did not improve. I'd rather the review make this call than have a mechanical "Ship" go out.

## Pre-registered test (14 days, 1.0M users/arm vs 900k planned, 95% CI, no CUPED, no sequential/Bonferroni)
| | Result | Bar / margin | Verdict |
|---|---|---|---|
| Primary: Queries per User (increase) | 11.80 → 12.08, **+2.4% (95% CI +1.5% to +3.3%)**, p<0.001 | point ≥ +1% | Met (CI lower bound also above 1%) |
| Guardrail: Latency p95 | 412.0 → 412.8 ms, +0.2% (CI −0.3% to +0.7%) | ≤ +2% | Passed |

Validity: exposures balanced (health check PASSED), 50/50 split, only `ranker_model` differs between arms (snippet_length is the same), audit log is empty (no mid-test changes), the window ran as planned (ds 2026-09-25 is day 14).

## Why I'm not recommending Ship
1. **More queries is not clearly better here.** For search, more queries per user can mean people aren't finding what they need.
   - Reformulation Rate is **up 5.1%** (14.3% → 15.0%, p<0.001), the wrong direction. This is the strongest secondary signal.
   - Successful Search Rate is **−0.35% (CI −0.75% to +0.05%, p=0.086)**. It is not significant, but it is not the lift the hypothesis predicted either.
   - Clicks per User is flat (−0.15%, p=0.71) and Sessions per User is −0.5% (p=0.054). So the extra queries come with no extra clicks.
2. **Ad Click Rate is down 2.0%** (p=0.001). Revenue per User is flat (−0.1%, CI ±0.7%), so there's no revenue evidence either way yet.
3. **Time to First Click is slower** by 1.3% (+0.08s, p=0.012).
4. **The config and the pre-reg disagree on the primary.** The Statsig config and its hypothesis name Successful Search Rate as primary. The pre-reg names Queries per User. The pre-reg predates launch and governs, but the mismatch should be settled by the review. Under the config's own primary, the result is "no improvement".

Caveat: Pulse reports about 60 metrics with no multiplicity correction. Time to First Click and Clicks per User (head queries) at p≈0.012 could be chance. Reformulation Rate and Ad Click Rate are far enough from chance that I treat them as real. Segment cuts (mobile/desktop, head/tail, nav/info) show nothing consistent beyond that. Reformulations dropped in mobile and head segments, which conflicts with the overall increase; this is odd and unexplained, so don't over-read segments.

## Ask of the review
- Decide whether Queries per User is a valid success metric for this change, given the reformulation and ad-click movement. The pre-reg guardrails did not cover reformulation, so the rule can't catch this.
- If it is not, this is a Don't ship / redesign. If the team accepts it, the pre-reg supports Ship.
- Cheap next step either way: check whether the extra queries are reformulation chains (query-level logs), and look at ad revenue with a longer window.

Not done: no CUPED run (requested without it), and no query-level breakdown was available.
