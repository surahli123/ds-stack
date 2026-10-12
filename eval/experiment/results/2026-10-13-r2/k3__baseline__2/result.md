Decision: No effect found

I saved the readout to `readout.md`. The summary:

- **Primary metric:** Successful Search Rate moved +0.00049 (CI −0.0015 to +0.0025, p=0.62). The pre-registered bar was +0.005. Even the top of the CI is well under the bar, so the data rule out an effect of the size the team needed.
- **Guardrails:** All four are within their margins. Latency p95 is +0.2% against a 2% margin. Abandonment is +0.1% against 1%. Zero Result Rate is 0.0% against 3%. Revenue per User is −0.1% against 1%. I read the margins as relative changes.
- **Validity:** The test is clean. Exposure balance passed, and both arms have 1M units against 900k planned. It ran the planned 14 days, the audit log shows no changes, and only `ranker_model` differed between arms.
- **Segments and secondary metrics:** There are about 70 uncorrected metrics. The few nominal hits go in both directions: mobile Clicks per User is down, Navigational SSR is down, and Informational Clicks per User is up. They look like chance and aren't a basis for a decision.
- **Recommendation:** Don't launch v7 on this evidence. It isn't harmful, but it shows no lift. Any further iteration needs a larger expected effect, or a smaller pre-registered bar with a matching sample size.