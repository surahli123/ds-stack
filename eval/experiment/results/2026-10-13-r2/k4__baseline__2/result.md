Decision: Keep running

# Ranker v7: launch review readout

**Don't treat this as a ship readout.** The only results I have are an interim snapshot from 2026-09-18, and they don't support shipping or killing the ranker.

## What the data covers
- **Snapshot date:** Pulse `ds` is 2026-09-18, about day 7 of the 14-day plan. The experiment started on 2026-09-12 and was due to end on 2026-09-26.
- **Sample size:** There are 481k test and 480k control users. The plan was 900k per arm, so the snapshot has about 53% of the planned sample.
- **Status:** Today is 2026-10-12 and the experiment still shows `status: active`, so it is about two weeks past its planned end. No final Pulse is in the files. I can't tell whether the final data exist and just weren't pulled, or whether the experiment ran over without anyone closing it.
- **Allocation and balance:** The exposure balance check passed (`has_balanced_exposures`).

## Primary metric: Successful Search Rate
The pre-registered ship rule is that the point estimate must reach at least +0.005 absolute, with a 95% sequential test.

| | Value |
|---|---|
| Control | 0.4120 |
| Test | 0.4143 |
| Observed lift | +0.00227 (+0.55% relative) |
| 95% sequential CI | −0.00087 to +0.00540 |
| 95% fixed-horizon CI (not the pre-registered analysis) | +0.00062 to +0.00391, p = 0.007 |

- **Bar not met:** The observed lift is less than half the +0.005 bar, so the ship rule fails on the current data.
- **Bar not ruled out:** The sequential CI includes 0 and also includes values above 0.005. The data can't confirm a real effect or rule out a bar-clearing one.
- **Don't quote p = 0.007:** That p-value comes from the fixed-horizon interval, which is invalid for a sequential design when peeked at. The pre-registration says sequential.
- **Config mismatch:** `experiment.json` has `sequentialTesting: false`, while the pre-registration and the Pulse request both use sequential. I used the sequential intervals. The audit log is empty, so I can't explain the mismatch. Someone should confirm the intended setting.

## Guardrails (sequential CIs, margins from the pre-registration)
Three of the four guardrails are cleared or ambiguous. I read each margin as relative to the control mean (one assumption, see below).

| Guardrail | Observed change | Worst end of sequential CI | Margin | Status |
|---|---|---|---|---|
| Latency p95 | +0.2% | about +1.0% | 2% | Cleared |
| Zero Result Rate | 0 | about +2.7% | 3% | Cleared |
| Abandonment Rate | +0.1% | about +1.2% | 1% | Not cleared, narrowly, if the margin is relative |
| Revenue per User | −0.1% | about −1.4% | 1% | Not cleared |

- **Revenue:** The interval can't exclude a revenue drop larger than the 1% margin.
- **Abandonment:** If the margin is absolute rather than relative, abandonment clears. Please confirm which the team intended.
- **Revenue point estimate:** The point estimate is flat, so this reflects wide intervals, not a visible harm.

## Secondary and segment results
- **Secondary metrics:** CTR, long clicks, reformulations, queries and sessions per user, and time to first click show nothing distinguishable from zero.
- **Head Queries:** Its p = 0.043 is one significant result among about 45 segment tests, with no multiplicity correction. That is the rate expected by chance, so I'm not treating it as a finding.

## Recommendation
1. **Get the final data first.** Pull a fresh Pulse (same settings: 95%, no CUPED, sequential) through the end of the experiment, and tell the review if the experiment was stopped or left running by mistake.
2. **Decision rules for the final data:**
   - **Ship** only if the lower sequential CI bound on Successful Search Rate is at or above the +0.005 bar, or the point estimate is at or above it with all guardrails cleared. The pre-registration says `point_at_bar`, so I'd read it as the point estimate. Please confirm.
   - **Don't ship / No effect** if the interval narrows around the current ~+0.002.
3. **Open items for the review:** the sequential setting mismatch, the abandonment margin definition, and whether the stale snapshot is the latest data.