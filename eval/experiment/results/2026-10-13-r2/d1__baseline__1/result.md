I wrote the readout to `readout.md` in the working directory. It starts with `Decision: Don't ship`.

- **Primary metric:** Successful Search Rate rose by +0.0033 (95% CI +0.0017 to +0.0050, p = 7e-5). That is below the pre-registered ship bar of +0.005, and the top of the CI (+0.00498) also stays under the bar.
- **Latency guardrail:** p95 latency got worse by 3.1% (CI 2.5% to 3.7%), against an allowed 2%. The whole CI is past the margin, so this guardrail fails.
- **Other guardrails:** Abandonment, Zero Result and Revenue per User are all within their margins. Abandonment and Revenue per User are inconclusive.
- **Setup:** Exposures are balanced, there are 1M users per arm (the plan was 900k), and the audit log is empty, so nothing changed mid-test.
- **One assumption:** The prereg doesn't say whether the bar is absolute or relative. I read it as absolute. If it meant +0.5% relative, the primary would pass (+0.81%), but the latency failure still blocks shipping. The readout asks the team to confirm the unit.
- **Informational queries:** Clicks per User for informational queries is down 1.5% (p = 0.037). It is one of many unplanned cuts with no multiple-comparison correction, so the readout treats it as a hypothesis, not a finding.

The readout recommends fixing the latency regression and re-testing.