Decision: Ship

I wrote the readout to `readout.md`. The pre-registered primary clears its bar and no pre-registered guardrail is breached, but two points need confirming at the review.

- **Primary:** Successful Search Rate rose 0.4120 → 0.4153. That is +0.81% relative (95% CI about +0.41% to +1.21%, p=7e-5), against a +0.5% bar.
- **Guardrails:** latency p95, abandonment, zero-result rate and revenue per user all pass. Revenue is the tightest, with the worst end of its CI at -0.8% against a 1% margin.
- **Setup:** the run lasted the planned 14 days with 1M users per arm. The exposure-balance check passed, the audit log is empty, and only `ranker_model` differs between arms.

**Needs confirming at the review:**
1. **Units of the bar.** I read the +0.5% bar as relative, because the guardrail margins in the same file can only be relative. If the bar was meant as an absolute +0.005, the observed +0.0033 misses it and the decision becomes Don't ship.
2. **Segment cuts don't reproduce the headline lift.** Every segment change is at most +0.0014, but the overall change is +0.0033. The segment control means also don't average to the overall 0.412. I couldn't tell whether the segment definitions differ or the arms differ in segment mix. Desktop is down 1.3% (p=0.003), but that is one of about 48 segment tests.

**Also flagged:** Clicks per User is down 1.2% (p=0.003). It wasn't pre-registered, it is 1 of 56 secondary and segment metrics, and it wouldn't survive a multiplicity correction. The readout recommends watching it post-launch.