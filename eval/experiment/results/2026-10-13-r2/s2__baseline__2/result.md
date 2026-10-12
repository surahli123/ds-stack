Decision: Ship

I wrote the readout to `readout.md` in the work directory. The ship call depends on one unit question, covered below.

**Primary metric:** Successful Search Rate rose from 0.4120 to 0.4153. That is +0.00334 absolute, or +0.81% relative (95% CI +0.41% to +1.21%, p = 7e-5). The pre-registered ship rule only requires the point estimate to reach the bar, and +0.81% clears a 0.5% bar.

**Guardrails:** All four hold. The worst end of each CI stays inside its pre-registered margin.

| Metric | Observed | Worst CI bound | Margin |
|---|---|---|---|
| Latency p95 | +0.2% | +0.7% | 2% |
| Abandonment rate | +0.1% | +0.7% | 1% |
| Zero result rate | 0.0% | +1.4% | 3% |
| Revenue per user | −0.1% | −0.8% | 1% |

**Experiment health:** The exposure balance check passed, with 1.0M users per arm against 900k planned. The audit log is empty, so nothing changed mid-run. Only `ranker_model` differs between arms.

**Caveats for the review:**
- **The bar's unit isn't stated in the pre-registration.** I read 0.005 as relative because the guardrail margins in the same file only make sense as relative fractions (0.02 on a 412 ms latency, for example). If the team meant 0.5 percentage points absolute, the result is +0.33 pp, with a CI upper end of +0.50 pp, so the bar is not met. The decision would then be Don't ship. The review should confirm which was meant.
- **Ad Click Rate fell 2.8% (p = 0.022).** It isn't a pre-registered guardrail, and it is one of 56 secondary metrics tested without correction. About three nominal hits at 5% are expected by chance, and seven came in below 0.05. Revenue per user is flat, but I'd keep Ad Click Rate on watch after launch.
- **The margin over the bar is thin.** The CI includes lifts below 0.5%, so the expected gain is small.