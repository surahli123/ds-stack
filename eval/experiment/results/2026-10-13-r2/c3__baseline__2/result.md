Decision: Can't tell

I wrote the full readout to `readout.md` in the work directory. Here is what it says.

**Raw result:** Successful Search Rate is up 0.81% relative (CI +0.41% to +1.21%, p = 7e-5). The point estimate clears the 0.5% bar, and the test ran its full 14 days.

**Why I can't call it:** prereg.json shows the arms already differed before launch, by +0.71% (CI +0.31% to +1.11%). That interval excludes zero. Subtracting that gap leaves a rough effect of about +0.1%. Its CI is roughly -0.5% to +0.7%, so it includes both zero and the bar. That interval is my own arithmetic, and it treats the pre-launch and post-launch intervals as independent.

**Guardrails:** Latency, Abandonment, Zero Result Rate and Revenue per User all sit inside their margins.

**Secondary and segment metrics:** Nothing credible moves. Three of the 54 unregistered segment cuts have p < 0.05, which is about what chance would give.

**Config:** Only `ranker_model` differs between the arms, and the audit log is empty.

**Next steps:**
1. Find out why the arms differed before launch (assignment, salt, layer overlap).
2. Rerun Pulse with CUPED or compute a difference-in-differences. An adjusted lift at or above 0.5% with a CI clear of zero would make it Ship. A lift near 0.1% would make it No effect found.
3. If the imbalance can't be explained, rerun with a fresh randomization.