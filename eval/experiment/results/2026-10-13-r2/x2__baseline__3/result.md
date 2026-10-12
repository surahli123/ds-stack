Decision: Can't tell

I wrote the readout to `readout.md`. The Pulse can't tell us whether Ranker v7 meets its ship bar, and I'd recommend against shipping on this evidence.

- **Wrong experiment:** The config and Pulse are for `q3_search_launches_holdout`, not the pre-registered `ranker_v7`. It is a 5% holdout measuring the combined effect of the quarter's ranking launches, so any lift isn't attributable to v7 alone.
- **Unit counts don't fit:** Pulse shows 1,000,000 units in each arm. The config says a 5%/95% split and the pre-reg planned 50,000 per arm. The audit log is empty, so there is nothing to explain the mismatch.
- **Early and stale:** The experiment started on 2026-09-12 and was planned for 90 days. The Pulse is dated 2026-09-25, about 2 weeks in, and today it would be about 30 days in.
- **Primary metric:** Successful Search Rate is +0.0033 absolute (95% CI +0.0017 to +0.0050, p=7e-5). The lift looks real, but the point estimate is below the +0.005 bar, and the pre-reg requires the point estimate to reach it.
- **Guardrails:** Latency p95, Abandonment Rate, Zero Result Rate and Revenue per User are all within their pre-registered margins.
- **Secondary metrics:** I treated the 56 exploratory secondaries and segment cuts as noise. A few have nominal p<0.05, but with that many tests some would be expected by chance.

To get a decision, the team needs to confirm whether a clean v7-only comparison exists and explain the unit counts. They also need a fresh Pulse closer to the planned duration.