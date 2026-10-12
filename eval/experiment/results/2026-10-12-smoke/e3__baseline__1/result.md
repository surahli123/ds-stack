Decision: Don't ship

I wrote the readout to `readout.md` in the working directory.

- **Primary metric:** Successful Search Rate rose by +0.00128 (95% CI +0.00054 to +0.00202, p=0.0007). The lift is real but small. The pre-registered ship bar is +0.005, so even the top of the interval is well short of it. Under the prereg rule (`point_at_bar`), v7 can't ship.
- **Guardrails:** None is breached. For each one, the worst-case end of the CI is inside its margin. I read the margins as relative to control, which the prereg doesn't state. The conclusion holds under an absolute reading too.
- **Validity:**
  - The exposure-balance check passed.
  - The audit log is empty, so nothing changed mid-run.
  - The run covers the full 14 days, and the arms are 1.0M units each against 0.9M planned.
  - Only `ranker_model` differs between arms.
- **Segments and secondary metrics:** About 50 were examined and none moved meaningfully. The one nominal hit (CTR, Navigational, p=0.023) is what chance would produce across that many uncorrected tests.

The readout says that shipping on the +0.13 pp lift anyway would mean the review changing the pre-registered criterion on purpose. It doesn't suggest that.