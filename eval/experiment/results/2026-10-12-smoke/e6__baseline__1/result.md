I wrote the readout to `readout.md`. Its decision is **Escalate**: the pre-registered ship criteria are met, but I wouldn't ship on that alone.

- **Setup is clean.** Allocation is 50/50 with the exposure check passed. The planned 14 days are complete (Sep 12–25), and the audit log is empty.
- **Pre-registered criteria pass.**
  - Queries per User is up 2.4%, with a 95% CI of about +1.5% to +3.3%. That clears the 1% bar.
  - Latency p95 is up 0.2%, well inside the 2% margin.
- **The configured primary disagrees with the prereg.** The Statsig config and its hypothesis use Successful Search Rate, which is flat to slightly negative (-0.35%, p=0.086). The data can't rule out a harm of about 0.75%. Nothing in the audit log explains why the prereg uses Queries per User instead.
- **Other metrics don't support "more queries means more engagement."**
  - Clicks, CTR, long clicks and revenue are flat, and sessions are slightly down.
  - Time to First Click is worse (+1.3%, p=0.012), and Ad Click Rate is down 2% (p=0.001).
  - Overall Reformulation Rate is up 5.1%, which could mean users are re-searching because results got worse.
- **The reformulation data is inconsistent.** Both the Mobile slice (-2.0%) and the Desktop slice (-0.8%) are negative, yet the overall figure is +5.1%. An overall effect can't fall outside both of its parts. Someone needs to reconcile this before the review relies on either reading.
- **Slice metrics are exploratory only.** They weren't pre-registered and have no multiplicity correction.

The readout asks the review to settle whether Queries per User is the right success metric and to have the reformulation numbers re-pulled. If the metric is confirmed, the prereg rule says ship. If the goal is successful searches, the answer moves toward "Don't ship." No extra run time is needed.