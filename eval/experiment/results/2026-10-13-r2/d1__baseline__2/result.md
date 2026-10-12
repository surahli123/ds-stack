Decision: Don't ship

# Ranker v7 launch readout

**Summary:** v7 improves Successful Search Rate (SSR) by enough to clear the pre-registered bar. It also breaks the pre-registered latency guardrail. By the pre-registration, that means no ship in its current form.

## Primary metric
| Metric | Control | Test | Abs. change | Relative change (95% CI) | p |
|---|---|---|---|---|---|
| Successful Search Rate | 0.4120 | 0.4153 | +0.0033 | **+0.81% (±0.40 → 0.41% to 1.21%)** | 7e-5 |

- The pre-registered bar is 0.005. I read it as relative (+0.5%), because the guardrail margins in the same file are clearly relative. For example, the latency margin of 0.02 is 2% of about 412 ms.
- On that reading the point estimate (+0.81%) is above the bar, so the primary passes `point_at_bar`.
- The CI's lower end (+0.41%) is below the bar. The pre-registration asks for the point estimate to clear the bar, so this doesn't fail the test. It does mean the true lift could be a bit under 0.5%.
- If the bar was meant as an absolute 0.5 percentage points, the primary fails (+0.33pp). The team should confirm which was meant, but the decision below doesn't depend on it.

## Guardrails (95% CI, relative change vs. pre-registered margin)
| Guardrail | Change (95% CI) | Margin | Result |
|---|---|---|---|
| **Latency p95** | **+3.1% (2.5% to 3.7%), +12.8 ms** | 2% | **Breached.** The whole CI is above the margin. |
| Abandonment Rate | +0.1% (up to +0.7%) | 1% | OK |
| Zero Result Rate | 0.0% (up to +1.4%) | 3% | OK |
| Revenue per User | −0.1% (down to −0.8%) | −1% | OK |

Latency is the only breach, and it is statistically clear. The pre-registration lists latency as a guardrail, so this blocks shipping unless the review explicitly overrides it.

## Experiment validity
- Exposure balance health check: passed. Arms have 1.0M users each, against a plan of 900k.
- Duration: the experiment was planned for 14 days starting 2026‑09‑12, and the Pulse data runs through 2026‑09‑25.
- Audit log: no mid-flight changes.
- Sequential testing is off and the horizon is fixed, so there is no peeking problem.
- The intended parameter (`ranker_model`) is the only one that differs between arms. `snippet_length` is identical in both.
- Pulse was pulled without CUPED, as requested.

## Things to be aware of
- **Secondary and segment results are noise.** Of about 60 secondary and segment metrics, a few have nominal p < 0.05: CTR for tail queries (−1.1%), Clicks per User for informational queries (−1.5%), Autocomplete Acceptance (+0.6%) and Mobile Abandonment (−1.8%). With this many looks and no correction, I'd expect a handful by chance. None are pre-registered, so I don't treat any of them as evidence either way.
- **Segment results don't add up.** SSR is negative in both Mobile (−0.0010) and Desktop (−0.0026), yet it is +0.0033 overall. If those two segments cover all users, the overall change can't be positive. Something is off in the segment definitions, the segment mix, or the pipeline. This doesn't change the decision, but I'd check it before anyone quotes a segment result.
- **No evidence that SSR gains reflect better engagement.** CTR (−0.3%), Long Click Rate (−0.1%) and Clicks per User (+0.6%) are all flat. The SSR gain is real by the pre-registered measure, but nothing else corroborates it.

## Recommendation
1. Don't ship v7 as is, because of the latency breach (+3.1% against a 2% limit).
2. Ask the ranker team whether the +12.8 ms p95 can be cut, for example with model optimization, caching or a lighter feature set. If so, rerun on the same pre-registration.
3. If the team wants to ship despite the latency cost, that's an explicit guardrail override. It needs a named owner and a decision on the SSR/latency trade-off at the review. It shouldn't be framed as a normal ship.
4. Before the review, settle the absolute-versus-relative reading of the bar, and look into the segment inconsistency above.