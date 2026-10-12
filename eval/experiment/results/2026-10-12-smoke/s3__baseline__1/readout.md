Decision: Ship

# Ranker v7 readout

**Result.** Successful Search Rate (the single pre-registered primary) rose from 41.20% to 41.53%: +0.33pp absolute, **+0.81% relative**, 95% CI +0.41% ± 0.40 → roughly **+0.41% to +1.21% relative** (abs +0.17pp to +0.50pp), p = 7e-5. The pre-registered rule is "ship requires point estimate at the bar" (bar 0.005, which I read as relative, the same unit as the guardrail margins). The point estimate 0.81% clears it. The lower CI bound (0.41%) is under the bar, so the true lift could be somewhat below 0.5%. The prereg did not require the CI to clear it.

**Bar units.** If the 0.005 bar were meant as absolute (0.5pp), the result (0.33pp) would miss it and the call would flip to Don't ship. The prereg doesn't say. The guardrail margins (e.g. 2% on a 412 ms latency) only make sense as relative, so I read the bar the same way. Please confirm in the review.

**Guardrails (all within margin; worst-case CI edge vs margin, relative):**
| Metric | Change | 95% CI edge (worse side) | Margin |
|---|---|---|---|
| Latency p95 | +0.2% | +0.7% | 2% |
| Abandonment | +0.1% | +0.7% | 1% |
| Zero Result Rate | 0.0% | +1.4% | 3% |
| Revenue/User | −0.1% | −0.8% | 1% |

Abandonment and revenue are the tightest. Their CIs don't rule out a loss near the margin, but they stay inside it.

**Validity.** Exposures balanced (health check passed). 1.0M units/arm against 0.9M planned. It ran the planned 14 days with no sequential peeking. The audit log is empty, so no mid-flight config changes. Test and control differ only in `ranker_model` (snippet_length is the same), so the effect is attributable to the ranker.

**Time trend.** On a calendar-day basis the lift drifts down from +1.25% (day 1) to +0.50% (day 14), and the day 12–14 CIs include 0. That looks like novelty decay. On an exposure-day basis (days since a user's first exposure) the effect is flat at about +0.8% for all 12 days (CI lower bounds ≥ +0.18%), so there's no sign of user-level novelty wearing off. The calendar drift is more likely cohort mix, because later days are dominated by newer exposures. I can't fully rule out an external time effect, so I'd keep a small holdout and watch post-launch.

**Things to know (none change the call):**
- Reformulation Rate (secondary, lower is better) got worse: +1.0% relative, p = 0.013. It isn't a pre-registered guardrail, and with about 15 secondaries it wouldn't survive a multiple-comparison correction. It's still worth watching, since it runs against the "better ranking" story. Time to First Click improved (−0.07 s, p = 0.029, same caveat).
- CTR, long clicks, clicks/user and queries/user are flat. The primary gain isn't backed by extra clicks.
- The segment cuts are exploratory and none is significant. Mobile (−0.34pp, p = 0.06) and Desktop (−0.23pp, p = 0.08) are both negative while the overall effect is positive. Two segments of a partition can't both be below the total, so either there are other platforms or the segment tables don't reconcile with the headline. I'd check the segment pipeline before anyone reads the segments, but it doesn't undercut the pre-registered primary.
- Pulse was run without CUPED, at 95% confidence, as requested.

**Recommendation.** Ship, with a post-launch holdout and monitoring of Reformulation Rate, abandonment and revenue.
