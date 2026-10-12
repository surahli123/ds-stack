Decision: Ship

**Ranker v7 (`lambdamart_v7` vs `lambdamart_v6`), Pulse ds 2026-09-25**

**Recommendation.** Ship. The pre-registered primary metric clears its bar at the point estimate. All four pre-registered guardrails stay inside their margins. The one open concern is a secondary metric, Reformulation Rate, which is worse. It wasn't pre-registered as a guardrail, so it doesn't change the decision.

**Design and validity**
- This is a clean A/B test on `userID`, a 50/50 split with 1.0M users per arm. That's above the 900k planned. The exposure-balance health check passed.
- It ran 14 days, 2026-09-12 to 2026-09-25, as planned. Sequential testing is off and there is one look, so the 95% CIs and p-values are valid as read.
- The audit log is empty, so there were no mid-flight config changes.
- Pulse was pulled with CUPED off, so these are the unadjusted numbers.

**Primary: Successful Search Rate (bar +0.5%)**

| | Control | Test | Change | 95% CI | p |
|---|---|---|---|---|---|
| Successful Search Rate | 0.4120 | 0.4153 | +0.334pp, **+0.81% relative** | +0.41% to +1.21% relative | 7e-5 |

- The point estimate of +0.81% clears the +0.5% bar, which is what the prereg requires (`point_at_bar`).
- The CI lower bound (+0.41%) is below the bar. So the data show a real lift but don't prove it is at least 0.5%.
- **Assumption on the bar.** I read the 0.005 bar as relative. The prereg's guardrail margins are only sensible as relative (a 0.02 margin on 412 ms latency, or 0.03 on a 3.1% rate). If the bar is meant as absolute (+0.5pp), the point estimate of +0.33pp would miss it. Please confirm this reading in the review.

**Guardrails (relative change, 95% CI upper or lower bound vs margin)**

| Guardrail | Change | Worst CI bound | Margin | Result |
|---|---|---|---|---|
| Latency p95 | +0.2% | +0.7% | 2% | Pass |
| Abandonment Rate | +0.1% | +0.7% | 1% | Pass |
| Zero Result Rate | 0.0% | +1.4% | 3% | Pass |
| Revenue per User | −0.1% | −0.8% | −1% | Pass |

Revenue has the least room: its lower bound of −0.8% is close to the −1% margin.

**Secondary metrics worth knowing about**
- **Reformulation Rate** (lower is better) rose +0.96% relative, p=0.018. It is concentrated in Informational queries (+1.7%, p=0.04).
- **Long Click Rate** fell −0.55%, p=0.07, not significant. CTR was flat (−0.09%, p=0.72).
- These sit slightly oddly next to a higher success rate. They may mean some of the lift comes from shallower successes, and I can't tell from this data.
- **Multiplicity.** The readout has about 60 unadjusted metrics and segments, so one or two p<0.05 results are expected by chance. I'd treat Reformulation as a watch item, not a blocker. It is the one I'd follow up on.
- **Segments.** Mobile, Desktop and the query-type segments show no significant heterogeneity. Head queries are nominally down (−0.26pp, p=0.16), which is within noise.
- Sessions per User is up +0.5% (p=0.058), consistent with the primary.

**Caveats and follow-ups**
- 14 days is short for novelty effects. I'd keep a holdout or monitor Successful Search Rate and Reformulation Rate after launch.
- Confirm the relative reading of the bar (see above).
- Check Reformulation on Informational queries on the post-launch dashboard.