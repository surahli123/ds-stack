Decision: Escalate

I saved the readout as `readout.md` in the working directory. I didn't run CUPED, since the pulse was requested without it.

- **Pre-registered test passes.** Queries per User rose 2.4% (95% CI +1.5% to +3.3%) against a 1% bar. The Latency p95 guardrail passed at +0.2% against a 2% margin. The exposure health check passed, the audit log is empty, and the test ran its planned 14 days.
- **The win may be harm.** Reformulation Rate is up 5.1% (p<0.001), which is the wrong direction. Ad Click Rate is down 2.0% (p=0.001). Time to First Click is slower. Clicks per User is flat, and Sessions per User is down 0.5% (p=0.054). The extra queries come with no extra clicks.
- **The two sources name different primary metrics.** The Statsig config's hypothesis names Successful Search Rate, which came in at −0.35% (p=0.086, not significant). The pre-registration names Queries per User. The review needs to settle which one counts.
- **Reformulation is not a pre-registered guardrail.** The pre-registered rule would say Ship, so it can't catch this.
- **Multiple comparisons.** Pulse reports about 60 metrics with no correction. The smaller signals (Time to First Click, head-query clicks, p≈0.012) could be chance. Reformulation and ad clicks are too strong to be.

The readout asks the review to decide whether Queries per User is a valid success metric for this change. It also suggests checking query-level logs for reformulation chains.