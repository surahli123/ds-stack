Decision: Don't ship

**Ranker v7 did not move Successful Search Rate, and the data rule out the +0.005 bar the pre-registration set for shipping.**

**Primary metric (Successful Search Rate)**
- Control was 0.4120 and test was 0.4122, a difference of +0.00016 (p = 0.79).
- The 95% CI is about [−0.0011, +0.0014]. Its upper end is well below the +0.005 bar, so we can't call this inconclusive.
- The pre-registration says to ship only if the point estimate reaches the bar. It doesn't, and the CI says the true lift is probably under a third of the bar.
- If the bar was meant as a relative lift (+0.5%, about +0.002 absolute), the upper CI limit of +0.0014 is still below it. The conclusion doesn't depend on that reading.

**Experiment validity**
- The test ran 14 days, from 2026-09-12 to about 09-25, as planned.
- Each arm had 1.0M users against 900k planned, so power is at least as good as planned.
- Exposures are balanced and that health check passed.
- The audit log is empty, so nothing changed mid-flight.
- The config shows a 50/50 split, and `ranker_model` is the only parameter that differs between arms, as intended. `snippet_length` is the same in both.
- Sequential testing and Bonferroni correction are both off, so the p-values are plain fixed-horizon values.

**Guardrails**
- Latency p95: +0.2% (CI ±0.5%), inside the 2% margin.
- Abandonment: +0.1% relative (CI ±0.6%), inside the 1% margin.
- Zero Result Rate: no change (CI ±1.4%), inside the 3% margin.
- Revenue per User: +3.1% (CI ±2.1%), which is not a regression.
- No guardrail is breached. That doesn't rescue the launch, because the primary goal wasn't met.

**Secondary results to treat with caution**
- Revenue per User is up (p = 0.004), but it is one of about 70 metrics and segment cuts, none of which were pre-registered as a win condition.
  - At that count we'd expect a few p-values below 0.05 by chance. It also wouldn't survive a Bonferroni correction (roughly 0.0007).
  - Nothing else supports it. Clicks, CTR and Ad Click Rate are flat, and Queries per User is slightly down (p = 0.10).
  - I'd treat it as a lead for a follow-up, not as a reason to ship.
- Desktop Time to First Click is worse (+0.28s, p = 0.004), and Clicks per User is higher for Mobile and Tail queries (p = 0.04 and 0.01). I read these as noise or exploratory only.
- Segment Successful Search Rate effects are all non-significant. Mobile is the largest at +0.3pp (p = 0.11), still under the bar.

**Recommendation**
- Don't ship v7 on the strength of this test.
- If the team believes in the ranker, any follow-up should be a new pre-registered test, for example one aimed at Revenue per User or at Mobile. It shouldn't reuse this result as evidence.