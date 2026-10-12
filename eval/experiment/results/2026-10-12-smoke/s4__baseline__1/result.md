Decision: Ship

I wrote the readout to `readout.md` in the working directory.

- **Primary result:** Successful Search Rate is up +0.81% relative (+0.33pp absolute; 95% CI +0.41% to +1.21%, p=7e-5). That clears the pre-registered bar of 0.5%. The prereg rule is `point_at_bar`, so it only needs the point estimate to clear the bar. The CI's lower end is below the bar, so the true lift could be somewhat under 0.5%.
- **Guardrails:** All four are within their margins, with the worst end of each CI inside the margin. Revenue per User is the tightest (worst case −0.8% against a −1% margin).
- **Validity:** The test ran the full 14 days (Sep 12 to Sep 25) with 1.0M users per arm. Exposure balance passed and the audit log is empty. Only `ranker_model` differs between arms.
- **Caveat 1, the bar's units:** I read the bar of 0.005 as a relative 0.5% lift. The guardrail margins only make sense as relative (a 3% margin on a 3.1% zero-result rate). If the bar was meant as an absolute 0.5pp, the result (+0.33pp) would fail. Confirm this in the review.
- **Caveat 2, exploratory segments:** Head-query Successful Search Rate is −0.95% (p=0.011). Reformulation Rate is also worse (+0.84%, p=0.039). Neither was pre-registered, and the Pulse output covers about 90 metrics and segments with no multiplicity correction, so they may be noise. The head and tail segments are both negative while the total is positive, which I couldn't reconcile from the data. The readout recommends monitoring head-query Successful Search Rate and Reformulation Rate after launch.