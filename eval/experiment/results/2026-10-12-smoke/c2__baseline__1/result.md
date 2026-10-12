Decision: Don't ship

I wrote the readout to `readout.md`. Ranker v7 does improve Successful Search Rate, but not by enough to meet the bar the team set before launch.

- **Primary metric:** Successful Search Rate rose 0.334 points (95% CI 0.169 to 0.499, p = 7e-5). The pre-registered bar is 0.5 points, and the pre-registration says shipping requires the point estimate to reach it. The CI's upper end (0.4985) is also just under the bar.
- **Run quality:** The test ran its full 14 days with 1.0M users per arm (900k planned), and the exposure-balance health check passed.
- **Guardrails:** Latency, Abandonment, Zero Result Rate and Revenue per User all stay inside their pre-registered margins. None is a reason to block.
- **Secondary and segment metrics:** About 50 segment metrics are exploratory only. A few were nominally significant, which is expected by chance at that count.
- **Confound:** The test arm also changed `snippet_length` from 160 to 220, which the pre-registration doesn't list as intended. The audit log is empty, so I can't say who changed it or when. The lift is therefore the combined effect of the ranker and the longer snippets.

The readout recommends rerunning with only `ranker_model` changed. It also notes that shipping at roughly +0.3 points would be a business decision, made explicitly against the pre-registration.