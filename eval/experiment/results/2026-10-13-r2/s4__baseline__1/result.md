I wrote the readout to `readout.md` in the working directory. It opens with `Decision: Ship`, but that depends on how I read the pre-registered bar (see the caveat below).

- **Primary result:** Successful Search Rate rose +0.81% relative (+0.33 pp). The 95% CI is +0.41% to +1.21%, with p = 7e-5. The point estimate clears the 0.5% bar.
- **Guardrails:** All four hold. The worst ends of the CIs are latency p95 +0.7% against a 2% margin, Abandonment +0.7% against 1%, Zero Result +1.4% against 3%, and Revenue −0.8% against −1%.
- **Setup checks:** The run covered the full planned 14 days, the exposure balance check passed, the audit log is empty, and only `ranker_model` differs between arms.
- **Exploratory results:**
  - Head-query Successful Search Rate is −0.95% (p = 0.011), the opposite sign from the overall lift. It doesn't survive a correction across the six segments.
  - Reformulation Rate and Time to First Click are nominally significant. I treated them as unadjusted noise-risk results because there are about 60 secondary metrics.

**Caveat:** `prereg.json` gives the bar as `0.005` with no unit. I read it as relative (0.5%), because the guardrail margins only make sense as fractions of baseline. If the team meant 0.5 percentage points absolute, the observed +0.33 pp misses the bar and the decision becomes Don't ship. The readout asks the review to confirm the unit.

The experiment status is also still "active", and the readout recommends closing it out.