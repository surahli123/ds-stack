Decision: Ship

I wrote the readout to `readout.md`, with the decision line first. The ship call depends on one assumption: that the pre-registered 0.005 bar is relative (0.5%).

- **Primary:** Successful Search Rate rose from 41.20% to 41.53%, which is +0.334 pp or +0.81% relative (p=7e-5). The pre-registration says to ship if the point estimate reaches the bar, and +0.81% clears 0.5%.
- **The unit question:** the pre-registration gives the bar as 0.005 with no unit. I read it as relative because the guardrail margins in the same file can only be relative. For example, 0.03 on Zero Result Rate, whose baseline is 0.031, would be absurd as an absolute margin. If the bar is actually 0.5 pp, the lift misses it and the decision becomes Don't ship. The team should confirm the unit at the review.
- **Guardrails:** all four are within their margins. Latency p95 is significantly worse, +1.2% (about +5 ms), with a worst case of +1.7% against the 2% limit. Abandonment, Zero Result Rate and Revenue per User are within margin.
- **Data checks:** exposures were balanced, there were 1,000,000 users per arm, and the audit log is empty, so nothing changed mid-test. Only `ranker_model` differs between arms.
- **Flagged, not blocking:**
  - CTR fell 0.71% (p=0.005). It is a secondary metric and I couldn't tell why from this data.
  - No segment shows a significant lift. Head queries and desktop point slightly negative, but they are underpowered.
  - The latency regression should be watched after launch.