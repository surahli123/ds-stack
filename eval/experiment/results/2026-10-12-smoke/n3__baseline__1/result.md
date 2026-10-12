The readout is written to `readout.md` in the work directory. It opens with `Decision: No effect found`.

- **Test validity:** The run is clean. It is a plain 50/50 A/B test, the exposure-balance check passed, and the full 14 days ran (Sep 12–25). Arms have 1.0M units each against 0.9M planned. The audit log is empty, and only `ranker_model` differs between arms.
- **Primary metric:** Successful Search Rate moved by -0.0002, with a 95% CI of [-0.0014, +0.0010] and p = 0.74. The pre-registered bar was +0.005 and the point estimate had to reach it, so v7 fails. The upper CI bound is about 5x below the bar. This is a well-powered null, not an inconclusive result.
- **Guardrails:** The CIs for latency, abandonment, zero-result rate and revenue per user all sit inside their margins. Revenue per User is the tightest, with a lower bound of about -0.8% against a -1% margin.
- **Secondaries:** Ad Click Rate is down 1.5% (p = 0.013) and Queries per User is up 1.9% (p = 0.028). Neither would survive correction across the 56 secondary metrics, and I labeled both exploratory. Ad Click Rate is worth a follow-up look.

The readout recommends not shipping v7 as a ranking win. It also notes that retiring v6 is a separate call, since v7 shows no harm on the guardrails. Any smaller-lift claim would need a new pre-registered bar and a new test.