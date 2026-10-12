Decision: No effect found

# Ranker v7 launch readout

**Bottom line:** Ranker v7 did not move Successful Search Rate. The experiment was powered to detect the 0.5 pp improvement the pre-registration required, and it rules that out. It does not meet the ship bar. I found no guardrail harm either, so this is "no effect found" and not "don't ship."

## Primary metric (pre-registered)
Successful Search Rate must rise by at least +0.005 (0.5 pp) at the point estimate for a ship.

| | Control | Test | Abs. change | 95% CI | p |
|---|---|---|---|---|---|
| Successful Search Rate | 0.4120 | 0.4118 | −0.0002 | [−0.0014, +0.0010] | 0.74 |

- The point estimate is slightly negative, about 25 times smaller than the bar.
- The CI's upper end is +0.0010, five times below the bar. Any true lift of 0.5 pp or more is excluded.
- A small positive or negative effect of up to about ±0.1 pp cannot be ruled out.

## Guardrails (pre-registered margins, relative)
Each guardrail is read as "the CI's worse end stays inside the margin."

| Guardrail | Change | Worse end of CI | Margin | OK? |
|---|---|---|---|---|
| Latency p95 | +0.2% | ~+0.7% | 2% | Yes |
| Abandonment Rate | +0.1% | ~+0.7% | 1% | Yes |
| Zero Result Rate | 0.0% | ~+1.4% | 3% | Yes |
| Revenue per User | −0.1% | ~−0.8% | 1% | Yes |

## Experiment validity
- **Duration:** It ran the full 14 days planned (2026-09-12 to 2026-09-26). The Pulse data is dated 2026-09-25.
- **Sample size:** There were 1,000,000 users per arm, above the 900,000 planned.
- **Balance and config:** The 50/50 split is balanced and the exposure health check passed. Only `ranker_model` differs between arms; `snippet_length` is the same in both. This matches the pre-registered intended parameter.
- **Audit log:** It is empty, so there were no mid-test changes.
- **Pulse settings:** CUPED was off, sequential testing was off, and no Bonferroni correction was applied. The 95% CIs are plain fixed-horizon intervals, which is what the pre-registration assumed.

## Secondary metrics (exploratory)
There are about 58 secondary and segment metrics at 95% confidence, so a few false positives are expected. I did not use them to change the decision. Two stood out in the top-level secondaries:
- **Ad Click Rate:** −1.5% relative (p=0.013). It is not a pre-registered guardrail, but it is revenue-adjacent. Revenue per User shows no significant change, so I'd watch it rather than act on it.
- **Queries per User:** +1.9% (p=0.028). It could mean more reformulation or more engagement. Reformulation Rate and Sessions per User are flat, so it is not clearly good or bad.

Neither survives a multiple-comparison correction, and neither affects the primary result. I did not review the segment breakouts (mobile/desktop, head/tail, navigational/informational) individually.

## Recommendation
- Don't launch v7 on the grounds of improved search success. The data doesn't support it.
- Launching it for other reasons (infrastructure, maintainability) would be safe on the guardrails, but that is a separate decision from this experiment.
- If the team still believes in v7, the next step is a redesign aimed at a larger effect, not a longer run. More time would only tighten an interval that already excludes the bar.