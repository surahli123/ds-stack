Decision: No effect found

**Ranker v7 readout (Successful Search Rate primary, data through 2026‑09‑25)**

**Result.** Ranker v7 did not measurably move the primary metric. The prereg ship rule requires the point estimate to reach the bar, and it falls well short.

| | Control | Test | Change (relative) | 95% CI (relative) | p |
|---|---|---|---|---|---|
| Successful Search Rate | 0.4120 | 0.4125 | +0.12% (+0.0005 abs) | −0.36% to +0.60% | 0.62 |

- **Bar:** the prereg bar is 0.005. I read it as relative (+0.5%), matching the guardrail margins. The point estimate is about a quarter of that.
- **If the bar is absolute:** that is 0.5 percentage points, and the CI upper bound of +0.25 pp excludes it. The conclusion is the same.
- **What the CI rules out:** the data are consistent with anything from a small loss to a gain slightly above the bar (+0.60%). So I can't fully exclude a bar‑sized gain. I can say the expected gain is about 0.1%, and that it is far from clearly reaching the bar.

**Validity checks.**
- **Design:** it is a clean A/B test, 50/50 at the user level.
- **Sample size:** 1.0M users per arm, against 900k planned.
- **Duration:** it ran the full 14 days (Sep 12–25).
- **Health:** the exposure balance check passed.
- **Config:** the audit log is empty, so nothing changed mid‑test. Only `ranker_model` differs between arms, as intended.
- **Settings:** CUPED was off and no sequential testing or multiplicity correction was applied. Only one primary metric was tested, so no correction is needed there.

**Guardrails.** None is breached. Each CI stays inside its prereg margin, treating the margins as relative.

| Metric | Change | 95% CI half‑width | Prereg margin |
|---|---|---|---|
| Latency p95 | +0.2% (412.0 → 412.8 ms) | ±0.5% | 2% |
| Abandonment Rate | +0.1% | ±0.6% | 1% |
| Zero Result Rate | 0.0% | ±1.4% | 3% |
| Revenue per User | −0.1% | ±0.7% | 1% |

**Secondary metrics and slices.**
- There are 56 secondary and slice metrics. Six have p<0.1 and about three have p<0.05, which is what chance would produce across that many tests, so I'm not treating them as findings.
- Several of them lean negative: Clicks per User (−0.8%, p=0.056), Mobile Clicks per User (−2.0%, p=0.011), and Navigational and Desktop Successful Search Rate (both about −0.8% to −0.9%).
- These are exploratory and not corrected for multiple comparisons. I'm flagging them only as a reason not to expect a hidden win in the slices.

**Recommendation.** Do not launch v7 on this evidence. There is no demonstrated gain at the bar and no harm on guardrails. If the team still believes in v7, the next step is a new, better‑powered test, or one targeted at a specific hypothesis. Extending this test is not worthwhile, because the expected effect (about 0.1%) is much smaller than the bar. A shipping decision based on other benefits (for example, a model replacement for maintenance reasons) would be safe on guardrails, but it is a separate decision from this experiment.

**Caveats.** I'm assuming the bar and margins are relative. The experiment status still reads "active" past its planned end. It should be closed out to stop exposing 20% of traffic to the test.