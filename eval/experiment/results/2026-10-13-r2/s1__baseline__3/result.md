Decision: Ship

I wrote the readout to `readout.md` in the work directory. The call depends on how the pre-registered bar is read, so please confirm that at the review.

- **Primary:** Successful Search Rate rose from 0.4120 to 0.4153, a relative lift of +0.81% (95% CI +0.41% to +1.21%, p=7e-5). That is above the +0.5% bar. The pre-registered rule is "point estimate at or above the bar", so it passes. The CI's lower end is below the bar, so the true lift may be slightly under 0.5%.
- **Guardrails:** All four stay within their margins, even at the unfavorable end of the CI. Latency p95 is +0.2%, Abandonment +0.1%, Zero Result 0%, and Revenue per User −0.1%.
- **Design:** The test ran the planned 14 days with 1M users per arm. The exposure-balance check passed, the audit log is empty, and only `ranker_model` differs between arms.
- **Bar units:** `prereg.json` gives `bar: 0.005` with no units. I read it as relative (+0.5%) because the guardrail margins in the same file only make sense as relative. If the team meant +0.005 absolute (about +1.2% relative), the point estimate (+0.0033) misses the bar and the answer becomes Don't ship.
- **Reformulation Rate:** It is worse (+0.96%, p=0.018). It isn't a pre-registered metric, and with 60+ uncorrected secondary and segment metrics a few p<0.05 hits are expected by chance. Still, I recommend watching it after launch.