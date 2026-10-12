Decision: Don't ship

I saved the full readout as `readout.md`. In short:

- **Why not ship:** The pre-registration requires both primary metrics to reach the 0.005 bar, and Long Click Rate doesn't. It moved +0.0003 (95% CI −0.0011 to +0.0016, p=0.70). The CI's upper end sits below the bar, so running longer wouldn't change that.
- **Successful Search Rate:** It rose by a real but small amount, +0.0033 (+0.81% relative, p=7e-5). That misses the bar if 0.005 is an absolute bar. If it's relative, it clears it. The pre-reg doesn't say which, and the review should settle that. The decision doesn't depend on it, because Long Click fails either way.
- **Test validity:** It looks sound. Exposures are balanced at 1M per arm, it ran the planned 14 days, and the audit log is empty, so there were no mid-test changes.
- **Guardrails:** All four are within their margins: latency, abandonment, zero results and revenue.
- **Secondary and segment results:** I treated them as exploratory. About 55 were tested without correction, and the few nominal hits point in different directions.
- **Config mismatch:** The Statsig config lists only Successful Search Rate as a primary, but the pre-reg lists both. I judged Long Click as a primary because the pre-reg does.
- **If the team wants to ship on Successful Search Rate alone:** That changes the pre-registered rule, so it needs explicit sign-off from the owners.