Decision: Ship

I wrote the readout to `readout.md`. The call depends on one assumption: that the pre-registered bar of 0.005 is a relative lift.

- **Design:** The test is clean. It has 1M users per arm, ran the planned 14 days (Sep 12–25), and the exposure health check passed. The audit log shows no mid-flight changes, and only the ranker model differs between arms.
- **Primary:** Successful Search Rate rose from 41.20% to 41.53%. That is +0.33 pt, or +0.81% relative (p = 7e-5). The relative CI is +0.41% to +1.21%. The pre-registered rule only requires the point estimate to reach the bar, and +0.81% clears 0.5%.
- **Bar units:** I read the bar as relative because the guardrail margins clearly are (2% on a 412 ms latency). If it was meant as absolute (+0.5 pt), the result misses it and the call becomes Don't ship. The review should confirm this with the prereg authors.
- **Guardrails:** All four are inside their margins, judged at the worst end of each CI. The closest are abandonment (+0.7% against a 1% margin) and revenue per user (-0.8% against a -1% margin).
- **Exploratory flags:** Clicks per User is down 1.2% (p = 0.003). Desktop Successful Search Rate is -0.69 pt (p = 0.003). Neither survives correction across the roughly 60 secondary and segment metrics, so I treat them as hypotheses to watch after launch.
- **Data oddity:** The overall lift is larger than the lift in every segment of every split. A weighted average cannot do that, so the segment definitions in Pulse need checking before anyone quotes the Desktop number.