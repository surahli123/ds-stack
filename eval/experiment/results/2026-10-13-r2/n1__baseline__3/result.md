Decision: No effect found

I saved the full readout to `readout.md`. The decision is based on these points:

- **Primary metric:** Successful Search Rate went from 41.20% to 41.22%, a change of +0.016pp (95% CI −0.107pp to +0.140pp, p=0.79). The pre-registered bar was +0.5pp. The whole CI sits below that bar, so a gain that large is ruled out at 95%.
- **Guardrails:** none were breached. At the worst end of the CI, latency p95 is up 0.7% (margin 2%) and zero-result rate is up 1.4% relative (margin 3%). Abandonment rate stays inside its 1% margin however you read it.
- **Revenue per User:** it rose 3.1% (p=0.004), but I'd treat that as exploratory. The report has about 70 metrics and segment cuts with no multiple-comparison correction. No engagement metric moves with it. It was a guardrail, not a primary. If the business cares, run a separate test with it pre-registered as the primary.
- **Segments:** 4 of 54 segment tests have p<0.05, which is about what chance would give (around 3). Successful Search Rate is flat in every segment.
- **Validity:** each arm has 1,000,000 users (plan was 900,000), split evenly, and the exposure health check passed. The test ran the planned 14 days, only `ranker_model` differs between arms, and the audit log is empty. Pulse was pulled with CUPED off and a 95% CI, matching the pre-registration.

I only had aggregated Pulse output, so I couldn't check for novelty effects or day-level trends. The CI doesn't exclude small gains below the bar, up to about +0.14pp.