Decision: No effect found

I also saved this readout as `readout.md` in the working directory.

**Primary metric (Successful Search Rate):** Control is 0.4120 and Test is 0.41216, a difference of +0.016pp (p = 0.79). The 95% CI is [-0.107pp, +0.140pp]. The pre-registered ship bar was +0.5pp, so the upper end of the CI is about a quarter of the bar and that size of lift is ruled out.

**Guardrails:** None is harmed (relative change, CI half-width, margin):
- **Latency p95:** +0.2% (±0.5%) against a 2% margin.
- **Abandonment:** +0.1% (±0.6%) against a 1% margin.
- **Zero Result Rate:** 0.0% (±1.4%) against a 3% margin.
- **Revenue per User:** +3.1% (±2.1%), so no drop.

**Revenue per User:** It is up 3.1% with p = 0.004, but it was not a pre-registered primary. It is one of about 15 overall secondary metrics, and about 70 counting the segment cuts, with no multiplicity correction. A Bonferroni correction over the 15 overall secondaries gives p ≈ 0.06. Clicks, CTR and ad click rate are all flat or slightly down, so there is no obvious mechanism. I'd treat it as a lead for a new pre-registered test, not a reason to ship.

**Segments:** The few nominally significant segment results are about what chance gives across ~60 uncorrected tests. Segment-level search success is flat everywhere.

**Validity:** The test is clean:
- **Allocation:** 50/50, with 1M users per arm (900k planned), and the exposure-balance check passed.
- **Variants:** Only `ranker_model` differs between arms, as pre-registered.
- **Config changes:** The audit log is empty, so nothing changed mid-test.
- **Timing:** The Pulse date is 2026-09-25, which looks like the end of the planned 14 days from the 2026-09-12 start. I couldn't confirm that the last day was complete.

**Recommendation:** Don't launch v7 as a search-quality win, and close this experiment. "No effect found" means no effect at the size the team cared about. A true effect within ±0.14pp can't be excluded.