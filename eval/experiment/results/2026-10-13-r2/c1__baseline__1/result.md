Decision: Don't ship

I wrote the readout to `readout.md` in the working directory. It starts with the exact decision line you specified.

- **Primary metric:** Successful Search Rate rose 0.334 pp (95% CI +0.169 to +0.499 pp, p = 7e-5). That is clearly positive, but below the +0.5 pp bar the team pre-registered, and the CI's upper end is also just under the bar. The pre-registered rule ("ship requires point at bar") therefore says don't ship.
- **Guardrails:** Latency p95, Abandonment Rate, Zero Result Rate and Revenue per User all stay within their margins. The CIs are fairly wide, so this is no evidence of harm rather than proof of none.
- **Possible sample-ratio mismatch:** `experiment.json` lists exposures of 1,010,000 control vs 990,000 test on a 50/50 split, which is far too large a gap for chance. But the platform's balance check says PASSED, and Pulse reports exactly 1,000,000 units per arm. I couldn't tell which is right, so someone should check the raw assignment counts. A real mismatch wouldn't change the decision, since the estimate is already below the bar.
- **Clicks per User:** It fell 1.0% (p = 0.014). It wasn't pre-registered and is one of about 70 unplanned metrics and slices, so I treated it as likely noise but flagged it for a look.

The readout also notes that the experiment is still running past its planned 14 days.