Decision: Can't tell

I've written the readout to `readout.md`. The Pulse numbers don't answer the question the pre-registration asked, so I can't recommend shipping or killing v7 from them.

- **Design mismatch:** The prereg specifies team-draft interleaving, which measures within-user preference for v7 over v6. The experiment is configured as a between-user split. Control gets plain v6 with no `serving_mode`, and test gets v7 with `team_draft_interleaving`. Pulse is therefore comparing pure v6 against an interleaved mix, not v7 against v6, so the lift is diluted by an unknown amount. Any serving-path difference is also confounded with the ranker.
- **Primary metric:** Successful Search Rate is +0.0033 (95% CI about +0.0017 to +0.0050, p = 7e-5). That is a real difference between arms, but it misses the prereg bar of a point estimate at or above +0.005. I wouldn't treat it as v7's true lift either.
- **Guardrails:** None is breached (latency, abandonment, zero-result rate, revenue), though the intervals are loose.
- **Secondary metrics:** Pagination Rate is up 1.4% (p = 0.03). With roughly 70 uncorrected secondary and segment metrics, I read that as likely noise.
- **Audit log:** It is empty, so I can't tell whether the config was always set up this way.

The next step is to compute the interleaving preference win rate from the raw logs and check it against the bar. Someone also needs to explain why control has no `serving_mode` and what the test arm's blend is.