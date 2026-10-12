Decision: Don't ship

I've written the readout to `readout.md`. v7 raises Successful Search Rate (SSR) on the searches it touches, but the lift is far below the pre-registered bar once it is scaled to all searches.

- **Primary metric:** Pulse reports SSR on triggered searches only. There it is +0.0078 absolute (+1.9% relative, 95% CI ±0.0025, p<0.001). The bar is +0.005 overall, and ship requires the point estimate to reach it. Comparing 0.0078 to 0.005 directly would be a mismatch.
- **Scaled to all searches:** Triggered searches are 10% of searches and 20.5% of control successes. That makes the overall lift about +0.0008 absolute (CI roughly +0.0005 to +0.0011), or about +0.39% relative (CI roughly +0.27% to +0.51%). Both the point estimate and the upper CI bound fall short, so more runtime won't change the outcome.
- **Assumption:** I read the bar as an absolute overall difference. If the team meant relative, v7 is still below the bar but closer.
- **Guardrails:** Latency p95, abandonment, zero-result rate and revenue per user are all within their margins, so none of them blocks a ship.
- **Validity:** The run is a clean A/B. The exposure balance check passed, it ran the planned 14 days (2026-09-12 to 09-25), and the audit log is empty, so there were no mid-run changes.
- **Queries per User:** It is down 1.0% (p=0.024). It's a secondary metric, and about 70 metrics and segments were read with no multiplicity correction. I treat it as chance, not evidence of harm. The segment cuts show no consistent pattern.

The readout lists three options for the review: stop, explicitly waive or redefine the bar as a recorded deviation, or widen the trigger and rerun.