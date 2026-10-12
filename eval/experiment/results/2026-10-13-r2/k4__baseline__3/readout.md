Decision: Keep running

# Ranker v7 – launch review readout

**Bottom line:** The data in hand can't support a ship call. The primary metric is up, but by less than half the pre-registered bar. The sequential CI is too wide to confirm or rule out the bar, and several guardrails aren't cleared. The experiment was planned for 14 days and is still marked active, so the right move is to let it finish and re-pull Pulse.

## Primary: Successful Search Rate (pre-reg: ship only if the point estimate is ≥ +0.005 absolute)
- Control 0.4120, test 0.4143: **+0.00227 absolute (+0.55% relative)**. The point estimate is **below the 0.005 bar**.
- Sequential 95% CI (the pre-reg specifies sequential): **[-0.0009, +0.0054]**. It includes 0 and the bar, so it supports neither "no effect" nor "meets the bar".
- The p = 0.007 in Pulse comes with the fixed-horizon CI (±0.00165). It is not valid for a sequential, peeked analysis. Don't cite it as evidence of a win. Even the fixed CI, [+0.0006, +0.0039], has an upper end below the bar.

## Data is interim and stale
- The Pulse snapshot is ds = 2026-09-18, which is day ~7 of 14. The experiment started 2026-09-12, and the planned end was 2026-09-26.
- Sample is ~481k test and 480k control, about 53% of the 900k per arm planned. Exposure balance is fine (health check passed; 481k vs 480k).
- Today is 2026-10-12 and the experiment is still `active`, past the planned end. **I don't have results from the full planned window.** Re-pull Pulse (95%, no CUPED, sequential) before the meeting if possible. That is the one thing that could change this call.

## Guardrails (pre-reg margins; sequential CIs, worst-case end of CI)
| Metric | Observed | Worst case in CI | Margin | Status |
|---|---|---|---|---|
| Latency p95 | +0.2% (worse) | ≈ +1.2% | 2% | OK |
| Zero Result Rate | 0.0% | ≈ +2.7% | 3% | OK (barely) |
| Abandonment Rate | +0.1% (worse) | ≈ +1.2% | 1% | **Not cleared** |
| Revenue per User | -0.1% | ≈ -1.4% | 1% | **Not cleared** |

None shows a significant harm. But the sequential CIs for abandonment and revenue extend past the margins, so non-inferiority isn't demonstrated yet. I assumed the margins are relative; the pre-reg doesn't say.

## Secondary and subgroup metrics
- No secondary metric is significant at 95%. CTR (-0.34%), Queries per User and Sessions per User are slightly negative, all within noise.
- There are ~50 segment cuts. One nominal hit (Head Queries SSR, p = 0.043) is not meaningful given that many comparisons and no correction. Mobile and Tail SSR point negative, also within noise. Treat these as hypotheses only.

## Config discrepancies to fix
- `experiment.json` has `sequentialTesting: false`, but the pre-reg and the Pulse request use sequential. Reconcile this so the console view matches the pre-registered analysis.
- `audit_logs.json` is empty, so I can't verify that nothing changed mid-run (allocation, groups, parameters). The groups differ only in `ranker_model`, as intended.

## Recommendation
1. Let the experiment run to the planned sample, then re-pull Pulse with the sequential analysis.
2. Ship only if SSR's point estimate is ≥ +0.005 **and** the guardrails are cleared. At the current +0.0023, that looks unlikely unless the estimate moves substantially.
3. If the final estimate stays near +0.002 with a CI excluding the bar, the honest call is a small positive effect that fails the bar, not a ship.
