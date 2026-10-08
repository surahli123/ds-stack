## Answer
Headline: about 0 pp (measured: within-segment CTR is unchanged, so the v2 effect is ≈0 pp on the CTR rates we can see). The overall drop is −2.10 pp (30.43% → 28.32%).

Overall CTR fell 2.10 pp, but that is a shift in traffic mix toward mobile, and v2 shows no measurable effect on CTR within any platform/country segment.

## What it means for the rollback decision
This data gives no reason to roll v2 back on CTR grounds, because rolling back would not recover the 2.1 pp. What we can't yet say is why mobile's share of searches jumped, so investigate that before closing the question.

## Why we believe it
- Alternatives considered:
  - v2 lowered CTR: ruled out as a CTR effect by identical per-segment CTRs before and after (desktop-US 37.08% in both weeks, desktop-other 34.74%, mobile-US 22.66%, mobile-other 21.23%) [measured].
  - Mix shift (Simpson's paradox): ruled in. Mobile share of searches went from 40% to 55%, and mobile CTR is far lower than desktop CTR. That fully accounts for the −2.1 pp [measured].
  - The mix shift was caused by v2 (e.g. v2 changing which users search): not ruled out. The step change lands exactly on 09-28, but there is no holdout or control because v2 went to 100% at once [inferred].
  - Daily noise or an earlier trend: ruled out. Daily CTR is flat at about 30.4% before 09-28 and flat at about 28.3% after, with a clean step on 09-28 [measured].
- Checks run:
  - Segment-level before/after comparison by platform × country: pass. Rates match to four decimals.
  - Mix-adjusted decomposition: pass. Holding the old mix fixed gives the same CTR as before, so all of the change comes from the mix.
  - Daily series for timing: pass. Mobile share steps from 0.40 to 0.55 on 2026-09-28 and stays there.
  - Randomized or holdout comparison of v1 vs v2: could not run. There is no concurrent v1 traffic after 09-28.

## Caveats, and what would change the answer
- The identical-to-four-decimal CTRs look unusually clean for real data. Check the pipeline for imputed or copied rates before relying on this.
- If v2 itself caused the mobile share to rise (for example, a UI change shipped alongside it), then part of the drop is attributable to the rollout, though not through ranking quality. The release log lists only the v2 rollout, so check for other changes made that day, such as a mobile app launch or a marketing campaign.
- Only one week of data is available on each side, and CTR is not the only metric for judging a ranker.
- A holdout of v1 on a small share of traffic would settle the causal question directly.