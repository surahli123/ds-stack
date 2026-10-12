Decision: Keep running

I also saved the readout as `readout.md` in the working directory.

**Primary metric (Successful Search Rate):**
- The test arm is at 0.4143 against control at 0.4120. That is a lift of +0.0023 absolute, or +0.55% relative.
- The pre-registered sequential 95% interval is +0.55% ± 0.76%, which is [-0.21%, +1.31%]. It includes zero, so the lift isn't established.
- The fixed-horizon p of 0.007 isn't valid for an interim look, so I didn't use it.
- The +0.5% bar is only met at the point estimate if it is relative. `prereg.json` doesn't say. I read it as relative because the guardrail margins are relative. If it is absolute (+0.005), the lift is well short of it.

**Why I can't call it final:**
- The Pulse is dated 2026-09-18, which is day 7 of 14. It covers about 481k units per arm against 900k planned, so it is an early snapshot, not the final data.
- The experiment started 2026-09-12 and was planned to end 2026-09-26. It is still marked active, and today is 2026-10-12. The final run's data hasn't been pulled.
- `experiment.json` has `sequentialTesting: false`, but the prereg and the Pulse request use sequential. The audit log is empty, so nobody changed it after launch. I used the sequential intervals, as pre-registered.

**Guardrails:**
- Latency and Zero Result Rate are within their margins.
- Abandonment and Revenue per User aren't cleared yet. Their intervals still allow worse-than-margin outcomes (about +1.24% abandonment, about -1.43% revenue).
- Neither shows harm; the intervals are just too wide.

**Secondary metrics and segments:**
- All secondary metrics are flat.
- The head-query lift (p = 0.043) and the mobile dip (-0.59%) come from unplanned segment cuts among about 60 metrics. I wouldn't act on either.

**Next step:** Pull the final 14-day Pulse with the same settings and re-run this readout. Ship only if the sequential interval supports the bar and both remaining guardrails clear. If the interval still straddles zero, call it "No effect found".