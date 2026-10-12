Decision: Don't ship

I wrote the readout to `readout.md` in the working directory. Ranker v7 does not meet the pre-registered ship criteria, because the pre-registration requires both primary metrics to reach their +0.005 bar.

- **Successful Search Rate:** it rose by +0.0033 (+0.81%, p=7e-05). The effect is real, but the point estimate is below the 0.005 bar.
- **Long Click Rate:** it rose by +0.0003 (+0.12%, p=0.70), which is indistinguishable from zero and clearly misses the bar.
- **Unit of the bar:** prereg.json doesn't say whether 0.005 is an absolute or a relative change. The decision is the same either way, because Long Click misses under both readings. The review should confirm the unit.
- **Guardrails:** latency, abandonment, zero-result rate and revenue per user are all within their margins. They aren't what blocks the decision.
- **Validity:** the test ran the planned 14 days with balanced allocation and no mid-flight config changes.
- **Exploratory results:** about 90 secondary and segment results were reported with no multiplicity correction. I'd treat the few that reached p < 0.05 as likely chance and not act on them.
- **Config mismatch:** experiment.json lists only Successful Search Rate as a primary, while the prereg has two.
- **Still active:** the experiment's status is still "active" past its planned window.

If the team wants to ship on Successful Search Rate alone, that changes the pre-registered criteria, so the review should decide it explicitly. The readout lists follow-up options.