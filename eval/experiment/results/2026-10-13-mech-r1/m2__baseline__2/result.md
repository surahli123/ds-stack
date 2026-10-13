**Ranker v7 does not win. Successful Search Rate (SSR) went down, not up, so the recommendation is don't ship. The "why" is partly a hypothesis that the deep-dive cuts below need to confirm.**

## Scorecard

Pre-registration had one primary metric, SSR, which had to rise by at least 0.5pp at the point estimate.

| Metric | Result | Read |
|---|---|---|
| **SSR (primary)** | 41.20% → 40.90%, **−0.30pp** (95% CI ±0.16pp), −0.72% relative, p=0.0004 | Fails. The whole interval is below zero and about 0.8pp short of the bar. |
| Reformulation Rate | +0.69pp (+4.8%), p<0.0001 | Clear regression. |
| Queries per User | +2.3%, p≈1e-6 | More queries per user, not more engagement. |
| Sessions, Clicks, CTR, Long Click, Time to First Click | All flat (p 0.25–0.82) | Users aren't clicking more. |
| Ad Click Rate | +1.4% relative, p=0.02 | Likely noise (see below). |
| Guardrails | All inside their margins | See below. |

**Guardrails:**
- **Latency p95:** +0.2%, margin 2%.
- **Abandonment:** +0.1% ±0.6%, margin 1%.
- **Zero Result Rate:** unchanged, margin 3%.
- **Revenue per User:** −0.1% ±0.7%, lower bound −0.8%, margin −1%.

## Why the metrics moved

The simplest story is that v7 makes users re-query more, and that story explains most of the movement:
- Reformulations and queries per user rise, while sessions and clicks stay flat. The extra queries are retries inside the same sessions.
- Each retry adds a search that ends without a successful click. That pulls SSR down even though total clicks haven't dropped.
- This is a hypothesis. The data is consistent with it but doesn't prove it.

Neutral movers:
- Latency, zero-result rate, abandonment, and revenue are all flat, so this isn't a performance or retrieval-coverage problem.
- Ad Click Rate is one nominal hit among about 60 unadjusted metrics and slices (no multiple-comparison correction is configured). Don't present it as a revenue upside.

The effect looks stable rather than transient. In the daily view the relative delta sits at about −0.7% on every day for 12 days, with no novelty effect and no trend. That view is by days since exposure, not calendar day, so day-of-week effects can't be checked from it.

## Deep-dive cuts, in order

1. **Reformulation by query type.** Tail queries show reformulation +2.1% (p=0.012) while head queries are flat. I expect the regression to concentrate in tail queries. Follow-up cuts:
   - Reformulation type: spelling vs. refinement vs. new intent.
   - Query-level pairs: first query → reformulated query.
   - Position of the first click.
2. **SSR with a per-query or per-session denominator.** The Statsig ratio is pooled. Computing it per session shows whether the drop is just a bigger denominator from extra queries. If per-session success is flat, v7 hasn't made search worse. It has made users retry more.
3. **Informational vs. navigational.** Informational shows SSR −0.20pp and Long Click Rate −1.3% (p=0.04). Navigational is +0.28pp, not significant. I'd expect v7 to help lookup-style queries and hurt exploratory ones.
4. **Desktop vs. mobile.** Desktop Abandonment fell 1.8% (p=0.014) while mobile didn't move. I expect this to be noise, but it needs a look before anyone tells a "desktop got better" story.
5. **Calendar-day view.** This checks ramp-up and day-of-week effects, which the days-since-exposure file can't show.

Segment p-values are unadjusted. About 50 slices were tested and four came in under 0.05 (Desktop Abandonment, Tail Reformulation, Informational Long Click, Tail Clicks). That is roughly what chance alone would give. Present these as hypotheses only. The overall reformulation and queries-per-user results are the solid findings.

## Issues to resolve before presenting

- **The segment SSR numbers don't add up.**
  - Overall SSR is −0.30pp, but Mobile (+0.17), Desktop (+0.18), Head (−0.01), Tail (−0.08), Navigational (+0.28) and Informational (−0.20) are all above that.
  - A pooled effect can't fall outside the range of a complete partition. That points to segment metrics defined on a different denominator or population, or a mix shift driven by the extra queries.
  - The engineer shouldn't use the segment table to explain the overall drop until this is reconciled.
- **The data may be stale.**
  - The Pulse snapshot is dated 2026-09-25 and the daily file covers 12 days.
  - The experiment started 2026-09-12 for 14 days, so it should have ended around 09-26. The config still shows `active` on 2026-10-13.
  - Refresh Pulse, or confirm the final results are the 09-25 numbers.
- **Enrollment is above plan.** There are 1.0M units per arm against 900k planned. The split is exactly 50/50 and the balance health check passed, so this is minor. Confirm why it's higher.
- **The audit log is empty.** There are no mid-flight config changes on record, which is good. `snippet_length` is identical in both arms, so only `ranker_model` differs, as intended.

## Readiness

The headline is solid enough to present: the primary failed, with a clear reformulation signal behind it. What isn't settled is the mechanism, the segment inconsistency, and snapshot freshness.

Ready for triage: Ready, with open questions