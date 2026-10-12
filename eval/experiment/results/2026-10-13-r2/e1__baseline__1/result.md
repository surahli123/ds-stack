Decision: Escalate

I saved the full readout to `readout.md`. In short:

- **Primary metric:** Successful Search Rate rose 41.20% → 41.53%, a relative lift of +0.81% (95% CI +0.41% to +1.21%, p = 7e-5). The point estimate is above the pre-registered +0.5% bar, and the prereg only requires the point estimate to reach it. The CI lower bound is below the bar, so the true lift could be somewhat under it.
- **Guardrails:** Latency, Zero Result Rate and Revenue per User are within their margins. Abandonment Rate is not cleared. Its point estimate is +0.6% (worse), with a 95% CI of −0.4% to +1.6%, and the upper end is past the 1% margin. That is inconclusive rather than evidence of harm. The prereg doesn't say what to do in that case, so I'm escalating instead of calling Ship or Don't ship.
- **Test health:** Exposures are balanced, there were 1.0M users per arm against 900k planned, and the snapshot covers the full 14 days. The audit log is empty, so nothing changed mid-test.
- **Segments and secondaries:** Nothing is significant. I treated the roughly 40 segment cuts (mobile, informational and so on) as hypotheses only, since none is corrected for multiple looks.

The prereg doesn't state units for the bar and margins, so I read them as relative changes. If the bar is actually absolute (0.5 percentage points), the primary misses it at +0.33pp, and the answer moves toward Don't ship or Keep running. Please confirm the units before the review.

The readout's recommendations: confirm the units, then decide if a possible abandonment increase of up to about 1.6% is acceptable for a lift of about 0.8%. If the guardrail is a hard gate, extend the test. If the team accepts the risk, ship with abandonment monitored and a holdback.