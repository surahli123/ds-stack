Decision: Keep running

# Ranker v7 readout (launch review)

**Bottom line:** The data in hand can't support a ship call. The primary metric points the right way, but the pre-registered sequential interval includes zero, and two guardrails aren't ruled out. The Pulse snapshot is also an interim one. Re-pull the final Pulse before the review and decide on that.

## Data caveats
- **The snapshot is interim and stale.** The Pulse is dated 2026-09-18. The experiment started 2026-09-12 and was planned for 14 days, so the snapshot is about 6–7 days in. Today is 2026-10-12, and the config still says `active`.
- **It has about half the planned sample.** There are 481k test and 480k control units. The pre-registration planned 900k per arm.
- **No config changes explain this.** The audit log is empty.
- **The config disagrees with the pre-registration on sequential testing.** The pre-registration specifies sequential testing, but the experiment config has `sequentialTesting: false`. I used the sequential intervals from the Pulse, as pre-registered. Because the snapshot is interim, the unadjusted interval (which gives p=0.007) is not valid for a decision.
- **Health checks.** Exposure balance passed. The `ranker_model` parameter is the only one that differs between arms, as intended.

## Primary: Successful Search Rate
- The effect is +0.00227 absolute, or +0.55% relative (0.4120 → 0.4143).
- The bar is 0.005. I read it as relative, i.e. +0.5%, which matches how the guardrail margins are expressed. If it means absolute (+0.005), the point estimate misses it.
- The sequential 95% CI is ±0.00313 absolute (±0.76% relative). That gives about −0.09% to +1.3% relative, so it includes zero and does not clear the bar.
- The unadjusted CI (±0.00165, p=0.007) excludes zero. It is not valid under the pre-registered sequential design with interim looks.
- The point estimate is only just above the bar, and the interval is wide enough that the true effect could fall on either side of it.

## Guardrails (relative change; sequential CI vs pre-registered margin)
| Metric | Change | Seq. CI half-width | Margin | Status |
|---|---|---|---|---|
| Latency p95 | +0.2% | ±0.95% | 2% | OK |
| Zero Result Rate | 0.0% | ±2.66% | 3% | OK |
| Abandonment Rate | +0.1% | ±1.14% | 1% | **Not ruled out** (upper bound ≈ +1.2%) |
| Revenue per User | −0.1% | ±1.33% | 1% | **Not ruled out** (lower bound ≈ −1.4%) |

Neither guardrail shows a significant harm. With this sample, a harm beyond the margin can't be excluded for abandonment or revenue.

## Secondary and segment metrics
- No secondary metric moves significantly, and the sequential CIs are wide.
- CTR (−0.3%) and Queries per User (−0.4%) lean slightly negative and are not significant.
- I scanned about 50 segment cuts. The one nominal hit is Head Queries (p=0.043, unadjusted), and Mobile is slightly negative. With that many cuts, one p<0.05 is expected by chance, so these are exploratory and not a basis for any claim.

## Recommendation
1. Don't ship on this snapshot, and don't call it a null either. The estimate is positive but not distinguishable from zero under the pre-registered design.
2. Re-pull Pulse with the same settings (95% CI, sequential, no CUPED) once the run reaches its planned size or end date. Apply the pre-registered rule then: ship only if the point estimate is at or above the bar and the Abandonment and Revenue guardrails are cleared. Decide whether the bar is relative or absolute before looking.
3. Confirm whether the experiment was meant to run past 2026-09-26. If it ran to completion, the review should use that final Pulse, not this snapshot.
4. Fix the config mismatch on sequential testing so the console matches the pre-registration.
