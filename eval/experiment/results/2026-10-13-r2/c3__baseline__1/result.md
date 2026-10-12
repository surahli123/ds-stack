Decision: Ship

I wrote the full readout to `readout.md`. The summary:

- **Primary metric:** Successful Search Rate rose from 41.20% to 41.53%, a relative lift of +0.81% (95% CI +0.41% to +1.21%, p=7e-5). The prereg bar is +0.5% relative and requires only the point estimate to reach it, so the bar is met. The lower CI bound sits just under the bar, which the prereg rule doesn't require to clear.
- **Guardrails:** All four are inside their margins at the worst end of the 95% CI.
  - Latency p95: +0.7% against a 2% margin.
  - Abandonment: +0.7% against 1%.
  - Zero results: +1.4% against 3%.
  - Revenue per User: -0.8% against -1%. This one is thin, so watch it after launch.
- **Experiment health:** The exposure-balance check passed, there are about 1M users per arm (900k planned), and the audit log is empty. Only `ranker_model` differs between arms.
- **Watch item:** Mobile Successful Search Rate points negative at -0.82% (p=0.11), while Desktop is +0.51%. Neither is significant, and these are unplanned cuts, so it is probably noise. Check mobile after ramp.
- **Assumption to confirm:** I read the 0.005 bar as relative, since the prereg margins and pre-period numbers are relative. If it was meant as 0.5 pp absolute, the +0.33 pp lift would fail.
- **Cleanup:** The experiment still shows "active" in Statsig past its 14-day duration. Close it out when launching.