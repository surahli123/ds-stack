Decision: Keep running

The readout is saved at `readout.md` in the working directory. It says don't ship on this snapshot.

- **Primary metric:** Successful Search Rate is up 0.585 percentage points (95% CI +0.13 to +1.04 pp, p = 0.011). The prereg rule requires the point estimate to reach +0.5 pp, and it does, but only just.
- **Guardrails:** Latency, abandonment, zero-result rate and revenue per user are all inside their margins at the worst end of their CIs.
- **Why I can't call ship:** The Pulse is dated 2026-09-15, so it covers about 3 of the 14 planned days and roughly 260k units per arm against 900k planned. It's a fixed-horizon test with sequential testing off, so the CI and p-value are only valid at the planned end.
- **Stale snapshot:** Today is 2026-10-12 and the planned end was around 09-26, but the experiment still shows as active. I don't know why, or whether a later Pulse exists. The audit log is empty, so I can't see any config changes.
- **Segment cuts:** None of the segment differences is a reliable signal. The one nominally significant result, Desktop Time to First Click at p = 0.0499, is one hit among about 60 unadjusted segment metrics.

Before the decision, we need a fresh Pulse covering the full window with the same settings (no CUPED, 95% confidence). Then apply the prereg rule to it.