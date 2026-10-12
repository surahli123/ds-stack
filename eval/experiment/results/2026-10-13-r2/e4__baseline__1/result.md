Decision: Don't ship

The readout is also saved as `readout.md`.

**Primary metric:** Ranker v7 raises Successful Search Rate on triggered searches by +0.78 pt (95% CI +0.54 to +1.03). That scorecard covers only triggered searches, which are 20.5% of control successes. The +0.5 pt bar is an overall number. Scaled to overall, the lift is about +0.16 pt (CI about +0.11 to +0.21). That is well under the bar, and even the top of the CI misses it. The pre-registration requires the point estimate to reach the bar, so v7 fails.

**Guardrails:** None shows harm. Latency, Abandonment, Zero Result Rate and Revenue per User all stay within their margins.

**Queries per User:** It fell 1.04% (p=0.024). This was not pre-registered and sits among about 60 metrics and segments, so it is probably chance. It is worth watching but doesn't change the call.

**Experiment validity:** It looks sound. It ran a 50/50 split for the full 14 days with a single look. The exposure-balance check passed and the audit log shows no mid-run changes. Only `ranker_model` differs between arms.

If the team still wants to launch v7, that means changing the bar. They should argue for that openly at the review, not by pointing at the +0.78 pt triggered number.