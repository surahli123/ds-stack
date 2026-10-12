The readout is in `readout.md`, and the decision is **Escalate**.

- **Pre-registered ship rule passes.** Queries per User is up 2.4% (CI +1.5% to +3.3%), against a bar of +1%. Latency p95 is up 0.2% (upper bound +0.7%), inside the 2% margin.
- **The primary win may not be a real benefit.** Reformulation Rate is up 5.1% (p<0.001), and lower is better for it. Users re-querying because the first results failed would produce the same queries lift. I haven't confirmed that, so the readout asks for a check.
- **The stated hypothesis isn't supported.** Successful Search Rate is flat to slightly down (−0.35%, p=0.09).
- **Other metrics are worse.** Ad Click Rate is down 2.0% (p=0.001) and Time to First Click is up 1.3% (p=0.012). Revenue per User is flat.
- **Config and pre-reg disagree on the primary.** `experiment.json` lists Successful Search Rate and `prereg.json` lists Queries per User. Someone should confirm which one the team meant.
- **The Pulse data is stale.** It is dated 2026-09-25, and the experiment still shows as active today (2026-10-12), so refresh it and close the test.

The readout also covers the caveats on the 56 uncorrected secondary metrics and the next steps. The main one is to split the extra queries by whether they are reformulations before shipping.