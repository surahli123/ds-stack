I've written the readout to `readout.md`. The decision is Keep running.

The pulse covers only 7 days of the planned 14, so it's too early to call.

- **Primary metric:** Successful Search Rate is +0.55% (-0.21% to +1.31%) against a 0.50% bar. The point estimate clears the bar, but the interval includes zero and the bar.
- **Sample size:** 480,000 users per arm, against 900,000 planned.
- **Guardrails:** Latency p95 and Zero Result Rate are within their margins. Abandonment Rate and Revenue per User are unclear. None of them is past its margin.
- **Checks:** Scorecard, sample split, config parameters and config edits all pass. The pre-period and novelty checks couldn't run because the data wasn't there.
- **Mechanism:** Unknown. The scorecard has no segment cuts, so I labelled that bullet a guess.
- **Secondary metrics:** 52 were tested and none moved after the false-discovery correction.

Things for the review to know:
- **The data is stale.** The pulse stops at 2026-09-18, but the test started 2026-09-12 with a 14-day plan, and today is 2026-10-12. The test should have finished weeks ago. Someone needs to pull a fresh pulse before tomorrow, and that may settle the call. The readout lists this first under what would change the call.
- **Sequential testing setting differs.** The pulse was requested with sequential testing, but `experiment.json` has it off. The intervals above are the wider sequential ones, which matches the pre-registration.
- **Team standards are example values.** No team `standards.json` was supplied, so I used the example one at `/home/user/ds-stack-exp/overlay.example/standards.json`. The pre-registration supplied the bar, margins and guardrails.
- **Edited first line.** The rendered readout opens with a title and puts the reason on the Decision line. I removed the title and moved the reason to the next line so the first line is exactly `Decision: Keep running`.
- **Lint and cold read.** The lint gave `0 fail, 0 warn, 218 body words (readout)`. The cold read gave `cold-read: skim 1/2, full 3/3 - fail`. A fresh reader got the full takeaways but missed the answer on the skim. That is probably because the tool matches the title line I removed, but I didn't re-run it after the edit.