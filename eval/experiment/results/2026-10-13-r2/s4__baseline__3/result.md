Decision: Don't ship

I saved the full readout as `readout.md`. The main points:

- **Primary metric:** Successful Search Rate rose from 0.4120 to 0.4134, a gain of +0.00334 (95% CI +0.0017 to +0.0050, p=7e-5). The gain is real.
- **Why not ship:** The pre-registered rule is `point_at_bar` with a bar of +0.005. The point estimate is below that. The top of the CI (0.00499) is also just under it.
- **Open question:** `prereg.json` doesn't say whether the 0.005 bar is absolute or relative. I read it as absolute, which is the natural reading for a rate metric. If the team meant a relative 0.5%, the +0.81% relative lift would clear it and the decision would flip. Please confirm this at the review.
- **Guardrails:** All four pass. I assumed the margins are relative. Revenue per User comes closest: its worst CI end is about -0.8% against a -1% margin.
- **Exploratory metrics:** Roughly 60 segment and secondary metrics were reported, so a few nominal hits are expected by chance.
  - Head-query success rate is down (-0.0038, p=0.011). It doesn't survive multiplicity correction, but it's worth a follow-up.
  - Reformulation rate is worse (p=0.039) and time to first click is better (p=0.031). They roughly offset, and neither survives correction.
- **Experiment checks:** The exposure-balance health check passed, and the audit log is empty, so there were no mid-test config changes. Pulse reports 1.0M units per arm against 0.9M planned. The 14-day run is complete, and sequential testing was off.