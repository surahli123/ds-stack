Decision: Escalate

I saved the readout as `readout.md`. The Ranker v7 arm clears the pre-registered bar and no guardrail is hurt, but I can't recommend shipping on this evidence alone, for two reasons:

- **Unplanned second change:** The Test arm changed `snippet_length` from 160 to 220 as well as the ranker. The pre-registration only covers `ranker_model`, and the audit log is empty, so nobody has recorded who made the change or why. The lift can't be credited to the ranker alone.
- **Unclear unit for the bar:** The pre-registered bar of 0.005 doesn't say whether it is relative or absolute.
  - **If relative:** Successful Search Rate rose 0.81% (95% CI 0.41% to 1.21%, p=7e-5), which passes the "point estimate at or above the bar" rule.
  - **If absolute:** The rise is 0.33 pp, which misses the bar, and the answer becomes Don't ship.

  I read it as relative because the guardrail margins only make sense that way.

All four guardrails sit inside their margins (Latency p95, Abandonment, Zero Result, Revenue per User). The segment cuts are exploratory and I wouldn't act on them. Desktop success rate is slightly down (−0.66%) but not significant.

The review needs to confirm the unit of the bar and who set `snippet_length` to 220. Then it can either ship the bundle as tested or rerun with snippet length held at 160.