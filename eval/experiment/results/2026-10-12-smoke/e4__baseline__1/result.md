Decision: Don't ship

I wrote the readout to `readout.md` in the working directory. Ranker v7 misses the pre-registered bar once the result is converted to the overall population.

- **Triggered scorecard:** Successful Search Rate (SSR) rises from 0.4120 to 0.4198, which is +0.0078 (+1.9% relative, p<0.001). The lift is real.
- **Bar population:** the pre-registration says the scorecard covers triggered searches only. Those are 10% of searches and 20.5% of control successes. The 0.005 bar is for the overall population.
- **Overall conversion:** this is my derivation from those shares, not Pulse output. It comes to about +0.0008 absolute, or +0.39% relative. In relative terms the CI is roughly +0.27% to +0.51%. Reading the bar as absolute or as relative gives the same answer, because the point estimate misses either way. The pre-registration requires the point estimate to be at the bar to ship.
- **Guardrails:** latency, abandonment, zero-result rate and revenue per user are all within their margins.
- **Validity:** no problems found. The audit log is empty, only `ranker_model` differs between arms, the exposure balance check passed, and there are 1M units per arm against 900k planned.
- **Exploratory signals:** about 60 secondary and segment metrics were checked, with no multiplicity correction. Three have p<0.05, and all three point the unfavorable way:
  - Queries per user, −1.0%.
  - Desktop time to first click, +0.13 s.
  - Informational reformulation rate, +1.8%.

  These are worth a follow-up look but aren't established harms.

The team should confirm whether 0.005 is meant as absolute or relative. If they still want to ship a ~0.4% relative overall gain, that means revising the bar explicitly. It shouldn't be done by reading the triggered number against the bar.