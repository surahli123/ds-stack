Decision: Keep running

I saved the readout as `readout.md`. It is built only on the day-7 interim snapshot; I have no results from the full 14-day window.

- **Primary metric:** Successful Search Rate is up +0.00227 absolute (+0.55% relative). That is below the pre-registered ship bar of +0.005. The sequential 95% CI is [-0.0009, +0.0054], so it neither meets nor rules out the bar. The p = 0.007 in Pulse is a fixed-horizon number. It isn't valid for a sequential analysis, so don't cite it as a win.
- **Stale data:** The Pulse snapshot is dated 2026-09-18, about day 7 of 14, with roughly 53% of the planned 900k users per arm. The experiment started 2026-09-12, was planned to end 2026-09-26, and is still marked active today (2026-10-12). Re-pull Pulse before the review.
- **Guardrails:** Latency and Zero Result Rate are within their margins. Abandonment and Revenue per User are not cleared, because their sequential CIs extend past the pre-registered margins. I assumed the margins are relative; the pre-reg doesn't say.
- **Segments:** One of about 50 segment cuts is nominally significant (Head Queries, p = 0.043). With that many comparisons it isn't meaningful.
- **Config gaps:**
  - `experiment.json` has sequential testing off, while the pre-reg and the Pulse request use it.
  - `audit_logs.json` is empty, so I can't confirm nothing changed mid-run.

Ship only if the final point estimate reaches +0.005 and the guardrails clear. At the current +0.0023 that looks unlikely.