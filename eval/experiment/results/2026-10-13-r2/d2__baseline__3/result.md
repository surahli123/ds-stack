Decision: Don't ship

Ranker v7 lowered Successful Search Rate, the pre-registered primary metric, and the drop is statistically significant. I also saved this readout as `readout.md` in the working directory.

**Primary metric**
- Successful Search Rate went from 0.4120 in control to 0.4094 in test, a change of -0.26 pp (-0.62% relative).
- The 95% CI is [-0.42 pp, -0.09 pp] and p = 0.0024.
- The ship bar was +0.005, which I read as +0.5 pp absolute. The point estimate is -0.0026, and even the top of the CI is below zero. The result also falls short of the bar if it was meant as +0.5% relative.

**Guardrails**
All four are within their pre-registered margins at 95%, so they don't change the decision.
- Latency p95: +0.2% (margin 2%).
- Abandonment Rate: +0.1% (margin 1%).
- Zero Result Rate: 0.0% (margin 3%).
- Revenue per User: -0.1%, with a worst case of about -0.8% against a -1% margin. This one is within margin but not strongly ruled out.

**Validity**
- The test is a clean A/B on userID, with 1.0M users per arm against 0.9M planned, and the exposure-balance check passed.
- It ran the planned 14 days (2026-09-12 to 09-25) with sequential testing off, so there is no peeking problem.
- The audit log is empty, so there were no mid-test config changes.
- `ranker_model` is the only parameter that differs between arms.

**Segments and secondaries**
- The secondary metrics are flat or slightly negative, and none is significant on its own.
- I scanned about 50 segment metrics with no multiplicity correction. Two CTR decreases are nominally significant: head queries (-1.5%, p = 0.003) and informational queries (-1.3%, p = 0.038).
- With that many looks, a couple of hits are expected by chance, so I treat these as hints only. They do point the same way as the primary.
- Successful Search Rate by segment is not significant anywhere, so there is no case for shipping to a subset.

**Next steps**
- The experiment still shows as "active" in Statsig, so end it.
- If the team still wants the v7 model, work out why Successful Search Rate fell (head and informational queries first) and run a new pre-registered test.