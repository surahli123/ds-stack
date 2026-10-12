Decision: No effect found

# Ranker v7 – launch review readout

**Bottom line:** Ranker v7 did not move Successful Search Rate (SSR) by anything near the pre-registered bar. Do not launch on this evidence. The one positive signal (Revenue per User) is not a basis for shipping.

## Primary metric (pre-registered: SSR, ship only if point estimate ≥ +0.5pp)
| | Control | Test | Abs. diff | 95% CI | p |
|---|---|---|---|---|---|
| Successful Search Rate | 41.20% | 41.22% | +0.016pp | [−0.107pp, +0.140pp] | 0.79 |

- The point estimate (+0.016pp) is about 30x below the +0.5pp bar. The entire CI sits below the bar (upper end +0.14pp), so this isn't "underpowered": a gain of the size we needed to see is ruled out at 95%.
- Test is flat to slightly negative on CTR (−0.06pp) and Long Click Rate (−0.03pp), all well within noise. Nothing supports a hidden engagement win.

## Guardrails (pre-registered margins, 95% CI upper bound of harm)
| Metric | Change | Worst end of CI | Margin | OK? |
|---|---|---|---|---|
| Latency p95 | +0.8 ms (+0.2%) | +2.9 ms (+0.7%) | 2% | Yes |
| Abandonment Rate | +0.02pp | +0.13pp | 1% | Yes (under either a relative or absolute reading) |
| Zero Result Rate | 0.0 | +1.4% rel. | 3% | Yes |
| Revenue per User | +$0.027 (+3.1%) | n/a (improvement) | −1% | Yes |

No guardrail was breached, so this is a neutral result, not a harmful one.

## Revenue per User +3.1% (p = 0.004): treat as exploratory
- Revenue is a guardrail, not a primary, and the prereg gave it no success role.
- The report has ~70 metrics and segment cuts with no multiple-comparison correction (`bonferroniCorrection: false`). A p=0.004 hit among that many looks is not strong evidence.
- It has no mechanism visible in the data: clicks, CTR, ad click rate (−0.002pp), queries and sessions per user are all flat or down.
- If the business wants to pursue it, run a follow-up with Revenue per User as the pre-registered primary. Don't launch on it now.

## Segments: consistent with noise
Of 54 segment-level tests (mobile/desktop, head/tail, navigational/informational), 4 have p<0.05 (Desktop time-to-first-click slower, p=0.004; Mobile and Tail clicks per user up, p=0.04 and 0.01). About 3 are expected by chance at that count, and none is on the primary or pre-registered. SSR is flat in every segment (largest: Mobile +0.31pp, p=0.11; Tail −0.27pp, p=0.29). These are hypotheses at most.

## Validity checks
- Exposure: 1,000,000 users per arm (plan 900,000), balanced 50/50. The Statsig balanced-exposure health check passed.
- Design: standard A/B, unit userID, 20% allocation. Only `ranker_model` differs between arms (`snippet_length` is identical at 160), matching the pre-registered parameter.
- Duration: the 14 days planned, started 2026-09-12. Pulse is dated 2026-09-25.
- Audit log is empty: no mid-test config changes.
- Pulse was pulled with CUPED off and 95% CI, as pre-registered (ci_level 0.95). No sequential testing, so a single end-of-test read is valid.

## Recommendation
1. Don't launch v7 as a search-quality improvement; it showed no detectable SSR change.
2. Any future iteration needs a larger expected effect, since v7's CI already excludes +0.5pp.
3. Optional: follow up on the revenue signal as a separately pre-registered test.

Caveats: I only had aggregated Pulse output, so I couldn't check for novelty effects or day-level trends. The CIs are wide enough that small gains below the bar (up to ~+0.14pp) are not excluded.
