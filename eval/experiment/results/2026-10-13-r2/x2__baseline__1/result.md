Decision: Keep running

I saved the full readout to `readout.md`.

- **Primary metric:** Successful Search Rate is up by +0.00334 (+0.81% relative), with a 95% CI of [+0.0017, +0.0050] and p = 7e-5. The effect is real, but the pre-registration requires the point estimate to reach +0.005. It doesn't, so the ship rule isn't met. The CI's upper end just touches the bar, so "Don't ship" would be premature too.
- **Guardrails:** All four (latency p95, abandonment, zero-result rate, revenue per user) have intervals inside their margins.
- **Timing:** The snapshot is from 2026-09-25, about 13 of the 90 planned days, and it is now 17 days old. Sequential testing is off, so repeated looks inflate false positives. Re-pull Pulse and apply the prereg rule at the planned end.
- **Design:** The config is the "Q3 search launches holdout", a 5% holdout against 95% test. Its stated goal is the combined effect of the quarter's ranking launches. Only `ranker_model` visibly differs between arms, so confirm nothing else differs before crediting the lift to v7.
- **Unit counts:** The config sets a 95/5 split, but Pulse shows 1M units in each arm. The prereg planned 50k per arm. Someone should check this before trusting the intervals.
- **Subgroups:** About 55 secondary and subgroup metrics were tested with no multiplicity correction. A few nominal hits (Head-query success rate, Navigational CTR, Mobile time-to-first-click) are consistent with chance, and none were pre-registered, so I'm not acting on them.

The audit log is empty, so there's no record of mid-flight config changes.