Decision: Don't ship

I wrote the readout to `readout.md`. Ranker v7 meets the primary bar but breaches the Abandonment Rate guardrail.

- **Primary:** Successful Search Rate is up 0.00511 absolute (95% CI +0.0035 to +0.0068). The point estimate clears the 0.005 bar by only 0.0001, and the prereg judges the bar on the point estimate, so this passes narrowly.
- **Guardrail breach:** Abandonment Rate is up 2.2% relative (95% CI +1.5% to +2.9%). The whole interval is beyond the 1% margin. Latency, Zero Result Rate and Revenue per User are within their margins.
- **Margin assumption:** The prereg doesn't say whether the margins are absolute or relative. I read them as relative, because a 0.02 margin on latency in milliseconds only makes sense that way. If the abandonment margin were absolute, the breach would go away, so the prereg authors should confirm.
- **Other signals:** CTR and Clicks per User are up, but Long Click Rate is flat. The extra clicks don't look like better outcomes.
- **Segments:** I treated the segment results as exploratory, since there are about 45 uncorrected slices.
- **Validity:** Exposures were balanced and the audit log shows no mid-test changes. The Pulse snapshot is dated 2026-09-25, possibly a day short of the 14-day window (the test started 2026-09-12), and I didn't re-pull it.

The readout recommends investigating the abandonment increase before any relaunch. Accepting the trade-off instead would mean changing the prereg, which needs explicit sign-off at the review.