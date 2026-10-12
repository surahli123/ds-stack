Decision: Not an A/B test

**Why**

- The pre-registration says this is a team-draft interleaving test of v6 against v7. In interleaving, every user sees a merged list from both rankers, and the analysis is a within-user preference between them.
- The Statsig config is a plain 50/50 between-group A/B instead. Control gets `lambdamart_v6` with no `serving_mode`. Test gets `lambdamart_v7` with `serving_mode=team_draft_interleaving`. The Pulse numbers are therefore an unpaired control-versus-test comparison of Successful Search Rate across users.
- That compares "v6 only" with "an interleaved v6/v7 list". It doesn't compare v6 with v7. The test arm's v7 exposure is diluted, so the Pulse delta isn't a v7-versus-v6 effect size. It can't be checked against the 0.005 bar, which assumes a clean comparison.
- Statsig can't tell us how the arms were really served, and the audit log is empty, so it doesn't show who set this up or when. I haven't confirmed whether the test arm really got interleaved lists or v7-only. The two readings give different answers.

**What Pulse shows (95% CI, no CUPED, 1.0M units per arm, data as of 2026-09-25)**

| Metric | Result | Pre-registered threshold |
|---|---|---|
| Successful Search Rate (primary) | +0.00334 absolute (+0.81% relative), CI about [+0.0017, +0.0050], p=7e-5 | Bar +0.005 |
| Abandonment Rate | +0.1% relative (worse), upper CI about +0.7% | Margin 1% |
| Zero Result Rate | 0.0%, CI ±1.4% | Margin 3% |
| Latency p95 | +0.2% (about +0.8 ms), CI ±0.5% | Margin 2% |
| Revenue per User | −0.1%, CI ±0.7% | Margin 1% |

- The difference is statistically significant, but the point estimate is below the pre-registered bar. Ship required the point estimate to reach 0.005, and it doesn't. The CI only just reaches the bar at its top edge.
- All four guardrails are within their margins. The secondary metrics are flat or noisy, with none significant after accounting for how many there are.
- Even read as a plain A/B, this would not meet the ship criterion. It also wouldn't justify "Don't ship", because the arms aren't v6 versus v7.

**Other observations**

- Timing is fine. The experiment ran from 2026-09-12 for 14 days.
- Exposure is slightly above plan, at 1.0M units per arm against 900k planned. The balanced-exposure health check passed.
- The config has an unplanned `snippet_length` parameter. It is 160 in both arms, so it has no effect.

**Recommendation for tomorrow**

1. Don't make a launch call from this Pulse readout.
2. Confirm with the experiment owner how the arms were served. If the test arm was interleaved v6/v7, run the interleaving analysis: per-user or per-query v7-versus-v6 preference, with a bootstrap CI.
3. If v7 alone should be compared with v6, re-run it as a proper A/B with `ranker_model` as the only difference. That also means re-checking the 0.005 bar.