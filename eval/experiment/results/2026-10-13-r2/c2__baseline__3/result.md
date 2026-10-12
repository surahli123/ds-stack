Decision: Escalate

**Why this goes to the review rather than being a straight ship**

1. **The test arm changed more than the ranker.** The pre-registration lists `ranker_model` as the only intended parameter. `experiment.json` shows Test also differs on `snippet_length` (160 in Control, 220 in Test). The audit log is empty, so I can't tell who changed it or when.
   - The measured lift belongs to "lambdamart_v7 plus longer snippets". It can't be attributed to the ranker alone.
   - Snippet length plausibly affects the primary metric (Successful Search Rate) directly. It could also affect time to first click and CTR.
   - Someone needs to say whether the snippet change was deliberate. If it was, we can ship the bundle that was tested. If it wasn't, we need to fix it or rerun with the ranker isolated.

2. **The primary result clears the bar only under one reading of the units.** The pre-registered bar is 0.005, with no unit given. The rule is that the point estimate must reach the bar.

| Reading | Point estimate | Clears the bar? |
|---|---|---|
| Relative, matching the guardrail margins | +0.81% | Yes |
| Absolute | +0.33 pp | No |

   - I read it as relative, because the guardrail margins in the same file are relative fractions. The prereg owners should confirm that.
   - Under the relative reading, the 95% CI on the lift is about +0.41% to +1.21%. The lower end is below 0.5%, but the rule only asks for the point estimate.

**Results (day 14, ds 2026-09-25, no CUPED, 95% CI)**

- **Design and data quality:**
  - The experiment is a proper A/B test with a 50/50 split and 1,000,000 users per arm, above the 900,000 planned.
  - The exposure-balance health check passed.
  - The test ran its planned 14 days, starting 2026-09-12.
  - There was a single end-of-test look, with no sequential testing.
- **Primary, Successful Search Rate:** 0.4120 in Control, 0.4153 in Test. That is +0.00334 absolute (CI ±0.00165) and +0.81% relative, p = 7e-05.
- **Guardrails** (changes are relative to Control; each is judged on the CI bound against the margin; all pass):

| Guardrail | Change | Worst CI bound | Margin |
|---|---|---|---|
| Latency p95 | +0.2% | +0.7% | 2% |
| Abandonment Rate | +0.1% | +0.7% | 1% |
| Zero Result Rate | 0.0% | +1.4% | 3% |
| Revenue per User | −0.1% | −0.8% | 1% |

- **Secondary metrics:** None moved significantly, and CTR, long clicks, queries, sessions and clicks per user are flat.
  - Time to First Click is slightly worse (+0.9%, p = 0.08).
  - That is the one metric where a longer snippet could plausibly have an effect. It's worth a look given the snippet confound.
- **Segments:** Tail queries (p = 0.015), Mobile CTR (p = 0.013) and Head-query long clicks (p = 0.04) are nominally significant. There are about 40 uncorrected segment cuts, so I'm treating these as noise, not findings.

**Recommendation for tomorrow**

- Confirm whether `snippet_length` 220 was intentional.
- Confirm the unit of the 0.005 bar.
- If the snippet change was intended and the bar is relative, the evidence supports shipping the tested bundle (new ranker with 220-character snippets). All guardrails are clear.
- If the ranker must be credited or shipped on its own, run a follow-up with `snippet_length` held at 160 in both arms.