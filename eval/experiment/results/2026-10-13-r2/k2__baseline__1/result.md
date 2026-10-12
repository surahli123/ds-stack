Decision: Keep running

The readout is saved at `readout.md` in the working directory. I'd extend the test rather than ship tomorrow, because the lift is shrinking day by day.

**Primary metric (Successful Search Rate):**
- **Pooled result:** +0.33 pp absolute (+0.81% relative), 95% CI +0.17 to +0.50 pp, p = 7e-5.
- **Decay:** the daily lift falls from +1.5% on day 1 to +0.4% on day 12, and the CI includes zero from day 10. The pooled number is mostly the early, larger days. That pattern looks like a novelty effect, so the lasting effect is probably smaller.
- **Missing days:** the daily file stops at day 12, although the test ran 14 days (Sep 12 – Sep 25).

**Unclear bar unit:** the pre-registration sets the bar at 0.005 but doesn't say relative or absolute. Read as relative (0.5%, matching the guardrail margins), the pooled result passes. Read as absolute (0.5 pp), it fails. The review needs to confirm which was meant.

**Guardrails:** latency, abandonment, zero-result rate and revenue per user are all within their margins. The CIs are wide enough that small losses aren't ruled out.

**Validity:** the exposure-balance check passed, only the ranker model differed between arms, and the audit log is empty. The test was read at its planned end, so there's no peeking problem.

**Segment cuts:** tail-query clicks per user are down 2.25% (p = 0.004) and desktop search success is down 0.79% (p = 0.07). These come from about 60 unplanned, uncorrected comparisons, so I treated them as exploratory.

The readout also proposes a rule for the extension: ship if the lift on late exposure days has a point estimate at or above the bar and the guardrails hold.