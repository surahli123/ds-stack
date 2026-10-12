I wrote the readout to `readout.md`. It starts with `Decision: Not an A/B test`.

**Why that call:** the pre-registration says this was a team-draft interleaving test. The experiment config doesn't set it up that way.
- **Control:** pure v6 rankings, with no `serving_mode` set.
- **Test:** v7 with `serving_mode=team_draft_interleaving`, so users see a blend of v6 and v7 results.
- **What Pulse compares:** pure v6 against that blend. It does not compare v6 against v7.

A proper interleaving readout is a within-user preference between the two rankers. The files don't contain that, so I couldn't compute it.

**What the Pulse numbers say, for reference only:**
- **Successful Search Rate:** it moved +0.0033 (0.4120 to 0.4153), with a 95% interval of about ±0.0016. The pre-registered bar is +0.005 at the point estimate, so this misses it. Because the test arm is only part v7, I can't scale it up to a v7 effect.
- **Guardrails:** none moved outside its margin. Latency p95, abandonment, zero-result rate and revenue per user are all inside their margins.
- **Segments:** I didn't read anything into the segment metrics. There are about 45 of them and no multiple-comparison correction.

The readout recommends re-analysing from the interleaving logs, or rerunning as a plain v6-only vs v7-only A/B test. It also says to settle the ship criterion before looking at that result. The audit log is empty, so nothing records or explains how the experiment was configured.