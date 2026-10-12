The readout is written to `readout.md` in the working directory, and I just fixed one sentence in it. It starts with `Decision: No effect found`.

- **Primary metric:** Successful Search Rate moved +0.016 pp, with a 95% CI of −0.107 to +0.140 pp (p = 0.79). The pre-registered ship bar was +0.5 pp, and even the top of the CI is well below it. This is a precise null.
- **Guardrails:** Latency p95, Abandonment Rate, Zero Result Rate and Revenue per User are all within their pre-registered margins.
- **Experiment health:** There are 1.0M units per arm against 900k planned, and the exposure health check passed. The audit log is empty, so nothing changed during the run.
- **Revenue per User:** It is up 3.1% (p = 0.004), but it isn't a pre-registered primary. Ad Click Rate is flat, and it doesn't survive correction across the 57 reported metrics. The readout treats it as a hypothesis, not a win.
- **Next steps:** The experiment is still marked `active` past its planned end, so the readout recommends stopping it.