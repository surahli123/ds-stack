**Bottom line:** Ranker v7 did not move the primary metric, and the CI rules out the pre-registered bar. The one eye-catching result, CTR and clicks up about 2%, doesn't reconcile with any of the slices. The engineer should be able to explain that before triage.

## Scorecard

| Metric | Result | What to say |
|---|---|---|
| **Successful Search Rate (primary)** | 0.412 vs 0.412, Δ = 0.0000, 95% CI ±0.0012, p = 1.0 | A clean null. The upper bound (+0.0012) is below the 0.005 bar. Even if the bar means relative (about 0.002 absolute), it is still ruled out. The test had enough data to say the effect is not at the bar. |
| Guardrails | Latency +0.2% (±0.5%), Abandonment +0.1% (±0.6%), Zero Result 0.0% (±1.4%), Revenue/User −0.1% (±0.7%) | All CIs sit inside their pre-registered margins (2%, 1%, 3%, 1%). Revenue is the closest: its lower bound is about −0.8% against a −1% margin. |
| CTR | +0.0073 (+2.4%), p ≈ 0 | The only large movement. |
| Clicks per User | +0.079 (+2.2%), p ≈ 0 | Matches CTR, since Queries per User is flat (−0.1%). |
| Long Click Rate | −0.1%, p = 0.70 | Flat, so the extra clicks are not long clicks. |
| Abandonment, Reformulation, Time to First Click | Flat, except Reformulation −0.9% (p = 0.027) | Reformulation is one unadjusted p-value among about 70 metrics. Don't build a story on it. |

## Why the metrics moved

- **Primary flat.** The new ranker changes which results get clicked, but not whether the search succeeds.
- **CTR and clicks up.** The extra clicks are short ones. The CTR gain is +0.0073 while Long Click Rate is flat at −0.0002, and Successful Search Rate, Abandonment and Reformulation are also flat. The likely mechanism is that v7 makes results look more clickable without making them more useful. That is a hypothesis the cuts below can test. The data doesn't establish it yet.
- **Scattered p < 0.05 results.** About 70 metrics and slices were reported with no multiplicity correction, so roughly 3–4 false positives are expected. Four showed up:
  - Reformulation, overall: −0.9%, p = 0.027, which is the favourable direction.
  - CTR on Desktop: p = 0.018.
  - Reformulation on Navigational: p = 0.043, which is the unfavourable direction.
  - Time to First Click on Navigational: p = 0.015, which is the unfavourable direction.

  They point both ways, so treat them as noise.
- **No novelty effect.** The daily relative delta by days since exposure stays between −0.04% and +0.04% across all 12 days, with CIs of about ±0.6%.

## The problem to fix before triage

The overall CTR and clicks lift is not reproduced in any slice:

- **CTR.** Every slice is negative:
  - Mobile −0.0016
  - Desktop −0.0050
  - Head −0.0012
  - Tail −0.0009
  - Navigational −0.0015
  - Informational −0.0009

  The overall figure is +0.0073.
- **Clicks per User.** The overall lift is +0.079. Mobile and Desktop are about +0.04 each. Head is −0.05 and Tail is 0.
- **Baselines don't add up.** Control CTR is 0.305 overall but 0.320 on Mobile and 0.334 on Desktop. Control Successful Search Rate is 0.412 overall but 0.346 on Mobile and 0.401 on Desktop. A pooled average can't sit outside its components.

Possible causes are a third device bucket, slice metrics with different denominators or filters, or an issue in the overall CTR and Clicks per User computation. Until this is resolved, the engineer can't say where the click lift comes from, and the CTR number may not be trustworthy.

## Deep-dive cuts to run next

1. **Reconcile slices with the overall metric.** Check metric definitions, denominators, and the share of units per slice, including any untagged bucket. Expected result: the +2.4% either disappears or is explained by a definition or mix issue.
2. **Click dwell-time buckets** (short, medium, long). If the hypothesis is right, the extra clicks concentrate in sub-10-second dwells, and pogo-stick (return-to-SERP) rate rises.
3. **Click position and clicks per query.** Expect more clicks at ranks 2–5, or multiple clicks per query, with no change in rank-1 success.
4. **Head vs tail, with a power check.** Head has the largest Successful Search Rate point estimate (+0.0026), with CI ±0.0044. Tail is −0.0007. Neither is distinguishable from zero, so don't present a segment win.
5. **New vs returning users.** This checks whether a learning or novelty effect is hidden in the pooled flat result. The days-since-exposure series is already flat, so expect no difference.

## Open data-quality items

- **Stale pull.** Pulse is dated 2026-09-25. The experiment started 2026-09-12 with a 14-day plan, and the daily series has only 12 days. It's now Oct 13 and the status is still "active". Re-pull the final 14-day data and confirm the result holds.
- **Audit log is empty.** Nothing changed mid-flight, which is good.
- **Health checks.** The only check is exposure balance, and it passed. 1,000,000 units per arm, against 900,000 planned, is fine.
- **Settings.** Sequential testing and Bonferroni correction are off, which matches a fixed-horizon design. The CUPED-off request matches the config.

## Verdict

The headline is solid: no lift on the primary, guardrails intact, and not shippable on this evidence. The open items are the unreconciled CTR and clicks lift and the stale data pull.

Ready for triage: Ready, with open questions