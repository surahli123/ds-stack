Decision: Don't ship

I saved the readout to `readout.md`. The result is a miss against the pre-registered bar, and two data problems need checking before the meeting.

- **Primary metric:** Successful Search Rate is up 0.33 pp, from 0.4120 to 0.4153 (95% CI +0.16 to +0.50 pp, p = 7e-5). The effect is real, but the pre-registration requires the point estimate to reach +0.50 pp. The CI's upper bound only just touches that bar.
- **Guardrails:** All four are within their margins. Latency p95 is +0.2%, Abandonment Rate +0.1%, Zero Result Rate 0%, and Revenue per User −0.1%.
- **Secondary and segment metrics:** Nothing stands out. A few of the roughly 40 segment metrics have p < 0.05, which is about what chance gives across that many uncorrected looks.
- **Config doesn't match the prereg:** `experiment.json` is "Q3 search launches holdout", a 5% holdout meant to measure the combined effect of the quarter's launches. The prereg id is `ranker_v7`. Only `ranker_model` differs between arms (v6 vs v7), so the contrast is plausibly v7 alone. The owner should confirm no other launches are bundled in, and the audit log is empty, so I couldn't check the change history.
- **Arm sizes look inconsistent:** The config says a 5/95 split with 20% allocation, but Pulse shows exactly 1,000,000 units in each arm, and the balanced-exposure check passed. Either the Pulse arms aren't what the config describes, or the config changed after launch. If either data problem shows the data isn't a clean v6-vs-v7 comparison, the decision becomes "Can't tell".
- **Early look:** The Pulse is dated 2026-09-25, about 13 days into a planned 90. Sequential testing is off, so the interval is a fixed-horizon one read early. The estimate would still have to move by about 50% to reach the bar.

If the team still wants v7, the route is a documented decision to lower the bar, not a reinterpretation of this result.