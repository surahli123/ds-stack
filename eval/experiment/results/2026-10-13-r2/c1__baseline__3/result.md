Decision: Can't tell

I've saved the readout as `readout.md`. It can't be a Ship yet, because the experiment config suggests the arms were not split evenly.

- **Why I can't call it:** `experiment.json` lists exposures of 1,010,000 in Control and 990,000 in Test for a 50/50 design. At about 2M users that gap is far beyond chance, with a z of about 14. The same file reports the balanced-exposures health check as PASSED, which contradicts those numbers. Pulse analyzed exactly 1,000,000 per arm, so I can't tell which count is right. Someone needs to check the raw assignment counts.
- **Primary metric:** Successful Search Rate went from 41.20% to 41.53%, a lift of +0.81% relative (+0.33 percentage points). The 95% CI is +0.41% to +1.21%, and p is 7e-05. The prereg's ship rule requires only the point estimate to reach the bar, and I read the bar of 0.005 as a relative 0.5%. If the SRM concern clears, this meets the rule.
- **Unit of the bar:** If the bar was meant as an absolute 0.5 percentage points, the result misses it and the call flips to Don't ship. The team should confirm which they meant.
- **Guardrails:** Latency, Abandonment, Zero Result and Revenue per User are all inside their margins. I read the prereg margins as relative.
- **Other findings:** The audit log is empty, so nothing changed mid-flight. Two of the 56 unadjusted secondary metrics are nominally significant: Clicks per User (down 1.0%, p=0.014) and tail-query Abandonment (up 1.7% relative, p=0.034). That is about what chance would produce across 56 metrics, and neither is a prereg metric or guardrail.