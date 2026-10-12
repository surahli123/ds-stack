Decision: Keep running

The readout is saved as `readout.md` in the working directory.

- **Primary (Successful Search Rate):** The effect is +0.00227 absolute, or +0.55% relative. That is just above the 0.5% bar, if the bar is relative. The pre-registered sequential 95% CI is ±0.76% relative, so it includes zero and doesn't clear the bar. The unadjusted p=0.007 isn't valid for a decision on an interim look.
- **Guardrails:** Latency and Zero Result Rate are fine. Abandonment (upper bound about +1.2% against a 1% margin) and Revenue per User (lower bound about −1.4% against a 1% margin) can't be ruled out as harmed.
- **Data is stale and interim:** The Pulse is dated 2026-09-18, about a week into a 14-day run, with roughly 481k units per arm against 900k planned. Today is 2026-10-12 and the config still says `active`. The audit log is empty.
- **Config mismatch:** The experiment config has `sequentialTesting: false`, but the pre-registration says sequential. I used the sequential intervals.
- **Segments:** I scanned about 50 segment cuts. The one nominal hit (Head Queries, p=0.043) is expected by chance at that count, so I treated the cuts as exploratory.

The readout recommends re-pulling the final Pulse with the same settings. Ship only if the point estimate is at or above the bar and the Abandonment and Revenue guardrails clear. The team also needs to settle whether the 0.005 bar is relative or absolute. I assumed relative; if it's absolute, the current estimate misses it.